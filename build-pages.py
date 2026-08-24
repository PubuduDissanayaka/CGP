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

import pathlib

ROOT = pathlib.Path(__file__).parent

WHATSAPP = "https://wa.me/94704008952"
PHONE = "+94 70 400 8952"
EMAIL = "hello@cgp.lk"
FACEBOOK = "https://www.facebook.com/CeylonGermanPathway"
INSTAGRAM = "https://www.instagram.com/ceylongermanpathway"
LOGO = "assets/images/CGPLogo.png"

# Bump this whenever css/ or js/ changes, then re-run, and mirror it in
# index.html. Forces browsers to fetch the new file instead of a cached one.
ASSET_VERSION = "9"

PAGES = [
    ("index.html", "Home"),
    ("about.html", "About CGP"),
    ("students.html", "Students"),
    ("partners.html", "German Partners"),
    ("current-students.html", "Current Students"),
    ("resources.html", "Resources &amp; Downloads"),
    ("contact.html", "Contact"),
]


def nav(current):
    out = []
    for href, label in PAGES:
        cur = ' aria-current="page"' if href == current else ""
        out.append(f'        <a class="nav__link" href="{href}"{cur}>{label}</a>')
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


def section_head(index, label, meta):
    return f"""        <header class="section-head">
          <span class="section-head__index">{index}</span>
          <h2 class="section-head__label">{label}</h2>
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
    "02", "Page 02 / 07", "About CGP",
    "Guidance you can hold us to.",
    "Ceylon German Pathway is a Sri Lankan organisation preparing motivated young people for Nursing Ausbildung and professional healthcare careers in Germany - through ethical guidance, structured German language training and support that continues after arrival.",
    [("Based in", "Wilimbula, Henegama, Gampaha District, Sri Lanka"),
     ("Serving", "Sri Lankan students and families nationwide"),
     ("Focus", "Nursing Ausbildung and healthcare careers in Germany")],
) + band("students-group.jpg", "Students studying together in a library", "CGP students in preparation") + f"""
    <section class="section" aria-labelledby="who-title">
      <div class="container">
{section_head("01", "Who we are", "Wilimbula &middot; Gampaha District")}
        <div class="grid">
          <div class="col-wide prose reveal">
            <p class="display" id="who-title" style="margin-bottom: var(--space-4);">We don't just recruit students. We prepare them - and stay with them.</p>
            <p>Ceylon German Pathway (CGP) is based in Wilimbula, Henegama, in the Gampaha District, and serves Sri Lankan students and families nationwide. We help motivated young people pursue vocational education and healthcare career opportunities in Germany.</p>
            <p>Most people who come to us are asking the same question: <em>&ldquo;I want to build a healthcare career in Germany, but I don't know how to start, what documents I need, how to learn German, or how to handle the Ausbildung and visa process.&rdquo;</em> Our entire service is built to answer that question properly, in order, with someone accountable at each step.</p>
            <p>That means candidate selection, German language training, application and document preparation, employer interview coordination, visa guidance, pre-departure orientation, and support once you have arrived in Germany.</p>
          </div>
          <figure class="col-narrow reveal">
            <img class="img-bw" src="assets/images/nurse-care.jpg" alt="One person's hands holding another's in a gesture of care and reassurance" width="1600" height="1067" loading="lazy">
            <figcaption class="small" style="padding-top: var(--space-1); border-bottom: 1px solid var(--color-rule);">Student welfare first</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section section--dark" aria-labelledby="believe-title">
      <div class="container">
{section_head("02", "What we believe", "Five working principles")}
        <div class="grid row-gap">
          <div class="col-wide reveal" style="margin-bottom: var(--space-4);">
            <p class="display" id="believe-title">Principles, not slogans.</p>
          </div>
          <div class="col-full grid row-gap" style="grid-column: 1 / 13;">
{about_principles}
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="diff-title">
      <div class="container">
{section_head("03", "What makes us different", "The long view")}
        <div class="grid">
          <div class="why__breakout reveal" style="grid-column: 1 / 13;">
            <blockquote id="diff-title">&ldquo;We don't just recruit students. We prepare and support them through the entire pathway - from candidate selection and German language training to employer interviews, visa preparation, pre-departure orientation, arrival in Germany and integration support - while building long-term relationships with German healthcare institutions.&rdquo;</blockquote>
            <p class="micro-label">- The CGP model</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top: 0;" aria-labelledby="how-title">
      <div class="container">
{section_head("04", "How we work", "Illustrative examples")}
        <div class="grid row-gap-lg">
          <div class="col-wide reveal">
            <p class="display" id="how-title">Two examples of the model in practice.</p>
          </div>
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

