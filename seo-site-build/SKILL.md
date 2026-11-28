---
name: seo-site-build
description: "Technical SEO guidelines for BUILDING or REDESIGNING a website — page architecture, one-H1 rule, title/meta budgets, JSON-LD per page type, canonical host, clean URLs, sitemap, crawl-size budget, Core Web Vitals and accessibility hardening, migration redirects, hreflang for multilingual sites. Also runs the site kickoff (brand interview, design directions, scaffold, parallel homepage prototypes, locked design system), Astro build conventions, safe editing of an existing Astro site (content config, Zod, H1 source, MDX, schema injection), and post-build rendered verification plus changed-file hygiene. Platform-agnostic rules with Astro, Webflow, Next.js and Shopify implementation notes. Use BEFORE and DURING any site build, redesign, or platform migration so the agent knows the rules to follow. Triggers on: build a website, new site, start my website, vibe code my site, redesign, homepage concepts, design directions, scaffold Astro, edit Astro content, frontmatter, content collection, verify the build, hreflang, migrate to Webflow, site structure, technical SEO guidelines, page templates, schema plan, URL structure, launch checklist. For auditing an EXISTING page use seo-onpage-audit instead."
---

# SEO Site Build — technical guidelines for a new or redesigned site

This skill applies when building or redesigning a website. Every rule below came from a real audit failure.
Follow these rules from the first page, not at the end.

Companion skills: `seo-onpage-audit` (verify a built page), `seo-schema` (schema detail),
`internal-linking` (link pass after content exists), `keyword-research` (what pages to build),
`image-seo-audit` (images).

Read ./brand/ per _system/brand-memory.md if present (`./brand/site-brief.md` is written by the
kickoff interview).

---

## How to use this skill

0. **New site or redesign with no agreed design yet:** run the kickoff in
   `references/site-concepts.md` (interview → directions → scaffold → prototypes → lock). Its
   site blueprint feeds §1. Skip it when the design already exists (e.g. a `DESIGN.md`).
1. **Before designing:** run through §1 (page architecture) and §5 (URLs) with the user and
   write the page-type table and URL map into the project's notes. These are the decisions
   that are expensive to change later.
2. **While building each template:** apply §2 (headings), §3 (titles/meta), §4 (schema),
   §6 (canonical/sitemap), §8 (performance/accessibility) to the template, then verify one
   instance of it with `seo-onpage-audit`.
3. **Before launch:** run the §10 checklist top to bottom.
4. **If migrating an existing site:** §9 is mandatory. Build the redirect map before the
   new site goes live.
5. **Editing a site that already builds** (content, frontmatter, headings, links, schema): read
   `references/astro-edit-safety.md` first (Next.js and Shopify analogues inside), and finish
   with `references/build-verify.md`.
6. **Every build or edit ends with** §11: build, rendered checks, changed-file hygiene.

Platform notes are marked **Astro**, **Webflow**, **Next.js**, **Shopify**. Apply the one that
matches.

### References and scripts (load when the step needs them)

| File | When |
|---|---|
| `references/site-concepts.md` | kickoff workflow, state/resume, approval gate, lock |
| `references/interview.md` | brand/site interview and brief template |
| `references/directions.md` | design directions, palette/font rules, `directions.json` |
| `references/prototype-brief.md` | prototype subagent template and done checklist |
| `references/astro.md` | Astro stack, scaffold, config, tokens/fonts, base layout, Pages vs Workers |
| `references/astro-edit-safety.md` | Stage 0 detection, edit preflight, Zod, H1 source, MDX, links, schema injection, edge cases |
| `references/hreflang-i18n.md` | multilingual rules and checks |
| `references/build-verify.md` | build, rendered checks, changed-file hygiene |
| `scripts/detect_stack.py` | framework, package manager, config facts, content schema mode, CMS, drafts |
| `scripts/verify_build.py` | H1/H2, titles, canonicals, JSON-LD types, hreflang reciprocity, links, size over built HTML. This script is not included in this repository. |
| `scripts/git_hygiene.py` | classifies `git status` incl. ignored output against allowed paths |
| `scripts/scaffold_guard.py` | empty-folder guard + temp scaffold move-up |
| `scripts/extract_brand.py` | colors (by frequency), fonts, brand CSS variables, logo from a live site |
| `scripts/download_site_images.py` | a live page's content images → `public/images/redesign/` + manifest |

