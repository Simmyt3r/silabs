"""Fast dependency-free checks for the static Silabs website."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.forms = 0
        self.headings = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            assert attributes["id"] not in self.ids, f"Duplicate id: {attributes['id']}"
            self.ids.add(attributes["id"])
        if tag == "a":
            self.links.append(attributes.get("href", ""))
        if tag == "form":
            self.forms += 1
        if tag in ("h1", "h2"):
            self.headings.append(tag)


page = Page()
source = (ROOT / "index.html").read_text(encoding="utf-8")
page.feed(source)
assert page.headings.count("h1") == 1, "Expected one h1"
assert page.forms == 1, "Expected one contact form"
for link in page.links:
    if link.startswith("#"):
        assert link[1:] in page.ids, f"Broken anchor: {link}"
    if link.startswith("/") and not link.startswith("//"):
        assert (ROOT / link.lstrip("/")).is_file(), f"Broken internal link: {link}"
for asset in ("assets/brand.svg", "assets/silabs-official.webp", "assets/unixpress-official.webp", "assets/site.js", "assets/styles.css", "privacy.html"):
    assert (ROOT / asset).is_file(), f"Missing {asset}"
headers = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
assert headers["version"] == 2
js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
assert "encodeURIComponent" in js and "mailto:" in js
assert re.search(r'name="description"', source)
print("PASS: markup, anchors, files, metadata, config and mailto flow")

# Portfolio, partners and directors must be separate and complete.
products_html = source.split('<div class="products-grid">', 1)[1].split('<div class="product-bottom-note">', 1)[0]
partners_html = source.split('id="partners"', 1)[1].split('id="academy"', 1)[0]
directors_html = source.split('id="directors"', 1)[1].split('id="contact"', 1)[0]
for product in ("UniXpress", "CampPhoto AI", "iRoya", "MyPlatoon", "TechDialect", "Silabs AI"):
    assert product in products_html, f"Missing Silabs product: {product}"
for partner in ("ChombuTar", "CareerMirror"):
    assert partner in partners_html, f"Missing partner: {partner}"
    assert partner not in products_html, f"Partner is misclassified: {partner}"
assert directors_html.count('class="director-card') == 8
for director in ("Sarverun Simeon Tertese", "Abel Priscilla", "Ishaq Muhammad Idris", "Abu Princess Tarfa", "Abubakar Mustapha Sadiq", "Ishaya Hakuri", "Simon Nancy Mshellia", "Abdullahi Ahmad"):
    assert director in directors_html, f"Missing director: {director}"
assert "Agape Dimas" not in source, "Former HR director should not appear on website"
assert directors_html.count("<h3>Abubakar Mustapha Sadiq</h3>") == 1
assert "<h3>Abubakar Mustapha Sadiq</h3><p>Director of Public Relations and Human Resources</p>" in directors_html
assert "silabs-official.webp" in source and "unixpress-official.webp" in source
print("PASS: official logos, six products, two partners and eight directors")

# Confirm the website reflects the approved logo colors and iRoya's hospitality scope.
css = (ROOT / "assets/styles.css").read_text(encoding="utf-8").lower()
assert "--brand-navy:#00006a" in css, "Official dark blue missing"
assert "--brand-royal:#3130bc" in css, "Official royal blue missing"
assert "hospitality technology" in products_html.lower(), "iRoya category is not hospitality"
iroya_html = products_html.split('product-card product-iroya', 1)[1].split('</article>', 1)[0].lower()
for required in ("hotel", "booking", "reservations", "room inventory", "front-desk"):
    assert required in iroya_html, f"iRoya must describe {required}"
for wrong in ("messaging", "digital communication", "we're connected"):
    assert wrong not in iroya_html, f"Old iRoya messaging description remains: {wrong}"
assert '<meta name="theme-color" content="#00006A">' in source
print("PASS: official blue palette, hospitality-specific iRoya content and imagery")

# The opening section must be light, accessible and use the requested company name.
assert 'class="hero-stage"' in source, "Light hero stage absent"
assert '<div class="hero-computing-bg" aria-hidden="true">' in source
assert source.count('class="brand-name">Silabs And Co ') == 2, "Header and footer must show complete brand"
assert "Silabs And Co Technologies Ltd | Technology for Everyone" in source
assert "SIMEON'S LABORATORIES AND CO TECHNOLOGIES LTD" in source, "Keep registered legal identity"
assert "Silabs AI" in products_html, "Preserve product brand"
for expected in ("silabs-grid-drift", "silabs-node-pulse", "silabs-scan", "prefers-reduced-motion:reduce", ".hero-stage .hero h1", ".hero-stage .primary-nav.is-open"):
    assert expected in css, f"Missing hero feature or accessibility rule: {expected}"
assert "background:rgba(255,255,255,.78)" in css, "Light header background missing"
assert "linear-gradient(180deg,#ffffff 0%,#fcfcff 50%,#eef1ff 100%)" in css, "Light hero background missing"
print("PASS: light animated computing hero, accessible motion, expanded company name")

# A cached stylesheet must never be allowed to hide the company name or
# turn the decorative animation into a third grid column.
asset_cache = next(h for h in headers["headers"] if h["source"] == "/assets/(.*)")
assert next(h["value"] for h in asset_cache["headers"] if h["key"] == "Cache-Control") == "public, max-age=0, must-revalidate"
assert 'href="/assets/styles.css?v=20261019-languages1"' in source, "Stylesheet needs a fresh asset URL"
assert '<span class="tech-code code-one"></span>' in source
assert '<span class="tech-code code-two"></span>' in source
assert '<span class="tech-code code-three"></span>' in source
assert '<span class="tech-bracket bracket-one"></span>' in source
assert ".hero-stage .code-one::before" in css and ".hero-stage .hero-computing-bg{position:absolute" in css
assert source.count('class="hero-copy"') == 1 and source.count('class="hero-art"') == 1
print("PASS: cache-busted stylesheet, no unstyled code, hero grid fallback")

# All 21 user-provided Nigerian words must be present, accurately accented,
# kept out of the normal hero grid and available as visible reference text.
from html import unescape
language_bg = source.split('<div class="hero-computing-bg" aria-hidden="true">',1)[1].split('<div class="hero-copy">',1)[0]
assert language_bg.count('class="language-float language-') == 21
assert 'id="languages"' in source and '<details class="language-details">' in source
language_ref = source.split('id="languages"',1)[1].split('id="services"',1)[0]
expected_languages = [["Yoruba","Wá","Across Nigeria",""],["Hausa","Zo","Across Nigeria",""],["Igbo","Bịa","Across Nigeria",""],["Tiv","Va","Middle Belt",""],["Ebira","Vevé","Middle Belt","Vee"],["Idoma","Bie","Middle Belt",""],["Berom (Plateau)","Vwé","Middle Belt",""],["Igala","Bí","Middle Belt",""],["Gbagyi","Be","Middle Belt",""],["Ibibio","Di","Niger Delta & South-South",""],["Efik","Di","Niger Delta & South-South",""],["Urhobo","Rho","Niger Delta & South-South",""],["Itsekiri","Wá","Niger Delta & South-South",""],["Isoko","Zio","Niger Delta & South-South",""],["Ijaw (Izon)","Bo","Niger Delta & South-South",""],["Edo (Bini)","Khian","Niger Delta & South-South","Vwá"],["Khana (Ogoni)","Inoo","Niger Delta & South-South",""],["Kanuri","Íso","Northern & North-Eastern","Káso"],["Fulfulde (Fula)","War","Northern & North-Eastern",""],["Nupe","Be","Northern & North-Eastern",""],["Jukun","Ba","Northern & North-Eastern",""]]
for name,word,zone,alt in expected_languages:
    assert f'data-word="{word}" data-language="{name}"' in language_bg, f"Missing floating word: {name} {word}"
    assert f'class="language-name">{name}</span><strong lang="und">{word}</strong>' in language_ref, f"Missing language reference: {name} {word}"
    if alt:
        assert f'<small>or {alt}</small>' in language_ref, f"Missing alternative form: {name}"
assert "language-float" in css and "silabs-word-drift" in css
assert "content:attr(data-word)" in css
assert "prefers-reduced-motion:reduce" in css
print("PASS: 21 Nigerian languages, alternate forms, dynamic background and accessible reference")
