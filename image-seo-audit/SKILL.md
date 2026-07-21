---
name: image-seo-audit
description: "Audit the images on a page or article for SEO and Core Web Vitals — alt text, file size, format, responsive markup, lazy loading, layout-stability dimensions, descriptive filenames, and ImageObject schema. Use when checking an article's images or before publishing image-heavy content. Triggers on: image SEO, alt text check, image optimization, are my images optimized, image file size, webp, image audit. Outputs a per-image findings table + prioritized fixes."
---

# Image SEO Audit

Images are the most common silent SEO leak on a content site: missing alt text loses accessibility and
image-search traffic, oversized heroes wreck LCP, and dimensionless `<img>` tags cause layout shift
(CLS). We source images from a CDN with alt text already — this skill verifies that discipline held and
catches the misses, on a per-image basis.

Companion to `skills/seo-onpage-audit/SKILL.md` (which flags only image basics; this is the deep pass).

---

## What it checks (thresholds)

| Aspect | Rule | Severity if violated |
|---|---|---|
| **Alt text** | Present, descriptive, **10–125 chars**, keyword-integrated where natural (not stuffed) | Missing = High; weak = Medium |
| **File size** | Thumbnails **< 50 KB**, in-content images **< 100 KB**, hero **< 200 KB** | > 500 KB = Critical (LCP); over-tier = Medium |
| **Format** | WebP/AVIF preferred (JPEG/PNG fallback acceptable) | Unoptimized large PNG/JPEG = Medium |
| **Responsive** | `srcset`/`sizes` present for content images | Missing = Low–Medium |
| **Lazy loading** | `loading="lazy"` on below-fold images (native or JS) | Missing below-fold = Medium |
| **CLS dimensions** | `width`/`height` (or aspect-ratio box) on every `<img>` | Missing = High (CLS risk) |
| **Filename** | Descriptive, hyphenated; not `IMG_0042.jpg`/`image001` | Generic = Low |
| **Schema** | ImageObject (or image in BlogPosting/Product) where relevant | Missing = Low |

> Most of our images sit on Shopify/CDN with `?width=` params and theme-applied `loading`/dimensions,
> so size/format/responsive are often handled by the theme's image pipeline — verify, don't assume.

---

## Workflow
1. **Get the images:** WebFetch the live page and extract every `<img>` (src, alt, width, height,
   loading, srcset). For one of our articles, also scan the `.md`/`.html` for the image markdown/URLs.
2. **Per image, evaluate** each aspect above. File size: infer from the CDN URL's width param where a
   real byte size isn't available, and flag obvious oversize (full-res hero with no width transform).
3. **Score & prioritize:** roll up to a short summary (total images, # missing alt, # oversized, #
   missing dimensions) then a Critical→Low fix list.

## Output format

```
IMAGE AUDIT — [url]   12 images
Missing alt: 1 · Missing dimensions: 3 · Over size-tier: 2 · Non-descriptive filename: 4

CRITICAL
- hero.jpg ~610 KB, no width transform → LCP risk. Serve via CDN ?width=1200 + WebP.
HIGH
- img #7 ([spec]-chart) missing alt text → add "[key spec] requirements by [product] chart".
- imgs #3,#5,#9 missing width/height → CLS risk; add dimensions.
MEDIUM
- img #4 1.2 MB PNG → convert to WebP.
LOW
- 4 images use generic CDN filenames — rename to descriptive-hyphenated where re-uploading.
```

## Alt-text guidance (quick)
- Describe the image's content and its role in the section; 10–125 chars.
- Work in the relevant keyword **only when it genuinely describes the image** — a [key spec] chart's alt is
  "[key spec] requirements by [product] chart," not the article's primary keyword jammed in.
- Decorative-only images: empty alt (`alt=""`) is correct — don't narrate spacers.

## Optional — image SERP gap (DataForSEO)
If DataForSEO is available, cross-reference the page's images against Google Images results for the
target keyword to find queries where the page ranks but has no image presence. Optional; not required.

## How this connects
- **`skills/seo-onpage-audit/SKILL.md`** — basics overlap; this is the detailed image pass.
- **`skills/seo-content/SKILL.md`** — Phase 1.5 image research (alt text written at draft time) and the
  GEO multi-modal pairing rule (image next to a citable block).
- **`skills/seo-schema/SKILL.md`** — ImageObject / image fields in BlogPosting/Product.
- **`skills/seo-image-gen/SKILL.md`** — when an audit gap is "no suitable image," generate one.
