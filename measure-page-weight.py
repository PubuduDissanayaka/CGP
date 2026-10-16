#!/usr/bin/env python3
"""Measure the real transferred weight of every page on the CGP site.

Counts what a browser actually downloads: the compressed HTML, the CSS and JS
referenced from it (including url() references inside CSS), and every image.
Text assets are measured by downloading them with `--compressed`; binaries by
Content-Length. Writes a JSON report so before/after runs can be diffed.

Usage:
    python3 measure-page-weight.py                                   # live site
    python3 measure-page-weight.py --base http://127.0.0.1:4173/     # local build
    python3 measure-page-weight.py --json before.json
"""
import argparse
import json
import re
import subprocess
import sys
from urllib.parse import urljoin

PAGES = [
    "index.html", "about.html", "students.html", "who-can-apply.html",
    "complete-pathway.html", "faq.html", "partners.html", "current-students.html",
    "resources.html", "contact.html",
    "downloads/nursing-ausbildung-pathway-guide.html",
    "downloads/document-checklist.html",
    "downloads/frequently-asked-questions.html",
    "downloads/german-language-getting-started.html",
    "downloads/pre-departure-checklist.html",
    "downloads/fees-and-payment-policy.html",
]

# css/js/img references in markup, both plain and inside srcset
ASSET_RE = re.compile(
    r'(?:href|src|srcset)="([^"]+?\.(?:css|js|png|jpe?g|webp|svg|gif|ico|avif))'
    r'(?:\?[^"\s,]*)?(?:\s+[^",]+)?(?:,|")')
CSSURL_RE = re.compile(r'url\((["\']?)([^)"\']+\.(?:png|jpe?g|webp|svg|gif|avif))\1\)')
TEXT_EXT = (".css", ".js", ".html", ".svg")

_cache = {}


def _curl(args, binary=False):
    r = subprocess.run(["curl", "-sS", "--compressed", *args], capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def fetch(url):
    """Return (body_text, transfer_bytes) for a URL, honouring compression."""
    out = subprocess.run(
        ["curl", "-sS", "--compressed", "-w", "\n__SIZE__%{size_download}", url],
        capture_output=True, text=True).stdout
    body, _, size = out.rpartition("\n__SIZE__")
    try:
        n = int(size.strip())
    except ValueError:
        n = len(body.encode())
    return body, n


def size_of(url):
    if url in _cache:
        return _cache[url]
    if url.endswith(TEXT_EXT):
        n = fetch(url)[1]
    else:
        head = subprocess.run(["curl", "-sSI", url], capture_output=True, text=True).stdout
        m = re.search(r"content-length:\s*(\d+)", head, re.I)
        n = int(m.group(1)) if m else len(_curl([url], binary=True))
    _cache[url] = n
    return n


def measure(base):
    base = base.rstrip("/") + "/"
    report = {"base": base, "pages": {}}
    for page in PAGES:
        url = urljoin(base, page)
        html, hsize = fetch(url)
        refs = set()
        for a in ASSET_RE.findall(html):
            if a.startswith(("http://", "https://", "//", "data:", "#")):
                continue
            refs.add(urljoin(url, a.split("?")[0]))
        css = js = img = 0
        css_urls = []
        for a in sorted(refs):
            n = size_of(a)
            if a.endswith(".css"):
                css += n
                css_urls.append(a)
            elif a.endswith(".js"):
                js += n
            else:
                img += n
        for c in css_urls:
            for _, ref in CSSURL_RE.findall(fetch(c)[0]):
                if not ref.startswith(("data:", "http")):
                    img += size_of(urljoin(c, ref))
        report["pages"][page] = {
            "html": hsize, "css": css, "js": js, "images": img,
            "total": hsize + css + js + img,
        }
    report["site_total"] = sum(p["total"] for p in report["pages"].values())
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://cgp.lk/")
    ap.add_argument("--json", help="write the full report to this path")
    args = ap.parse_args()

    r = measure(args.base)
    print(f"{'page':52} {'html':>8} {'css':>8} {'js':>7} {'images':>10} {'total':>10}")
    for page, v in r["pages"].items():
        print(f"{page:52} {v['html']/1024:7.1f}K {v['css']/1024:7.1f}K "
              f"{v['js']/1024:6.1f}K {v['images']/1024:9.1f}K {v['total']/1024:9.1f}K")
    print(f"\nsite total (16 URLs): {r['site_total']/1024/1024:.2f} MB")
    print(f"home page:            {r['pages']['index.html']['total']/1024:.0f} KB "
          f"(images {r['pages']['index.html']['images']/1024:.0f} KB)")
    if args.json:
        with open(args.json, "w") as fh:
            json.dump(r, fh, indent=2)
        print(f"report written to {args.json}")


if __name__ == "__main__":
    sys.exit(main())