All scripts are Python 3 stdlib, run with `python`. Paths: see `site-concepts.md` "Script paths".

---

## 1. Page architecture

Every page type must earn its own query class. Write the table before building anything:

| Page type | Target query pattern | Example |
|---|---|---|
| Home | `{niche} directory`, `{niche} near me` | one page, carries the brand |
| Category / hub | `{niche} in {state}` | bounded lists |
| Local / city | `{niche} in {city}` — usually the money query | one per city with 2+ items |
| Detail / listing / product | brand searches + long-tail | one per entity |
| Facet pages with editorial | `{service} cost`, `what is {service}` | needs real content, not just a list |
| Resource articles | informational long-tail | from the keyword plan |

Rules:
- **Decide upfront which queries belong to money pages vs. articles** so articles never
  cannibalize them. `best {niche} near me` is homepage territory, never an article.
- **"Near me" queries are geo-localized.** City pages and Google Business Profile win them.
  Put "near you" phrasing in the homepage title/H1/FAQ, but do not build pages for it.
- **Facet and hub pages need editorial content** (how it works, what to expect, typical
  cost, FAQs) plus a jump-nav for long lists. A bare list is thin content.
- **Duplicate-content control for multi-location entities:** same website + same street =
  one entity, merge. Same website + different addresses = real locations, keep both but make
  each page unique (location-specific sentence with street + zip, its own hours/rating/photos).
- Custom 404 page. Default OG image 1200×630. SVG favicon.
- **Blueprint columns.** Beyond query pattern, record per page: purpose (one sentence), sections
  in order, content status (ready / needs writing / placeholder agreed), launch or later.
- **Build around the content that exists.** Two real testimonials → a section for two. No proof
  → no proof section. Never fabricate testimonials, counts, logos or client names; illustrative
  content says so on its face.

**Webflow:** each page type is one CMS Collection + one Collection Page template. City and
state pages are separate Collections with a Reference field between them. Facet editorial
content lives in rich-text fields on the Collection item, not in static page copy.
**Next.js:** one dynamic route per page type (`[state]/[city]`), fully static SSG.
**Astro:** one content collection or data file per page type, one dynamic route per type
(`src/pages/blog/[slug].astro`), `output: 'static'` (see `references/astro.md`).
**Shopify:** collections = hubs, products = detail pages, blog = resources; facet pages need
a page template with metafield-driven content.

---

## 2. Headings

- **Exactly one H1 per page.** The H1 carries the primary keyword.
- Secondary keywords go in H2s.
- **Never put buttons, "read more", or nav text inside heading tags.** Designers do this for
  styling; use a class instead.
- Section titles that are purely decorative should be `<p>` or `<div>`, not H3.

**Webflow:** the Designer defaults to H1 for any "Heading" element dropped in. Set the tag
explicitly on every heading in the template; check the Navigator for stray H1s in nav,
footer and symbols. Symbols (components) reused across pages must not contain an H1.

---

## 3. Titles and meta descriptions

Each of these came from a real audit failure.

- **No global title-template suffix.** A `%s | Brand` template pushed nearly every page
  past 60 characters. Deep pages get self-contained keyword titles; **only the homepage
  carries the brand.**
- **Title patterns** (front-load the keyword):
  - Detail: `{Name} — {Niche} in {City}, {ST}`
  - City: `{Niche} in {City}, {ST} — {N} Locations`
  - State: same with the state name
  - Facet: `{Facet} — {N} Options`, with a **fallback that drops the count when a long facet
    name pushes past 60**.
- **Same-name entities in one city produce duplicate titles.** Disambiguate with the street
  (`… in Springfield, IL (101 Main St)`) only when a name+city collision exists.
- **Meta descriptions ≤160 characters.** Hand-written short templates for list pages; a
  shared helper that truncates at a word boundary (~158) for anything fed by scraped or
  user-supplied text.
- Long entity names will keep some titles over 60. Accept it: front-load the keywords and let
  Google truncate. **Never truncate the entity name.**
