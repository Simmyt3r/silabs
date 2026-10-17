# Silabs And Co Technologies Ltd | Corporate website

Official corporate website source for **SIMEON'S LABORATORIES AND CO TECHNOLOGIES LTD (Silabs)**.

> **TECHNOLOGIA OMNIBUS**: Technology for everyone.

## What is included

- Responsive, accessible public-facing website with sections for services, products, academy, about, process and contact.
- Product showcase: UniXpress, CampPhoto AI, iRoya (hospitality and hotel booking/operations), MyPlatoon, TechDialect and Silabs AI. ChombuTar and CareerMirror appear separately as ecosystem partners. Maturity labels avoid misrepresenting development-stage products.
- Nine leadership profiles based on the company profile dated **2024–2025**. Current-year board and role confirmation is still required.
- Mobile navigation, keyboard-focus styles, reduced-motion handling and working enquiry flow.
- A **mailto-based contact form**. It opens the visitor's email client and **does not send or store** enquiries. This is deliberate: no deceptive success message, server-side API key or database.
- Basic organisation structured data, social metadata, privacy page and security headers.
- No build tool, framework or database. Suitable for Vercel or ordinary static hosting.

## Structure

| Path | Purpose |
| --- | --- |
| \`index.html\` | Accessible website markup and corporate content |
| \`assets/styles.css\` | Responsive visual system |
| \`assets/site.js\` | Mobile menu, year and mailto form |
| \`assets/brand.svg\` | **Temporary brand mark**. Replace with approved company logo before official launch. |
| \`privacy.html\` | Website privacy disclosures |
| \`vercel.json\` | Vercel static hosting headers |
| \`tests/smoke.py\` | Dependency-free static QA checks |

The existing \`academy/\` curriculum files are preserved.

## Preview locally

Open \`index.html\` using a static server so absolute-root asset links work:

\`\`\`bash
python -m http.server 8000
\`\`\`

Visit http://localhost:8000.

Run checks:

\`\`\`bash
python tests/smoke.py
node --check assets/site.js
\`\`\`

## Deploy to Vercel

1. Vercel → **Add New Project** → Import \`Simmyt3r/silabs\`.
2. Framework preset: **Other**. Root directory: repository root.
3. Build command: **leave blank**. Output directory: **leave blank** for static files.
4. Deploy and review the preview domain first.
5. Configure the verified corporate domain in Vercel when ownership/DNS are ready.

No environment variables, database migrations or server runtime are required.

## Before announcing launch

- [ ] Replace the temporary \`assets/brand.svg\` with Silabs' **official approved logo**.
- [ ] Confirm each product URL and its development status.
- [ ] Confirm director names and appointments against the current board, since the profile supplied covers 2024–2025.
- [ ] Confirm contact email and telephone number.
- [ ] Verify the main corporate domain and then add canonical and sitemap URLs.
- [ ] Test contact handoff on Windows, Android and iOS with a configured email application.
- [ ] Review the privacy text against the actual hosting provider configuration and applicable law.
- [ ] Add a real server-side contact endpoint later if automatic submission is needed. Protect it with spam prevention, rate limits and appropriate handling notices before enabling.

## Brand and contacts

- Registered company: SIMEON'S LABORATORIES AND CO TECHNOLOGIES LTD
- Brand: Silabs
- Motto: TECHNOLOGIA OMNIBUS
- Email: silabtechnologies@gmail.com
- WhatsApp: +234 903 993 0006

This initial implementation intentionally avoids invented testimonials, customer logos, staff counts, fabricated performance metrics and unsupported certifications.

## Corporate source notes

The registered company name, CAC RC 7740645, ICICLE values and nine listed directors were taken from the supplied *Company Profile (2024–2025)*. This source is historical and the leadership line-up should be reconfirmed before treating appointments as current. The Silabs and UniXpress graphics were provided by the company and stored as small optimized WebP copies; the prior illustrative graphic and invented brand lettermark are no longer used.

## Official brand palette

Colors were sampled from the company-supplied Silabs logo. The website uses:

- **Logo navy:** `#00006A` for dark corporate backgrounds and primary identity.
- **Logo royal blue:** `#3130BC` for headings, links, brand accents and interface details.
- **Soft blue-white:** `#EEF0FF` for neutral surfaces, with accessible lighter blue buttons on navy.

The site retains green only where it carries semantic meaning (such as available/confirmed status), not as a competing corporate brand color.

**iRoya** is a hospitality technology platform for independent hotels, supporting direct booking, property room inventory, rates, reservations and hotel operations. Do not describe iRoya as a messaging or social communication product.

## Light animated corporate hero

The landing page opens with a light white-to-blue stage in official brand colors, a subtly drifting computing grid, discreet circuit lines, pulsing nodes, soft scanning light, and floating monospace code. The illustration panels also use light surfaces with sufficient contrast. Motion is decorative, has no extra JavaScript dependencies, and is disabled via `prefers-reduced-motion`. The expanded visible company brand is **Silabs And Co Technologies Ltd**; the registered legal name remains **SIMEON'S LABORATORIES AND CO TECHNOLOGIES LTD** in the organizational record and legal footer. Existing product names (including Silabs AI), email addresses, and URLs have not been changed.