FAQS = [
    ("What is Nursing Ausbildung in Germany?",
     "Ausbildung is Germany's dual vocational training system. For nursing, it combines classroom study with paid, hands-on training inside a real healthcare institution, and leads to a state-recognised German nursing qualification."),
    ("Do I need to know German before applying?",
     "You do not need German to make your first enquiry - but you do need it to succeed. German language training is a core part of the CGP pathway, and reaching the level required by employers and authorities is a genuine requirement of the process, not an optional extra."),
    ("What are the eligibility requirements?",
     "The pathway suits motivated students, typically around 18 to 25, who want to build a professional healthcare career in Germany and are prepared to commit to language training. Exact requirements depend on the German institution and the current rules that apply to your application, so we confirm them with you during assessment and counselling rather than publishing a generic list."),
    ("How much does the CGP programme cost?",
     "There are three fee components: registration, the German language course, and the CGP service fee. The structure is set out on this page, and the exact amounts and payment schedule are confirmed in writing before you commit. There are no hidden charges."),
    ("What does CGP support me with during the application and visa process?",
     "Application preparation, document preparation and checking, employer interview coordination and preparation, and step-by-step visa guidance. If something goes wrong or a document is queried, you have a named point of contact rather than being left to work it out alone."),
    ("How long does the process take?",
     "It depends mainly on two things: how quickly you progress through German language training, and the timelines of the German institution you are matched with. We give you a realistic timeline during counselling and update it honestly as you progress - we would rather tell you it will take longer than promise a date we cannot control."),
    ("Will CGP support me after I arrive in Germany?",
     "Yes. Arrival support and integration support are part of the pathway, and ongoing student support continues while you are settling into your training."),
    ("Is accommodation available in Germany?",
     "Accommodation arrangements vary between German healthcare institutions. It is one of the specifics we confirm with the institution for your particular placement, and we cover it fully in pre-departure orientation so you know exactly what applies before you travel."),
    ("Can I work after completing Nursing Ausbildung?",
     "A completed Nursing Ausbildung is a state-recognised German qualification, and it opens routes to continued employment, specialisation and further study within German healthcare. We will not promise you a specific job or salary - what we can do is prepare you properly for the qualification."),
    ("How do I apply to become a CGP student?",
     "Message us on WhatsApp or send an enquiry through the contact page. We will talk you through the pathway, the requirements and the fees, and assess whether Nursing Ausbildung is the right route for you before anyone commits to anything."),
]

faq_items = "\n".join(
    f"""            <div class="accordion__item{' is-open' if i == 1 else ''}">
              <h3>
                <button class="accordion__trigger" aria-expanded="{'true' if i == 1 else 'false'}">
                  <span class="accordion__index">4.{i:02d}</span>
                  <span class="accordion__title">{q}</span>
                  <span class="accordion__glyph" aria-hidden="true">+</span>
                </button>
              </h3>
              <div class="accordion__panel">
                <div class="accordion__panel-inner">
                  <p>{a}</p>
                </div>
              </div>
            </div>""" for i, (q, a) in enumerate(FAQS, 1)
)