- Audit caveat: crawlers count HTML entities (`&#x27;` = 6 chars), so a "162-char" finding
  may be a false positive. Check raw text length before rewriting.

**Webflow:** Page Settings → SEO → use CMS field binding in the title and description
(`{Name} — {Niche} in {City}`). Do NOT append the site name in the template title. Webflow
has no truncation helper, so add a dedicated short `meta-description` CMS field (≤158 chars)
rather than binding a long summary field.
**Next.js:** `metadata.title.template: "%s"`, per-route `generateMetadata`.
**Astro:** the base layout strips a trailing `| Brand` off non-home pages and measures CJK
characters as width 2. If an inherited layout appends a suffix that cannot be
removed, budget the frontmatter title to 60 minus the suffix length.
**Shopify:** theme `title` liquid must not append `shop.name` on non-home templates.

---

## 4. Structured data (JSON-LD)

JSON-LD on every page type from day one. Verify each template in Google's Rich Results Test. (FAQPage and Article-author rows last verified 2026-09-26.)

| Page type | Schema |
|---|---|
| Sitewide (layout) | `Organization` + `WebSite` in one `@graph`, with `@id`s other pages reference |
| Detail / listing | `LocalBusiness` (or subtype: `Dentist`, `Plumber`, `Store`) |
| List pages (city/state/facet) | `ItemList` + `BreadcrumbList` |
| Any page with FAQs | `FAQPage` — **optional**. Google has shown no FAQ rich result for any site since 2026-05-07; the markup is harmless if it matches the visible Q&A text exactly (see `seo-schema`) |
| Articles | `Article` with `datePublished`, `dateModified`, `author` = a real `Person` with a bio/about page and `sameAs` links when one exists (Organization only when no real author exists; never invent bylines), `publisher` as `@id` ref to the layout Organization |
| Every non-home page | `BreadcrumbList` |

Rules:
- **Cap `ItemList` at ~50 `itemListElement`s** while keeping the true `numberOfItems`.
  Partial lists are valid schema.org and keep the HTML under the crawl budget (§7).
- Rich Results Test flags date-only values; use full ISO datetimes.
- Page constants (title, description) are the single source for schema fields, so schema
  never drifts from the visible page.
- **`JSON.stringify` does not escape the `<` character.** JSON-LD built from scraped or
  user-supplied text is an XSS sink until every `<` is emitted as the JSON escape `\u003c`.

**Webflow:** put a `<script type="application/ld+json">` in the Collection Page's custom
code (Page Settings → Before `</body>`) with CMS fields bound inside the JSON. Custom code
is a paid-site feature. Keep the sitewide `Organization`/`WebSite` block in Project Settings
→ Custom Code so it is on every page. Webflow escapes bound fields as HTML, so quotes inside
a field will break the JSON: bind only fields the site controls (names, addresses, numbers), never
free-text rich fields.
**Next.js:** one `JsonLd` component, rendered per route, data from the same object as the
page metadata.
**Astro:** the base layout emits one `@graph` (Organization + WebSite) and accepts page nodes
through a `jsonLd` prop; serialize with `set:html` and `<` → `\u003c`. Other injection options
and their order of preference: `references/astro-edit-safety.md` "Schema on Astro pages".
**Shopify:** most themes emit `Product`/`Organization` already; add `FAQPage` via a metafield
(see `faq-jsonld` skill) and check for duplicates.

---

## 5. Clean, de-duplicated URLs (day one)

A URL should read like a tidy keyword phrase: short, human, **no word repeated**.

- **Never build a slug as `slugify(name + " " + city)`.** Entity names already contain the
  keyword and often the city, so the result is `…-{niche}-{niche}-{city}-{city}`.
  Build it deterministically: slugify the name → drop repeated significant tokens keeping the
  first → append the city **once, and only if absent from the name**. Protect city tokens and
  stopwords so legitimate doubles survive (Walla Walla). Keep a collision suffix (`-2`).
- **Do not repeat the domain's head keyword in the path prefix.** `/{niche}/` under
  a `{niche}` domain adds nothing. Pick a prefix that adds a term (`/{service}/`, `/mobile/`).
- **Keep browse/category URLs on the money keyword** (`/{niche}/{state}/{city}`).
  There the repetition IS the target query.
