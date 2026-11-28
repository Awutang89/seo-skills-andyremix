# Stage 5: Delivering the audit

Deliver in this order: (1) a short summary in chat, (2) ask if the user wants the full write-up,
(3) offer CSV for any table. Save the full write-up as `<run>\audit.md`. Every number comes from
`gsc-lane.json`; nothing is estimated in prose.

## Summary (chat)
```
GSC audit: <property>  |  <current window> vs <previous window>  |  status <complete/partial>, confidence <x>
- Clicks <n> (<+/-%> vs previous, <+/-%> YoY), impressions <n>, trend <label>
- <n> CTR gaps (directional upside ~<n> clicks per 28 days)
- <n> decaying pages (<n> clicks lost), <n> dead pages
- <n> striking-distance pairs on <n> pages
- <n> overlapping queries (<n> same-type)
- <n> device gaps; non-brand share <x%> (<health>)
- Index issues: <n> of <n> inspected; sitemaps <ok/issues>
Top 10 URLs to work first: <path - action> ...
Caveats: data through <settled_end> (last 3 days excluded); <row cap note>; average position is not a rank.
```

## Full write-up (`audit.md`)
```
# GSC audit: <property>
Generated <date> | Period <current> vs <previous> (YoY <yoy>) | Curve: <default|calibrated>

## Executive summary
## Top 10 URLs to work first        (from url_briefs; action, owner, route, confidence)
## Trend                            (16-month monthly clicks/impressions, anomalies, seasonality; cards: current / previous / YoY)
## 1. CTR gaps                      | Page | Position | Impressions | Actual CTR | Expected CTR | Gap | Upside |
## 2. Content decay                 | Page | Old clicks | New clicks | Change | Old pos | New pos | Diagnosis | Seasonal |
## 3. Striking distance             | Query | Page | Position | Impressions | Clicks | CTR |  (grouped by page)
## 4. Overlapping queries           per query: pages by position + overlap label + recommendation
## 5. Mobile vs desktop             | Page | Desktop CTR | Mobile CTR | Ratio | Desktop pos | Mobile pos | Gap | Likely issue |
## 6. Dead pages + inspection       | Page | Prev clicks | Prev impressions | Index status | Last crawl | Diagnosis |
## 7. Brand vs non-brand            bucket table + ratio + health + top 10 non-brand queries
## Segments                         search type bars, country heat table, appearance table
## Sitemaps                         health card
## Data limitations                 (verbatim from data_limitations)
```

Visual suggestions when the audit goes to HTML (orchestrator or artifact): 16-month line chart
with anomaly notes, current/previous/YoY cards, page opportunity matrix (impressions x action),
CTR gap table, stacked search-type bars, country heat table, device gap table, appearance table,
index status chips, sitemap card.

## Labels
- Upside numbers: "GSC-based directional estimate, clicks per 28 days". Never revenue.
- If the lane is partial or any gate is open: "GSC-gated directional estimate".
- Third-party figures shown next to GSC ones: "DataForSEO estimate (not first-party GSC data),
  <locale>, <device>, <date>".

## CSV export
Header row, then one row per item. Example (CTR gaps):
```csv
page,position,impressions,actual_ctr,expected_ctr,gap,potential_clicks
/products/sample-product-a,3.0,2000,2.00%,10.00%,8.00%,160
```

## Before/after loop
The run folder is the baseline. After changes ship, wait for a settled window (28+ days, ending 3
days before the re-pull), run a new audit, and compare the affected URLs' briefs. That comparison
is the acceptance test named in each recommendation.

File: gsc-audit/references/output-format.md · Version 1.0 · November 2026
