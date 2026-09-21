"""One-off release-branch editor and browser checks; removed before merge."""
from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path.cwd()
OUT = ROOT / '.release-checks'


def replace_once(text, old, new):
    count = text.count(old)
    if count != 1:
        raise AssertionError(f'Expected one copy, found {count}: {old[:100]!r}')
    return text.replace(old, new, 1)


def apply():
    p = ROOT / 'index.html'
    s = p.read_text()
    s = replace_once(s, 'Geometallurgical consulting for mining and mineral-processing teams. Model reviews, ore-to-plant investigations and practical analytical software by Matt Clauson.', 'Geometallurgical consulting by Matt Clauson: modelling, testwork strategy, ore-to-plant investigations and practical analytical tools for mining teams.')
    s = s.replace('Geological understanding. Defensible inference. Practical implementation. Consulting for mining and mineral-processing teams.', 'Geological and operating-plant experience combined with statistics to turn orebody, testwork and plant data into practical decisions.')
    s = replace_once(s, '<a href="#approach">Approach</a><a href="#services">Services</a><a href="#experience">Experience</a>', '<a href="#services">Services</a><a href="#experience">Experience</a><a href="#approach">Approach</a>')
    s = replace_once(s, 'I help mining and mineral-processing teams make better decisions from orebody, testwork and plant data.', 'I help mining and mineral-processing teams turn orebody, testwork and plant data into better sampling, modelling and operating decisions.')
    old_detail = '          <p class="hero-detail">Combining geological and operating-plant experience with statistical inference, I develop defensible analyses and practical software tailored to the problem.</p>\n'
    s = replace_once(s, old_detail, '')
    marker = '          <div class="hero-emblem"'
    detail = '          <p class="hero-detail">Combining geological and operating-plant experience with statistical inference, I review and develop geometallurgical models, investigate plant performance, and build practical analytical tools.</p>\n'
    s = replace_once(s, marker, detail + marker)
    s = replace_once(s, 'Focused reviews, investigations and tool development. Each engagement is scoped around your decision, the available data and an agreed output.', 'Modelling, reviews, investigations and tool development. Each engagement is scoped around your question, the available data and an agreed output.')
    s = replace_once(s, '01 / REVIEW', '01 / MODEL &amp; REVIEW')
    s = replace_once(s, '<h3>Geometallurgical model review</h3>', '<h3>Geometallurgical modelling and review</h3>')
    s = replace_once(s, 'Understand whether an existing model is fit for its intended use, and where the evidence or validation needs strengthening.', 'Develop or review models that connect ore characteristics to processing behaviour. Assess their suitability for the intended decision, and identify where validation or additional testwork would be most useful.')
    s = replace_once(s, 'A review of assumptions, sampling, validation and uncertainty, with prioritised recommendations.', 'A model or review report, as scoped, with documented assumptions, validation, uncertainty and prioritised recommendations for further testwork.')
    s = replace_once(s, 'Browse technical articles, open-source packages and practical applications separately.', 'Explore the methods through technical writing, open-source software and interactive examples.')
    s = replace_once(s, 'Essays and case studies on geometallurgy, mineral inference and defensible technical decision-making.', 'Articles and worked examples on geometallurgy, mineral inference and the questions behind technical decisions.')
    s = replace_once(s, '<strong>Matt Clauson</strong> is a Perth-based geometallurgist and statistical modeller with more than 10 years of experience across mining and mineral processing.', '<strong>I’m Matt Clauson</strong>, a Perth-based geometallurgist and statistical modeller with more than 10 years of experience across mining and mineral processing.')
    s = replace_once(s, 'His background spans operating-plant roles, commissioning, mineralogical characterisation and geometallurgical studies. That practical experience informs how he connects ore variability, testwork and plant performance.', 'My background spans operating-plant roles, commissioning, mineralogical characterisation and geometallurgical studies. That practical experience informs how I connect ore variability, testwork and plant performance.')
    s = replace_once(s, '          <p>Through Clauson Geomet, Matt develops analyses and software around the decision a client needs to make — not a predetermined modelling technique. His applied research focuses on <a href="#research">compositional data analysis and causal inference</a>.</p>', '          <p>My experience spans iron ore, nickel, bauxite, manganese, tin–tungsten and lead–zinc–silver projects.</p>\n          <p>Through Clauson Geomet, I develop analyses and software around the question a client needs to answer — not a predetermined modelling technique. My applied research focuses on <a href="#research">compositional data analysis and causal inference</a>.</p>')
    s = replace_once(s, '<p>He holds an MSc in Mining Geology, a BSc (Hons) in Geology and a Graduate Diploma of Science in Mathematics &amp; Statistics.</p>', '<p>I hold an MSc in Mining Geology, a BSc (Hons) in Geology and a Graduate Diploma of Science in Mathematics &amp; Statistics.</p>')
    s = replace_once(s, 'Have a project<br>worth discussing?', 'Have a geometallurgical<br>question?')
    sections = {}
    for key in ('approach', 'services', 'experience', 'work', 'research'):
        match = re.search(r'    <section id="' + key + r'".*?    </section>', s, re.S)
        assert match, key
        sections[key] = match.group(0)
    research = sections['research']
    research = replace_once(research, 'class="research shell section-rule"', 'class="research research-inline"')
    research = replace_once(research, 'class="section-heading"', 'class="research-heading"')
    research = replace_once(research, '        <p class="section-index">05 / APPLIED RESEARCH</p>\n', '')
    research = research.replace('<h3>', '<h4>').replace('</h3>', '</h4>')
    research = research.replace('<h2 id="research-title">', '<h3 id="research-title">').replace('</h2>', '</h3>')
    approach = sections['approach'].replace('01 / THE APPROACH', '03 / THE APPROACH')
    insertion = approach.rfind('    </section>')
    approach = approach[:insertion] + '\n' + research + '\n' + approach[insertion:]
    ordered = [sections['services'].replace('02 / SERVICES', '01 / SERVICES'), sections['experience'].replace('03 / PROJECT EXPERIENCE', '02 / PROJECT EXPERIENCE'), approach, sections['work']]
    start = s.index(sections['approach'])
    end = s.index(sections['research']) + len(sections['research'])
    s = s[:start] + '\n'.join(ordered) + s[end:]
    s = s.replace('06 / ABOUT', '05 / ABOUT').replace('07 / CONTACT', '06 / CONTACT')
    p.write_text(s)

    p = ROOT / 'packages/index.html'
    s = p.read_text()
    s = replace_once(s, '<p>Explore variation in ordered process data using chronological variograms, integral transforms and engineering variance-component analysis.</p>', '<p><strong>Understand how process variability changes over time and with sampling interval.</strong></p>\n                <p>Use chronological variograms, integral transforms and engineering variance-component analysis to explore ordered process data.</p>')
    p.write_text(s)

    p = ROOT / 'tools/index.html'
    s = p.read_text()
    s = replace_once(s, 'The first public demonstration focuses on selecting Bond Ball Work Index (BBWi) laboratory tests from intervals that have already been drilled and assayed.', 'Select Bond Ball Work Index (BBWi) laboratory tests from intervals that have already been drilled and assayed. This is testwork selection, not planning new drill-hole locations.')
    p.write_text(s)

    p = ROOT / 'drillhole-optimiser/index.html'
    s = p.read_text()
    s = replace_once(s, '</h1>\n<p class="demo-lede">', '</h1>\n<p class="demo-note">A synthetic demonstration of selecting BBWi tests from existing drill core.</p>\n<p class="demo-lede">')
    s = replace_once(s, '<nav class="nav">', '<nav class="nav" aria-label="Primary navigation">')
    s = replace_once(s, '<a href="../approach/">Approach</a><a href="../#experience">Experience</a>', '<a href="../#services">Services</a><a href="../#experience">Experience</a><a href="../approach/">Approach</a>')
    p.write_text(s)

    for p in ROOT.rglob('*.html'):
        if '.git' in p.parts or '.release-checks' in p.parts:
            continue
        old = p.read_text()
        s = old.replace('Geometallurgical Drillhole Optimiser', 'Geometallurgical Testwork Optimiser').replace('GEOMETALLURGICAL DRILLHOLE OPTIMISER', 'GEOMETALLURGICAL TESTWORK OPTIMISER').replace('Information-Theoretic BBWi Testwork Optimiser | Clauson Geomet', 'Geometallurgical Testwork Optimiser | Clauson Geomet')
        s = s.replace('<a href="../approach/">Approach</a><a href="../#services">Services</a><a href="../#experience">Experience</a>', '<a href="../#services">Services</a><a href="../#experience">Experience</a><a href="../approach/">Approach</a>')
        s = re.sub(r'(href="(?:\.\./)?approach\.css)(?:\?[^\"]*)?"', r'\1?v=20260921-release"', s)
        if s != old:
            p.write_text(s)

    p = ROOT / 'approach.css'
    s = p.read_text()
    assert 'Launch polish: client-first' not in s
    s += '''
/* Launch polish: client-first content, integrated research and compact mobile entry. */
.research-inline{margin-top:48px;padding-top:30px;border-top:1px solid var(--line)}
.research-heading{margin-bottom:26px}
.research-heading h3{font-size:clamp(1.5rem,2.8vw,2.4rem);line-height:1.12;letter-spacing:-.025em;margin:0}
.research-card h4{font-size:clamp(1.4rem,2.2vw,2rem);line-height:1.12;letter-spacing:-.025em;margin:0 0 22px}
.hero-actions{margin-top:24px}
.hero-detail{margin:24px 0 0}
.demo-actions .button{max-width:100%;min-width:0;white-space:normal;text-align:center;padding-block:12px}
@media(max-width:600px){
  .site-header{min-height:0;padding-block:12px;gap:8px}
  .site-header .brand-logo-image{width:min(210px,66vw);height:auto}
  .nav{gap:0 16px;font-size:.64rem;letter-spacing:.08em}
  .nav a{padding-block:6px}
  .hero{padding:30px 0 48px}
  .hero-grid{gap:22px;margin-top:20px}
  .hero .eyebrow{font-size:.65rem;letter-spacing:.12em}
  .hero .lede{font-size:1.1rem;line-height:1.45;margin-bottom:0}
  .hero-actions{margin-top:20px;gap:16px}
  .hero-detail{font-size:1rem;margin-top:24px}
  .contact h2{font-size:clamp(2rem,9.8vw,4rem)}
  .research-inline{margin-top:36px}
}
'''
    p.write_text(s)
    subprocess.run(['git', 'diff', '--check'], check=True)
    print('Applied source edits without changing assets, CV, URLs or application code.')