- One shared slug function used by every generator, so slugs never churn between runs.
- The slug is the universal join key (data files, database foreign keys, redirect maps).
  Treat any change as a migration (§9).

**Webflow:** the Collection slug field auto-generates from Name. Override it with a computed
clean slug in the import CSV; do not let Webflow generate it. The Collection URL prefix is
set once in Collection Settings and cannot be nested (`/{niche}/{state}/{city}` is not
possible; Webflow gives `/cities/austin-tx`). Plan for flat prefixes and put the state in
the slug.

---

## 6. Canonical host, sitemap, robots.txt, indexing

- **Pick apex vs www on day one and enforce it.** The non-canonical host must permanently
  redirect (301/308) to the canonical. A stale site-URL env var silently forced wrong-host
  canonicals on every page; hard-code the canonical host and delete any env var that can
  contradict it.
- **Every page has exactly one canonical, self-referencing, on the canonical host.**
- Sitemap includes every indexable page type and nothing else. Linked set == sitemap set:
  zero pages in the sitemap that no page links to (orphans), zero linked pages missing from
  the sitemap.
- Google Search Console: DNS-verify the domain property, submit the sitemap, **resubmit
  after every large page addition**. Spend the ~10-12/day URL-inspection quota on the
  highest-keyword-value new URLs, not the newest.
- After GSC verification, open **Settings → Search generative AI** and confirm it is set to
  **Include**. The control rolled out to all sites on 2026-08-31; **Exclude** keeps the site
  out of Search generative AI features, so it means no traffic from them. Use the
  **Generative AI performance report** as the AI-visibility metric.
  (support.google.com/webmasters/answer/16908024, last verified 2026-09-26)
