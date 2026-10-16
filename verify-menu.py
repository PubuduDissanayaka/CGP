#!/usr/bin/env python3
"""Verify the CGP menu structure change: build idempotency, page integrity,
nav consistency, and that every menu link resolves to a real target."""
import hashlib
import html.parser
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent

PAGES = ["index.html", "about.html", "students.html", "who-can-apply.html",
         "complete-pathway.html", "faq.html", "partners.html",
         "current-students.html", "resources.html", "contact.html"]

failures = []
notes = []


def check(cond, msg):
    (notes if cond else failures).append(("PASS " if cond else "FAIL ") + msg)


def hashes():
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in PAGES}


# --- 1. build idempotency -------------------------------------------------
before = hashes()
r = subprocess.run([sys.executable, "build-pages.py"], cwd=ROOT,
                   capture_output=True, text=True)
check(r.returncode == 0, f"build-pages.py exits 0 ({r.stderr.strip()[:200]})")
after = hashes()
for p in PAGES:
    check(before[p] == after[p], f"re-running the generator leaves {p} byte-identical")

# --- 2. version stamps ----------------------------------------------------
for p in PAGES:
    txt = (ROOT / p).read_text()
    vs = set(re.findall(r"\?v=(\d+)", txt))
    check(vs == {"14"}, f"{p} asset stamp is ?v=14 only (found {sorted(vs)})")

# --- 3. page integrity ----------------------------------------------------
for p in PAGES:
    txt = (ROOT / p).read_text()
    check(txt.count("<h1") == 1, f"{p} has exactly one <h1>")
    ids = re.findall(r'\sid="([^"]+)"', txt)
    dupes = {i for i in ids if ids.count(i) > 1}
    check(not dupes, f"{p} has no duplicate ids ({sorted(dupes)})")
    imgs = re.findall(r"<img\b[^>]*>", txt)
    noalt = [i for i in imgs if " alt=" not in i]
    check(not noalt, f"{p}: every <img> has alt ({len(noalt)} missing)")

# --- 4. nav consistency across pages -------------------------------------
def nav_of(txt):
    m = re.search(r'<nav class="nav" id="site-nav"[^>]*>(.*?)\n      </nav>', txt, re.S)
    return m.group(1) if m else None

def shape(nav):
    """Nav with the per-page aria-current values removed, so the *structure*
    can be compared across pages."""
    return re.sub(r' aria-current="[a-z]+"', "", nav)

shapes = {}
for p in PAGES:
    n = nav_of((ROOT / p).read_text())
    check(n is not None, f"{p} has the main nav")
    if n:
        shapes[p] = shape(n)
uniq = set(shapes.values())
check(len(uniq) == 1, f"all {len(PAGES)} pages render an identical nav structure "
                      f"({len(uniq)} distinct)")

nav = shapes.get("index.html", "")
order = re.findall(r'class="nav__link"[^>]*>([^<]+)<', nav)
expected_order = ["Home", "About CGP", "Students &amp; Parents", "German Partners",
                  "Current Students", "Resources", "Contact"]
check(order == expected_order, f"top-level menu order is the client's ({order})")

for want in ['aria-controls="submenu-about"', 'aria-controls="submenu-students"',
             'aria-controls="submenu-partners"', 'aria-label="About CGP menu"',
             'aria-label="Students &amp; Parents menu"',
             'aria-label="German Partners menu"']:
    check(want in nav, f"nav carries {want}")

# --- 5. every menu target exists and is labelled ---------------------------
about_ids = set(re.findall(r'\sid="([^"]+)"', (ROOT / "about.html").read_text()))
partners_ids = set(re.findall(r'\sid="([^"]+)"', (ROOT / "partners.html").read_text()))

sublinks = re.findall(r'<a class="nav__sublink" href="([^"]+)"[^>]*>([^<]+)</a>', nav)
check(len(sublinks) == 12, f"three section menus carry 4 + 4 + 4 = 12 links (got {len(sublinks)})")
check("students.html" in [h for h, _ in sublinks],
      "the Students & Parents menu links the section's own page")
for href, text in sublinks:
    page, _, frag = href.partition("#")
    check((ROOT / page).exists(), f"menu item '{text}' -> {page} exists")
    if frag:
        target_ids = about_ids if page == "about.html" else partners_ids
        check(frag in target_ids, f"menu item '{text}' anchor #{frag} exists on {page}")

# --- 6. aria-current correctness ------------------------------------------
def nav_cur(p):
    return re.findall(r'<a class="nav__link"[^>]*href="([^"]+)"([^>]*)>([^<]+)</a>',
                      nav_of((ROOT / p).read_text()))

for p, expect in [("index.html", [("index.html", "page")]),
                  ("about.html", [("about.html", "page")]),
                  ("students.html", [("students.html", "page")]),
                  ("partners.html", [("partners.html", "page")]),
                  ("who-can-apply.html", [("students.html", "true")]),
                  ("faq.html", [("students.html", "true")]),
                  ("complete-pathway.html", [("students.html", "true")]),
                  ("current-students.html", [("current-students.html", "page")]),
                  ("resources.html", [("resources.html", "page")]),
                  ("contact.html", [("contact.html", "page")])]:
    got = [(h, re.search(r'aria-current="([a-z]+)"', a).group(1))
           for h, a, _ in nav_cur(p) if 'aria-current' in a]
    check(got == expect, f"{p}: aria-current is {got} (expected {expect})")

# --- 7. the sub-page marks its own menu item ------------------------------
sub_cur = re.findall(r'<a class="nav__sublink" href="([^"]+)" aria-current="page">',
                     nav_of((ROOT / "who-can-apply.html").read_text()))
check(sub_cur == ["who-can-apply.html"], f"who-can-apply.html marks itself ({sub_cur})")

print("\n".join(notes))
print()
if failures:
    print("\n".join(failures))
    print(f"\n{len(failures)} FAILED of {len(failures) + len(notes)}")
    sys.exit(1)
print(f"ALL {len(notes)} CHECKS PASSED")
