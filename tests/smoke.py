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
assert directors_html.count('class="director-card') == 9
for director in ("Sarverun Simeon Tertese", "Abel Priscilla", "Ishaq Muhammad Idris", "Abu Princess Tarfa", "Abubakar Mustapha Sadiq", "Ishaya Hakuri", "Simon Nancy Mshellia", "Abdullahi Ahmad", "Agape Dimas"):
    assert director in directors_html, f"Missing director: {director}"
assert "silabs-official.webp" in source and "unixpress-official.webp" in source
print("PASS: official logos, six products, two partners and nine directors")

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
