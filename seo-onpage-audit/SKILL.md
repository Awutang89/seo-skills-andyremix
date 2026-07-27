---
name: seo-onpage-audit
description: "Audit a live web page's on-page and technical SEO — title/meta, headings, keyword coverage (primary + secondary/long-tail), URLs, canonical, indexability, links, schema (present AND missing-but-qualifying), and Core Web Vitals thresholds. Native WebFetch, no crawler/Playwright infra. Works on ANY website — the target keyword is inferred from the page, no keyword list required. Optional site-level crawl pass (Firecrawl/Scrapling) for cross-page checks, including verifying every URL declares its own unique canonical. Use to spot-check a published page, a client site, or before/after a change. Triggers on: audit this page, on-page SEO check, technical SEO, is this page optimized, check canonical/robots, duplicate canonicals, canonical uniqueness, site-wide canonical check, core web vitals, CWV check, schema audit. Outputs a 0-100 score with a prioritized fix list."
---

# On-Page & Technical SEO Audit (any website)

A lean, WebFetch-based spot-check of the on-page and technical SEO signals you control on a single
URL — scored and prioritized. It works on **any website**: the target keyword is **inferred from
the page itself** (H1, title, first paragraph, repeated phrases), so you can audit a page you've
never seen without a keyword list.

This is deliberately **not** a full crawler/Playwright audit. That infra is heavy, Windows-buggy,
and buys little for a single-page spot-check — field Core Web Vitals need PageSpeed/CrUX anyway.
For the four cross-page items a single fetch can't prove (uniqueness, orphans, URL-structure
consistency, inbound-link distribution), use the **optional site-level pass** (crawl-based) below.

Companion skills, if present in your library: `seo-schema` (schema fixes), `image-seo-audit`
(deeper image checklist).

---

## What it checks

| Category | Checks |
|---|---|
| **Title** | 50–60 chars (≤~600px); primary keyword present + front-loaded; short/descriptive. Advisory: click-worthy. Uniqueness → site-level pass |
| **Meta description** | 50–160 chars; primary keyword present; accurately summarizes the page. Advisory: engaging. Uniqueness → site-level pass |
| **H1** | exactly one; 40–65 chars; primary keyword present; matches page intent/search intent. Advisory: grabs attention |
| **H2–H6** | descriptive/meaningful; carry secondary / long-tail keywords; cover the subtopics the main query implies |
| **Keyword coverage** | primary keyword in title, H1, **first 100 words**, **≥1 H2**, URL slug, and meta; secondary/long-tail terms present across subheads + body |
| **URL / slug** | lowercase, hyphenated, concise, human-readable (not an ID); **no repeated keywords**; no redirect chains (max 1 hop) |
| **Links** | internal count + even spacing (no two links within 200–300 words); descriptive/informative anchor text (not "click here"/bare URLs); external links point to authorities; paid/affiliate/UGC links carry `rel="sponsored/ugc/nofollow"`; no broken links |
| **Schema** | JSON-LD present + valid types — AND recommend structured-data types the page **qualifies for but is missing** (content-signal based; see `references/schema-opportunities.md`) |
| **Indexability** | canonical — exactly one, in `<head>`, absolute, self-referencing, character-for-character equal to the live URL; meta robots (no accidental `noindex`/`nofollow`); present in sitemap |
| **Core Web Vitals** | thresholds + HTML heuristic flags (no field data without PSI/CrUX) |
| **Images** | alt text present, ≤125 chars, descriptive, keyword-aware (basics only — deeper checks in `image-seo-audit`) |
| **Cross-page** (site-level pass) | title/meta uniqueness; **canonical uniqueness — every URL must declare its own canonical, no two URLs sharing one target**; orphan pages; URL-structure consistency; inbound-link distribution |

Full thresholds: `references/cwv-and-onpage.md`. Schema recommendation map: `references/schema-opportunities.md`.

---

## Workflow

1. **Fetch the page** with WebFetch (the live URL). If you also have the page source locally, read
   it — source is truth for content, the live page for rendered markup.

2. **Infer the target keyword.** From the H1, title tag, first paragraph, and the most repeated
   noun phrases, state the page's **primary keyword** explicitly at the top of the audit, plus the
   **secondary / long-tail** terms the page itself signals. Everything keyword-related is judged
   against these inferred targets — no external keyword list is assumed. If the page gives no clear
   keyword signal, say so (that itself is a finding: unfocused page).

3. **Parse on-page elements:** `<title>`, meta description, **every `rel="canonical"` in the served
   HTML** (count them — two conflicting tags means Google ignores both; one after `</head>` is
   ignored too), meta robots, H1 (count +
   text + char length), H2–H6 outline, body word count + the first 100 words, internal vs external
   `<a>` (with `rel` values + anchor text), `<img>` alt/dimensions, every
   `<script type="application/ld+json">` block, and the URL slug.

