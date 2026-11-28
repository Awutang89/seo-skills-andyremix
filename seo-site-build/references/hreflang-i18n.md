# hreflang and multilingual builds (en + de-DE on Astro, with Next.js / Shopify notes)

Example setup with placeholder locales: English (`en`) at `/`, German (`de-DE`)
at `/de/`, Astro built-in i18n with `prefixDefaultLocale: false`. Google rules below were
checked against Google's "Localized versions" doc (page dated 2026-09-21, read 2026-09-27).

---

## Google's rules (non-negotiable)

1. **Reciprocal.** If page A lists B as an alternate, B must list A. One-way annotations are
   ignored.
2. **Self-reference.** Each page lists itself as well as every other language version.
3. **Absolute URLs** including `https://`, on the canonical host, in the site's trailing-slash
   form (the same string as that page's canonical).
4. **Codes:** ISO 639-1 language, optionally + ISO 3166-1 region (`en`, `en-GB`, `de-DE`) or a
   script subtag (`<language>-<Script>`). A region alone (`DE`) is invalid.
5. **`x-default`** names the page for users no listed language matches, usually the default
   language or a language picker.
6. One method per site: `<link rel="alternate" hreflang>` in `<head>`, HTTP `Link` headers, or
   `<xhtml:link>` in the sitemap. Using two is allowed but they must agree exactly; mixing is
   where drift starts.
7. hreflang does not replace canonical. **Each locale's page is self-canonical.** Never
   canonicalize `/de/x` to `/x`: that tells Google the German page is a duplicate and drops it.

## The Astro pattern

- `astro.config.mjs`:
  `i18n: { defaultLocale: 'en', locales: ['en', 'de'], routing: { prefixDefaultLocale: false } }`.
  The route folder is `de`; the emitted **hreflang value** is `de-DE` (the audience: the
  `de-DE` market). Keep the map in one place (for example `hreflang` in `src/i18n/ui.ts`:
  `{ en: 'en', de: 'de-DE' }`) and reuse it for `<html lang>`, hreflang, JSON-LD `inLanguage`,
  and the sitemap. `og:locale` uses the underscore form (`en_US`, `de_DE`) plus
  `og:locale:alternate` for the other language.
- **Base layout** emits, on every indexable page: one `<link rel="alternate">` per locale
  (`en`, `de-DE`) + `x-default` pointing at the English URL. The alternate is built from the
  locale-neutral path (`stripLocale`) and re-prefixed per locale (`localizePath`), so the pair is
  reciprocal by construction.
- **Pages with no translation must not advertise one.** A page without a mirror emits only its
  own self-referencing alternate (or none) instead of pointing at a 404. A site can require a mirror
  for every page and article; for sites that do not, pass the alternate only when the mirror
  exists (`altPath` or `translationOf` in frontmatter).
- **Articles:** one content collection with a `lang` field and folders `en/` and `de/`; the
  bare slug is shared across locales (`/blog/x` ↔ `/de/blog/x`), and `translationOf` links
  pairs whose slugs differ. Drafts are filtered out of both locales' `getStaticPaths`, and the
  alternate must not point at a draft mirror.
- **Noindex pages** (`/thanks`, `/de/thanks`) should not emit hreflang alternates (an alternate
  pointing at a noindexed page is a mixed signal), and are excluded from the sitemap in both
  locales.
- **Sitemap:** `@astrojs/sitemap` with `i18n: { defaultLocale: 'en', locales: { en: 'en', de: 'de-DE' } }`
  adds `<xhtml:link>` alternates that must match the `<head>` tags exactly. The filter removes
  noindex and 404 pages for every locale.
- **404 per locale:** Cloudflare Pages serves the nearest `404.html` walking up the path. Astro
  emits `/de/404` as `de/404.html` with `build.format: 'file'`, or `de/404/index.html` with the
  directory format; a build hook moves the latter so German misses get the German 404.
- **Titles:** CJK characters render about twice as wide, so count them as 2 against the 60
  display-unit budget (roughly 30 CJK characters). Snippets are cut by pixel width, not
  character count, so measure CJK meta descriptions the same way (CJK = 2 units, ~160 units,
  roughly 80 characters). This is a working heuristic, not a Google-published number.
- **Fonts:** a CJK face is large. Self-host it with unicode-range subsets (fontsource splits
  them), load its stylesheet async only on CJK pages (`media="print" onload="this.media='all'"` +
  `<noscript>` fallback), do not preload it, and switch the font tokens under `html.lang-<locale>`
  with zero letter-spacing and looser leading.
- **JSON-LD:** one entity keeps one `@id` across languages (the Organization, the author Person,
  the Service). Only page-level nodes (WebPage, BlogPosting, BreadcrumbList, FAQPage) get
  per-locale `@id`s and `inLanguage`. Breadcrumb labels are localized.
- **Copy:** `de` is written natively for the `de` reader, not machine-translated word for word;
  prices can stay in the site's currency with a localized label.
- **Language switcher:** a plain link to the mirror URL. Never auto-redirect by
  `Accept-Language` or IP: Googlebot crawls mostly from the US without that header and would
  never see the `de` pages.

## Checks (run after every build; `verify_build.py` does 1-4)

This script is not included in this repository.

1. Every indexable page has a self alternate, the other-locale alternate (when a mirror
   exists) and `x-default`.
2. Every alternate target exists in the build and lists the source page back (reciprocal).
3. Alternate URLs are absolute, on the canonical host, and equal the target's canonical.
4. `<html lang>` equals the page's own hreflang value.
5. Sitemap alternates match the `<head>` tags. No noindex page in the sitemap.
6. `de` titles within the width budget; no English leftovers in `de` UI strings.

## Next.js and Shopify

- **Next.js App Router:** `app/[lang]/…` segments or middleware-free locale folders;
  `generateMetadata` returns `alternates: { canonical, languages: { en: …, 'de-DE': …, 'x-default': … } }`.
  Build the map from one locale config, and emit sitemap alternates from `app/sitemap.ts`.
- **Shopify:** Shopify Markets + Translate & Adapt (or a translation app) creates locale
  subfolders (`/de-de/…`) and emits hreflang automatically for published languages. Check the
  live `<head>`: themes sometimes add a second, hard-coded set. Unpublished languages must not
  appear. Translated handles are optional; an untranslated handle is fine.

File: seo-site-build/references/hreflang-i18n.md · Version 1.0 · November 2026
