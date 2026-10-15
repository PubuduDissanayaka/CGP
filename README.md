<div align="center">

# Ceylon German Pathway — Official Website

### The Sri Lankan pathway to a nursing career in Germany 🇱🇰 → 🇩🇪

A ten-page static website in the Swiss International Typographic style — German flag tricolor, hard-cropped black-and-white photography, zero frameworks, zero dependencies, zero tracking.

<br>

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Vanilla](https://img.shields.io/badge/vanilla-100%25%20no%20frameworks-%23DD0000?style=flat-square)
![No CDN](https://img.shields.io/badge/no%20CDN-%231e1e1e?style=flat-square)
![No Tracking](https://img.shields.io/badge/no%20tracking-%23FFCE00?style=flat-square&color=black)
![Accessible](https://img.shields.io/badge/accessibility-WCAG%20AA-%23000000?style=flat-square)

---

**Black `#000000` · Red `#DD0000` · Gold `#FFCE00`** — the tricolour runs through every page, from the header rule to the footer.

</div>

---

## ✦ Overview

CGP connects Sri Lankan nurses and healthcare professionals with careers in Germany — German language training, the Nursing Ausbildung pathway, and partnership with German healthcare institutions. This repository is the complete public website: **ten pages, six printable guides, one design system.**

- **Fully static** — plain HTML, CSS and vanilla JavaScript. No build step, no frameworks, no CDN links, no tracking.
- **Works offline** — every asset is stored locally. Open `index.html` and it just works.
- **Accessible by default** — keyboard navigation, ARIA tabs/accordions, `prefers-reduced-motion`, contrast-checked at WCAG AA.

## ✦ Pages

| Page | Purpose |
|------|---------|
| [Home](index.html) | Three rotating hero banners plus eight approved sections |
| [About CGP](about.html) | Four sections: Who We Are, Vision & Mission, How CGP Works, Our Approach |
| [Students & Parents](students.html) | Section landing page: the client's hero banner, twelve services, programme transparency |
| [Who Can Apply](who-can-apply.html) | Eligibility and the personal commitment CGP asks for, plus the no-guarantee notice |
| [Complete Pathway](complete-pathway.html) | The fifteen-stage pathway in five phases, with CGP's role and the institution's role separated |
| [Frequently Asked Questions](faq.html) | The sixteen questions students and parents ask most, in an accordion |
| [German Partners](partners.html) | Partnership services and the seven-stage partnership process |
| [Current Students](current-students.html) | Progress board and support along the pathway |
| [Resources & Downloads](resources.html) | Guides, full FAQ, plain-English German glossary |
| [Contact](contact.html) | Contact details and the enquiry form |

The four pages under **Students & Parents** are the section's content; `students.html` is the section landing page. The main navigation opens the section from the **Students & Parents** dropdown (Who Can Apply · Complete Pathway · Frequently Asked Questions), and `students.html` is linked from the footer and from every page inside the section.

Each of the six **downloadable guides** (`downloads/`) is a self-contained printable page — document checklist, fee policy, FAQ, German language starter guide, Nursing Ausbildung pathway guide, and a pre-departure checklist.

## ✦ Run it

The folder is self-contained — keep it together. Then either:

**Double-click `index.html`** — the whole site works, including navigation between pages.

Or serve it over HTTP (closer to production):

```bash
python3 -m http.server 4173
# → http://localhost:4173
```

## ✦ Structure

```
.
├── index.html … contact.html   The ten pages — this is the deliverable
├── css/
│   ├── tokens.css              Design tokens: colour, type scale, spacing, grid, motion
│   └── styles.css              All component styles — references tokens only
├── js/
│   └── main.js                 Nav, accordions, tabs, journey rail, form, scroll reveal
├── assets/
│   ├── images/                 Photography (local) + logo, JPEG + WebP pairs
│   ├── fonts/                  Empty — the site uses the native Helvetica stack
│   └── icons/                  Reserved
├── downloads/                  Six printable PDF-style guides (self-contained HTML)
├── Hero-Slide/                 Client-supplied banner artwork (PNG masters)
├── build-pages.py              Optional dev tool — generates the shared chrome
├── Changes Home page.docx      Client change request, 2026-10-12
└── README.md
```

### About `build-pages.py`

This generated eight of the ten pages so the header, navigation and footer are byte-identical across the site. **It is not required to run or edit the site** — the `.html` files are complete and safe to hand-edit.

The main navigation — including the **About CGP** dropdown (its four section links) and the **Students & Parents** dropdown (Who Can Apply · Complete Pathway · Frequently Asked Questions) — lives in `nav()` in that script, and the About page's four sections are generated from the `ABOUT` template below it. Changing either means changing the script, then re-running it.

> ⚠️ If you hand-edit shared chrome (header/nav/footer) inside a generated page, either mirror the change into the script or delete the script — otherwise the next run overwrites your edit. `index.html` is hand-maintained and is never touched by the script.

### Cache busting

CSS and JS are referenced as `css/styles.css?v=11`. When you change either file, bump `ASSET_VERSION` in `build-pages.py`, re-run it, and change the matching `?v=` numbers in `index.html`.

## ✦ Design system

Swiss International Typographic Style: a strict 12-column modular grid, flush-left ragged-right text, extreme contrast between oversized display type and small body copy, thin hairline rules, numbered sections, sharp corners (no rounding, no shadows), and hard-cropped black-and-white photography. **No two sections repeat the same layout.**

- **Brand colours** are the German flag palette — black `#000000`, red `#DD0000`, gold `#FFCE00`. Red is the single bold accent; gold appears sparingly (labels on dark sections, the active tab, the tricolour rule above the header).
- **Photography** is stored in colour and rendered black-and-white by the `.img-bw` class, so the treatment can be changed or removed in one place.
- **Fonts** — the native Helvetica stack (`Helvetica Neue → Helvetica → Liberation Sans → Arial`). No font files shipped, no licence needed. Drop licensed `.woff2` files into `assets/fonts/` later and they take priority automatically.

## ✦ Before launch — placeholders to replace

| Item | Where | Note |
|------|-------|------|
| **Logo** | `assets/images/CGPLogo.png` | Live in header, footer and favicon |
| **Testimonials** | `current-students.html` | Clearly labelled "Sample testimonials" — replace with real, verified quotes |
| **Statistics** | About, Current Students | Client-supplied working placeholders, each with a visible footnote. The counters on the **home** page's About section were removed at the client's request (2026-10-12) |
| **Photography** | `assets/images/` | Unsplash placeholders as visual direction for the real shoot. The Students & Parents hero banner is the client's own supplied artwork (`Hero-Slide/ChatGPT Image Oct 15, 2026, 03_34_38 PM.png` → `hero-students-parents.jpg/.webp`) |
| **Favicon** | `<link rel="icon">` | Currently points at `CGPLogo.png`; a square mark-only export would be sharper |

**Enquiry form:** `contact.html` opens the visitor's email app pre-filled (static site, no backend). Before launch, consider pointing `form.action` at a form service (Formspree, Netlify Forms…) so enquiries arrive reliably — handler marked in `js/main.js`.

## ✦ Content & compliance

- All copy is drawn from the completed client questionnaire and the client's own change requests — nothing invented.
- Banned phrases (guaranteed visa/job/placement, 100% success, "easy way to Germany", "no German required", unrealistic salary claims) are **not used anywhere** — please keep it that way when editing.
- The Students & Parents section is explicit that CGP prepares and supports candidates but does **not** guarantee or sell Ausbildung positions: final assessment and selection remain with the German institution. That wording is deliberate and appears on the Who Can Apply, Complete Pathway and FAQ pages.
- No fee table is published in the Students & Parents section (client instruction, 2026-10-15). Costs are explained to each candidate directly, before enrolment.
- Case studies are labelled as illustrative of the service model, not completed cases.
- Unverified figures carry visible footnotes rather than being presented as fact.

## ✦ Accessibility

Semantic HTML with one `<h1>` per page; alt text on every image; a skip link; visible focus states; WAI-ARIA tabs and accordions that work by keyboard; `aria-current` on the active nav item; `prefers-reduced-motion` honoured. Body text is 18px with contrast checked on both light and dark sections.

## ✦ Security

- **No secrets in the repo** — no API keys, credentials, or environment files. The only contact data present is CGP's public business details (WhatsApp, `hello@cgp.lk`).
- Client-confidential working files (questionnaire, build prompts, client requirements) are **git-ignored** and never pushed.
- All external links use `rel="noopener"`.

## ✦ Known follow-ups

- **Image weight** — `assets/images/` is ~7 MB (JPEG + WebP pairs already added). Running the remaining JPEGs through an optimiser would roughly halve page weight — matters for mobile visitors in Sri Lanka.
- **Favicon** has not been created — it needs the logo file first.

---

<div align="center">

**© 2026 Ceylon German Pathway** — Built by [DevTenent](https://devtenent.com) · Colombo, Sri Lanka

</div>

## ✦ Client change request — 2026-10-12

Applied from `Changes Home page.docx` plus the three banner artworks in `Hero-Slide/`.
Recorded here so the next editor knows what was deliberate.

**Home page**

- Hero replaced by a three-banner accessible slider (`[data-hero-slider]` in the markup,
  driven by `js/main.js`). Source artwork is PNG in `Hero-Slide/`; the site loads
  `assets/images/hero-banner-01..03.jpg` (with matching `.webp` spares). Each banner is
  shown whole — never cropped — and its headline is repeated as real text in the caption
  underneath, which is what mobile visitors actually read. The male nurse portrait
  (`hero-portrait.jpg/.webp`) is no longer used; the file is still on disk.
- Home page section order (owner instruction, 2026-10-12): the **banner slider leads the
  page**, immediately under the header, and the headline band (kicker · H1 · lede ·
  enquiry buttons) is the next section below it — followed by the three-fact strip, then
  `About CGP`. The hairline rule that used to sit between the band and the slider now sits
  above the band, and the slider no longer draws its own top rule against the header's.
- `ASSET_VERSION` / `?v=` raised to **11** across all seven pages for this change.
- The About CGP section: statistics counters removed, the "transparent fees and documented
  policies" principle replaced, and a **Learn more about CGP** button added. Copy aligned to
  the client's eight-stage pathway wording.
- Why Choose CGP: the "Transparent fees" card removed and the remaining cards renumbered
  3.1–3.6, with a "Cultural & professional preparation" card added to cover the themes the
  client listed.

**About CGP**

- Main navigation: "About CGP" is now a dropdown (Who We Are · Vision & Mission · How CGP
  Works · Our Approach), anchored to sections on `about.html`. The nav label "Resources &
  Downloads" was shortened to "Resources" to match the client's proposed navigation.
- The page was re-headed into those four sections; the previous "What we believe",
  "What makes us different" and "How we work" copy is retained inside them.
- New eight-stage pathway diagram (`#how-cgp-works`, `.pathway`), stages named exactly as the
  client listed them.
- New "Our Approach" section — the client's eight points, verbatim.

**Accessibility follow-up — 2026-10-12 (review findings)**

Two defects reported by the review pass and fixed here; neither changes any rendered
pixel, both are attribute-only edits:

- `index.html` — the hero slider (`div.hero-slider[data-hero-slider]`) carried
  `aria-roledescription="carousel"` and `aria-label` but no `role`, so the carousel was not
  exposed to assistive technology at all. Added `role="region"`; Chrome's accessibility
  tree now reports `region · "CGP in three banners"`.
- `partners.html` — `section[aria-labelledby="pmodel-title"]` referenced an id that did not
  exist, leaving the section unnamed. The id now sits on its own heading
  (`<h2 class="section-head__label" id="pmodel-title">`). `section_head()` in
  `build-pages.py` takes an optional `label_id` argument and the partners call passes it, so
  a regeneration reproduces the fix; the argument is optional and every other call renders
  byte-identically.

Known, deliberate, and *not* fixed here (recorded on the Multica issue, awaiting the owner's
call): the low-contrast slider dot marks and `.section-head__meta` label colour (WCAG AA
contrast findings from the design review), and the design review's recommendation to obtain
banner artwork in the site's own visual language.

**Still to confirm with the client** (see the Multica issue): which supplied artwork belongs
to which banner, the Vision and Mission wording, and whether the placeholder statistics should
also come off the About and Current Students pages. *(The Students navigation item became a
dropdown on 2026-10-15; the German Partners item did not.)*

## ✦ Client change request — 2026-10-15

Applied from `Website - Students.docx` (*Website Amendment – Students Section*) plus the
client's Students & Parents banner artwork. The section was rebuilt around the client's three
pages.

**Students & Parents section**

- The main navigation's **Students** item became a **Students & Parents** dropdown containing
  exactly the three pages the client listed: **Who Can Apply**, **Complete Pathway** and
  **Frequently Asked Questions**. It uses the same disclosure-menu pattern as About CGP
  (`[data-nav-menu]` in `js/main.js`; no JS changes were needed).
- `students.html` is now the section landing page: the client's supplied banner artwork,
  the headline band (real text, not text baked into the image), a three-card "Start here"
  listing the three pages, the twelve student services, and the **Programme Information &
  Transparency** statement.
- **Fee & payment policy content removed** from the public Students section: the fee table,
  the fee wording in the intro and the fee question in the old FAQ are gone, replaced by the
  client's verbatim Programme Information & Transparency statement.
- **New page `who-can-apply.html`** — the client's seven eligibility and commitment areas as
  numbered rows, the approved "This pathway asks something of you" copy, and the important
  notice that meeting CGP's criteria guarantees nothing.
- **New page `complete-pathway.html`** — all fifteen stages, grouped into five phases and each
  carrying a role badge (**CGP** or **German institution**), plus a "Two roles, one pathway"
  split so CGP's preparation role is never confused with the institution's assessment and
  selection role.
- **New page `faq.html`** — the client's sixteen questions in an accessible accordion, followed
  by the Programme Information & Transparency statement.
- New components in `css/styles.css` (§16.15): `.hero-banner`, `.route-cards` / `.route-card`,
  `.route` (phased pathway) and `.roles`. `ASSET_VERSION` / `?v=` raised to **12** on all ten
  pages, `index.html` included.
- Page numbering in the page heroes was renumbered to `Page NN / 10` and the footer's
  "Students" item renamed to "Students & Parents", so the running count stays true.
- `resources.html`: its "full FAQ" accordion now shares the single FAQ source in
  `build-pages.py`, and the note about publishing fee amounts was replaced with the client's
  transparency wording.

**Known, deliberate and awaiting the client's call** (recorded on the Multica issue):

- `downloads/fees-and-payment-policy.html` and its card on `resources.html` were **left in
  place**. The client asked for the "Fee & Payment Policy page/section" to come off the
  Students menu and the prominent public Students content, which is done; whether the separate
  printable fee-policy download should also go is a client decision, not a developer one.
- `downloads/frequently-asked-questions.html` is still the older ten-question printable
  summary, and its fee answer predates this change.
- Two earlier FAQ answers (accommodation in Germany; how to apply) are no longer in the FAQ,
  because the client's list of sixteen questions supersedes the old set. The application route
  is on `contact.html`.
- The FAQ states that nursing Ausbildung in Germany "normally runs for three years" and that
  the required German level is "normally B1 or B2". Both are the generally documented position
  and both are hedged as set by law and by the institution, but the client should confirm the
  wording before it is published.

