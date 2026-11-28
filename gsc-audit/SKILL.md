---
name: gsc-audit
description: "Audit a Google Search Console property and turn first-party clicks, impressions, CTR and position into one action brief per URL. Runs 7 analyses (CTR gaps, content decay, striking distance, cannibalization, mobile/desktop gaps, dead pages, brand vs non-brand), a page-query map, device/country/search-type/search-appearance segments, a 16-month trend with YoY, URL Inspection sampling for suspicious pages and sitemap health. Archives every pull so history outlives Google's 16-month limit. Emits a lane result JSON for a site audit orchestrator and handoff queues for seo-page-diagnosis and the seo-content refresh flow. Triggers on: GSC audit, Search Console analysis, CTR wins, low CTR pages, content decay, which pages lost traffic, striking distance keywords, quick wins, cannibalization, dead pages, deindexed pages, brand vs non-brand, organic traffic drop, set up GSC, connect Search Console."
---

# GSC Audit (Search Console lane)

Search Console is the only first-party record of how Google shows our pages. Use it to see what is
actually happening: which pages earn impressions, which queries matter, where clicks moved, and
whether third-party estimates (DataForSEO) deserve belief.

The output is **not** seven separate tables. It is a decision map: for each URL, is the problem a
snippet (CTR), a ranking loss (decay), distance to page one, overlap with another page, a device
gap, or an indexing fault? What should happen next, who does it, and how sure are we?

Works for any number of sites (separate businesses, separate properties, separate runs), one config each:
- **Example Kitchen** (example.com): the shipped EXAMPLE config `configs/example-kitchen.json`.
  Copy it to `configs/<store>.json` and replace every value.
- A client or prospect site: copy a config and set `"owner_type": "client"`.

---

## Prerequisite: the `gsc` MCP server

The skill reads Search Console through an MCP server named **`gsc`** (tools appear as
`mcp__gsc__...`). Check that it is present before Stage 0: ask for the property list, or call the
server's capabilities tool.

- **Not connected + own site:** stop the lane and point the user to
  `references/setup.md`. Do not do setup inside an audit run unless the user asks.
- **Not connected + client/prospect:** the owner must grant access (a Restricted user is enough).
  Keep all traffic numbers directional until then.
- Either way, write the not-run lane result so the wider audit continues:
  ```powershell
  python "gsc-audit/scripts/gsc_analyzer.py" not-run --reason "gsc MCP not connected" --owner-type own --out "<run>\gsc-lane.json"
  ```

### Missing-GSC gate (hard rule)
Without GSC rows: **no traffic sizing, no CTR upside, no decay claims, no standalone dollar
figure.** The not-run result opens the `missing-gsc` dependency gate, which blocks
`traffic_sizing`, `ctr_upside` and `decay_confidence`. Anything sized elsewhere while the gate is
open carries the label "GSC-gated directional estimate". A partial run opens the same gate but
blocks only what is actually missing (e.g. no comparison period blocks `decay_confidence` only).

---

## Workflow

```
Stage 0  Property selection        list properties, pick the store's property      (confirm)
Stage 1  Configuration             brand terms, period, analyses, high-value paths  (confirm)
Stage 2  Data collection           MCP pulls -> <run>\raw\*.json (paginated)
Stage 3  Analysis                  gsc_analyzer.py analyze (archives + analyses + briefs)
Stage 4  URL Inspection sampling   inspect the queue, save, re-run analyze
Stage 5  Report + handoffs         summary, url-briefs.md, lane JSON, handoff queues
```

Read each reference on reaching its stage, not before.

| Stage | Read |
|---|---|
| 0-1 | this file (below) |
| 2 | `references/data-collection.md` (pull plan, file format, pagination, caveats) |
| 3-4 | `references/analyses.md` (thresholds, interpretation, remediation) |
| 5 | `references/output-format.md` and `references/lane-contract.md` |
| setup | `references/setup.md` |

