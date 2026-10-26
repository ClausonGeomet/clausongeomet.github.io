"""Bounded static checks for public demo landing pages (standard library only)."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "tools/index.html", "beat-the-sampler/index.html",
         "drillhole-optimiser/index.html")
GAME = "https://01a16671-529d-e153-02bf-4aa206a894ae.share.connect.posit.cloud/"
DH = "https://01a0b868-67ef-8c01-436c-52596c278d71.share.connect.posit.cloud/"
PRIVATE_REPOS = (
    "github.com/ClausonGeomet/beat-the-sampler",
    "github.com/ClausonGeomet/geometallurgical_DH_optimiser",
)


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.urls: list[tuple[str, str, dict[str, str]]] = []
        self.h1 = 0
        self.canonical: list[str] = []
        self.og_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {key: (value or "") for key, value in attrs}
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag in ("a", "link", "script", "img"):
            value = a.get("href") or a.get("src")
            if value:
                self.urls.append((tag, value, a))
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical.append(a.get("href", ""))
        if tag == "meta" and a.get("property") == "og:url":
            self.og_urls.append(a.get("content", ""))


def resolve_local(page: Path, raw: str) -> Path | None:
    uri = urlsplit(raw)
    if uri.scheme or uri.netloc:
        return None
    if uri.path.startswith("/writing/"):
        # Separate published writing repository, outside this site checkout.
        return None
    location = uri.path
    if location.startswith("/"):
        path = ROOT / unquote(location.lstrip("/"))
    else:
        path = page.parent / unquote(location)
    path = path.resolve()
    if not path.is_relative_to(ROOT.resolve()):
        raise AssertionError(f"Local URL escapes site root: {raw}")
    if path.is_dir():
        path /= "index.html"
    return path


def validate_page(name: str) -> None:
    page = ROOT / name
    markup = page.read_text(encoding="utf-8")
    assert markup.lstrip().lower().startswith("<!doctype html>"), name
    assert all(private not in markup for private in PRIVATE_REPOS), name
    doc = Links()
    doc.feed(markup)
    assert doc.h1 == 1, f"{name}: expected one h1, got {doc.h1}"
    assert len(doc.ids) == len(set(doc.ids)), f"{name}: duplicate IDs"
    expected = "https://clausongeomet.com/" + ("" if name == "index.html" else name[:-10])
    assert doc.canonical == [expected], (name, doc.canonical, expected)
    assert doc.og_urls == [expected], (name, doc.og_urls, expected)
    for tag, url, attrs in doc.urls:
        uri = urlsplit(url)
        if attrs.get("target") == "_blank":
            assert "noopener" in set(attrs.get("rel", "").split()), (name, url)
        if not uri.scheme and uri.fragment and not uri.path:
            assert uri.fragment in doc.ids, f"{name}: missing anchor #{uri.fragment}"
        relative = resolve_local(page, url)
        if relative is not None and not relative.is_file():
            raise AssertionError(f"{name}: missing {tag} path {url} -> {relative}")
        if relative is not None and uri.fragment:
            target_doc = Links()
            target_doc.feed(relative.read_text(encoding="utf-8"))
            assert uri.fragment in target_doc.ids, f"{name}: invalid target #{uri.fragment} in {url}"
    print("PASS", name, "links", len(doc.urls))


def main() -> None:
    for name in PAGES:
        validate_page(name)
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    index = (ROOT / "tools/index.html").read_text(encoding="utf-8")
    game = (ROOT / "beat-the-sampler/index.html").read_text(encoding="utf-8")
    dh = (ROOT / "drillhole-optimiser/index.html").read_text(encoding="utf-8")
    assert "beat-the-sampler/" in home and "drillhole-optimiser/" in home
    assert "beat-the-sampler/" in index and "drillhole-optimiser/" in index
    assert GAME in index and GAME in game
    assert DH in index and DH in dh
    assert GAME + "how-it-works.html" in game
    assert "weighted sum of marginal" in dh
    assert "genuinely missing" in game
    assert "Do not upload confidential" in dh
    xml = ET.parse(ROOT / "sitemap.xml")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = {el.text for el in xml.findall(".//s:loc", ns)}
    for url in (
        "https://clausongeomet.com/",
        "https://clausongeomet.com/tools/",
        "https://clausongeomet.com/beat-the-sampler/",
        "https://clausongeomet.com/drillhole-optimiser/",
    ):
        assert url in locs, ("Missing sitemap URL", url)
    print("PASS", "public app endpoints, scientific limits, local paths and sitemap")


if __name__ == "__main__":
    main()
