# The seven analyses: rules, reading, fixes

The thresholds here match the `T` table in `scripts/gsc_analyzer.py`. After a change to one, change
the other. Our additions (not from the original rule set) are marked **(ours)**.

General reading rules:
- Under 50 impressions a metric swings; 100+ is dependable. 7-day windows are noisier than 28.
- Problems overlap: a decaying page often has a CTR gap too; overlapping pages can both show as
  striking distance; a dead page may have lost to another of our URLs. The URL brief merges them.
  Report the one most useful interpretation per URL, not every table.

---

## 1. CTR gap (under-clicked pages)
**Rule.** Page rows with position below 20 and 50+ impressions. Expected CTR comes from the curve
(interpolated between whole positions). Flag when actual CTR < expected x 0.70.
Upside = impressions x (expected - actual), in clicks, directional. Sorted by upside.

**Read it.**
- Homepage: navigational and brand queries distort CTR. Act only on a severe gap.
- Collection pages: broad head terms get lower CTR. Check the query mix first.
- Near position 1 with low CTR: something on the SERP (AI Overview, shopping pack, snippet,
  map pack) usually takes the clicks. Check the live SERP before rewriting anything. This is the
  zero-click split: weak snippet versus a SERP feature or intent mismatch. The analyzer marks the
  cause "unverified" until someone looks.
- A calibrated curve compares the page with this store's own average at that position.

**Fixes.** Title that matches the query's intent with the keyword early (mind the theme's brand
suffix in the rendered title); a specific meta description; eligible rich results that still
exist (Product/merchant listings: price, availability, reviews); align commercial vs
informational wording. Not FAQ or HowTo markup: those rich results are gone.

## 2. Content decay
**Rule.** Pages with 10+ clicks in the previous window whose clicks fell 25%+. Pages that fell to
zero are reported once, as dead pages. Diagnosis:
- `ranking_drop`: average position worse by 2+
- `ctr_drop`: CTR below 75% of the previous CTR
- `ranking_and_ctr_drop`: both
- `demand_or_visibility_drop` **(ours)**: impressions down 25%+ with position and CTR stable
- `traffic_loss`: none of the above clearly
- `seasonal_likely` **(ours)**: current clicks are at least 90% of the same window last year

**Read it.** Seasonal content (sunscreen in spring, gift guides in November) decays on schedule, so check
YoY before acting. News-like posts fade after a spike. A URL change or redirect can look like
decay. Check the other URL.

**Fixes.** Ranking drop: a real refresh (current facts, missing sections, better answer to the
query), run through `seo-page-diagnosis` first. CTR drop: competitors improved their snippets,
so rewrite title/meta. Both: a full overhaul. Demand drop: nothing to fix on the page. Watch the
query trend.

## 3. Striking distance (quick wins)
**Rule.** Query/page pairs at positions 11-20 with 100+ impressions, sorted by impressions and
grouped by page. Brand queries are flagged, since navigational intent is rarely worth pushing.
- `striking_distance_score` **(ours)** = impressions x weight (1.0 for positions 8-15, 0.6 for
  4-7, 0.7 for 16-20).
- `directional_click_gain_at_target` **(ours)** = impressions x (expected CTR at position 5 -
  current CTR). Directional, never promised.

**Read it.** Very competitive queries may be stuck at 11-20 for authority reasons. Check who
ranks above. Positions 11 to 20 are the one striking-distance band for every SEO skill.

**Fixes.** Put the query in the H1, the first paragraph and a subheading where it fits naturally;
answer the query's sub-questions; add internal links with descriptive anchors from related
articles and collections (`internal-linking`); improve mobile speed.

## 4. Cannibalization (overlap)
**Rule.** Non-brand queries where 2+ of our URLs appear with 50+ total impressions. Brand queries
are excluded (sitelinks are normal). Pages sorted by position. Labels **(ours)**:
- `same_type_overlap`: two blog articles or two products: a likely true overlap
- `shop_hierarchy`: collection + product on one query: normal store structure
- `mixed_intent`: guide vs product and similar: often two intents served correctly
`top_page_impression_share` shows how dominant the leading URL is.

**Read it.** Many URLs per query can be legitimate. A comparison page and a review page can both
belong on "X vs Y". Never merge automatically.

**Fixes.** True overlap: merge into the stronger page and 301 the other, or differentiate the
angle clearly. Hierarchy: point the head term at the collection and the specific term at the
product through titles and internal links. Old page beating a newer one: update or redirect.

