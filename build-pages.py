#!/usr/bin/env python3
"""
Ceylon German Pathway - page generator.

DEV TOOL, NOT A DEPENDENCY. The deliverable is the plain .html files this
writes out; they are complete, standalone and safe to hand-edit.

Its only job is to keep the header, navigation and footer byte-identical
across all seven pages. Run it after changing shared chrome:

    python3 build-pages.py

It writes about / students / partners / current-students / resources /
contact. index.html is maintained by hand and is NOT touched.

If you hand-edit the shared chrome inside a generated page, either mirror
the change into SHELL below or stop using this script - otherwise the next
run will overwrite your edit.
"""

import html as html_lib
import pathlib
import re

ROOT = pathlib.Path(__file__).parent

WHATSAPP = "https://wa.me/94704008952"
PHONE = "+94 70 400 8952"
EMAIL = "hello@cgp.lk"
FACEBOOK = "https://www.facebook.com/CeylonGermanPathway"
INSTAGRAM = "https://www.instagram.com/ceylongermanpathway"
LOGO = "assets/images/CGPLogo.png"

# Bump this whenever css/ or js/ changes, then re-run, and mirror it in
# index.html. Forces browsers to fetch the new file instead of a cached one.
ASSET_VERSION = "13"

# Ten pages as of the 2026-10-15 Students & Parents rebuild: the seven main
# pages plus the three pages that now sit under the Students & Parents menu.
PAGES = [
    ("index.html", "Home"),
    ("about.html", "About CGP"),
    ("students.html", "Students &amp; Parents"),
    ("partners.html", "German Partners"),
    ("current-students.html", "Current Students"),
    ("resources.html", "Resources &amp; Downloads"),
    ("contact.html", "Contact"),
]

# The pages that sit under the "Students & Parents" dropdown in the main
# navigation. Also used for the "site number" shown in each page hero, so the
# running "Page NN / 10" stays true.
STUDENTS_SUBMENU = [
    ("who-can-apply.html", "Who Can Apply"),
    ("complete-pathway.html", "Complete Pathway"),
    ("faq.html", "Frequently Asked Questions"),
]

# Page numbers, in menu order. index.html is hand-maintained but its number
# lives here so the total is written down in one place.
PAGE_NUMBERS = {
    "index.html": ("01", 1),
    "about.html": ("02", 2),
    "students.html": ("03", 3),
    "who-can-apply.html": ("04", 4),
    "complete-pathway.html": ("05", 5),
    "faq.html": ("06", 6),
    "partners.html": ("07", 7),
    "current-students.html": ("08", 8),
    "resources.html": ("09", 9),
    "contact.html": ("10", 10),
}

PAGE_TOTAL = len(PAGE_NUMBERS)


def page_hero_of(filename):
    """The 'Page NN / 10' stamp for a page."""
    number, _ = PAGE_NUMBERS[filename]
    return f"Page {number} / {PAGE_TOTAL:02d}"


# The main navigation and the footer list the same pages, but the main nav is
# where "About CGP" expands into its four section links and where
# "Resources & Downloads" is shortened to "Resources".
NAV_LABELS = {"resources.html": "Resources"}

# Every item in a section menu is the section's own heading, verbatim, and the
# anchor is the id on that heading's <section> - so a menu item can never
# disagree with the page it points at.
ABOUT_SUBMENU = [
    ("about.html#who-we-are", "Who We Are"),
    ("about.html#vision-mission", "Vision &amp; Mission"),
    ("about.html#how-cgp-works", "How CGP Works"),
    ("about.html#our-approach", "Our Approach"),
]

# The client's proposed main navigation (Changes Home page.docx, 2026-10-12)
# marks German Partners as a dropdown as well. The client has not supplied its
# items, so - as on About CGP - the section's own headings are used. Swap these
# four lines when the client names their own items.
PARTNERS_SUBMENU = [
    ("partners.html#partnership-services", "Partnership services"),
    ("partners.html#how-the-partnership-works", "How the partnership works"),
    ("partners.html#partnership-model", "The partnership model"),
    ("partners.html#why-work-with-cgp", "Why work with CGP"),
]

# The three main-nav items that are section menus rather than single links:
# page -> (label, menu items, submenu id).
SECTION_MENUS = {
    "about.html": ("About CGP", ABOUT_SUBMENU, "submenu-about"),
    "students.html": ("Students &amp; Parents", STUDENTS_SUBMENU, "submenu-students"),
    "partners.html": ("German Partners", PARTNERS_SUBMENU, "submenu-partners"),
}


def dropdown(label, current, section_href, items, submenu_id):
    """A main-nav section menu (disclosure menu).

    Every top-level item in the main navigation is a link to its own page, so
    no destination is reachable only from inside a menu. The sections that have
    more than one destination carry a caret button beside the label; the button
    - and only the button - opens the menu, which keeps "go to the page" and
    "show me what is in it" as two separate, predictable actions.

    label        - the visible top-level label (may contain character entities)
    current      - the page currently being rendered
    section_href - the section's own page; the label links to it
    items        - [(href, text)] shown inside the menu
    submenu_id   - id the caret button points at with aria-controls
    """
    child_hrefs = [href for href, _ in items]

    if current == section_href:
        cur = ' aria-current="page"'
    elif current in child_hrefs:
        # A page inside the section is open. aria-current="true" marks the
        # section the visitor is in without claiming this link is the page
        # they are on.
        cur = ' aria-current="true"'
    else:
        cur = ""

    # The caret button carries only a glyph, so it needs its own name.
    plain = html_lib.escape(html_lib.unescape(re.sub(r"<[^>]+>", "", label)), quote=True)

    lines = []
    for href, text in items:
        sub_cur = ' aria-current="page"' if href == current else ""
        lines.append(
            f'              <a class="nav__sublink" href="{href}"{sub_cur}>{text}</a>'
        )
    sub = "\n".join(lines)

    return f"""        <div class="nav__item" data-nav-menu>
          <div class="nav__row">
            <a class="nav__link" href="{section_href}"{cur}>{label}</a>
            <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="{submenu_id}" aria-label="{plain} menu">
              <span class="nav__caret" aria-hidden="true">&#9662;</span>
            </button>
          </div>
          <div class="nav__submenu" id="{submenu_id}">
            <div class="nav__menu">
{sub}
            </div>
          </div>
        </div>"""


def nav(current):
    out = []

    for href, label in PAGES:
        if href in SECTION_MENUS:
            menu_label, items, submenu_id = SECTION_MENUS[href]
            out.append(dropdown(menu_label, current, href, items, submenu_id))
            continue

        cur = ' aria-current="page"' if href == current else ""
        out.append(
            f'        <a class="nav__link" href="{href}"{cur}>{NAV_LABELS.get(href, label)}</a>'
        )
    return "\n".join(out)


def footer_nav():
    return "\n".join(
        f'            <li><a href="{href}">{label}</a></li>' for href, label in PAGES
    )


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <!-- ?v= is a cache-busting version stamp. Bump ASSET_VERSION in
       build-pages.py (and index.html) whenever CSS or JS changes,
       so returning visitors are not served a stale copy. -->
  <link rel="stylesheet" href="css/tokens.css?v={version}">
  <link rel="stylesheet" href="css/styles.css?v={version}">
  <link rel="icon" href="{logo}" type="image/png">
</head>
<body>

  <a class="skip-link" href="#main">Skip to main content</a>

  <div class="flag-rule" aria-hidden="true"><span></span><span></span><span></span></div>

  <header class="header">
    <div class="container header__bar">

      <a class="logo" href="index.html" aria-label="Ceylon German Pathway - home">
        <img class="logo__img" src="{logo}" alt="Ceylon German Pathway">
        <span class="logo__fallback" aria-hidden="true">
          <span class="logo__mark">CGP</span>
          <span class="logo__type">Ceylon German Pathway</span>
        </span>
      </a>

      <nav class="nav" id="site-nav" aria-label="Main navigation">
{nav}
      </nav>

      <a class="btn btn--solid header__cta" href="{whatsapp}" target="_blank" rel="noopener">WhatsApp</a>

      <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <main id="main">
{content}
  </main>

  <footer class="footer">
    <div class="container">
      <div class="grid footer__grid">

        <div class="footer__brand">
          <a class="logo" href="index.html" aria-label="Ceylon German Pathway - home">
            <img class="logo__img" src="{logo}" alt="Ceylon German Pathway">
            <span class="logo__fallback" aria-hidden="true">
              <span class="logo__mark">CGP</span>
              <span class="logo__type">Ceylon German Pathway</span>
            </span>
          </a>
          <p>Preparing Sri Lankan youth for Nursing Ausbildung and professional healthcare careers in Germany - through ethical guidance, German language training and ongoing support.</p>
        </div>

        <nav class="footer__col footer__col--wide" aria-label="Footer navigation">
          <h4>Site</h4>
          <ul>
{footer_nav}
          </ul>
        </nav>

        <div class="footer__col">
          <h4>Follow</h4>
          <ul>
            <li><a href="{facebook}" target="_blank" rel="noopener">Facebook</a></li>
            <li><a href="{instagram}" target="_blank" rel="noopener">Instagram</a></li>
          </ul>
        </div>

        <div class="footer__col footer__col--wide">
          <h4>Contact</h4>
          <ul>
            <li><a href="mailto:{email}">{email}</a></li>
            <li>No. 143/10, Wilimbula, Henegama 11715</li>
            <li>Gampaha District, Sri Lanka</li>
            <li>Mon&ndash;Fri, 9:00&ndash;17:00 (SLT)</li>
          </ul>
        </div>
      </div>

      <div class="footer__bottom">
        <p>&copy; 2026 Ceylon German Pathway. All rights reserved.</p>
        <p>Sri Lanka &rarr; Deutschland</p>
      </div>
    </div>
  </footer>

  <script src="js/main.js?v={version}"></script>