### Stage 0: Property selection
1. List properties through the `gsc` server.
2. Match the store: prefer the Domain property (`sc-domain:example.com`) over a URL-prefix
   property, because it covers http/https and www/non-www. Both candidates are listed in the
   store config.
3. Confirm with the user which property to use. Record it in `config.json`.

### Stage 1: Configuration
Create the run folder `<store folder>\gsc-runs\<YYYY-MM-DD>-<brand>\` (for example
`<workspace>\example-kitchen\gsc-runs\2026-10-05-example-kitchen\`). Copy the store config into it as
`config.json` and confirm with the user (defaults shown):

- **Brand terms: our brands only** (the `brand_terms` list in the config). Example config
  (Example Kitchen): example kitchen, example-kitchen, examplekitchen, example.com, exk. Add any
  sub-brand the site owns. Names of other makers the site sells (Maker A, Maker B and so on)
  are **not** our brand. Queries that contain them are non-brand
  demand. "example kitchen" is also an everyday phrase ("example kitchen ideas"), so it is marked
  ambiguous: it counts as brand only when the query is exactly the name or also carries a
  navigational hint (reviews, coupon, .com, shipping, phone...). Brand terms are matched as whole
  words, so "exk" never matches inside another word. Add misspellings if they have volume.
- **Period:** 28 days (`period_days`). Get the exact windows with
  `python gsc_analyzer.py periods`: current = the 28 days ending 3 days ago (data lag),
  previous = the 28 days before that, YoY = the current window shifted 364 days (same
  weekdays), history = about 16 months.
- **Analyses:** all 7 by default. The user can pick a subset; the pulls in Stage 2 shrink to match.
- **High-value patterns:** `/products/`, `/collections/`, `/cart`. They push matching URLs up the
  queue (`high_value_weight`, default 1.5x) and select decaying money pages for inspection.
  Impressions on `/cart` point to an indexing problem in themselves.
- **CTR curve:** `ctr_curve_mode: auto` (see below).
- **Dead pages:** ask how to read pages removed on purpose (discontinued products, ended sales)
  so they are not reported as accidents.
- `owner_type` (own/client), `inspection_budget` (10), `source_type` (`live`).

### Stage 2: Data collection
Follow `references/data-collection.md`. Every MCP response is saved as JSON under `<run>\raw\`
**before** any analysis, one file per pull kind (`current_page.json`, `current_query_page.json`,
`previous_page.json`, `yoy_page.json`, `daily.json`, `page_device.json`, `page_country.json`,
`search_type_totals.json`, `search_appearance.json`, `sitemaps.json`, ...). Paginate any pull that
returns exactly 25,000 rows. Show progress during the pulls ("Pulling query/page rows, page 2...").

### Stage 3: Analysis
```powershell
python "gsc-audit/scripts/gsc_analyzer.py" analyze --run-dir "<run>" --register "<store folder>\KEYWORD-REGISTER.csv"
```
This, in order:
1. **Archives** every raw pull to `<store folder>\gsc-runs\_archive\<property>\<kind>\` with the
   date range and pull date in the name. Identical files are skipped, nothing is overwritten.
   Google keeps only 16 months and offers no backfill, so this archive is the only way history
   accumulates past that limit. `history` merges every archived `daily` pull (latest pull wins
   per date, since recent days get revised) and the trend uses the merged series.
2. Builds the **CTR curve**: one default curve (positions 1-20; 21-30 = 0.3%, beyond = 0.1%).
   In `auto` mode it calibrates from the property's own non-brand query/page rows when at least
   5 rounded positions each have 30+ rows and 500+ impressions, keeps the curve non-increasing,
   and falls back to the default for thin positions. `default` forces the fixed curve; `own`
   calibrates whatever positions qualify. The lane JSON records which source each position used.
   The curve and these minimums are the `T` constants and the default curve in
   `scripts/gsc_analyzer.py`.
   Note: a calibrated curve measures a page against the store's own average at that position.
3. Runs the **7 analyses** (exact thresholds in `references/analyses.md`):

   | Analysis | Rule |
   |---|---|
   | CTR gap | position < 20, 50+ impressions, actual CTR < 70% of expected; upside = impressions x (expected - actual) |
   | Content decay | 10+ previous clicks, clicks down 25%+; ranking drop (2+ positions worse), CTR drop (below 75% of before), both, demand/visibility drop (impressions down 25%+), or plain loss; seasonal if within 90% of the same window last year |
   | Striking distance | query/page pairs at positions 11-20 with 100+ impressions, grouped by page |
   | Cannibalization | non-brand query with 2+ of our pages and 50+ total impressions; labelled same-type overlap, store hierarchy (collection + product) or mixed intent; never auto-merge |
   | Mobile vs desktop | 50+ impressions on each device; CTR ratio 2x+ or position gap 5+ |
   | Dead pages | 10+ clicks last period, 0 now; top 5 queued for URL Inspection |
   | Brand vs non-brand | non-brand click share: over 70% excellent, 50-70% healthy, 30-50% needs growth, under 30% critical |

4. Builds the **page-query map** (every query/page row, brand class, source `gsc`,
   confidence 0.9, ready to join with DataForSEO keywords at 0.6).
5. Builds **segments**: device split, country table with low-CTR market flags, search type
   (web/image/video/news/discover), search appearance (with period change when a previous
   appearance pull exists).
6. Builds the **trend**: monthly series over all available history, current vs previous vs YoY
   windows (provisional last 3 days excluded), month-over-month anomalies, seasonality index once
   13+ full months exist. Optional `page_date` rows add a first-vs-last month position per URL,
   which is our first-party rank history.
7. Reads **sitemap health** and **inspection results**, if pulled.
8. Writes **one brief per URL** (see below), recommendations, evidence, the inspection queue and
   the handoff files.

### Stage 4: URL Inspection sampling
`inspection-queue.json` lists at most `inspection_budget` URLs, by reason: dead pages (top 5),
decaying high-value pages with a ranking drop, high-impression zero-click pages, pages earning
clicks that are missing from the sitemap (when sitemap URLs were pulled), and collection-scoped
Shopify product URLs (`/collections/x/products/y`) that earn impressions. Inspect each through
the `gsc` server, save all results to `<run>\raw\inspections.json`, then re-run `analyze`.
Inspection shows indexed state, not guaranteed visibility for every query. noindex, redirects and
canonicals may be deliberate: treat them as review items and ask before calling them bugs.

### Stage 5: Report and handoffs
Present the summary first (counts, top-line numbers, top 10 URLs to work first), then offer the
full write-up and CSV exports (`references/output-format.md`). Outputs in the run folder:

| File | For |
|---|---|
| `gsc-lane.json` | a site audit orchestrator (`evidence/gsc.json` there); contract in `references/lane-contract.md` |
| `url-briefs.md` | The user: one section per actionable URL |
| `handoff/page-diagnosis-queue.json` | `seo-page-diagnosis`: URL, target query, position, signals, action |
| `handoff/refresh-candidates.json` | `seo-content` refresh auto-detect: URL + KEYWORD-REGISTER match (Article #, Primary Keyword, Complete URL Slug, Shopify Article ID) + outcome hint |
| `inspection-queue.json` | Stage 4 |

---

## One brief per URL

Each URL gets a single brief that merges every signal: CTR gap, decay, dead page, striking-distance
queries, overlap, device gap, inspection state, Shopify URL notes, register match, and previous
and YoY metrics. The action follows a fixed ladder (first match wins):

1. `fix_indexing`: inspection risk 4+ (not indexed, noindex, robots, 404/5xx, unknown to Google)
2. `restore_or_redirect`: dead page with no index explanation yet
3. `check_seasonality`: decay that matches last year's season
4. `refresh_content`: ranking or demand decay
5. `fix_snippet`: CTR gap or CTR-only decay
6. `review_cannibalization`: same-type overlap
7. `push_to_page_one`: striking-distance queries
8. `fix_device_gap`
9. `monitor`

Routes and owners: content work goes to `seo-page-diagnosis` then `seo-content` (owner content;
product and collection pages go to owner catalog); indexing and device problems go to
`seo-onpage-audit` / theme work (owner theme-dev). The refresh outcome hint maps actions to the
seo-content refresh outcomes: `fix_snippet` and `push_to_page_one` = quick_update,
`refresh_content` = substantive_refresh, `restore_or_redirect` = restore,
`review_cannibalization` = consolidate/redirect/prune handoff, seasonal or monitor = no_change.
seo-content still confirms the outcome after its own diagnosis. The hint is a starting point.

Scores: `ctr_upside` (clicks), `traffic_loss` (lost clicks x 1.0 when the page had 50+ clicks,
else 0.7), `striking_distance` (impressions x a weight that peaks at positions 8-15),
`striking_click_gain` (directional clicks if the pair reached position 5), `index_risk` (0-5).
Priority = (ctr upside + traffic loss + striking gain) x confidence x high-value weight. Blocking
index issues always sort first. Confidence rises with impressions (100+), clicks (10+), a 28-day
window and agreeing signals, and drops when the 25,000-row cap was hit.

---

## Data caveats (always state them)

- **Lag:** data arrives 2-3 days late and the latest days get revised. Windows end 3 days before
  today. The archive keeps re-pulls, and the newest pull wins per date.
- **Row cap:** 25,000 rows per request. Page with `start_row` until a page returns fewer rows.
  If a file holds exactly 25,000 rows and was not paged to the end, the lane lowers confidence and
  says so.
- **Average position is not a rank.** It is impression-weighted across every query, device and
  location. Rely on clicks, impressions and settled trends.
- **Anonymised queries are withheld,** so query-level totals never add up to page-level totals.
  Say which grain a number comes from.
- **Thin data:** below 50 impressions metrics swing, 100+ is dependable. Under 100 impressions
  for the whole property, the lane caps confidence at 0.40 and says the audit is not meaningful.
- **FAQ rich results are gone** for all sites (HowTo is deprecated). Never recommend FAQ or HowTo
  markup as a CTR or visibility fix.
- Retry only transient errors (rate limit, 5xx, timeout): wait 30 s, retry once, then mark the
  lane partial with the exact error. Do not retry auth, permission, invalid-property or
  malformed-request errors.

## Rules
- No invented numbers. Every figure in the report traces to a raw file in the run folder.
  Directional estimates (striking gain, CTR upside) are labelled "GSC-based directional estimate",
  never revenue.
- Brand terms = our brands only. Never count another maker's brand as brand traffic.
- Overlap is a question, not a verdict: several URLs on one query can be legitimate (collection +
  product is normal store hierarchy).
- Dead pages: confirm intent before recommending a restore. Removed products usually need a 301
  to the closest collection, not a restore.
- Credentials: never read, print or copy OAuth JSON. It lives only under `.secrets/`
  or `~\.claude\mcp-gsc\`.

## Files
- `scripts/gsc_analyzer.py`: analysis engine (stdlib). Commands: `analyze`, `archive`, `history`, `periods`, `not-run`.
- `scripts/setup_gsc.py`: dry-run-first setup planner (see `references/setup.md`).
- `configs/*.json`: per-store defaults.
- `tests/test_gsc_analyzer.py`: synthetic-fixture tests (`python gsc-audit/tests/test_gsc_analyzer.py`).
- Run folders and the archive (`<store>\gsc-runs\`) are generated data and gitignored.

File: gsc-audit/SKILL.md · Version 1.0 · November 2026