## 5. Mobile vs desktop gap
**Rule.** Pages with 50+ impressions on each device. Flag when CTR ratio (higher / lower) is 2x+
or the position gap is 5+.
- Mobile position much worse: check mobile rendering and Core Web Vitals.
- Mobile CTR much lower: check title truncation on mobile, speed, layout.
- Desktop worse: rare. Check whether desktop serves different content.

**Read it.** Local "near me" intent favours mobile. Video-heavy and configurator pages often
engage less on mobile.

**Fixes.** PageSpeed Insights on the mobile URL, tap targets and font size, shorter front-loaded
titles, theme work through `seo-onpage-audit`.

## 6. Dead pages
**Rule.** Pages with 10+ clicks last window and 0 now, sorted by lost clicks. The top 5 go into the
URL Inspection queue automatically.

**Inspection reading** (coverage state to meaning; `index_risk` 0-5):

| Coverage state | Status | Risk | Meaning |
|---|---|---|---|
| Submitted and indexed | indexed | 0 | Fine. Traffic moved to another URL or demand changed |
| Indexed, not submitted in sitemap | indexed_not_in_sitemap | 1 | Add to sitemap |
| Page with redirect | redirect | 2 | Check the target and chain |
| Alternate page with proper canonical | canonicalized | 2 | Often a collection-scoped product URL |
| Google chose different canonical than user | canonical_mismatch | 3 | Canonical signals conflict |
| Duplicate without user-selected canonical | duplicate_no_canonical | 3 | Declare a canonical |
| Crawled - currently not indexed | crawled_not_indexed | 4 | Quality or duplication |
| Discovered - currently not indexed | discovered_not_indexed | 4 | Crawl priority, weak internal links |
| Excluded by noindex / Blocked by robots.txt | noindex / robots_blocked | 5 | Remove if unintended |
| Soft 404 / Not found (404) / Server error | soft_404 / not_found_404 / server_error | 5 | Restore or 301 |
| URL is unknown to Google / not on Google | unknown / not_on_google | 5 | Removed, blocked or never linked |

A declared canonical that differs from Google's choice raises risk to 3. A robots disallow or a
failed fetch raises it to 4-5.

**Read it.** Removals may be deliberate (discontinued product, ended promotion, seasonal page).
Confirm with the user. A URL change looks like a death: look for the new URL in current rows.

**Fixes.** Accidental deletion: restore, or 301 to the closest live page (for a discontinued
product, usually its collection). Redirect loop: fix the chain. Unwanted noindex: remove it.
Deindexed: fix quality, then request indexing. Lost to another of our pages: may be fine.

## 7. Brand vs non-brand
**Rule.** Classify each query (whole-word match on our brand terms; the ambiguous-term rule for
"example kitchen"). Non-brand share = non-brand clicks / all clicks:
over 70% excellent, 50-70% healthy, 30-50% needs growth, under 30% critical. Report clicks,
impressions, CTR and impression-weighted position per bucket, plus the top 10 non-brand queries.

**Read it.** Our brands only. Maker A, Maker B and the like are other makers, so
their queries are non-brand demand. A low share means the store lives on people who already know
it.

**Fixes.** Grow non-brand coverage: `keyword-research` for gaps, collection copy, buying guides,
comparison pages, internal links toward money pages.

---

## Segment analyses **(ours, extending the base set)**
- **Country:** countries with 5%+ of impressions and CTR under 70% of the property average are
  flagged. First decide whether the store serves that market (shipping, currency). If not, ignore it.
- **Search type:** share of clicks and impressions for web, image, video, news and Discover.
  Image impressions with tiny CTR are normal for product photos.
- **Search appearance:** product snippets, merchant listings, review snippets and so on. With a
  previous-period pull, appearances that lost 25%+ of clicks are flagged. FAQ appearance is noted
  as retired and never recommended.
- **Trend:** month-over-month swings of 40%+ are flagged for a cause check (algorithm update,
  site change, tracking gap, season). With 13+ full months, a month-of-year index finds the peak
  and trough. "Seasonal" means peak/trough of 1.5x or more. Growth/decline labels use a ±10%
  change on the settled windows.
- **Sitemaps:** errors, warnings, pending state, and not downloaded by Google for 30+ days.

File: gsc-audit/references/analyses.md · Version 1.0 · November 2026
