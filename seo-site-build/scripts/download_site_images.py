#!/usr/bin/env python
"""download_site_images.py - save a live page's content images for redesign prototypes (stdlib only).

Finds candidate images in the page (<img> src / data-src / data-lazy-src / data-original /
srcset, <picture><source srcset>, inline background-image), skips decoration and tracking
pixels, downloads up to --max, and writes a manifest the prototype subagents read.

Files are named from the alt text (image SEO: descriptive names), e.g. `blue-front-door-01.jpg`,
falling back to `image-01.jpg`. Output goes to <project>/public/images/redesign/ (Astro and
Next.js both serve public/).

Usage:
  python download_site_images.py https://example.com --project-dir . \
      --manifest .site-concepts/site-images.json --max 15
Exit code: 0 when at least one image was saved, 1 when none could be saved.
Only for the client's own site; third-party or stock images need a license check before launch.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 (compatible; seo-site-build-image-fetch/1.0; +site owner redesign)"
MIN_BYTES = 2000  # smaller responses are pixels, spacers or icons
# Path fragments that almost always mean decoration. Matched on path segments/filename words,
# not raw substrings, so "background-hero.jpg" or "texture-of-linen.jpg" photos are not dropped
# by accident; --keep-all disables the filter.
SKIP_WORDS = {"logo", "icon", "icons", "favicon", "sprite", "sprites", "pixel", "1x1", "spacer",
              "blank", "placeholder", "avatar", "gravatar", "separator", "divider", "arrow",
              "checkmark", "star-rating", "stars", "badge", "seal", "ribbon", "loader", "spinner"}
SKIP_EXT = {".svg", ".gif", ".ico"}
EXT_BY_TYPE = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/avif": ".avif"}


class ImgParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found = []  # (url, alt)
        self._picture_srcs = []
        self._in_picture = False

    @staticmethod
    def _first_srcset(v):
        best, best_w = None, -1
        for part in (v or "").split(","):
            bits = part.strip().split()
            if not bits:
                continue
            w = 0
            if len(bits) > 1 and bits[1].endswith("w"):
                try:
                    w = int(bits[1][:-1])
                except ValueError:
                    w = 0
            if w > best_w:
                best, best_w = bits[0], w
        return best

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if a.get("style"):
            for u in re.findall(r"background(?:-image)?\s*:[^;]*url\(\s*['\"]?([^'\")]+)", a["style"]):
                self.found.append((u, a.get("aria-label", "")))
        if tag == "picture":
            self._in_picture, self._picture_srcs = True, []
        elif tag == "source" and self._in_picture:
            s = self._first_srcset(a.get("srcset") or a.get("data-srcset"))
            if s:
                self._picture_srcs.append(s)
        elif tag == "img":
            alt = a.get("alt", "")
            # Lazy loaders put a data: placeholder in src and the real URL in a data-* attribute,
            # so prefer the data-* attributes and srcset over src.
            cands = [a.get("data-src"), a.get("data-lazy-src"), a.get("data-original"),
                     self._first_srcset(a.get("srcset") or a.get("data-srcset")), a.get("src")]
            if self._in_picture and self._picture_srcs:
                cands.insert(0, self._picture_srcs[0])
            url = next((c for c in cands if c and not c.startswith("data:")), None)
            if url:
                self.found.append((url, alt))

    def handle_endtag(self, tag):
        if tag == "picture":
            self._in_picture = False


def slugify(s, limit=50):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:limit].rstrip("-")


def decorative(url):
    path = urlparse(url).path.lower()
    if Path(path).suffix in SKIP_EXT:
        return True
    words = set(re.split(r"[/_.\-]+", path)) | set(path.split("/"))
    return bool(words & SKIP_WORDS) or "1x1" in path


def main():
    ap = argparse.ArgumentParser(description="Download a page's content images for redesign prototypes.")
    ap.add_argument("url")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--manifest", default=".site-concepts/site-images.json")
    ap.add_argument("--max", type=int, default=15)
    ap.add_argument("--keep-all", action="store_true", help="do not skip decorative-looking paths")
    args = ap.parse_args()

    try:
        req = urllib.request.Request(args.url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            html = r.read().decode("utf-8", errors="replace")
            final = r.geturl()
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
        print(f"Could not fetch {args.url}: {e}")
        sys.exit(1)

    p = ImgParser()
    p.feed(html)
    seen, cands = set(), []
    for u, alt in p.found:
        full = urljoin(final, u.strip())
        if len(full) < 10 or full in seen or not full.startswith(("http://", "https://")):
            continue
        seen.add(full)
        if not args.keep_all and decorative(full):
            continue
        cands.append((full, alt.strip()))

    project = Path(args.project_dir).resolve()
    dest = project / "public" / "images" / "redesign"
    dest.mkdir(parents=True, exist_ok=True)
    saved, used_names = [], set()
    for url, alt in cands:
        if len(saved) >= args.max:
            break
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": final})
            with urllib.request.urlopen(req, timeout=15) as r:
                ctype = r.headers.get("Content-Type", "").split(";")[0].strip().lower()
                data = r.read()
        except (urllib.error.URLError, TimeoutError, ValueError, OSError):
            continue
        if len(data) < MIN_BYTES or (ctype and not ctype.startswith("image/")):
            continue
        ext = Path(urlparse(url).path).suffix.lower()
        ext = {".jpeg": ".jpg"}.get(ext, ext)
        if ext not in (".jpg", ".png", ".webp", ".avif"):
            ext = EXT_BY_TYPE.get(ctype, ".jpg")
        n = len(saved) + 1
        base = slugify(alt) or "image"
        name = f"{base}-{n:02d}{ext}"
        while name in used_names:
            n += 1
            name = f"{base}-{n:02d}{ext}"
        used_names.add(name)
        tmp = dest / (name + ".part")
        tmp.write_bytes(data)
        tmp.replace(dest / name)
        saved.append({"filename": name, "public_path": f"/images/redesign/{name}", "alt": alt,
                      "original_url": url, "bytes": len(data)})

    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = project / manifest
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({"source_url": args.url, "total": len(saved), "images": saved},
                                   indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(cands)} candidate image(s), saved {len(saved)} to {dest}")
    missing_alt = sum(1 for s in saved if not s["alt"])
    if missing_alt:
        print(f"{missing_alt} saved image(s) had no alt text; write real alt text before launch.")
    print(f"Manifest: {manifest}")
    sys.exit(0 if saved else 1)


if __name__ == "__main__":
    main()