</body>
</html>
"""


def page_hero(index, of, label, title, lede, aside_items, meta=""):
    aside = "\n".join(
        f"            <dt>{dt}</dt>\n            <dd>{dd}</dd>" for dt, dd in aside_items
    )
    return f"""
    <section class="page-hero" aria-labelledby="page-title">
      <div class="container">
        <div class="grid">
          <div class="page-hero__index">
            <span class="micro-label">{index}</span>
            <span class="micro-label">{label}</span>
            <span class="micro-label page-hero__of">{meta or of}</span>
          </div>
          <h1 class="page-hero__title" id="page-title">{title}</h1>
          <div class="page-hero__lede">
            <p class="lead">{lede}</p>
          </div>
          <dl class="page-hero__aside">
{aside}
          </dl>
        </div>
      </div>
    </section>
"""


def band(img, alt, caption):
    return f"""
    <figure class="page-band">
      <img class="img-bw" src="assets/images/{img}" alt="{alt}" width="1600" height="1067">
      <figcaption>{caption}</figcaption>
    </figure>
"""


def section_head(index, label, meta, label_id=None):
    # label_id lets a section's aria-labelledby point at this heading (see the
    # partners page "pmodel-title" section). Optional, so every existing call
    # renders byte-identically.
    id_attr = f' id="{label_id}"' if label_id else ""
    return f"""        <header class="section-head">
          <span class="section-head__index">{index}</span>
          <h2 class="section-head__label"{id_attr}>{label}</h2>
          <span class="section-head__meta">{meta}</span>
        </header>
"""


def cta_strip(title_black, title_white, blurb):
    return f"""
    <section class="section cta" aria-labelledby="cta-title">
      <div class="container">
        <div class="grid">
          <p class="cta__title reveal" id="cta-title"><span class="de">{title_black}</span> {title_white}</p>
          <div class="cta__actions reveal">
            <a class="btn btn--inverse" href="{WHATSAPP}" target="_blank" rel="noopener">Chat on WhatsApp <span class="btn__glyph" aria-hidden="true">&rarr;</span></a>
            <a class="btn btn--inverse" href="contact.html">Request information</a>
          </div>
          <ul class="cta__contact reveal">
            <li><span class="micro-label">Email</span> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><span class="micro-label">Hours</span> <span>Monday&ndash;Friday, 9:00&ndash;17:00 (Sri Lanka time)</span></li>
            <li><span class="micro-label">Note</span> <span>{blurb}</span></li>
          </ul>
        </div>
      </div>
    </section>
"""


# ==========================================================================
# ABOUT CGP
# ==========================================================================

PRINCIPLES = [
    ("Ethical recruitment",
     "Student welfare comes before placement numbers. We are honest about requirements, timelines and what the pathway does and does not involve."),
    ("Transparency",
     "Our fees and payment policy are written down and explained before you commit. No hidden charges at any stage."),
    ("Student welfare",
     "We treat every student as a person building a career, not a file to be processed."),
    ("Continuous support",
     "Our responsibility runs from the first enquiry through to integration support after arrival in Germany."),
    ("Privacy",
     "Your personal information and documents are handled carefully and kept secure throughout the process."),
]

about_principles = "\n".join(
    f"""          <article class="why-card reveal">
            <p class="why-card__index">2.{i}</p>
            <h3>{name}</h3>
            <p>{desc}</p>
          </article>""" for i, (name, desc) in enumerate(PRINCIPLES, 1)
)

ABOUT = page_hero(
    "02", page_hero_of("about.html"), "About CGP",
    "Guidance you can hold us to.",
    "Ceylon German Pathway is a Sri Lankan organisation preparing motivated young people for Nursing Ausbildung and professional healthcare careers in Germany - through ethical guidance, structured German language training and support that continues after arrival.",
    [("Based in", "Wilimbula, Henegama, Gampaha District, Sri Lanka"),
     ("Serving", "Sri Lankan students and families nationwide"),
     ("Focus", "Nursing Ausbildung and healthcare careers in Germany")],
) + band("students-group.jpg", "Students studying together in a library", "CGP students in preparation") + f"""
    <section class="section" id="who-we-are" aria-labelledby="who-title">
      <div class="container">
{section_head("01", "Who We Are", "Wilimbula &middot; Gampaha District")}
        <div class="grid">
          <div class="col-wide prose reveal">
            <p class="display" id="who-title" style="margin-bottom: var(--space-4);">We don't just recruit students. We prepare them - and stay with them.</p>
            <p>Ceylon German Pathway (CGP) is based in Wilimbula, Henegama, in the Gampaha District, and serves Sri Lankan students and families nationwide. We help motivated young people pursue vocational education and healthcare career opportunities in Germany.</p>
            <p>Most people who come to us are asking the same question: <em>&ldquo;I want to build a healthcare career in Germany, but I don't know how to start, what documents I need, how to learn German, or how to handle the Ausbildung and visa process.&rdquo;</em> Our entire service is built to answer that question properly, in order, with someone accountable at each step.</p>
            <p>That means candidate identification, German language preparation, cultural and professional preparation, documentation, partner interviews and selection, pre-departure preparation, and support once you have arrived in Germany.</p>
          </div>
          <figure class="col-narrow reveal">
            <img class="img-bw" src="assets/images/nurse-care.jpg" alt="One person's hands holding another's in a gesture of care and reassurance" width="1600" height="1067" loading="lazy">
            <figcaption class="small" style="padding-top: var(--space-1); border-bottom: 1px solid var(--color-rule);">Student welfare first</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section section--dark" id="vision-mission" aria-labelledby="vm-title">
      <div class="container">
{section_head("02", "Vision &amp; Mission", "Unsere Vision")}
        <div class="grid row-gap-lg">
          <div class="vm reveal">
            <article class="vm__block">
              <p class="micro-label vm__label">Vision</p>
              <p class="vm__statement" id="vm-title">A trusted, sustainable pathway between Sri Lanka and Germany: candidates prepared properly, German partners who can rely on them, and families who know exactly what to expect at every stage.</p>
            </article>
            <article class="vm__block">
              <p class="micro-label vm__label">Mission</p>
              <p class="vm__statement">We prepare motivated young Sri Lankans for Nursing Ausbildung in Germany - through systematic German language learning, cultural and professional preparation and honest guidance - and we stay with them from their first enquiry to their working life in Germany.</p>
            </article>
          </div>
          <div class="col-full reveal" style="grid-column: 1 / 13; margin-top: var(--space-5);">
            <p class="display" style="margin-bottom: var(--space-4);">Principles, not slogans.</p>
          </div>
          <div class="col-full grid row-gap" style="grid-column: 1 / 13;">
{about_principles}
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="how-cgp-works" aria-labelledby="how-title">
      <div class="container">
{section_head("03", "How CGP Works", "Eight stages &middot; Sri Lanka &rarr; Ausbildung")}
        <div class="grid row-gap-lg">
          <div class="col-wide reveal">
            <p class="display" id="how-title">One pathway, eight stages.</p>
            <p class="lead" style="margin-top: var(--space-3); max-width: 44em;">From the first conversation in Sri Lanka to a training place in Germany - the same sequence for every candidate, and one that students, families and German partner institutions can all follow.</p>
          </div>

          <ol class="pathway reveal" aria-label="The CGP candidate pathway">
            <li class="pathway__step"><span class="pathway__num">01</span><span class="pathway__label">Candidate Identification</span></li>
            <li class="pathway__step"><span class="pathway__num">02</span><span class="pathway__label">German Language Preparation</span></li>
            <li class="pathway__step"><span class="pathway__num">03</span><span class="pathway__label">Cultural &amp; Professional Preparation</span></li>
            <li class="pathway__step"><span class="pathway__num">04</span><span class="pathway__label">Documentation</span></li>
            <li class="pathway__step"><span class="pathway__num">05</span><span class="pathway__label">German Partner Interview &amp; Selection</span></li>
            <li class="pathway__step"><span class="pathway__num">06</span><span class="pathway__label">Pre-departure Preparation</span></li>
            <li class="pathway__step"><span class="pathway__num">07</span><span class="pathway__label">Germany</span></li>
            <li class="pathway__step"><span class="pathway__num">08</span><span class="pathway__label">Ausbildung</span></li>
          </ol>

          <div class="col-full reveal" style="grid-column: 1 / 13;">
            <div class="notice">
              <p><strong>Please read:</strong> the two examples below describe how the CGP service model is designed to work. They are illustrative of our process - they are not accounts of specific completed cases, and no outcome is implied or promised. Real, verified case studies will replace them as they are confirmed.</p>
            </div>
          </div>
          <div class="span-6 reveal">
            <article class="case-study">
              <h3>Nursing Ausbildung candidate preparation</h3>
              <dl>
                <dt>Situation</dt>
                <dd>A motivated Sri Lankan student wants to pursue a Nursing Ausbildung in Germany but needs structured guidance on the application process, German language preparation, documentation, interviews and visa requirements.</dd>
                <dt>What CGP does</dt>
                <dd>Guides the student through the preparation pathway: German language training, professional preparation, document support, interview preparation and pre-departure guidance.</dd>
                <dt>Intended result</dt>
                <dd>The student progresses through the CGP preparation pathway with a clear understanding of the requirements and is better prepared for the next stages of the Germany journey.</dd>
              </dl>
            </article>
          </div>
          <div class="span-6 reveal">
            <article class="case-study">
              <h3>German healthcare partnership</h3>
              <dl>
                <dt>Situation</dt>
                <dd>A German healthcare institution is looking for a reliable international partner to help identify and prepare suitable candidates from Sri Lanka.</dd>
                <dt>What CGP does</dt>
                <dd>Applies its partnership model: candidate selection, German language preparation, professional development, documentation, employer interviews, visa preparation and integration support.</dd>
                <dt>Intended result</dt>
                <dd>A structured pathway for institutions to work with motivated, professionally prepared Sri Lankan candidates, supporting long-term cooperation between Germany and Sri Lanka.</dd>
              </dl>
            </article>
          </div>
          <div class="why__breakout reveal" style="grid-column: 1 / 13;">
            <blockquote>&ldquo;We don't just recruit students. We prepare and support them through the entire pathway - from candidate identification and German language preparation to partner interviews, pre-departure preparation, arrival in Germany and integration support - while building long-term relationships with German healthcare institutions.&rdquo;</blockquote>
            <p class="micro-label">- The CGP model</p>
          </div>
        </div>

        <div class="stats reveal">
          <div class="grid">
            <div class="stat">
              <p class="stat__value">3<sup>+</sup></p>
              <p class="stat__label">Years of experience</p>
            </div>
            <div class="stat">
              <p class="stat__value">100<sup>+</sup></p>
              <p class="stat__label">Students guided</p>
            </div>
            <div class="stat">
              <p class="stat__value">500<sup>+</sup></p>
              <p class="stat__label">Hours of German language training</p>
            </div>
            <div class="stat">
              <p class="stat__value">24<sup>h</sup></p>
              <p class="stat__label">Average enquiry response time</p>
            </div>
          </div>
          <p class="stats__note">Figures shown are working placeholders supplied for layout purposes and will be replaced with verified numbers before launch.</p>
        </div>
      </div>
    </section>

    <section class="section" id="our-approach" aria-labelledby="approach-title">
      <div class="container">
{section_head("04", "Our Approach", "Wie wir arbeiten")}
        <div class="grid row-gap-lg">
          <div class="col-wide reveal">
            <p class="display" id="approach-title">Prepared, guided and monitored - at every stage.</p>
            <p class="lead" style="margin-top: var(--space-3); max-width: 42em;">Eight commitments that shape how we work with every candidate.</p>
          </div>
          <ol class="approach reveal">
            <li class="approach__item"><span class="approach__index">01</span><span class="approach__text">Starting candidate preparation at an early stage.</span></li>
            <li class="approach__item"><span class="approach__index">02</span><span class="approach__text">Systematic German-language learning.</span></li>
            <li class="approach__item"><span class="approach__index">03</span><span class="approach__text">Selecting motivated and suitable candidates.</span></li>
            <li class="approach__item"><span class="approach__index">04</span><span class="approach__text">Individual guidance and monitoring.</span></li>
            <li class="approach__item"><span class="approach__index">05</span><span class="approach__text">Cultural and professional preparation.</span></li>
            <li class="approach__item"><span class="approach__index">06</span><span class="approach__text">Realistic expectations about Ausbildung and life in Germany.</span></li>
            <li class="approach__item"><span class="approach__index">07</span><span class="approach__text">Preparation before departure.</span></li>
            <li class="approach__item"><span class="approach__index">08</span><span class="approach__text">Long-term cooperation with German institutions.</span></li>
          </ol>
        </div>
      </div>
    </section>
