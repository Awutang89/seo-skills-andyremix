# GEO / AI-Search Citation Checklist

GEO (Generative Engine Optimization) = optimizing content so AI answer engines — Google AI
Overviews, ChatGPT web search, Perplexity, Bing Copilot — quote and cite it. From Google's side
it is still SEO; this is an extra layer on top of the on-page work in `SKILL.md`, not a separate
discipline.

This file has two parts: **per-article rules** (apply to every draft, fold into Phase 4 + the QA
gate) and **site-level enablement** (one-time setup, not per article).

> **Provenance / verify-before-publish:** The quantitative figures below (passage lengths, the
> multi-modal lift, the brand-mention correlation) are structural rationale adapted from public
> AI-search analyses (e.g. Ahrefs' Dec-2025 AI-search study, as compiled in the open-source
> `claude-seo` project, MIT). Use them to shape *structure*. Do **not** drop the raw figures into a
> published article as cited claims until you have confirmed them against the primary source —
> brand voice requires numbers with real attribution. The structural advice (write self-contained,
> right-length answer blocks) holds regardless of the exact percentages.

---

## Per-article rules

### 1. Direct answer in the first 60 words of each section
Every H2 opens by answering the heading's implicit question inside the first ~60 words — no
warm-up. This is the existing **Answer-First H2 Rule** (40–60 words, stat + named source). It wins
featured snippets and gives AI engines a clean extract point.

### 2. Build a self-contained citable answer block (~130–170 words)
The 40–60-word opening wins snippets; AI *citation* favors a slightly longer, fully self-contained
passage. For each section that answers a discrete question, continue past the opening to a
**~130–170-word block** that:
- makes complete sense quoted out of context (no "as mentioned above")
- contains at least one specific statistic with a named source
- ends a thought — doesn't trail into the next section

This sits between the short **citation capsule** (40–60w quotable nugget, keep ≥2/article) and the
full section (120–250w). In practice: open with the 40–60w direct answer, then round the block out
to ~130–170 self-contained words before the next sub-point.

### 3. Pair citable sections with a relevant visual (multi-modal)
Sections that contain a citable answer block should sit next to a relevant **image, chart, or
table** (use the verified assets from Phase 1.5). Text-plus-visual passages are selected by AI
answer engines at meaningfully higher rates than text alone. We already place images/charts — the
GEO rule is to put them *adjacent to the answer blocks*, not just wherever they look nice.

### 4. Question-based H2s
Where natural, phrase H2s as the question a user would ask (still respecting the secondary-keyword
header rules in `SKILL.md`). Question headings map directly onto how AI engines segment a page.

### 5. TL;DR box
Already required (40–60 words, includes a stat, standalone, immediately after the intro). It is one
of the most frequently quoted blocks on a page — keep it self-contained.

### Per-article QA (mirror in the Phase 7 gate)
- [ ] Each major H2 answers its question in the first ~60 words
- [ ] Key sections contain a self-contained ~130–170-word citable answer block (stat + source)
- [ ] ≥2 citation capsules (40–60w) present
- [ ] Citable sections are paired with a relevant image/chart/table
- [ ] TL;DR box present (40–60w + stat, standalone)

---

## Site-level enablement (one-time — NOT per article)

These are configured once on the Shopify store, not in each article. Check them when standing up
the workflow, then periodically.

### A. Let AI crawlers in (robots.txt)
Confirm the store's `robots.txt` (Shopify: `robots.txt.liquid`) does **not** block the AI search
crawlers you want citing you:
- `GPTBot`, `OAI-SearchBot`, `ChatGPT-User` (OpenAI)
- `ClaudeBot` (Anthropic)
- `PerplexityBot` (Perplexity)
- `Google-Extended` — **note:** this only governs Gemini *training*. Blocking it does **not** affect
  Google Search indexing or AI Overviews. Decide deliberately; don't block it by accident assuming
  it kills AI Overviews — it doesn't.

### B. Server-side rendering (already satisfied)
AI crawlers generally do not execute JavaScript, so SEO-critical content and JSON-LD must be in the
server-rendered HTML. **Shopify storefronts render server-side (Liquid), so this is already met** —
keep article content and schema in the rendered body, not injected client-side. (Ties into the
`seo-schema` skill: emit Article/Breadcrumb/Product JSON-LD as theme-rendered metafields, not JS.)

### C. Brand mentions / entity presence (off-page, strategic)
AI-visibility analyses report that **brand mentions across the web correlate more strongly with AI
citation than raw backlinks do**. Practically, for your-project that means: get the brand named
in roundups, supplier/manufacturer pages, industry forums, and Q&A sites — unlinked mentions still
count. This is a strategy note, not a per-article task. (Verify the specific correlation figure
before citing it anywhere public — see provenance note above.)

### D. Cloudflare AI-bot block (only if the store is behind Cloudflare)
As of Jul 2025, Cloudflare blocks known AI crawlers by default on new zones. **Shopify storefronts are
served by Shopify's own CDN, not Cloudflare**, so this usually does **not** apply to your-project.
It only matters if a custom domain is proxied through Cloudflare (orange-cloud). If it is: Cloudflare
dash → Security → Bots → AI Crawlers/Scrapers, and allow the bots from §A you want citing you.
Otherwise mark N/A and move on.

### E. Crawl-friendly delivery (TTFB + HTML size)
AI crawlers fetch raw HTML and mostly skip slow or oversized pages. Soft targets: **TTFB < 200 ms** (a
page consistently > 1 s gets crawled less often) and **rendered HTML < ~200 KB** (very large DOMs risk
partial extraction — the crawler may not reach the bottom of a long article). Shopify's CDN handles
TTFB; the lever we control is not bloating article markup (avoid giant inline SVG / base64 images, keep
the DOM lean). Not a per-article gate — flag only if a page is egregiously heavy.

### F. llms.txt (experimental — low priority)
A proposed `/llms.txt` machine-readable site summary for LLMs. **No major AI platform has confirmed
reading it**, so treat it as optional/experimental, not a citation factor. If we ever add one it's a
single sitewide file — don't spend per-article effort on it. INFO priority only.

---

## How this connects
- Drafting rules live in `SKILL.md` Phase 4 (TL;DR / Answer-First / Citation Capsule).
- Enforcement lives in `SKILL.md` Phase 7 → **GEO / AI Citation Readiness** rows.
- Schema enablement lives in `skills/seo-schema/SKILL.md`.
