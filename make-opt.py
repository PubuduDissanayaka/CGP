#!/usr/bin/env python3
"""make-opt.py — build the responsive image derivatives under assets/images/opt/.

This is the tool that was missing: the 2026-10-16 performance pass published 109
derivatives under `assets/images/opt/` but left no script behind, so the pipeline
was not reproducible. Run it after adding or replacing any source image.

    python3 make-opt.py --manifest images-gen.json          # build
    python3 make-opt.py --manifest images-gen.json --check  # verify only

Manifest entry:

    {
      "key":    "hero-nurse",                 # base filename
      "src":    "/path/to/source.png",        # full-size master (any raster format)
      "base":   "gen/hero-nurse",             # path under assets/images, no extension
      "widths": [640, 1024, 1600]             # real served widths, ascending
    }

For each entry it produces:

    assets/images/<base>.jpg                     master JPEG   (-q:v 3)
    assets/images/<base>.webp                    master WebP   (quality 88)
    assets/images/opt/<base>-<W>w.jpg            derivative    (-q:v 4)
    assets/images/opt/<base>-<W>w.webp           derivative    (quality 78)

Encoder settings were calibrated against the existing derivative set rather than
invented: re-encoding `students-group.jpg` at `-q:v 4` yields 47,402 B against the
shipped 45,472 B (4% heavier) and WebP `-quality 78` lands between the shipped
level and `-quality 80`. No derivative is ever upscaled — a requested width above
the master width is refused rather than silently interpolated.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "assets", "images")
OPT = os.path.join(IMAGES, "opt")

JPEG_MASTER_Q = "3"
JPEG_DERIV_Q = "4"
WEBP_MASTER_Q = "88"
WEBP_DERIV_Q = "78"


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:4])}... failed: {p.stderr.strip()[:400]}")


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
        capture_output=True, text=True,
    ).stdout.strip()
    if not out or "," not in out:
        raise RuntimeError(f"cannot probe {path}")
    w, h = out.split(",")[:2]
    return int(w), int(h)


def build(entry, check=False):
    key, src, base = entry["key"], entry["src"], entry["base"]
    widths = sorted(entry["widths"])
    if not os.path.exists(src):
        raise RuntimeError(f"{key}: master not found at {src}")

    sw, sh = probe(src)
    problems = []
    for w in widths:
        if w > sw:
            problems.append(f"{key}: requested {w}w derivative exceeds master width {sw}px (would upscale)")
    if problems:
        raise RuntimeError("; ".join(problems))

    made = []
    master_jpg = os.path.join(IMAGES, base + ".jpg")
    master_webp = os.path.join(IMAGES, base + ".webp")
    os.makedirs(os.path.dirname(master_jpg), exist_ok=True)
    os.makedirs(os.path.join(OPT, os.path.dirname(base)), exist_ok=True)

    if not check:
        run(["ffmpeg", "-v", "error", "-y", "-i", src, "-map_metadata", "-1",
             "-q:v", JPEG_MASTER_Q, master_jpg])
        run(["ffmpeg", "-v", "error", "-y", "-i", src, "-map_metadata", "-1",
             "-c:v", "libwebp", "-quality", WEBP_MASTER_Q, "-compression_level", "6",
             master_webp])
    made += [(master_jpg, sw), (master_webp, sw)]

    for w in widths:
        for fmt, args in (
            ("jpg", ["-q:v", JPEG_DERIV_Q]),
            ("webp", ["-c:v", "libwebp", "-quality", WEBP_DERIV_Q, "-compression_level", "6"]),
        ):
            dest = os.path.join(OPT, f"{base}-{w}w.{fmt}")
            if not check:
                run(["ffmpeg", "-v", "error", "-y", "-i", src, "-map_metadata", "-1",
                     "-vf", f"scale={w}:-2", *args, dest])
            made.append((dest, w))

    for path, expect_w in made:
        if not os.path.exists(path):
            raise RuntimeError(f"{key}: missing output {path}")
        size = os.path.getsize(path)
        if size < 500:
            raise RuntimeError(f"{key}: suspiciously small output {path} ({size} B)")
        aw, ah = probe(path)
        if abs(aw - expect_w) > 2:
            raise RuntimeError(f"{key}: {path} is {aw}px wide, expected ~{expect_w}px")
        print(f"   {'ok  ' if check else 'made'} {os.path.relpath(path, HERE):52} {aw}x{ah}  {size:>8} B")
    return len(made)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--check", action="store_true", help="verify existing outputs only")
    a = ap.parse_args()
    entries = json.load(open(os.path.join(HERE, a.manifest)))
    total = 0
    for e in entries:
        print(f"-- {e['key']}")
        total += build(e, check=a.check)
    print(f"\n{'verified' if a.check else 'built'}: {total} files across {len(entries)} images")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