""" + cta_strip("Fragen?", "Ask us anything.",
                "We aim to respond to every enquiry within one working day.")


# ==========================================================================
# STUDENTS
# ==========================================================================

STUDENT_SERVICES = [
    ("Nursing Ausbildung Programme",
     "Our main pathway: complete preparation for Germany's recognised vocational nursing training."),
    ("Other Ausbildung Guidance",
     "Guidance on other Ausbildung routes where nursing is not the right fit for your goals."),
    ("German Language Training",
     "Structured coursework building towards the level German employers and authorities require."),
    ("Application Support",
     "We prepare and submit your applications correctly and on time."),
    ("Document Preparation",
     "Certificates, translations and supporting paperwork - checked before anything is submitted."),
    ("Interview Preparation",
     "Practice and coaching for employer interviews with German healthcare institutions."),
    ("Visa Guidance",
     "Step-by-step guidance through the German visa process with your documents in order."),
    ("Career Guidance",
     "Honest advice on where the pathway can lead and what it will ask of you."),
    ("Pre-Departure Orientation",
     "Practical preparation for life in Germany: culture, workplace expectations and arrival logistics."),
    ("Germany Arrival Support",
     "Support in the first period after you land, when everything is unfamiliar."),
    ("Integration Support",
     "Help settling into your workplace, your training and daily life in Germany."),
    ("Ongoing Student Support",
     "A continuing point of contact for as long as you are on the pathway."),
]

student_rows = "\n".join(
    f"""          <div class="service-row reveal">
            <p class="service-row__index">1.{i:02d}</p>
            <h3 class="service-row__title">{name}</h3>
            <p class="service-row__desc">{desc}</p>
          </div>""" for i, (name, desc) in enumerate(STUDENT_SERVICES, 1)
)

STUDENT_FAQ = [
    ("What is Ausbildung in Germany?",
     "Ausbildung is Germany's dual vocational training system. It combines classroom study with paid, hands-on training inside a real workplace, and leads to a state-recognised German qualification. It is a training route with a contract and a training allowance - not a university degree, and not a job placement."),
    ("What is nursing Ausbildung?",
     "Nursing Ausbildung is the Ausbildung route for nursing. It prepares you for a state-recognised German nursing qualification, combining theory at a training school with supervised practical training inside a hospital, clinic or care institution."),
    ("How long does nursing Ausbildung take?",
     "In Germany, nursing Ausbildung is a full vocational training programme and normally runs for three years. The exact duration and structure are set by German law and by the institution that takes you on, so we confirm the specifics for your pathway with you during counselling."),
    ("Who can apply through CGP?",
     "CGP works with young Sri Lankans who want to pursue nursing Ausbildung in Germany and who are ready to commit to the preparation it requires. The full picture is on the <a href=\"who-can-apply.html\">Who Can Apply</a> page - educational background, genuine interest in nursing and healthcare, systematic German-language learning, and readiness for professional and cultural preparation."),
    ("Do I need to know German before joining CGP?",
     "No. You do not need any German to make your first enquiry or to start with CGP - building that language is the purpose of the programme. You do need it to succeed: reaching the level required by German institutions is a genuine requirement of the process, not an optional extra."),
    ("What German-language level will I need?",
     "The level is set by the German institution you apply to, and for nursing Ausbildung it is normally B1 or B2. The CGP pathway runs from A1 to B2 so that you are prepared for what the institution asks of you, and we confirm the exact requirement for your intended institution during assessment."),
    ("How long does it normally take to reach B2 German?",
     "It depends on your starting point, how intensively you study and how much practice you get. CGP does not promise a fixed number of months, and you should be sceptical of anyone who does. We assess your progress continuously and give you a realistic timeline during counselling, updated honestly as you go."),
    ("Does CGP guarantee an Ausbildung position?",
     "No. CGP prepares and supports candidates; it does not guarantee or sell Ausbildung positions. Final assessment and selection remain with the respective German institution. What we do promise is proper preparation and honest information at every stage."),
    ("Who makes the final decision on my application?",
     "The German Ausbildung institution. Its interview panel and admissions team assess your application and decide whether to offer you a training place. CGP's role is to prepare you for that assessment and to submit your documentation correctly."),
    ("Does CGP guarantee a German visa?",
     "No, and no one can. The decision is made by the German authorities on the basis of your documents, your training contract and the rules that apply to your case. CGP's role is visa guidance: making sure your file is complete, correct and submitted properly."),
    ("Will I receive a salary during nursing Ausbildung?",
     "Yes. Ausbildung in Germany is a paid training contract: trainees receive a monthly training allowance paid by the training institution, which rises with each year of training. The amount is set by the institution or the applicable collective agreement, varies between employers and regions, and is confirmed to you by the institution that offers you a place. CGP does not quote salary figures."),
    ("What support does CGP provide during preparation?",
     "German language training from A1 to B2, professional and cultural preparation for living and working in Germany, documentation and application preparation, support with applications to German institutions, interview preparation, visa guidance, pre-departure preparation, arrival support and ongoing student support for as long as you are on the pathway. The <a href=\"complete-pathway.html\">Complete Pathway</a> page sets out the full sequence."),
    ("What documents will I need for applications?",
     "Typically your passport, school certificates and transcripts, a curriculum vitae, language certificates, and the medical and other documents the German institution or the authorities ask for. The exact list is set by the institution and the authorities, and translations or certified copies may be required. We confirm the list with you in writing and check everything before it is submitted."),
    ("Can I apply directly to German institutions?",
     "Yes. Nothing prevents you from applying directly, and CGP does not claim exclusivity over any institution. What CGP provides is preparation, correct documentation and support through a process that is unfamiliar, conducted in a second language, and assessed by institutions applying their own criteria."),
    ("What happens after completing nursing Ausbildung in Germany?",
     "A completed nursing Ausbildung is a state-recognised German qualification. It opens routes to employment as a qualified nursing professional, and to specialisation and further study within German healthcare. We will not promise you a specific job or salary - what we do is prepare you properly for the qualification itself."),
    ("What responsibilities do students have while following the CGP preparation programme?",
     "Attendance and active participation in German-language classes and preparation activities, completing the assigned learning tasks, keeping to the timelines agreed with you, providing accurate documents and information, responding to your point of contact, and telling us early if your circumstances or intentions change. Preparation is a two-way commitment: we do our part and you do yours."),
]


def faq_items(items, group):
    return "\n".join(
        f"""            <div class="accordion__item{' is-open' if i == 1 else ''}">
              <h3>
                <button class="accordion__trigger" aria-expanded="{'true' if i == 1 else 'false'}">
                  <span class="accordion__index">{group}.{i:02d}</span>
                  <span class="accordion__title">{q}</span>
                  <span class="accordion__glyph" aria-hidden="true">+</span>
                </button>
              </h3>
              <div class="accordion__panel">
                <div class="accordion__panel-inner">
                  <p>{a}</p>
                </div>
              </div>
            </div>""" for i, (q, a) in enumerate(items, 1)
    )


students_faq_items = faq_items(STUDENT_FAQ, "1")

# The hero banner artwork supplied by the client (2026-10-15), shown whole and
# never cropped. Its message is repeated as real text below it.
STUDENTS_HERO_IMAGE = "hero-students-parents.jpg"
STUDENTS_HERO_ALT = ("Banner: Students &amp; Parents - Your journey starts with preparation. "
                     "Four young Sri Lankan students studying German together, with the "
                     "German flag and the Berlin TV tower behind them.")

STUDENTS = f"""
    <section class="hero" aria-labelledby="students-hero-title">

      <!-- Client-supplied Students & Parents banner (2026-10-15). It carries
           its own headline, so it is shown whole - never cropped - and that
           message is repeated as real text underneath. No call-to-action
           buttons appear in this banner, by instruction. -->
      <div class="container">
        <figure class="hero-banner">
          <img src="assets/images/{STUDENTS_HERO_IMAGE}" alt="{STUDENTS_HERO_ALT}" width="1944" height="809" fetchpriority="high">
          <figcaption class="hero-banner__caption">
            <span class="micro-label">Students &amp; Parents</span>
            <span class="hero-banner__line">Learn German. Prepare Yourself. Build Your Pathway to Germany.</span>
          </figcaption>
        </figure>

        <div class="grid hero__head">
          <div class="hero__head-main">
            <p class="hero__kicker micro-label">Preparation &middot; Education &middot; Support</p>
            <h1 class="hero__title" id="students-hero-title">Your journey starts with <em>preparation.</em></h1>
          </div>
          <div class="hero__head-side">
            <p class="lead hero__lede">CGP supports young Sri Lankans through structured German-language education, professional and cultural preparation, and responsible guidance towards vocational training opportunities in Germany.</p>
          </div>
        </div>
      </div>

      <div class="hero__strip">
        <div class="container">
          <div class="grid">
            <p class="hero__fact"><strong>Best suited to</strong> Motivated students, around 18&ndash;25, aiming at healthcare in Germany.</p>
            <p class="hero__fact"><strong>Core requirement</strong> Commitment to systematic German-language learning.</p>
            <p class="hero__fact"><strong>Main offering</strong> Nursing Ausbildung Programme.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="start-title">
      <div class="container">
{section_head("01", "Start here", "Three pages")}
        <div class="grid">
          <div class="col-wide reveal" style="margin-bottom: var(--space-5);">
            <p class="display" id="start-title">The Students &amp; Parents section, in three pages.</p>
          </div>
          <div class="route-cards">
            <a class="route-card reveal" href="who-can-apply.html">
              <p class="route-card__index">01</p>
              <h3 class="route-card__title">Who Can Apply</h3>
              <p class="route-card__desc">The eligibility and the personal commitment CGP asks for from candidates before anyone enrols.</p>
              <span class="route-card__more">Read <span aria-hidden="true">&rarr;</span></span>
            </a>
            <a class="route-card reveal" href="complete-pathway.html">
              <p class="route-card__index">02</p>
              <h3 class="route-card__title">Complete Pathway</h3>
              <p class="route-card__desc">The whole preparation journey in fifteen stages - and which of them CGP is responsible for.</p>
              <span class="route-card__more">Read <span aria-hidden="true">&rarr;</span></span>
            </a>
            <a class="route-card reveal" href="faq.html">
              <p class="route-card__index">03</p>
              <h3 class="route-card__title">Frequently Asked Questions</h3>
              <p class="route-card__desc">The sixteen questions students and parents ask us most, answered honestly.</p>
              <span class="route-card__more">Read <span aria-hidden="true">&rarr;</span></span>
            </a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="included-title">
      <div class="container">
{section_head("02", "What's included", "Twelve student services")}
        <div class="grid">
          <div class="col-wide reveal" style="margin-bottom: var(--space-5);">
            <p class="display" id="included-title">Every step, covered by someone accountable.</p>
          </div>
          <div class="service-list">
{student_rows}
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="transparency-title">
      <div class="container">
{section_head("03", "Programme Information &amp; Transparency", "Before you enrol")}
        <div class="grid">
          <div class="col-left reveal">
            <p class="display" id="transparency-title" style="margin-bottom: var(--space-4);">Clear and transparent communication, before you commit.</p>
          </div>
          <div class="col-right prose reveal">
            <p>CGP believes in clear and transparent communication with students and their families. Detailed information regarding programme structure, German-language preparation, responsibilities, applicable educational and preparation costs, and payment arrangements is provided directly to prospective candidates before enrolment. No student should enrol without understanding the applicable programme conditions.</p>
            <p><a class="btn btn--outline" href="contact.html">Request programme information <span class="btn__glyph" aria-hidden="true">&rarr;</span></a></p>
          </div>
        </div>
      </div>
    </section>