4. **Score each scored category** against `references/cwv-and-onpage.md`.

5. **Schema opportunities.** From the parsed content signals (FAQ/Q&A block, ranked list /
   comparison table, product/price signals, embedded video, breadcrumb trail, images), recommend
   the structured-data types the page qualifies for but is missing — following
   `references/schema-opportunities.md`. **Never recommend HowTo** (deprecated — see that file).

6. **Advisory pass (unscored).** Make the subjective judgment calls as short notes — title
   click-worthiness, meta engagement, H1 attention, whether subheads are meaningful, whether
   title/meta accurately summarize the page. These are advisory only: they never PASS/FAIL and
   never move the 0–100 score.

7. **Core Web Vitals.** Report the thresholds and the heuristic flags visible from HTML (oversized
   images, missing image dimensions → CLS, render-blocking third-party scripts). For real field
   numbers, note "run PageSpeed Insights for [url]" — not measurable from HTML alone.

8. **Cross-page items.** Title/meta uniqueness, **canonical uniqueness**, orphans, URL-structure
   consistency, and inbound-link distribution cannot be proven from one URL. A single page can only
   show you that its canonical is *self-referencing* — it cannot show you that **no other URL claims
   the same canonical**. A page can pass every single-URL canonical check and still be one of forty
   URLs all pointing at the homepage. Never report canonical as fully PASS from a one-URL fetch. Emit them as INFO pointing to the **site-level pass**
   rather than a fake PASS.

9. **Output** the 0–100 score, the per-category breakdown, a Critical→Low fix list, the Advisory
   notes, and the Schema opportunities.

---

## Scoring (0-100)

| Category | Weight |
|---|---|
| Content / on-page (title, meta, headings, keyword coverage) | 30 |
| Links (internal density + spacing, descriptive anchors, external `rel`, no broken) | 20 |
| Schema (right types present + valid; opportunities noted) | 15 |
| Indexability (canonical, robots, in sitemap) | 15 |
| Performance / CWV (heuristic flags + thresholds) | 15 |
| Security / URL (HTTPS, clean concise slug, no keyword repetition, no redirect chains) | 5 |

Report the number, the per-category breakdown, and the single weakest category as the priority.
**Advisory flags and the site-level cross-page checks sit OUTSIDE the 0–100** — they are reported
but do not change the score.

---

## Output format

```
ON-PAGE AUDIT — https://example.com/some-page   Score: 78/100
Inferred primary keyword: "portable espresso maker"  ·  secondary: "manual", "for travel", "usb"
Content/on-page 24/30 · Links 14/20 · Schema 9/15 · Indexability 15/15 · CWV 11/15 · Security 5/5

CRITICAL
- (none)
HIGH
- Keyword coverage: primary keyword absent from every H2 and from the first 100 words.
- H2–H6: no secondary/long-tail keywords in any subheading — subtopics of the query uncovered.
- Schema: no BlogPosting/Article JSON-LD detected on the rendered page.
MEDIUM
- Title 64 chars (>60) — trim.
- H1 is 31 chars (<40) — expand to describe the page.
- Meta description 168 chars (>160) — tighten.
- 2 images missing width/height → CLS risk.
LOW
- URL repeats "espresso" twice in the slug — de-duplicate.
- 1 external link to a forum — not an authoritative source.

SCHEMA OPPORTUNITIES (present → recommend adding)
- Page has a visible FAQ block but no FAQPage JSON-LD → add FAQPage (INFO: rich-result-restricted).
- Page is a "best X" ranked list with a comparison table → add ItemList (+ Product/AggregateRating).
- No BreadcrumbList detected → add BreadcrumbList.
  (No HowTo suggested — deprecated.)

ADVISORY (subjective, unscored)
- Title is descriptive but flat — no curiosity hook or benefit; likely under-performs on CTR.
- Meta reads like a summary, not a pitch — no reason-to-click.
- Two H2s ("Overview", "More Info") are decorative, not meaningful — rename to the subtopic.

CROSS-PAGE (needs the optional site-level pass)
- Canonical is self-referencing and exact on THIS URL — but whether any other URL claims the same
  canonical is unproven from one fetch. Run the site-level pass.
- Title/meta uniqueness, orphan status, URL-structure consistency, inbound-link distribution —
  run the site-level pass to verify.
```

---

## Optional: Site-Level Pass (cross-page items)

Opt-in mode for the items a single-URL fetch can't prove: **title/meta uniqueness**, **canonical
uniqueness**, **orphan pages**, **URL-structure consistency**, and **inbound-link distribution**.
It is fully **crawl-based** — it crawls the *target* site and derives everything from that crawl.
It reads no local files, so it works on any website.

