# Silabs website | Business and engineering audit
Date: 2026-10-20

## Primary goal
Generate relevant project conversations for Silabs And Co Technologies Ltd while maintaining trust and transparent scope. Target users are Nigerian businesses, founders, institutions and teams looking for software, IT consultancy, automation or practical training.

## Business framework
This is our independent evaluation using established offer-design and customer-acquisition concepts popularised by Alex Hormozi: describe a valuable outcome, reduce buyer uncertainty and effort, improve real evidence, and simplify the call to action. It is not an official audit or endorsement by him.

| Finding | Priority | Implementation |
| --- | --- | --- |
| Generic hero without customer or outcome | Critical | Audience-focused heading, clear business challenge and project discussion CTA |
| Email-app-only handoff | Critical | WhatsApp-first composed enquiry plus email fallback |
| Service list lacks a decision path | High | Three starting points: Build, Improve and Equip |
| No verified customer proof | High | Honest own-product showcase; never invent case studies or ROI |
| Language feature competes with lead conversion | High | Keep floating words and reference; move reference further down |
| Many navigation destinations | High | Reduce primary nav to Services, Our Work, Process, About, Contact |
| Commercial uncertainty | High | Explain scope, milestones, handover and FAQs without fictional commitments |
| Asset cache mismatch risk | Medium | Version the CSS and JavaScript URLs |
| Privacy description outdated | Medium | Disclose WhatsApp/email preparation and third-party handling |

## Customer journey
New visitor → understands fit → chooses Build/Improve/Equip → reviews work → submits qualified enquiry to WhatsApp/email. Technical evaluators may browse the portfolio, process and FAQs. Partnerships, Academy, languages and leadership remain reachable.

## Engineering and commercial safeguards
- Contact submission is a *handoff* to WhatsApp or an email app. **No website backend receives the message**. The visitor must press Send. Do not falsely show a delivery success.
- Required inputs have client-side HTML validation. Optional stage and budget are not disguised fees or price quotes.
- WhatsApp and email URLs are encoded using encodeURIComponent. Never interpolate visitor content into innerHTML.
- No database or API keys are needed; maintain the existing static hosting and privacy disclosures.
- Product previews remain distinct from verified client testimonials.
- Do not promise response times, guaranteed results, fixed project pricing, warranty or ownership without a written agreement.
- Preserve registered legal name, blue brand palette, iRoya's hospitality classification, six products, two partners, 21 language expressions and eight director profiles.

## Acceptance
1. Static smoke checks for anchors, features, branding, menu and portfolio.
2. JavaScript syntax and simulated DOM tests of both enquiry channels, service preselection, validation and privacy wording.
3. Vercel successful build and GitHub Actions success.
4. Manual browser and mobile testing is still required; static tests cannot certify rendered layout, actual WhatsApp delivery or email-client configuration.

## Business work still needed
- Publish two or three **permissioned and independently verifiable** case studies with actual client problems, delivery evidence and customer-approved outcomes. Internal products do not automatically count as client projects.
- Approve pricing policy and engagement terms before displaying packages, timelines or guarantees.
- Assign an owner for inbound messages, maintain a lead register and set a response-time SLA only if operationally achievable.
- Confirm the production domain, WhatsApp/email ownership and company registrations.
- Consider privacy-reviewed server-side lead capture only after defining consent, spam control, retention, security and operational ownership.
- Track received qualified leads, proposals and closed work rather than treating clicks as delivered enquiries.

## Performance considerations
No extra frameworks or illustrations were introduced. CSS remains a legacy concatenated file and should eventually be consolidated; desktop/mobile visual QA and Lighthouse measurements are still outstanding.