""" + cta_strip("Bereit?", "Start with a conversation.",
                "No commitment at the enquiry stage - we assess fit first.")


# ==========================================================================
# STUDENTS & PARENTS · WHO CAN APPLY
# ==========================================================================

WHO_CAN_APPLY_CRITERIA = [
    ("Interest in nursing Ausbildung in Germany",
     "CGP works with young Sri Lankans who want to pursue nursing Ausbildung in Germany, and who are interested in building a professional healthcare career there rather than taking a short-term route abroad."),
    ("An appropriate educational background",
     "The intended Ausbildung pathway has an educational starting point. German institutions set their own entry requirements, so we review your school certificates and results with you during eligibility assessment, and tell you honestly where you stand."),
    ("Genuine interest in nursing, healthcare and vocational education",
     "Nursing Ausbildung is a demanding profession and a real qualification, not a route chosen for the destination alone. We look for candidates who actually want the work."),
    ("Commitment to systematic German-language learning",
     "You must be ready to learn German systematically, up to the level required by German institutions. Language is the foundation of everything else in this pathway, and it is not optional."),
    ("Willingness to participate regularly",
     "Regular participation in language classes, preparation activities and the learning tasks assigned to you. Progress depends on consistent attendance and work between sessions."),
    ("Readiness for professional and cultural preparation",
     "Readiness to undertake professional and cultural preparation for living, studying and working in Germany - including the expectations of a German workplace and daily life away from home."),
    ("Ability to meet institutional requirements",
     "The ability and willingness to meet the individual requirements set by German Ausbildung institutions and the relevant authorities, which can differ between institutions and can change over time."),
]

criteria_rows = "\n".join(
    f"""          <div class="service-row reveal">
            <p class="service-row__index">2.{i:02d}</p>
            <h3 class="service-row__title">{name}</h3>
            <p class="service-row__desc">{desc}</p>
          </div>""" for i, (name, desc) in enumerate(WHO_CAN_APPLY_CRITERIA, 1)
)

WHO_CAN_APPLY = page_hero(
    "04", page_hero_of("who-can-apply.html"), "Who Can Apply",
    "Who can apply.",
    "This page sets out the basic eligibility and the personal commitment CGP asks for from candidates interested in the nursing Ausbildung pathway in Germany - and what meeting those criteria does and does not mean.",
    [("For", "Young Sri Lankans aiming at nursing Ausbildung in Germany"),
     ("Core requirement", "Commitment to systematic German-language learning"),
     ("Decided by", "The German institution - not CGP")],
)

WHO_CAN_APPLY += band("student-writing.jpg", "A student writing notes by hand in a notebook", "This pathway asks something of you") + f"""
    <section class="section" aria-labelledby="asks-title">
      <div class="container">
{section_head("01", "Who this is for", "Be honest with yourself here")}
        <div class="grid">
          <div class="col-wide prose reveal">
            <p class="display" id="asks-title" style="margin-bottom: var(--space-4);">This pathway asks something of you.</p>
            <p>Our best students are motivated young people - usually around 18 to 25 - who genuinely want to build a professional healthcare career in Germany, and who need reliable guidance with German language training, applications, documentation, visa preparation and ongoing support.</p>
            <p>What it is not: a shortcut. Nursing Ausbildung is real vocational training in a second language, inside a demanding profession. The students who do well are the ones who treat the language course as the foundation of everything else.</p>
            <p>If that sounds like the wrong fit, tell us early and we will say so honestly. That is a better outcome for everyone than a student who commits to a pathway they did not want.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="criteria-title">
      <div class="container">
{section_head("02", "What we look for", "Seven points")}
        <div class="grid">
          <div class="col-wide reveal" style="margin-bottom: var(--space-5);">
            <p class="display" id="criteria-title">Eligibility and commitment.</p>
          </div>
          <div class="service-list">
{criteria_rows}
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="notice-title">
      <div class="container">
{section_head("03", "Important notice", "Please read this")}
        <div class="grid">
          <div class="col-wide reveal">
            <div class="notice">
              <p id="notice-title"><strong>Meeting CGP's initial eligibility criteria does not guarantee an Ausbildung position, employment contract or visa.</strong> Final assessment and selection remain with the respective German institution.</p>
            </div>
          </div>
          <div class="col-full reveal" style="margin-top: var(--space-5);">
            <div class="route-cards">
              <a class="route-card reveal" href="complete-pathway.html">
                <p class="route-card__index">Next</p>
                <h3 class="route-card__title">Complete Pathway</h3>
                <p class="route-card__desc">See all fifteen stages of the preparation journey, and which of them CGP is responsible for.</p>
                <span class="route-card__more">Read <span aria-hidden="true">&rarr;</span></span>
              </a>
              <a class="route-card reveal" href="faq.html">
                <p class="route-card__index">Questions</p>
                <h3 class="route-card__title">Frequently Asked Questions</h3>
                <p class="route-card__desc">German level, timelines, decisions, costs and support - answered for students and parents.</p>
                <span class="route-card__more">Read <span aria-hidden="true">&rarr;</span></span>
              </a>
              <a class="route-card reveal" href="students.html">
                <p class="route-card__index">Section</p>
                <h3 class="route-card__title">Students &amp; Parents</h3>
                <p class="route-card__desc">Back to the section overview, with the twelve services included in the programme.</p>
                <span class="route-card__more">Read <span aria-hidden="true">&rarr;</span></span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