def check():
    from bs4 import BeautifulSoup
    from urllib.parse import urlsplit, unquote
    from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
    from threading import Thread
    from playwright.sync_api import sync_playwright
    OUT.mkdir(exist_ok=True)
    files = [ROOT / x for x in ('index.html', 'approach/index.html', 'packages/index.html', 'tools/index.html', 'drillhole-optimiser/index.html')]
    soups = {p: BeautifulSoup(p.read_text(), 'html.parser') for p in files}
    home = soups[ROOT / 'index.html']
    ids = [s.get('id') for s in home.select('main > section')]
    assert ids == [None, 'services', 'experience', 'approach', 'work', 'about', 'contact'], ids
    assert home.select_one('#approach #research')
    assert [x.get('class', []) for x in home.select('.hero-side > *')][:3] == [['lede'], ['hero-actions'], ['hero-detail']]
    assert 'employed roles, not commissions delivered by Clauson Geomet' in home.get_text()
    assert 'Geometallurgical modelling and review' in home.get_text()
    assert 'tin–tungsten' in home.get_text()
    local_links = 0
    for p, soup in soups.items():
        assert len(soup.select('h1')) == 1, p
        page_ids = [x['id'] for x in soup.select('[id]')]
        assert len(page_ids) == len(set(page_ids)), (p, 'duplicate IDs')
        assert 'Geometallurgical Drillhole Optimiser' not in p.read_text(), p
        for element in soup.select('[aria-labelledby]'):
            for label in element['aria-labelledby'].split():
                assert soup.find(id=label), (p, label)
        for element in soup.select('a[href], img[src], link[href]'):
            url = element.get('href') or element.get('src')
            u = urlsplit(url)
            if u.scheme or u.netloc or u.path.startswith('/writing/'):
                continue
            target = ROOT / u.path.lstrip('/') if u.path.startswith('/') else p.parent / u.path
            if not u.path:
                target = p
            if target.is_dir():
                target = target / 'index.html'
            assert target.exists(), (p, url, target)
            if u.fragment and target.suffix == '.html':
                parsed = soups.get(target) or BeautifulSoup(target.read_text(), 'html.parser')
                assert parsed.find(id=unquote(u.fragment)), (p, url)
            local_links += 1
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    rows = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(origin) else route.abort())
            for width in (320, 375, 390, 600, 768, 900, 1024, 1440):
                page.set_viewport_size({'width': width, 'height': 800})
                for path in ('/', '/approach/', '/packages/', '/tools/', '/drillhole-optimiser/'):
                    page.goto(origin + path, wait_until='networkidle')
                    page.evaluate('document.fonts.ready')
                    dims = page.evaluate('({width:innerWidth, scroll:document.documentElement.scrollWidth})')
                    assert dims['scroll'] <= width + 1, (path, width, dims)
                    assert page.locator('h1').count() == 1
                    if path == '/':
                        first_button = page.locator('.hero-actions .button').bounding_box()
                        if width <= 390:
                            assert first_button['y'] + first_button['height'] <= 800, (width, first_button)
                        if width in (320, 390, 1440):
                            page.screenshot(path=str(OUT / f'home-{width}.png'), full_page=True)
                    if width in (390, 1440) and path == '/tools/':
                        page.screenshot(path=str(OUT / f'tools-{width}.png'), full_page=True)
                    rows.append({'page': path, 'viewport': width, 'scroll_width': dims['scroll']})
            browser.close()
    finally:
        server.shutdown()
    (OUT / 'responsive-results.json').write_text(json.dumps(rows, indent=2))
    summary = f'Passed: {len(files)} pages; {len(rows)} browser viewport/page combinations; {local_links} local links/assets; unique headings and IDs; valid anchors; mobile primary contact button visible within the first 800px.\nCV download, LinkedIn preview and live Shiny interaction are not part of these checks.\n'
    (OUT / 'summary.md').write_text(summary)
    print(summary)


if __name__ == '__main__':
    {'apply': apply, 'check': check}[sys.argv[1]]()
