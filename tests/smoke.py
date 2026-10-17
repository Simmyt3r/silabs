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