""" + cta_strip("Bereit?", "Start with a conversation.",
                "No commitment at the enquiry stage - we assess fit first.")


# ==========================================================================
# STUDENTS & PARENTS · COMPLETE PATHWAY
# ==========================================================================

# The fifteen stages, grouped into phases. The client's developer note requires
# CGP's preparation role to be distinguishable from the German institution's
# assessment and selection role, so every stage carries an owner badge.
COMPLETE_PATHWAY_PHASES = [
    ("Phase 01", "Enquiry &amp; assessment", "Carried out by CGP", [
        ("01", "Initial Enquiry", "cgp", "CGP"),
        ("02", "Eligibility Assessment", "cgp", "CGP"),
    ]),
    ("Phase 02", "Registration &amp; German language", "Carried out by CGP", [
        ("03", "Registration with CGP", "cgp", "CGP"),
        ("04", "German Language &ndash; A1", "cgp", "CGP"),
        ("05", "German Language &ndash; A2", "cgp", "CGP"),
        ("06", "German Language &ndash; B1", "cgp", "CGP"),
        ("07", "German Language &ndash; B2", "cgp", "CGP"),
    ]),
    ("Phase 03", "Preparation, documentation &amp; applications", "Carried out by CGP", [
        ("08", "Professional &amp; Cultural Preparation", "cgp", "CGP"),
        ("09", "Documentation &amp; Application Preparation", "cgp", "CGP"),
        ("10", "Applications to German Institutions", "cgp", "CGP"),
    ]),
    ("Phase 04", "Assessment &amp; selection", "Carried out by the German institution", [
        ("11", "Interview &amp; Assessment by German Institution", "de", "German institution"),
        ("12", "Selection &amp; Ausbildung Contract", "de", "German institution"),
    ]),
    ("Phase 05", "Visa, departure &amp; arrival", "CGP prepares, then the training begins", [
        ("13", "Visa &amp; Pre-Departure Preparation", "cgp", "CGP"),
        ("14", "Travel to Germany", "cgp", "CGP"),
        ("15", "Start Nursing Ausbildung", "de", "German institution"),
    ]),
]


def route_phase(number, label, role, steps):
    step_rows = "\n".join(
        f"""            <li class="route__step">
              <span class="route__num">{num}</span>
              <span class="route__name">{name}</span>
              <span class="route__owner route__owner--{owner_class}">{owner_label}</span>
            </li>""" for num, name, owner_class, owner_label in steps
    )
    return f"""          <li class="route__phase">
            <div class="route__phase-head">
              <p class="route__phase-label"><span class="micro-label">{number}</span> {label}</p>
              <span class="micro-label route__phase-role">{role}</span>
            </div>
            <ol class="route__steps">
{step_rows}
            </ol>
          </li>"""


complete_pathway_rows = "\n".join(
    route_phase(number, label, role, steps)
    for number, label, role, steps in COMPLETE_PATHWAY_PHASES
)

COMPLETE_PATHWAY = page_hero(
    "05", page_hero_of("complete-pathway.html"), "Complete Pathway",
    "One pathway, fifteen stages.",
    "The complete preparation journey, from your first enquiry to your first day of nursing Ausbildung in Germany - with CGP's role and the German institution's role shown separately at every stage.",
    [("Starts with", "Initial enquiry and eligibility assessment"),
     ("Prepared by", "CGP - language, preparation and documentation"),
     ("Decided by", "The German institution - assessment and selection")],
) + f"""
    <section class="section" aria-labelledby="route-title">
      <div class="container">
{section_head("01", "The complete pathway", "Fifteen stages &middot; five phases")}
        <div class="grid">
          <div class="col-wide reveal" style="margin-bottom: var(--space-3);">
            <p class="display" id="route-title">Every stage, and who is responsible for it.</p>
            <p class="lead" style="margin-top: var(--space-3);">CGP prepares and supports candidates. It does not guarantee or sell Ausbildung positions - assessment and selection belong to the German institution.</p>
          </div>
          <ol class="route reveal">
{complete_pathway_rows}
          </ol>
        </div>
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="roles-title">
      <div class="container">
{section_head("02", "Two roles, one pathway", "Who does what")}
        <div class="grid">
          <div class="roles">
            <div class="roles__block reveal">
              <h3>What CGP is responsible for</h3>
              <p>Eligibility assessment and counselling, registration, German language training from A1 to B2, professional and cultural preparation, documentation and application preparation, submitting applications, interview preparation, visa guidance, pre-departure preparation and support after arrival. CGP prepares and supports candidates throughout.</p>
            </div>
            <div class="roles__block reveal">
              <h3>What the German institution is responsible for</h3>
              <p>Interviewing and assessing applicants, deciding who is selected, offering the Ausbildung contract, and setting the requirements a candidate must meet. The final decision on every application rests with the institution - not with CGP.</p>
            </div>
          </div>
          <div class="col-wide reveal">
            <div class="notice">
              <p><strong>CGP prepares and supports candidates; it does not guarantee or sell Ausbildung positions.</strong> Meeting CGP's initial eligibility criteria does not guarantee an Ausbildung position, employment contract or visa. Final assessment and selection remain with the respective German institution.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
""" + cta_strip("Bereit?", "Start with a conversation.",
                "No commitment at the enquiry stage - we assess fit first.")


# ==========================================================================
# STUDENTS & PARENTS · FREQUENTLY ASKED QUESTIONS
# ==========================================================================

FAQ_PAGE = page_hero(
    "06", page_hero_of("faq.html"), "Frequently Asked Questions",
    "Straight answers.",
    "The sixteen questions students and parents ask us most - about Ausbildung, German language, timelines, who decides, visas, salary, documents and what we expect of you while you are on the programme.",
    [("Written for", "Students and parents"),
     ("Covers", "Ausbildung, language, decisions, costs and support"),
     ("Still unsure?", f'<a href="mailto:{EMAIL}">{EMAIL}</a>')],
) + f"""
    <section class="section" aria-labelledby="faq-title">
      <div class="container">
{section_head("01", "Frequently asked questions", "Sixteen questions")}
        <div class="grid">
          <div class="col-wide reveal" style="margin-bottom: var(--space-4);">
            <p class="display" id="faq-title">No promises we cannot keep.</p>
          </div>
          <div class="col-full">
            <div class="accordion--light" data-accordion>
{students_faq_items}
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="transparency-title">
      <div class="container">
{section_head("02", "Programme Information &amp; Transparency", "Before you enrol")}
        <div class="grid">
          <div class="col-wide reveal">
            <p class="display" id="transparency-title" style="margin-bottom: var(--space-4);">No student should enrol without understanding the programme.</p>
            <div class="prose">
              <p>CGP believes in clear and transparent communication with students and their families. Detailed information regarding programme structure, German-language preparation, responsibilities, applicable educational and preparation costs, and payment arrangements is provided directly to prospective candidates before enrolment. No student should enrol without understanding the applicable programme conditions.</p>
            </div>
            <p class="lead" style="margin-top: var(--space-4);">Still have a question that is not here? Ask us directly - before you commit to anything.</p>
          </div>
        </div>
      </div>
    </section>