- **robots.txt** (write it on day one, verify it after every deploy):
  - Allow the AI search/citation crawlers: `OAI-SearchBot`, `ChatGPT-User`,
    `Claude-SearchBot`, `Claude-User`, `PerplexityBot`, `Perplexity-User`. Training crawlers
    (`GPTBot`, `ClaudeBot`, `Google-Extended`, `CCBot`) are a policy choice and are not needed
    for citations. `Google-Extended` covers Gemini training and Gemini Apps / Vertex AI
    grounding; it does not affect Google Search or AI Overviews.
  - **Do not `Disallow` a noindexed page.** Google must crawl the page to see its `noindex`;
    a disallowed page can stay indexed from links alone.
  - Include the sitemap line: `Sitemap: https://{canonical-host}/sitemap.xml`.
  - **Cloudflare:** in the dashboard, Security → Bots → "Block AI bots" / AI Crawl Control
    must be off or must allow the search crawlers above, and "Managed robots.txt" must not
    inject blocks. Cloudflare can prepend its own rules, so after every deploy verify the
    live file with `curl -s https://{canonical-host}/robots.txt`, not the source file.
    Recommended Cloudflare settings for a content or service site (Free plan, dashboard as of
    2026-09-26, Security → Settings → filter "Bot traffic", plus the zone Overview panel):
    - **Configure AI bot policies:** nothing set to Block. Allow the search/citation crawlers.
    - **Bot Preference Sync** (Overview → "Manage AI bot access"): turn it off, so robots.txt
      is exactly what the site's code serves. If it stays on, it prepends Cloudflare's bot rules.
    - **AI Labyrinth:** off. It serves decoy pages to bots, and the goal is AI search bots reading
      real content.
    - **Bot Fight Mode:** off. It can challenge legitimate crawlers and the site's own API
      calls (e.g. a form's fetch requests).
    - **Challenge passage:** leave the default. **Cloudflare managed ruleset:** leave on (free,
      always active).
    - **Precursor:** off (it adds behavioural challenges a small site does not need).
      **Markdown for Agents:** skip (Pro plan, no evidence it helps).
      **Under Attack Mode:** never on, except during a real attack, because it challenges every
      visitor, including Googlebot. **Development Mode:** off, except while debugging the cache.
    - The Free-plan defaults (CDN, DDoS protection, SSL/TLS, WAF) need no changes.
  - Do not set `nosnippet` / `max-snippet` (meta or `X-Robots-Tag` header) or
    `data-nosnippet` on pages that should feed AI Overviews / AI Mode; they remove or limit
    that input.
  - (Crawler groups last verified 2026-09-26 against the OpenAI, Anthropic, Perplexity and
    Google common-crawler pages.)
- Monitoring, all free: a scripted audit over the built HTML (title/desc lengths, duplicate
  titles, JSON-LD types per route), a Screaming Frog crawl of the live site after each
  deploy, Chrome DevTools performance traces for LCP/CLS. The keyless PageSpeed Insights
  API rate-limits; drive it in a browser, not a script.
- Know whether a finding refers to a build or to production before "fixing" something
  already fixed.
- **Multilingual sites:** every indexable page carries a reciprocal, self-including hreflang
  set with `x-default`, each locale self-canonical, sitemap alternates matching the head tags.
  Full rules and the Astro pattern: `references/hreflang-i18n.md`.

**Astro:** hard-code `site` in `astro.config.*`; pick `trailingSlash` and a matching
`build.format` (Cloudflare Pages: `'never'` + `'file'`); sitemap `filter` drops noindex and
404 pages in every locale; robots.txt as a route (`src/pages/robots.txt.ts`) with the sitemap
line. See `references/astro.md` §3.

**Webflow:** Project Settings → Publishing → set the default domain (apex or www) so the
other redirects. Auto-generate sitemap is ON in SEO settings; exclude utility pages (search,
password, 401) and any Collection that should not be indexed. Webflow sets self-canonicals by
default only if "Global canonical tag URL" in SEO settings matches the canonical host
exactly. Check it after every domain change.

---

## 7. Crawl-size budget (the 2 MB Googlebot cutoff)

**Googlebot stops indexing an HTML file at 2 MB uncompressed.** Big list pages cross it
silently. A facet page with hundreds of full cards went over 2 MB.

- Hub/facet pages render **compact link chips** (`{Name} ({City})`) grouped by region. Full
  cards live only on pages where counts are bounded (city, state).
- Cap `ItemList` JSON-LD at ~50 items (§4).
- After every build or content import, sweep for pages over ~800 KB. Anything approaching
  1 MB will cross 2 MB as the dataset grows.

**Next.js:** RSC hydration payload duplicates everything rendered (~60% of bytes on the
worst page), so the real budget is ~1 MB of visible HTML. Sweep with
`find .next/server/app -name "*.html" -size +800k`.
**Webflow:** Collection Lists cap at 100 items per list and paginate. Use the cap as a
feature: paginated hubs stay small. Do not stack many Collection Lists on one page to work
around the limit.

---

## 8. Core Web Vitals and accessibility hardening

Run PageSpeed Insights on **each page template**, not just the homepage. Fix for **mobile**;
desktop passes once mobile does. In priority order, each from a real failure:

1. **Gate third-party embeds behind IntersectionObserver.** `loading="lazy"` is not enough;
   a map iframe (~295 KB of foreign JS) still loaded upfront. Mount the embed only when its
   container scrolls within ~400 px of the viewport, with a same-height placeholder.
2. **Contrast: light gray text on white fails WCAG AA.** `slate-400`-style gray (~2.9:1) is
   the default "muted helper text" reflex and fails everywhere: field hints, captions,
   dates, bylines. `slate-500` (~4.8:1) is the floor for small gray text. Grep for it before
   launch.
3. **Inline text links need a non-color affordance.** Links inside prose that differ only by
   color fail. Add an underline. Bordered or background "button" links are exempt.
4. **Search inputs with `aria-expanded`/`aria-controls` need `role="combobox"`** and
   `aria-autocomplete="list"`, or they fail `aria-allowed-attr` and the newer
   agent-accessibility-tree audit.
5. **Conditional preconnect only.** A preconnect to an origin the page never requests is
   itself flagged. Emit the hint only when the page actually has an asset on that origin.
6. **Console errors from a cold backend dent Best Practices.** A paused free-tier database
   logging failed fetches is an audit failure even when the page renders. Keep it alive and
   confirm it is up before "fixing" code.
7. **Self-host fonts; no Google Fonts `<link>`.** The cross-origin stylesheet + font chain
   blocks first render. Use fontsource (or `next/font`), load only the weights in use, preload
   only the one or two above-the-fold files, never inline woff2 as base64 into CSS, load large
   CJK faces async on the pages that need them.
8. **Motion respects `prefers-reduced-motion`.** Every animation has a reduced or no-motion
   path, and no content depends on JavaScript animation to become visible.
9. Images: alt text mirrors the page H1 (`{name} — {niche} in {city}, {state} (photo N)`);
   serve ~800 px variants not 1920 px; always `width`/`height` attributes.

Unactionable noise, do not chase: "legacy JavaScript" and "unused JavaScript" flags pointing
at framework chunks (Next.js polyfill shim, React runtime, Webflow's `webflow.js`). Read the
URL column: an embed or the site's own script is real, the framework is not.

Non-problems that look like problems: field data "No Data" is normal for a new domain (CrUX
needs weeks of traffic); the public PSI API returning 429 is a quota issue, not a site issue.

**Webflow:** interactions (IX2) ship `webflow.js` on every page; keep interactions minimal on
high-traffic templates. Lazy-load is on by default for images. Embeds go in an HTML Embed
element; wrap them in the IntersectionObserver pattern via a small custom-code snippet.
Webflow's responsive image variants handle the 800 px rule if large originals are uploaded.
Do not upload SVG for photos, and set alt text via a CMS field binding on the image element.

---

## 9. Migrating a live site (mandatory when redesigning or changing platform)

The URL is the asset. A redesign that changes URLs without redirects throws away the
authority the site built.

1. **Crawl the old site first** (Screaming Frog or the old sitemap) and export every
   indexable URL with its title, H1, and inbound-link count. This is the source of truth.
2. **Map every old URL to exactly one new URL** in a CSV (`old_url,new_url,reason`). Old
   pages with no equivalent go to the closest parent, never the homepage, and never to a
   404 unless the content is deliberately being retired.
3. **Reuse old slugs wherever the content is the same.** A redesign is not the moment to
   "clean up" URLs unless they are actively harmful (§5); every changed URL costs ranking
   time. If they are cleaned, do it in the same migration, once.
4. **301 redirects, not 302 or 307.** Wildcard rules cover a prefix change; per-URL entries
   (ordered first) cover the exceptions.
5. **Verify live** before switching DNS if possible, and immediately after: old → 301 →
   new URL, new → 200, no chains longer than one hop, no redirect to a redirect.
6. **Keep canonicals, sitemap, and internal links pointing only at new URLs.** Then resubmit
   the sitemap in GSC. Old URLs stay in Google's index for weeks; that is normal. An optional
   accelerant if it drags past a month: a temporary migration sitemap listing the old URLs
   so Google recrawls them and sees the 301s.
7. **Preserve title/meta/H1 for pages that already rank.** Change copy below the fold
   freely; change the head signals only with a reason.
8. Do the migration while the site is young if possible. Risk scales with accrued authority.

**Webflow:** Project Settings → Publishing → 301 Redirects accepts `/old-path` → `/new-path`
and wildcard `(.*)` patterns; there is a limit on the number of rules (check current plan
limits) so use wildcards for prefix changes and per-URL rules only for exceptions. Import
the CSV in batches. Webflow cannot redirect a different host; the old domain must be pointed
at Webflow and added as a redirecting domain, or redirected at the registrar/DNS level.
**Next.js:** `next.config.ts redirects()`, `statusCode: 301` (`permanent: true` emits 308).
**Shopify:** Online Store → Navigation → URL redirects, CSV import; Shopify forces
`/products/`, `/collections/`, `/pages/`, `/blogs/` prefixes so plan the map around them.

---

## 10. Launch checklist

Run top to bottom. Every item is a yes/no.

- [ ] Page-type table written; each type has a distinct target query pattern (§1)
- [ ] Every template: exactly one H1, no buttons in headings (§2)
- [ ] No brand suffix in the title template; homepage only (§3)
- [ ] Sample of 20 titles ≤60 and descriptions ≤160, no duplicate titles across the site (§3)
- [ ] JSON-LD per template passes Rich Results Test; sitewide Organization+WebSite present (§4)
- [ ] Slugs generated by one clean function; no repeated tokens; path prefix does not repeat the domain keyword (§5)
- [ ] Canonical host chosen; other host 301s; every page self-canonical on that host (§6)
- [ ] Sitemap == linked page set; zero orphans; utility pages excluded (§6)
- [ ] GSC verified, sitemap submitted; Settings → Search generative AI = Include (§6)
- [ ] Live robots.txt (checked with curl) allows the AI search/citation crawlers, has the sitemap line, disallows no noindexed page; Cloudflare bot settings not blocking them (§6)
- [ ] Largest list page under 1 MB HTML (§7)
- [ ] PageSpeed mobile pass on every template; contrast grep done; embeds gated (§8)
- [ ] PageSpeed Insights / Lighthouse run on mobile + desktop for the homepage and one article, scores recorded. If the keyless PSI API quota is exhausted, `npx lighthouse <url> --output=json` (add `--preset=desktop` for desktop) gives the same lab scores (§8)
- [ ] Custom 404, OG image, favicon (§1)
- [ ] Multilingual: hreflang reciprocal with x-default, each locale self-canonical, sitemap alternates match (§6, `references/hreflang-i18n.md`)
- [ ] Fonts self-hosted, no Google Fonts link; reduced-motion path for every animation (§8)
- [ ] Build passes; `verify_build.py` over the build reports 0 failures (§11)
- [ ] Concept/prototype pages deleted, or noindexed and outside the sitemap (`references/site-concepts.md`)
- [ ] If migrating: redirect CSV complete, 301s verified with curl, old sitemap retired (§9)
- [ ] Write-capable endpoints (forms, click tracking) have rate limits and validate IDs against the canonical dataset before any number from them is trusted or reported

---

## 11. Build, verify, clean up (after every build or edit)

1. Source checks: touched frontmatter fields exist in the content schema; one H1 source; every
   added or changed internal link resolves.
2. Build with the detected package manager (`scripts/detect_stack.py`), plus `check` if the
   project has it.
3. Rendered checks on the built HTML: `python scripts/verify_build.py <build-dir>` sitewide,
   then `--page <path> --expect-h2 … --expect-link … --expect-type …` for each changed page.
   Report H1 count, H2 count, JSON-LD types in the DOM, and whether new sections, FAQs and links
   are present. If a check could not run, say which; never call the run clean without them.
4. Changed-file hygiene: `git status --short` and `git status --short --ignored`
   (`scripts/git_hygiene.py --allow …`). Restore unrelated generated changes only when that is
   safe, report the rest, list ignored build/dependency output, keep installed dependencies.

Details and Next.js/Shopify equivalents: `references/build-verify.md`.

---

## Pitfalls to check on every build

1. Global `%s | Brand` title template pushes nearly every page over 60 chars.
2. A stale site-URL env var or platform setting overrides the canonical host and poisons
   every canonical, sitemap and JSON-LD URL.
3. Full cards on hub pages blow past the 2 MB Googlebot cutoff.
4. `slugify(name + city)` double-stuffs URLs; fix retroactively only with 301s.
5. `loading="lazy"` does not keep an embed off the initial load.
6. ~2.9:1 gray on white fails WCAG AA and is the single most common Lighthouse ding.
7. Audit-tool character counts include HTML entities; verify raw length before rewriting.
8. Lighthouse flags pointing at framework chunks are noise on every site on that framework.
9. Never cite references from memory in YMYL content; fetch every source and quote verbatim.
10. Never trust a dashboard-stored URL that cannot be read back; validate config by shape at the
    point of use and fall back loudly.
11. A health check that cannot say why it failed hides config bugs for weeks; echo the cause.
12. JSON-LD built from third-party text is an XSS sink until `<` is escaped.
13. Astro/Zod: a frontmatter key missing from a default `z.object()` schema is silently stripped;
    the build passes and the field never renders. Add it to the schema first.
14. Layout H1 + Markdown `#` = two H1s. Check where the H1 comes from before adding one.
15. `trailingSlash: 'never'` without `build.format: 'file'` on Cloudflare Pages: every
    canonical points at a URL that redirects.
16. A font token naming `"Inter"` while the package registers `"Inter Variable"` silently falls
    back to the system font.

File: seo-site-build/SKILL.md · Version 1.0 · November 2026
