#!/usr/bin/env python
"""extract_brand.py - pull a live site's visual identity for a redesign brief (stdlib only).

Collects CSS from <style> blocks, linked stylesheets (and one level of @import), and inline
style attributes, then reports:
  - brand-looking CSS custom properties (framework/CMS preset variables filtered out)
  - colors ranked by how often they occur (hex 3/4/6/8 digits and rgb()/rgba(), alpha kept),
    with near-neutral grays reported separately instead of dropped
  - font families in use (generic/system names removed), plus every family requested from
    Google Fonts (all `family=` params of css2 URLs and the `|`-separated css v1 form)
  - logo candidates (inline <svg> in a logo-ish container, <img> with logo/brand in
    src/alt/class/id or a parent's class/id, apple-touch-icon / icon links, og:image), and
    downloads the best one

Writes <out>/brand-identity.json and <out>/logo.<ext> (or logo.svg for inline SVG).

Usage:
  python extract_brand.py https://example.com -o .site-concepts/brand-extraction [--max-css 12]
Exit code: 0 on success, 1 if the page could not be fetched.
Only use this on the client's own site. Shopify stores: prefer the theme's settings_data.json.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 (compatible; seo-site-build-brand-extract/1.0; +site owner redesign)"
PAGE_TIMEOUT, CSS_TIMEOUT, ASSET_TIMEOUT = 30, 10, 15

# Variables that come from frameworks, page builders or CMS presets, not from the brand.
PRESET_PREFIXES = ("--wp--preset--", "--wp--custom--", "--wp--style--", "--wp-admin-", "--global--",
                   "--swiper-", "--bs-", "--chakra-", "--mantine-", "--tw-", "--fa-", "--toastify-",
                   "--plyr-", "--glide-", "--splide-", "--e-global-", "--e-a-", "--ast-", "--kadence-")
BRAND_WORDS = ("color", "colour", "brand", "primary", "secondary", "accent", "surface", "bg",
               "background", "text", "heading", "link", "button", "btn", "cta", "highlight",
               "border", "gradient", "theme", "font", "ink", "canvas")
GENERIC_FONTS = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-sans-serif",
                 "ui-serif", "ui-monospace", "ui-rounded", "-apple-system", "blinkmacsystemfont",
                 "segoe ui", "roboto", "helvetica", "helvetica neue", "arial", "noto sans",
                 "liberation sans", "apple color emoji", "segoe ui emoji", "segoe ui symbol",
                 "noto color emoji", "inherit", "initial", "unset", "var", "emoji", "math",
                 "sfmono-regular", "liberation mono", "dejavu sans mono", "menlo", "monaco", "consolas", "courier new", "courier",
                 "times new roman", "times", "georgia", "verdana", "tahoma"}
# Icon fonts are not brand typography.
ICON_FONTS = ("awesome", "icon", "glyph", "material symbols", "material icons", "dashicons", "eicons")


def fetch(url: str, timeout: int, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
        final = r.geturl()
    if binary:
        return data, ctype, final
    charset = re.search(r"charset=([\w-]+)", ctype)
    return data.decode(charset.group(1) if charset else "utf-8", errors="replace"), ctype, final


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.styles, self.inline, self.css_links = [], [], []
        self.logo_imgs, self.icon_links, self.og_image = [], [], None
        self.svgs = []  # inline svg markup found inside logo-ish containers
        self._in_style = False
        self._buf = []
        self._stack = []  # (tag, logoish)
        self._svg_depth = 0
        self._svg_buf = []

    @staticmethod
    def _logoish(a):
        blob = " ".join(str(a.get(k, "")) for k in ("class", "id", "alt", "src", "aria-label", "title")).lower()
        return any(w in blob for w in ("logo", "brand", "site-icon", "wordmark"))

    @staticmethod
    def _icon_svg(a):
        """UI glyphs (chevrons, carets, cart icons) sit inside logo containers too; skip them."""
        cls = (a.get("class", "") + " " + a.get("id", "")).lower()
        if "icon" in cls and "logo" not in cls:
            return True
        digits = re.sub(r"[^\d.]", "", a.get("width", ""))
        try:
            return bool(digits) and float(digits) < 24
        except ValueError:
            return False

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        parent_logo = any(l for _, l in self._stack)
        me_logo = self._logoish(a)
        if tag not in ("img", "link", "meta", "br", "hr", "input", "source", "path", "circle", "rect",
                       "polygon", "line", "ellipse", "use", "stop"):
            self._stack.append((tag, me_logo))
        if self._svg_depth:
            attr_txt = "".join(f' {k}="{v}"' for k, v in attrs if v is not None)
            self._svg_buf.append(f"<{tag}{attr_txt}>")
            if tag == "svg":
                self._svg_depth += 1
            return
        if tag == "style":
            self._in_style = True
            self._buf = []
        if a.get("style"):
            self.inline.append(a["style"])
        if tag == "link":
            rel = a.get("rel", "").lower()
            if "stylesheet" in rel and a.get("href"):
                self.css_links.append(a["href"])
            if "icon" in rel and a.get("href"):
                size = a.get("sizes", "")
                self.icon_links.append((rel, size, a["href"]))
        elif tag == "meta" and a.get("property", "").lower() == "og:image":
            self.og_image = a.get("content")
        elif tag == "img":
            src = a.get("src", "")
            if src.startswith("data:"):
                src = a.get("data-src") or a.get("data-lazy-src") or src
            if (me_logo or parent_logo) and src and not src.startswith("data:"):
                # Own logo-ish attributes rank above "inside a logo-ish container".
                self.logo_imgs.append((0 if me_logo else 1, src))
        elif tag == "svg" and (me_logo or parent_logo) and not self._icon_svg(a):
            self._svg_depth = 1
            attr_txt = "".join(f' {k}="{v}"' for k, v in attrs if v is not None)
            self._svg_buf = [f"<svg{attr_txt}>"]

    def handle_startendtag(self, tag, attrs):
        if self._svg_depth:
            attr_txt = "".join(f' {k}="{v}"' for k, v in attrs if v is not None)
            self._svg_buf.append(f"<{tag}{attr_txt}/>")
            return
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if self._svg_depth:
            self._svg_buf.append(f"</{tag}>")
            if tag == "svg":
                self._svg_depth -= 1
                if not self._svg_depth:
                    self.svgs.append("".join(self._svg_buf))
        if tag == "style" and self._in_style:
            self._in_style = False
            self.styles.append("".join(self._buf))
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                break

    def handle_data(self, data):
        if self._svg_depth:
            self._svg_buf.append(data)
        elif self._in_style:
            self._buf.append(data)


def gather_css(page_url, col, max_css):
    chunks = list(col.styles) + [f"x{{{s}}}" for s in col.inline]
    seen, queue, fetched = set(), [urljoin(page_url, h) for h in col.css_links], 0
    # @import inside inline <style> blocks.
    for s in col.styles:
        queue += [urljoin(page_url, u) for u in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", s)]
    google = []
    while queue and fetched < max_css:
        u = queue.pop(0)
        if u in seen:
            continue
        seen.add(u)
        if "fonts.googleapis.com" in u:
            google.append(u)
            continue
        try:
            css, _, final = fetch(u, CSS_TIMEOUT)
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
            print(f"  skip stylesheet {u}: {e}")
            continue
        fetched += 1
        chunks.append(css)
        for imp in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", css):
            queue.append(urljoin(final, imp))
    google += [urljoin(page_url, h) for h in col.css_links if "fonts.googleapis.com" in h]
    return "\n".join(chunks), sorted(set(google)), fetched


def to_hex(tok: str):
    tok = tok.strip().lower()
    if tok.startswith("#"):
        h = tok[1:]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return None
        if len(h) == 8 and h[6:] == "ff":
            h = h[:6]
        return "#" + h
    m = re.match(r"rgba?\(\s*([\d.]+%?)[\s,]+([\d.]+%?)[\s,]+([\d.]+%?)(?:\s*[,/]\s*([\d.]+%?))?\s*\)", tok)
    if not m:
        return None

    def ch(v):
        return round(float(v[:-1]) * 2.55) if v.endswith("%") else round(float(v))
    r, g, b = (max(0, min(255, ch(v))) for v in m.groups()[:3])
    out = f"#{r:02x}{g:02x}{b:02x}"
    if m.group(4) is not None:
        a = m.group(4)
        alpha = float(a[:-1]) / 100 if a.endswith("%") else float(a)
        if alpha < 1:
            out += f"{round(alpha * 255):02x}"
    return out


def is_neutral(h: str) -> bool:
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return max(r, g, b) - min(r, g, b) < 12


def main():
    ap = argparse.ArgumentParser(description="Extract colors, fonts, variables and logo from a site.")
    ap.add_argument("url")
    ap.add_argument("-o", "--out", default=".site-concepts/brand-extraction")
    ap.add_argument("--max-css", type=int, default=12, help="max stylesheets to fetch (default 12)")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    try:
        html, _, final = fetch(args.url, PAGE_TIMEOUT)
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
        print(f"Could not fetch {args.url}: {e}")
        print("The site may block scripts. Ask the user for brand colors, fonts and a logo file instead.")
        sys.exit(1)
    col = Collector()
    col.feed(html)
    css, google_urls, n_css = gather_css(final, col, args.max_css)

    # CSS variables.
    variables = {}
    for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;}{]+)", css):
        low = name.lower()
        if low.startswith(PRESET_PREFIXES):
            continue
        if any(w in low for w in BRAND_WORDS):
            variables.setdefault(name, value.strip())

    # Colors by frequency.
    counts = Counter()
    for tok in re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)", css):
        h = to_hex(tok)
        if h:
            counts[h] += 1
    ranked = [{"hex": h, "count": n} for h, n in counts.most_common()]
    brand_colors = [c for c in ranked if not is_neutral(c["hex"][:7]) and len(c["hex"]) == 7][:20]
    neutrals = [c for c in ranked if len(c["hex"]) == 7 and is_neutral(c["hex"])][:10]
    translucent = [c for c in ranked if len(c["hex"]) == 9][:10]

    # Fonts.
    fam_counts = Counter()
    for decl in re.findall(r"font-family\s*:\s*([^;}{]+)", css):
        for f in decl.split(","):
            name = f.strip().strip("'\"\\) ").strip()
            low = name.lower()
            if not name or low.startswith("var(") or low in GENERIC_FONTS or any(w in low for w in ICON_FONTS):
                continue
            fam_counts[name] += 1
    google_fonts = []
    for u in google_urls:
        q = parse_qs(urlparse(u).query)
        for fam in q.get("family", []):
            for part in fam.split("|"):
                name = part.split(":")[0].replace("+", " ").strip()
                if name and name not in google_fonts:
                    google_fonts.append(name)

    # Logo.
    candidates = []
    for _, src in sorted(col.logo_imgs, key=lambda t: t[0]):
        candidates.append(("img", urljoin(final, src)))
    icons = sorted(col.icon_links, key=lambda t: ("apple-touch" not in t[0], t[1] == ""))
    if col.og_image:
        candidates.append(("og_image", urljoin(final, col.og_image)))
    for _, _, href in icons:
        candidates.append(("icon", urljoin(final, href)))
    logo_file, logo_source = None, None
    own_img_logo = any(rank == 0 for rank, _ in col.logo_imgs)
    if col.svgs and not own_img_logo:
        svg = max(col.svgs, key=len)
        if 'xmlns="' not in svg[:200]:
            svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        (out / "logo.svg").write_text(svg, encoding="utf-8")
        logo_file, logo_source = "logo.svg", "inline_svg"
    else:
        for kind, url in candidates:
            try:
                data, ctype, _ = fetch(url, ASSET_TIMEOUT, binary=True)
            except (urllib.error.URLError, TimeoutError, ValueError, OSError):
                continue
            if len(data) < 200:
                continue
            ext = {"image/svg+xml": "svg", "image/png": "png", "image/jpeg": "jpg", "image/webp": "webp",
                   "image/x-icon": "ico", "image/vnd.microsoft.icon": "ico", "image/avif": "avif"}.get(
                ctype.split(";")[0].strip().lower())
            if not ext:
                ext = Path(urlparse(url).path).suffix.lstrip(".").lower() or "png"
            (out / f"logo.{ext}").write_bytes(data)
            logo_file, logo_source = f"logo.{ext}", f"{kind}: {url}"
            break

    result = {
        "url": args.url,
        "final_url": final,
        "stylesheets_fetched": n_css,
        "css_variables": variables,
        "colors_ranked": brand_colors,
        "neutrals_ranked": neutrals,
        "translucent_colors": translucent,
        "fonts_ranked": [{"family": f, "count": n} for f, n in fam_counts.most_common(12)],
        "google_fonts_requested": google_fonts,
        "logo_candidates": [{"source": k, "url": u} for k, u in candidates[:10]],
        "logo_file": logo_file,
        "logo_source": logo_source,
        "note": "Counts are occurrences in CSS, a proxy for prominence, not rendered area.",
    }
    (out / "brand-identity.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Fetched {final} + {n_css} stylesheet(s)")
    print("Top colors: " + ", ".join(f"{c['hex']} (x{c['count']})" for c in brand_colors[:8]) or "none")
    print("Neutrals:   " + ", ".join(f"{c['hex']} (x{c['count']})" for c in neutrals[:5]))
    print("Fonts:      " + ", ".join(f"{f} (x{n})" for f, n in fam_counts.most_common(5)))
    if google_fonts:
        print("Google Fonts requested: " + ", ".join(google_fonts))
    print(f"Brand variables: {len(variables)}")
    print(f"Logo: {logo_file or 'not found'}" + (f" ({logo_source})" if logo_source else ""))
    print(f"Wrote {out / 'brand-identity.json'}")


if __name__ == "__main__":
    main()