""" + cta_strip("Bereit?", "Start with a conversation.",
                "No commitment at the enquiry stage - we assess fit first.")


# ==========================================================================
# GERMAN PARTNERS
# ==========================================================================

PARTNER_SERVICES = [
    ("Candidate Selection &amp; Preparation",
     "We identify motivated Sri Lankan candidates and prepare them - language, professional readiness and documentation - before they reach your interview panel."),
    ("Employer Interview Coordination",
     "We coordinate and schedule interviews between your team and prepared candidates, and brief candidates thoroughly beforehand."),
    ("Partnership Development",
     "We build long-term working relationships with German healthcare institutions rather than one-off placements."),
]

partner_rows = "\n".join(
    f"""          <div class="service-row reveal">
            <p class="service-row__index">1.{i:02d}</p>
            <h3 class="service-row__title">{name}</h3>
            <p class="service-row__desc">{desc}</p>
          </div>""" for i, (name, desc) in enumerate(PARTNER_SERVICES, 1)
)

PARTNER_STEPS = [
    ("Introduction",
     "We learn what your institution needs: roles, timing, language expectations and the profile of candidate that succeeds in your environment."),
    ("Candidate selection",
     "We select from motivated Sri Lankan candidates already engaged with the CGP pathway, matched against your requirements."),
    ("Preparation",
     "Language training and professional preparation continue against the level your institution requires."),
    ("Documentation",
     "Certificates, translations and supporting paperwork are compiled and checked before they reach you."),
    ("Interviews",
     "We coordinate interviews with your team and prepare candidates so the conversation is substantive on both sides."),
    ("Visa &amp; departure",
     "We guide the candidate through visa preparation and pre-departure orientation."),
    ("Arrival &amp; integration",
     "Arrival support and integration support continue after the candidate lands, so they settle into your institution properly."),
]

partner_timeline = "\n".join(
    f"""            <div class="timeline__item reveal">
              <p class="timeline__index">{i:02d}</p>
              <div class="timeline__body">
                <h3>{name}</h3>
                <p>{desc}</p>
              </div>
            </div>""" for i, (name, desc) in enumerate(PARTNER_STEPS, 1)
)

PARTNERS = page_hero(
    "07", page_hero_of("partners.html"), "German Partners",
    "A partner, not a placement agency.",
    "CGP works with German hospitals, clinics and care institutions as a long-term partner. We select motivated Sri Lankan candidates and prepare them properly - language, professional readiness and documentation - before they ever sit in front of your interview panel.",
    [("For", "German hospitals, clinics and care institutions"),
     ("Model", "Long-term partnership, not one-off recruitment"),
     ("Contact", f'<a href="mailto:{EMAIL}">{EMAIL}</a>')],
    meta="F&uuml;r Partnereinrichtungen",
) + band("medical-team.jpg", "A team of healthcare professionals in surgical dress viewed from below", "Partnering with German healthcare institutions") + f"""
    <section class="section section--dark" id="partnership-services" aria-labelledby="pservices-title">
      <div class="container">
{section_head("01", "Partnership services", "What we provide")}
        <div class="grid">
          <div class="col-wide reveal" style="margin-bottom: var(--space-5);">
            <p class="display" id="pservices-title">Prepared candidates. Reliable process.</p>
          </div>
          <div class="service-list">
{partner_rows}
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="how-the-partnership-works" aria-labelledby="pwork-title">
      <div class="container">
{section_head("02", "How the partnership works", "Seven stages")}
        <div class="grid">
          <div class="col-left reveal" style="margin-bottom: var(--space-4);">
            <p class="display" id="pwork-title">From introduction to integration.</p>
            <p class="small" style="margin-top: var(--space-3); max-width: 34em;">The same structure applies to every partnership, so your team always knows which stage a candidate is at.</p>
          </div>
          <div class="col-full timeline" style="grid-column: 1 / 13;">
{partner_timeline}
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="partnership-model" style="padding-top: 0;" aria-labelledby="pmodel-title">
      <div class="container">
{section_head("03", "The partnership model", "Illustrative example", "pmodel-title")}
        <div class="grid row-gap-lg">
          <div class="col-full reveal" style="grid-column: 1 / 13;">
            <div class="notice">
              <p><strong>Please read:</strong> the example below describes how the CGP partnership model is designed to work. It is illustrative of our process - it is not an account of a specific completed partnership, and no outcome is implied or promised.</p>
            </div>
          </div>
          <div class="col-left reveal">
            <article class="case-study">
              <h3>German healthcare partnership</h3>
              <dl>
                <dt>Situation</dt>
                <dd>A German healthcare institution is looking for a reliable international partner to help identify and prepare suitable candidates from Sri Lanka.</dd>
                <dt>What CGP does</dt>
                <dd>Candidate selection, German language preparation, professional development, documentation, employer interviews, visa preparation and integration support.</dd>
                <dt>Intended result</dt>
                <dd>A structured pathway for institutions to work with motivated, professionally prepared Sri Lankan candidates, while supporting long-term cooperation between Germany and Sri Lanka.</dd>
              </dl>
            </article>
          </div>
          <figure class="col-right reveal">
            <img class="img-bw" src="assets/images/clinical-review.jpg" alt="Two clinicians reviewing medical imaging together on a screen" width="1600" height="1067" loading="lazy">
            <figcaption class="small" style="padding-top: var(--space-1); border-bottom: 1px solid var(--color-rule);">Professionally prepared candidates</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section section--dark" id="why-work-with-cgp" aria-labelledby="pwhy-title">
      <div class="container">
{section_head("04", "Why work with CGP", "Four reasons")}
        <div class="grid row-gap">
          <div class="col-wide reveal" style="margin-bottom: var(--space-4);">
            <p class="display" id="pwhy-title">Preparation is the whole point.</p>
          </div>
          <div class="span-6 reveal">
            <article class="case-study" style="border-top-color: var(--color-gold);">
              <h3>Candidates arrive prepared</h3>
              <p class="small" style="color: var(--color-grey-400); max-width: 40em;">Language training, professional preparation and complete documentation happen before the interview, not after the contract.</p>
            </article>
          </div>
          <div class="span-6 reveal">
            <article class="case-study" style="border-top-color: var(--color-gold);">
              <h3>One accountable partner</h3>
              <p class="small" style="color: var(--color-grey-400); max-width: 40em;">A single point of contact from selection through to integration, rather than a chain of intermediaries.</p>
            </article>
          </div>
          <div class="span-6 reveal">
            <article class="case-study" style="border-top-color: var(--color-gold);">
              <h3>Ethical recruitment</h3>
              <p class="small" style="color: var(--color-grey-400); max-width: 40em;">Transparent fees and documented policies on the student side, so candidates arrive without hidden debts or false expectations.</p>
            </article>
          </div>
          <div class="span-6 reveal">
            <article class="case-study" style="border-top-color: var(--color-gold);">
              <h3>Support after arrival</h3>
              <p class="small" style="color: var(--color-grey-400); max-width: 40em;">Integration support continues once the candidate joins you, which is when retention is actually decided.</p>
            </article>
          </div>
        </div>
      </div>
    </section>

    <section class="section cta" aria-labelledby="pcta-title">
      <div class="container">
        <div class="grid">
          <p class="cta__title reveal" id="pcta-title"><span class="de">Interesse?</span> Let's talk.</p>
          <div class="cta__actions reveal">
            <a class="btn btn--inverse" href="mailto:{EMAIL}?subject=Partnership%20enquiry%20%2D%20German%20healthcare%20institution">Email our partnership team <span class="btn__glyph" aria-hidden="true">&rarr;</span></a>
            <a class="btn btn--inverse" href="contact.html">Contact page</a>
          </div>
          <ul class="cta__contact reveal">
            <li><span class="micro-label">Email</span> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><span class="micro-label">Address</span> <span>No. 143/10, Wilimbula, Henegama 11715, Gampaha District, Sri Lanka</span></li>
            <li><span class="micro-label">Hours</span> <span>Monday&ndash;Friday, 9:00&ndash;17:00 (Sri Lanka time)</span></li>
          </ul>
        </div>
      </div>
    </section>
