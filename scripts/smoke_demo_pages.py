"""Desktop and mobile local-browser review of public static landing pages.

No Posit authentication, model run, network fetch or website publication.
Screenshots are saved as CI artifacts for human review.
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.error
import urllib.request

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "browser-evidence" / "public-demo-pages"
URL = "http://127.0.0.1:8764"
PAGES = (
    ("/", "home"),
    ("/tools/", "tools"),
    ("/beat-the-sampler/", "sampler"),
    ("/drillhole-optimiser/", "optimiser"),
)


def ready(process: subprocess.Popen) -> None:
    for _ in range(45):
        if process.poll() is not None:
            raise AssertionError("Local static server exited unexpectedly")
        try:
            with urllib.request.urlopen(URL + "/", timeout=1) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(1)
    raise AssertionError("Local preview server did not start")


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    log = (ARTIFACTS / "server.log").open("w", encoding="utf-8")
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8764", "--bind", "127.0.0.1"],
        cwd=ROOT,
        env=os.environ.copy(),
        stdout=log,
        stderr=subprocess.STDOUT,
    )
    try:
        ready(proc)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for name, viewport in [
                    ("desktop", {"width": 1365, "height": 920}),
                    ("mobile", {"width": 390, "height": 844}),
                ]:
                    page = browser.new_page(viewport=viewport)
                    errors: list[str] = []
                    page.on("pageerror", lambda e: errors.append(str(e)))
                    for path, label in PAGES:
                        response = page.goto(URL + path, wait_until="domcontentloaded")
                        assert response is not None and response.status == 200, (path, response)
                        page.locator("h1").wait_for(state="visible")
                        assert page.locator("h1").count() == 1, path
                        page.locator("main").wait_for(state="visible")
                        no_overflow = page.evaluate(
                            "() => document.documentElement.scrollWidth <= innerWidth + 1"
                        )
                        assert no_overflow, (name, path, "horizontal overflow")
                        imgs = page.locator("header img").count()
                        assert imgs == 1, (name, path, "missing brand image")
                        assert page.locator("header img").evaluate(
                            "(img) => img.complete && img.naturalWidth > 0"
                        ), (name, path, "broken header logo")
                        if label == "home":
                            assert page.locator("#work .resource-card").count() == 4
                            assert page.locator('a[href="beat-the-sampler/"]').count() > 0
                        if label == "tools":
                            assert page.get_by_role("heading", name="Beat the Sampler").is_visible()
                            assert page.get_by_role(
                                "heading", name="Geometallurgical Testwork Optimiser"
                            ).count() == 1
                        if label == "sampler":
                            assert page.get_by_role("heading", name="Beat the Sampler. What would you test?").is_visible()
                            assert page.locator(
                                'a[href="https://01a16671-529d-e153-02bf-4aa206a894ae.share.connect.posit.cloud/"]'
                            ).count() > 0
                        if label == "optimiser":
                            assert page.get_by_role("heading", name="Which available core should we test next?").is_visible()
                            assert page.locator(
                                'a[href="https://01a0b868-67ef-8c01-436c-52596c278d71.share.connect.posit.cloud/"]'
                            ).count() > 0
                        page.screenshot(
                            path=str(ARTIFACTS / f"{name}-{label}.png"),
                            full_page=True,
                        )
                    assert not errors, (name, errors)
                    page.close()
                print("PASS static website desktop/mobile layout, branding and app links")
            finally:
                browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
        log.close()


if __name__ == "__main__":
    main()