**Getting the crawl (needs an API key from whoever runs the audit):**
1. **Prefer a running Firecrawl MCP server** if one is available in the session — use its map +
   scrape tools directly.
2. **Else** run the bundled script `scripts/site-audit.py`, which reads the key from the
   **`FIRECRAWL_API_KEY` environment variable** (never hardcode it) and uses Firecrawl v2 `map`
   (URL discovery) + `batch/scrape` (per-page title/meta/markdown), stdlib-only. Ask the user for
   the key if it isn't set.
3. **Scrapling** is a keyless local alternative for users who don't want an API key — swap it in as
   the fetcher; the analysis below is identical.

**What it derives from the crawl (per page: `url`, `title`, `meta_description`, `internal_links[]`,
and the raw served HTML — the canonical must be parsed from HTML, it is not reliably present in
crawler metadata):**
- **Title/meta uniqueness** — flag duplicate or near-duplicate titles and meta descriptions.
- **Canonical uniqueness** — see below.
- **URL-structure consistency** — flag slug/path outliers (depth, casing, separators, trailing
  slash) against the site's dominant pattern.
- **Orphan pages** — pages with zero inbound internal links in the crawled link graph.
- **Inbound-link distribution** — flag shallow/important pages that receive few inbound links.

### Canonical uniqueness — one own canonical per URL

The rule: **every indexable URL declares exactly one canonical, in `<head>`, absolute, pointing at
itself.** Two URLs sharing a canonical target means one of them is asking Google not to index it.
At scale this is the single most destructive technical-SEO bug — a bad template can de-index a
whole section while every page still "has a canonical."

Findings, in severity order:

| Finding | Severity | Why |
|---|---|---|
| 2+ URLs share a canonical target that is **not one of them** | **CRITICAL** | Classic broken template — e.g. every article canonicalizing to `/` or to one hub. All of them drop out. |
| Canonical points at a **different page** (non-self-referencing) | **CRITICAL** | The URL is asking to be dropped from the index. |
| **Cross-host** canonical | **CRITICAL** | Hands ranking signals to another domain. Check for a staging/CDN hostname leaking into the template. |
| **Missing** canonical | HIGH | Google picks one for you, using parameters and duplicates you don't control. |
| **Multiple conflicting** canonical tags on one page | HIGH | Google ignores **all** of them — same effect as missing. |
| Canonical **outside `<head>`** | HIGH | Ignored entirely. Fix is to move it, not to add another. |
| **Relative** canonical (`/slug`) | MEDIUM | Resolves today, breaks the moment the page is served on another path/host. Make it absolute. |
| Near-miss self-reference — `http` vs `https`, `www` vs bare, trailing-slash or case drift | MEDIUM | Resolves to the same doc but splits signals and contradicts the sitemap. |
| Canonical target **never seen in the crawl** | MEDIUM | Verify it returns 200 and is itself indexable — a canonical to a 404 or a `noindex` page is wasted. |
| Param URLs (`?variant=`, `?sort=`) consolidating to a clean URL | INFO | Normal, intended use. Confirm it's deliberate, don't flag it as a bug. |

**Do not report "missing canonical" without HTML to prove it.** If the fetcher returned no raw HTML
for a URL, the canonical is *unknown*, not absent — the script tracks these separately and the
report says SKIPPED rather than inventing a site-wide critical.

Output a short cross-page report (duplicates, canonical findings, orphans, structure outliers,
thin-inbound pages). This is separate from the single-page 0–100.

---

## Optional add-on (NOT installed) — lab Core Web Vitals

Lab CWV/Lighthouse numbers locally require a headless browser (Chromium) + a Lighthouse runner —
left out on purpose. For most sites the storefront/page is server-rendered, and field CWV needs
PageSpeed/CrUX regardless. The cleaner route is running **PageSpeed Insights** (free field data)
per URL rather than installing a local lab stack.

---

## How this connects
- **`references/cwv-and-onpage.md`** — CWV thresholds (INP not FID), on-page length rules,
  canonical/robots guidance, link rules, crawler/AI-bot notes.
- **`references/schema-opportunities.md`** — the content-signal → recommend-schema map, with the
  supported/restricted/deprecated gate (self-contained).
- **`scripts/site-audit.py`** — the optional generic site-level crawler (Firecrawl, env-keyed).
- **`seo-schema`** skill (if present) — for actually implementing the recommended schema.
- **`image-seo-audit`** skill (if present) — deeper image checklist (this skill flags only basics).

## Reference
- `references/cwv-and-onpage.md`
- `references/schema-opportunities.md`