"""


# ==========================================================================
# CURRENT STUDENTS
# ==========================================================================

CURRENT = page_hero(
    "08", page_hero_of("current-students.html"), "Current Students",
    "Where our students are right now.",
    "Trust is built on evidence, not adjectives. This page tracks where CGP students currently stand on the pathway - and sets out the support available to you while you are on it.",
    [("For", "Students currently enrolled with CGP"),
     ("Support", "Ongoing student support at every stage"),
     ("Response", "We aim to reply within one working day")],
) + f"""
    <section class="section" aria-labelledby="board-title">
      <div class="container">
{section_head("01", "Progress board", "Four stages")}
        <div class="grid">
          <div class="col-left reveal" style="margin-bottom: var(--space-5);">
            <p class="display" id="board-title">Real students. Visible progress.</p>
            <p class="small" style="margin-top: var(--space-3); max-width: 34em;">From the language classroom in Sri Lanka to training wards in Germany.</p>
          </div>

          <div class="col-full" style="grid-column: 1 / 13;">
            <div class="tabs" role="tablist" aria-label="Student progress stages">
              <button class="tab" role="tab" id="tab-1" aria-selected="true" aria-controls="panel-1">Language training</button>
              <button class="tab" role="tab" id="tab-2" aria-selected="false" aria-controls="panel-2" tabindex="-1">Interviews &amp; matching</button>
              <button class="tab" role="tab" id="tab-3" aria-selected="false" aria-controls="panel-3" tabindex="-1">Visa stage</button>
              <button class="tab" role="tab" id="tab-4" aria-selected="false" aria-controls="panel-4" tabindex="-1">In Germany</button>
            </div>

            <div class="tab-panel" role="tabpanel" id="panel-1" aria-labelledby="tab-1">
              <div class="tab-panel__count">
                <p class="stat__value">50<sup>+</sup></p>
                <p class="stat__label">Students currently in preparation</p>
              </div>
              <div class="tab-panel__desc">
                <p>Working through structured German coursework and healthcare career preparation at CGP, building from beginner level towards employer-ready proficiency.</p>
              </div>
              <figure class="tab-panel__media">
                <img class="img-bw" src="assets/images/students-laptop.jpg" alt="Students studying together at a laptop" width="1600" height="1067" loading="lazy">
              </figure>
            </div>

            <div class="tab-panel" role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
              <div class="tab-panel__count">
                <p class="stat__value stat__value--pending">Not yet published</p>
                <p class="stat__label">Candidates in interview &amp; matching</p>
              </div>
              <div class="tab-panel__desc">
                <p>Documents complete, now being coordinated with German healthcare institutions for employer interviews and preparation.</p>
              </div>
              <figure class="tab-panel__media">
                <img class="img-bw" src="assets/images/documents-desk.jpg" alt="Application documents and notes laid out on a desk" width="1600" height="1068" loading="lazy">
              </figure>
            </div>

            <div class="tab-panel" role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>
              <div class="tab-panel__count">
                <p class="stat__value stat__value--pending">Not yet published</p>
                <p class="stat__label">Students in the visa process</p>
              </div>
              <div class="tab-panel__desc">
                <p>Training position confirmed, now preparing visa applications and completing pre-departure orientation with CGP guidance.</p>
              </div>
              <figure class="tab-panel__media">
                <img class="img-bw" src="assets/images/airport-departure.jpg" alt="View of an aircraft wing above the clouds" width="1600" height="1063" loading="lazy">
              </figure>
            </div>

            <div class="tab-panel" role="tabpanel" id="panel-4" aria-labelledby="tab-4" hidden>
              <div class="tab-panel__count">
                <p class="stat__value">25<sup>+</sup></p>
                <p class="stat__label">Successful placements</p>
              </div>
              <div class="tab-panel__desc">
                <p>Arrived in Germany and begun Nursing Ausbildung, with CGP integration support continuing on the ground.</p>
              </div>
              <figure class="tab-panel__media">
                <img class="img-bw" src="assets/images/germany-berlin.jpg" alt="Berlin skyline at night with the television tower" width="1600" height="1067" loading="lazy">
              </figure>
            </div>

            <p class="students__note">Counts shown are working placeholders supplied for layout purposes. Verified student numbers and progress updates will be published here as they are confirmed.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="support-title">
      <div class="container">
{section_head("02", "Support available to you", "While you are on the pathway")}
        <div class="grid">
          <div class="col-wide reveal" style="margin-bottom: var(--space-5);">
            <p class="display" id="support-title">You always have someone to ask.</p>
          </div>
          <div class="service-list">
            <div class="service-row reveal">
              <p class="service-row__index">2.01</p>
              <h3 class="service-row__title">Ongoing student support</h3>
              <p class="service-row__desc">A continuing point of contact for as long as you are on the pathway - for questions about your course, your documents or your timeline.</p>
            </div>
            <div class="service-row reveal">
              <p class="service-row__index">2.02</p>
              <h3 class="service-row__title">Document &amp; visa help</h3>
              <p class="service-row__desc">If a document is queried or the visa process stalls, contact us. Getting stuck alone at this stage is exactly what CGP exists to prevent.</p>
            </div>
            <div class="service-row reveal">
              <p class="service-row__index">2.03</p>
              <h3 class="service-row__title">Interview preparation</h3>
              <p class="service-row__desc">Coaching and practice before every employer interview, plus a debrief afterwards.</p>
            </div>
            <div class="service-row reveal">
              <p class="service-row__index">2.04</p>
              <h3 class="service-row__title">Pre-departure orientation</h3>
              <p class="service-row__desc">Practical preparation for life in Germany - culture, workplace expectations and what happens when you land.</p>
            </div>
            <div class="service-row reveal">
              <p class="service-row__index">2.05</p>
              <h3 class="service-row__title">Arrival &amp; integration support</h3>
              <p class="service-row__desc">Support in your first period in Germany and while you settle into your training and daily life.</p>
            </div>
            <div class="service-row reveal">
              <p class="service-row__index">2.06</p>
              <h3 class="service-row__title">Privacy of your documents</h3>
              <p class="service-row__desc">Your personal information and documents are handled carefully and kept secure throughout the process.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="voices-title">
      <div class="container">
{section_head("03", "Student voices", "Sample testimonials")}
        <div class="grid row-gap">
          <div class="col-wide reveal">
            <p class="display" id="voices-title">What students say about the pathway.</p>
            <p class="small" style="margin-top: var(--space-2); max-width: 34em;">Real student voices will appear here as they are confirmed. The quotes below show how the space will look.</p>
          </div>
          <div class="col-full reveal">
            <div class="notice">
              <p><strong>Sample testimonials.</strong> These quotes are illustrative placeholders written for layout purposes. They will be replaced with real, verified testimonials from CGP students, shared with their permission, before launch.</p>
            </div>
          </div>
          <article class="why-card span-4 reveal">
            <p class="why-card__index">01 - Language training</p>
            <h3>&ldquo;The German course is structured, and CGP stayed honest with me about the timeline from the very first conversation.&rdquo;</h3>
            <p>Kasuni Fernando - currently in German language training</p>
          </article>
          <article class="why-card span-4 reveal">
            <p class="why-card__index">02 - Arrived in Germany</p>
            <h3>&ldquo;The arrival support made my first weeks far less stressful than I expected. I always had someone to ask.&rdquo;</h3>
            <p>Thisara Perera - began Nursing Ausbildung in Germany</p>
          </article>
          <article class="why-card span-4 reveal">
            <p class="why-card__index">03 - Visa stage</p>
            <h3>&ldquo;Every document was checked and explained before we submitted anything. No hidden fees, no surprises.&rdquo;</h3>
            <p>Nadun Silva - completing visa preparation</p>
          </article>
          <div class="col-full reveal">
            <p><a class="btn btn--outline" href="mailto:{EMAIL}?subject=Student%20testimonial">Are you a CGP student? Share your experience <span class="btn__glyph" aria-hidden="true">&rarr;</span></a></p>
          </div>
        </div>
      </div>
    </section>
""" + cta_strip("Brauchen Sie Hilfe?", "We're here.",
                "Current students: message us any working day, 9:00&ndash;17:00 Sri Lanka time.")


# ==========================================================================
# RESOURCES & DOWNLOADS
# ==========================================================================

RESOURCES_LIST = [
    ("Nursing Ausbildung - pathway guide", "PDF guide", "nursing-ausbildung-pathway-guide.html",
     "The full pathway explained end to end: what Ausbildung is, what it requires, and what CGP does at each stage."),
    ("Document checklist", "PDF checklist", "document-checklist.html",
     "Every certificate, translation and supporting document you will need, in the order you will need it."),
    ("German language - getting started", "PDF guide", "german-language-getting-started.html",
     "What the language requirement actually means, how the course is structured, and how to study effectively."),
    ("Fees & payment policy", "PDF document", "fees-and-payment-policy.html",
     "The written fee structure and payment schedule, including the no-hidden-charges commitment."),
    ("Pre-departure checklist", "PDF checklist", "pre-departure-checklist.html",
     "What to arrange, pack and understand before you fly to Germany."),
    ("Frequently asked questions", "PDF summary", "frequently-asked-questions.html",
     "The ten questions we are asked most, with our answers, in one printable document."),
]

resource_cards = "\n".join(
    f"""          <article class="resource-card span-4 reveal">
            <div class="resource-card__meta">
              <span class="resource-card__type">{kind}</span>
              <span class="badge badge--available">Available</span>
            </div>
            <h3><a href="downloads/{file}">{name}</a></h3>
            <p>{desc}</p>
          </article>""" for name, kind, file, desc in RESOURCES_LIST
)

GLOSSARY = [
    ("Ausbildung", "Vocational training",
     "Germany's dual vocational training system: classroom study combined with paid, hands-on training inside a real employer."),
    ("Pflege", "Nursing / care",
     "The German word for nursing and care. You will see it in role titles and course names."),
    ("Pflegefachfrau / Pflegefachmann", "Qualified nurse",
     "The professional title for a qualified nursing specialist in Germany - what a completed Nursing Ausbildung leads to."),
    ("Ausbildungsvertrag", "Training contract",
     "The contract between you and the German institution providing your training."),
    ("Anerkennung", "Recognition",
     "The formal recognition of qualifications and documents by the relevant German authority."),
    ("Sprachniveau (A1&ndash;C2)", "Language level",
     "The Common European Framework scale used to describe German proficiency. Employers and authorities set the level you need to reach."),
    ("Visum", "Visa",
     "The entry permission you apply for once your training position is confirmed."),
    ("Integration", "Settling in",
     "The process of settling into work and daily life in Germany - which CGP supports after you arrive."),
]

glossary_items = "\n".join(
    f"""            <div>
              <dt>{term}<span>{gloss}</span></dt>
              <dd>{desc}</dd>
            </div>""" for term, gloss, desc in GLOSSARY
)

resource_faqs = faq_items(STUDENT_FAQ, "2")

RESOURCES = page_hero(
    "09", page_hero_of("resources.html"), "Resources &amp; Downloads",
    "Everything you need to decide.",
    "Guides, checklists and answers - so you can understand the pathway properly before you commit to it. Not ready to apply yet? This page is for you.",
    [("Downloads", "Six guides and checklists, open in your browser"),
     ("Also here", "Full FAQ and a plain-English German glossary"),
     ("Cost", "Free - no enquiry required")],
) + band("books-study.jpg", "Long library shelves filled with books under hanging lights", "Read before you commit") + f"""
    <section class="section" aria-labelledby="dl-title">
      <div class="container">
{section_head("01", "Downloads", "Guides &amp; checklists")}
        <div class="grid row-gap">
          <div class="col-wide reveal" style="margin-bottom: var(--space-3);">
            <p class="display" id="dl-title">Read before you commit.</p>
          </div>
          <div class="col-full reveal" style="grid-column: 1 / 13; margin-bottom: var(--space-3);">
            <div class="notice">
              <p><strong>Free to download, no enquiry required.</strong> These documents are written from the same information this website is built on. Each opens in your browser and can be saved or printed as a PDF. Detailed information on programme structure, German-language preparation, responsibilities, applicable educational and preparation costs, and payment arrangements is provided directly to prospective candidates before enrolment.</p>
            </div>
          </div>
{resource_cards}
        </div>
      </div>
    </section>

    <section class="section section--dark" style="padding-block: var(--space-6);" aria-labelledby="ask-title">
      <div class="container">
        <div class="grid">
          <div class="col-wide reveal">
            <p class="title" id="ask-title">Want these as one file, or a printed copy?</p>
            <p class="small" style="margin-top: var(--space-2); max-width: 34em; color: var(--color-grey-400);">Open any guide above and use your browser's print or save-as-PDF option. If you would like several together, or a printed copy, message us and we will help.</p>
          </div>
          <div class="col-narrow reveal" style="align-self: center;">
            <a class="btn btn--gold" href="mailto:{EMAIL}?subject=Resource%20request">Ask for help <span class="btn__glyph" aria-hidden="true">&rarr;</span></a>
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="rfaq-title">
      <div class="container">
{section_head("02", "Frequently asked questions", "Sixteen questions we get most")}
        <div class="grid">
          <div class="col-wide reveal" style="margin-bottom: var(--space-4);">
            <p class="display" id="rfaq-title">Straight answers.</p>
          </div>
          <div class="col-full" style="grid-column: 1 / 13;">
            <div class="accordion--light" data-accordion>
{resource_faqs}
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top: 0;" aria-labelledby="gloss-title">
      <div class="container">
{section_head("03", "German glossary", "Words you will meet")}
        <div class="grid">
          <div class="col-left reveal" style="margin-bottom: var(--space-4);">
            <p class="display" id="gloss-title">The words, in plain English.</p>
            <p class="small" style="margin-top: var(--space-3); max-width: 34em;">General explanations of terms you will encounter in the German system.</p>
          </div>
          <div class="col-full" style="grid-column: 1 / 13;">
            <dl class="glossary">
{glossary_items}
            </dl>
          </div>
        </div>
      </div>
    </section>