STUDENTS = page_hero(
    "03", "Page 03 / 07", "Students",
    "The complete Nursing Ausbildung pathway.",
    "One route, from your first question to your first day of training in Germany - language, applications, documents, interviews, visa, departure and arrival. Everything below is part of the same programme.",
    [("Best suited to", "Motivated students, around 18&ndash;25, aiming at healthcare in Germany"),
     ("Core requirement", "Commitment to German language training"),
     ("Main offering", "Nursing Ausbildung Programme")],
) + band("nurse-tablet.jpg", "Close view of a healthcare professional in a white coat holding a phone", "A profession, not just a placement") + f"""
    <section class="section" aria-labelledby="forwhom-title">
      <div class="container">
{section_head("01", "Who this is for", "Be honest with yourself here")}
        <div class="grid">
          <div class="col-left prose reveal">
            <p class="display" id="forwhom-title" style="margin-bottom: var(--space-4);">This pathway asks something of you.</p>
            <p>Our best students are motivated young people - usually around 18 to 25 - who genuinely want to build a professional healthcare career in Germany, and who need reliable guidance with German language training, applications, documentation, visa preparation and ongoing support.</p>
            <p>What it is not: a shortcut. Nursing Ausbildung is real vocational training in a second language, inside a demanding profession. The students who do well are the ones who treat the language course as the foundation of everything else.</p>
            <p>If that sounds like the wrong fit, tell us early and we will say so honestly. That is a better outcome for everyone than a student who commits to a pathway they did not want.</p>
          </div>
          <figure class="col-right reveal">
            <img class="img-bw" src="assets/images/student-writing.jpg" alt="A student writing notes by hand in a notebook" width="1600" height="1067" loading="lazy">
            <figcaption class="small" style="padding-top: var(--space-1); border-bottom: 1px solid var(--color-rule);">Preparation, not shortcuts</figcaption>
          </figure>
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

    <section class="section" aria-labelledby="fees-title">
      <div class="container">
{section_head("03", "Fees &amp; payment policy", "Transparent by design")}
        <div class="grid">
          <div class="col-left reveal">
            <p class="display" id="fees-title" style="margin-bottom: var(--space-4);">Three fees. Written down. No surprises.</p>
            <div class="prose">
              <p>&ldquo;How much will this cost me, and are there any hidden charges?&rdquo; is the first question almost every family asks us. So here is the structure in full.</p>
              <p>You receive the exact amounts and the payment schedule in writing before you commit to anything. Nothing is added later.</p>
            </div>
          </div>
          <div class="col-right reveal">
            <table class="fee-table">
              <caption>CGP fee structure</caption>
              <thead>
                <tr>
                  <th scope="col">Fee</th>
                  <th scope="col">What it covers</th>
                  <th scope="col">Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">Registration</th>
                  <td>Enrolment as a CGP student, assessment and counselling.</td>
                  <td class="tbd">On enquiry</td>
                </tr>
                <tr>
                  <th scope="row">German language course</th>
                  <td>Structured German training towards the required level.</td>
                  <td class="tbd">On enquiry</td>
                </tr>
                <tr>
                  <th scope="row">CGP service fee</th>
                  <td>Applications, documents, interview coordination, visa guidance, pre-departure and arrival support.</td>
                  <td class="tbd">On enquiry</td>
                </tr>
              </tbody>
            </table>
            <div class="notice" style="margin-top: var(--space-4);">
              <p><strong>Amounts pending.</strong> Exact fee amounts are being finalised and will be published here. Until then we confirm them directly on enquiry, in writing, before any commitment is made.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top: 0;" aria-labelledby="faq-title">
      <div class="container">
{section_head("04", "Frequently asked questions", "Ten questions we get most")}
        <div class="grid">
          <div class="col-wide reveal" style="margin-bottom: var(--space-4);">
            <p class="display" id="faq-title">Straight answers.</p>
          </div>
          <div class="col-full" style="grid-column: 1 / 13;">
            <div class="accordion--light" data-accordion>
{faq_items}
            </div>
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
    "04", "Page 04 / 07", "German Partners",
    "A partner, not a placement agency.",
    "CGP works with German hospitals, clinics and care institutions as a long-term partner. We select motivated Sri Lankan candidates and prepare them properly - language, professional readiness and documentation - before they ever sit in front of your interview panel.",
    [("For", "German hospitals, clinics and care institutions"),
     ("Model", "Long-term partnership, not one-off recruitment"),
     ("Contact", f'<a href="mailto:{EMAIL}">{EMAIL}</a>')],
    meta="F&uuml;r Partnereinrichtungen",
) + band("medical-team.jpg", "A team of healthcare professionals in surgical dress viewed from below", "Partnering with German healthcare institutions") + f"""
    <section class="section section--dark" aria-labelledby="pservices-title">
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

    <section class="section" aria-labelledby="pwork-title">
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

    <section class="section" style="padding-top: 0;" aria-labelledby="pmodel-title">
      <div class="container">
{section_head("03", "The partnership model", "Illustrative example")}
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

    <section class="section section--dark" aria-labelledby="pwhy-title">
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
    "05", "Page 05 / 07", "Current Students",
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

