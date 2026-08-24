<div align="center">

# Ceylon German Pathway — Official Website

### The Sri Lankan pathway to a nursing career in Germany 🇱🇰 → 🇩🇪

A seven-page static website in the Swiss International Typographic style — German flag tricolor, hard-cropped black-and-white photography, zero frameworks, zero dependencies, zero tracking.

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

CGP connects Sri Lankan nurses and healthcare professionals with careers in Germany — German language training, the Nursing Ausbildung pathway, and partnership with German healthcare institutions. This repository is the complete public website: **seven pages, six printable guides, one design system.**

- **Fully static** — plain HTML, CSS and vanilla JavaScript. No build step, no frameworks, no CDN links, no tracking.
- **Works offline** — every asset is stored locally. Open `index.html` and it just works.
- **Accessible by default** — keyboard navigation, ARIA tabs/accordions, `prefers-reduced-motion`, contrast-checked at WCAG AA.

## ✦ Pages

| Page | Purpose |
|------|---------|
| [Home](index.html) | The whole pathway at a glance — eight approved sections |
| [About CGP](about.html) | Who CGP is, five working principles, how the model works |
| [Students](students.html) | Full pathway, twelve services, fee structure, ten FAQs |
| [German Partners](partners.html) | Partnership services and the seven-stage partnership process |
| [Current Students](current-students.html) | Progress board and support along the pathway |
| [Resources & Downloads](resources.html) | Guides, full FAQ, plain-English German glossary |
| [Contact](contact.html) | Contact details and the enquiry form |

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
├── index.html … contact.html   The seven pages — this is the deliverable
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
├── build-pages.py              Optional dev tool — generates the shared chrome
└── README.md
```

### About `build-pages.py`

This generated six of the seven pages so the header, navigation and footer are byte-identical across the site. **It is not required to run or edit the site** — the `.html` files are complete and safe to hand-edit.

> ⚠️ If you hand-edit shared chrome (header/nav/footer) inside a generated page, either mirror the change into the script or delete the script — otherwise the next run overwrites your edit. `index.html` is hand-maintained and is never touched by the script.

### Cache busting

CSS and JS are referenced as `css/styles.css?v=5`. When you change either file, bump `ASSET_VERSION` in `build-pages.py`, re-run it, and change the matching `?v=` numbers in `index.html`.

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
| **Statistics** | Home, About, Current Students | Client-supplied working placeholders, each with a visible footnote |
| **Photography** | `assets/images/` | Unsplash placeholders as visual direction for the real shoot |
| **Fee amounts** | `students.html` | Shown as "On enquiry" — questionnaire did not specify |
| **Favicon** | `<link rel="icon">` | Currently points at `CGPLogo.png`; a square mark-only export would be sharper |

**Enquiry form:** `contact.html` opens the visitor's email app pre-filled (static site, no backend). Before launch, consider pointing `form.action` at a form service (Formspree, Netlify Forms…) so enquiries arrive reliably — handler marked in `js/main.js`.

## ✦ Content & compliance

- All copy is drawn from the completed client questionnaire — nothing invented.
- Banned phrases (guaranteed visa/job/placement, 100% success, "easy way to Germany", "no German required", unrealistic salary claims) are **not used anywhere** — please keep it that way when editing.
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