""" + cta_strip("Noch Fragen?", "Ask us directly.",
                "No question is too basic - we would rather you asked.")


# ==========================================================================
# CONTACT
# ==========================================================================

CONTACT = page_hero(
    "10", page_hero_of("contact.html"), "Contact",
    "Talk to us.",
    "WhatsApp is the quickest way to reach us. If you are not ready to apply yet, use the form below to request information instead - there is no commitment at this stage.",
    [("Email", f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),
     ("Hours", "Monday&ndash;Friday, 9:00&ndash;17:00 (Sri Lanka time)"),
     ("Response", "We aim to reply within one working day")],
) + f"""
    <section class="section" aria-labelledby="reach-title">
      <div class="container">
{section_head("01", "How to reach us", "Three ways")}
        <div class="grid">
          <div class="col-left reveal">
            <p class="display" id="reach-title" style="margin-bottom: var(--space-4);">Message us. We answer.</p>
            <div class="prose" style="margin-bottom: var(--space-4);">
              <p>Most students start on WhatsApp - it is quick, and you can ask the awkward questions about money and timelines without booking anything.</p>
            </div>
            <div class="hero__actions" style="margin-bottom: var(--space-5);">
              <a class="btn btn--solid" href="{WHATSAPP}" target="_blank" rel="noopener">Chat on WhatsApp <span class="btn__glyph" aria-hidden="true">&rarr;</span></a>
              <a class="btn btn--outline" href="mailto:{EMAIL}">Send an email</a>
            </div>

            <dl class="contact-block">
              <dt>WhatsApp</dt>
              <dd><a href="{WHATSAPP}" target="_blank" rel="noopener">{PHONE}</a></dd>
              <dt>Phone</dt>
              <dd>{PHONE}</dd>
              <dt>Email</dt>
              <dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
              <dt>Address</dt>
              <dd>No. 143/10, Wilimbula,<br>Henegama 11715,<br>Gampaha District, Sri Lanka</dd>
              <dt>Opening hours</dt>
              <dd>Monday to Friday, 9:00&ndash;17:00 (Sri Lanka Time)</dd>
              <dt>Website</dt>
              <dd>www.cgp.lk</dd>
            </dl>
          </div>

          <div class="col-right reveal">
            <h2 class="title" style="margin-bottom: var(--space-2);">Request information</h2>
            <p class="small" style="margin-bottom: var(--space-4); max-width: 34em;">Not ready to apply? Tell us what you would like to know and we will send you the details. Fields marked <span class="req">*</span> are required.</p>

            <form class="form" data-enquiry-form novalidate>
              <div class="field">
                <label for="name">Full name <span class="req">*</span></label>
                <input type="text" id="name" name="name" autocomplete="name" required>
              </div>
              <div class="field">
                <label for="email">Email address <span class="req">*</span></label>
                <input type="email" id="email" name="email" autocomplete="email" required>
              </div>
              <div class="field">
                <label for="phone">Phone or WhatsApp</label>
                <input type="tel" id="phone" name="phone" autocomplete="tel">
              </div>
              <div class="field">
                <label for="interest">I am asking about <span class="req">*</span></label>
                <select id="interest" name="interest" required>
                  <option value="Nursing Ausbildung pathway">Nursing Ausbildung pathway</option>
                  <option value="German language training">German language training</option>
                  <option value="Other Ausbildung guidance">Other Ausbildung guidance</option>
                  <option value="Fees and payment policy">Fees and payment policy</option>
                  <option value="Partnership (German institution)">Partnership (German institution)</option>
                  <option value="Something else">Something else</option>
                </select>
              </div>
              <div class="field field--full">
                <label for="message">Your question <span class="req">*</span></label>
                <textarea id="message" name="message" required placeholder="Tell us where you are up to and what you would like to know."></textarea>
                <p class="field__hint">Please do not send copies of personal documents by email at this stage.</p>
              </div>
              <div class="form__actions">
                <button type="submit" class="btn btn--solid">Send enquiry <span class="btn__glyph" aria-hidden="true">&rarr;</span></button>
                <p class="form__status" data-form-status>This opens your email app with the details filled in.</p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--dark" style="padding-block: var(--space-6);" aria-labelledby="visit-title">
      <div class="container">
{section_head("02", "Visiting us", "Gampaha District")}
        <div class="grid">
          <div class="col-left reveal">
            <p class="title" id="visit-title" style="margin-bottom: var(--space-3);">No. 143/10, Wilimbula, Henegama 11715</p>
            <p class="small" style="color: var(--color-grey-400); max-width: 34em;">Gampaha District, Sri Lanka. We serve students and families nationwide, so if you cannot travel to us, everything can be handled by WhatsApp, email and phone.</p>
            <p style="margin-top: var(--space-4);">
              <a class="btn btn--inverse" href="{WHATSAPP}" target="_blank" rel="noopener">Arrange a visit on WhatsApp</a>
            </p>
          </div>
          <figure class="col-right reveal">
            <img class="img-bw" src="assets/images/hero-nurse.jpg" alt="A healthcare professional in a white coat standing outdoors" width="1600" height="1067" loading="lazy">
          </figure>
        </div>
      </div>
    </section>
"""


# ==========================================================================
# WRITE
# ==========================================================================

DESCRIPTIONS = {
    "about.html": "About Ceylon German Pathway (CGP) - a Sri Lankan organisation preparing students for Nursing Ausbildung in Germany through ethical guidance, transparency and continuous support.",
    "students.html": "Students & Parents - the CGP Nursing Ausbildung pathway for Sri Lankan families: who can apply, the complete fifteen-stage pathway, twelve student services and programme information and transparency.",
    "who-can-apply.html": "Who can apply for the CGP nursing Ausbildung pathway - the eligibility and personal commitment CGP looks for, including German-language commitment, and what meeting those criteria does not guarantee.",
    "complete-pathway.html": "The complete CGP pathway in fifteen stages, from initial enquiry through German language A1 to B2, preparation, applications, the German institution's assessment and selection, visa and arrival.",
    "faq.html": "Frequently asked questions about nursing Ausbildung in Germany with CGP - sixteen straight answers for students and parents on language levels, timelines, decisions, visas, salary and documents.",
    "partners.html": "CGP partners with German hospitals, clinics and care institutions - candidate selection and preparation, employer interview coordination and long-term partnership development.",
    "current-students.html": "Progress of current CGP students across language training, interviews, visa stage and arrival in Germany, plus the support available at every stage.",
    "resources.html": "Free guides, checklists, frequently asked questions and a plain-English German glossary for students considering Nursing Ausbildung in Germany with CGP.",
    "contact.html": "Contact Ceylon German Pathway - WhatsApp, email and enquiry form. Based in Wilimbula, Henegama, Gampaha District, Sri Lanka. Monday to Friday, 9:00 to 17:00.",
}

TITLES = {
    "about.html": "About CGP - Ceylon German Pathway",
    "students.html": "Students &amp; Parents - Nursing Ausbildung Pathway | Ceylon German Pathway",
    "who-can-apply.html": "Who Can Apply - Students &amp; Parents | Ceylon German Pathway",
    "complete-pathway.html": "Complete Pathway - Students &amp; Parents | Ceylon German Pathway",
    "faq.html": "Frequently Asked Questions - Students &amp; Parents | Ceylon German Pathway",
    "partners.html": "German Partners - Ceylon German Pathway",
    "current-students.html": "Current Students - Ceylon German Pathway",
    "resources.html": "Resources &amp; Downloads - Ceylon German Pathway",
    "contact.html": "Contact - Ceylon German Pathway",
}

CONTENT = {
    "about.html": ABOUT,
    "students.html": STUDENTS,
    "who-can-apply.html": WHO_CAN_APPLY,
    "complete-pathway.html": COMPLETE_PATHWAY,
    "faq.html": FAQ_PAGE,
    "partners.html": PARTNERS,
    "current-students.html": CURRENT,
    "resources.html": RESOURCES,
    "contact.html": CONTACT,
}

if __name__ == "__main__":
    for filename, content in CONTENT.items():
        html = SHELL.format(
            title=TITLES[filename],
            description=DESCRIPTIONS[filename],
            nav=nav(filename),
            footer_nav=footer_nav(),
            content=content,
            whatsapp=WHATSAPP,
            email=EMAIL,
            facebook=FACEBOOK,
            instagram=INSTAGRAM,
            logo=LOGO,
            version=ASSET_VERSION,
        )
        (ROOT / filename).write_text(html)
        print(f"wrote {filename:24} {len(html):>7,} bytes")
    print("\nNote: index.html is hand-maintained and was not touched.")