resource_faqs = "\n".join(
    f"""            <div class="accordion__item{' is-open' if i == 1 else ''}">
              <h3>
                <button class="accordion__trigger" aria-expanded="{'true' if i == 1 else 'false'}">
                  <span class="accordion__index">2.{i:02d}</span>
                  <span class="accordion__title">{q}</span>
                  <span class="accordion__glyph" aria-hidden="true">+</span>
                </button>
              </h3>
              <div class="accordion__panel">
                <div class="accordion__panel-inner">
                  <p>{a}</p>
                </div>
              </div>
            </div>""" for i, (q, a) in enumerate(FAQS, 1)
)

RESOURCES = page_hero(
    "06", "Page 06 / 07", "Resources &amp; Downloads",
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
              <p><strong>Free to download, no enquiry required.</strong> These documents are written from the same information this website is built on. Each opens in your browser and can be saved or printed as a PDF. A note on fees: exact amounts are being finalised and will be published here; until then they are confirmed directly, in writing, before any commitment is made.</p>
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
{section_head("02", "Frequently asked questions", "Ten questions we get most")}
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
    "07", "Page 07 / 07", "Contact",
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
    "students.html": "The complete CGP Nursing Ausbildung pathway for Sri Lankan students: German language training, applications, documents, interviews, visa guidance, pre-departure and arrival support, plus transparent fees and FAQs.",
    "partners.html": "CGP partners with German hospitals, clinics and care institutions - candidate selection and preparation, employer interview coordination and long-term partnership development.",
    "current-students.html": "Progress of current CGP students across language training, interviews, visa stage and arrival in Germany, plus the support available at every stage.",
    "resources.html": "Free guides, checklists, frequently asked questions and a plain-English German glossary for students considering Nursing Ausbildung in Germany with CGP.",
    "contact.html": "Contact Ceylon German Pathway - WhatsApp, email and enquiry form. Based in Wilimbula, Henegama, Gampaha District, Sri Lanka. Monday to Friday, 9:00 to 17:00.",
}

TITLES = {
    "about.html": "About CGP - Ceylon German Pathway",
    "students.html": "Students - Nursing Ausbildung Pathway | Ceylon German Pathway",
    "partners.html": "German Partners - Ceylon German Pathway",
    "current-students.html": "Current Students - Ceylon German Pathway",
    "resources.html": "Resources &amp; Downloads - Ceylon German Pathway",
    "contact.html": "Contact - Ceylon German Pathway",
}

CONTENT = {
    "about.html": ABOUT,
    "students.html": STUDENTS,
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
