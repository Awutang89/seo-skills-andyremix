# Stage 2: Data collection

Pull through the `gsc` MCP server and save every response as JSON in `<run>\raw\` **before**
analysing it. The raw file is the record: the analyzer archives it, and the report cites it.

## Tool names: check first
The server is expected to expose tools like `list_properties`, `get_advanced_search_analytics`,
`compare_search_periods`, `inspect_url_enhanced` and a sitemap listing tool, plus a capabilities
tool. Names and parameters vary between server versions, so **call the capabilities tool (or read
the tool list) at the start of every run** and adapt the calls below. Known quirk: in some
versions `inspect_url_enhanced` takes `page_url`, not `url`.

## Windows
Get the dates first:
```powershell
python "gsc-audit/scripts/gsc_analyzer.py" periods --days 28
```

## Pull plan

| # | File (kind) | Dimensions | Window | Search type | Needed for |
|---|---|---|---|---|---|
| 1 | `current_page.json` | page | current | web | CTR gaps, decay, dead pages, briefs |
| 2 | `previous_page.json` | page | previous | web | decay, dead pages |
| 3 | `yoy_page.json` | page | yoy | web | seasonal check on decay |
| 4 | `current_query_page.json` | query, page | current | web | page-query map, striking distance, cannibalization, curve calibration |
| 5 | `current_query.json` | query | current | web | brand vs non-brand (optional; otherwise derived from #4) |
| 6 | `daily.json` | date | sixteen_months | web | trend, YoY, seasonality |
| 7 | `page_device.json` | page, device | current | web | mobile vs desktop |
| 8 | `page_country.json` | page, country | current | web | country segment |
| 9 | `search_type_totals.json` | none (one call per type) | current | web, image, video, news, discover | search type split |
| 10 | `search_appearance.json` | searchAppearance | current | web | appearance performance |
| 11 | `previous_search_appearance.json` | searchAppearance | previous | web | appearance losses (optional) |
| 12 | `page_date.json` | page, date | sixteen_months, top pages only | web | per-URL position history (optional) |
| 13 | `sitemaps.json` | n/a | n/a | n/a | sitemap health |
| 14 | `sitemap_urls.json` | n/a | n/a | n/a | "earning traffic but not in sitemap" (optional: URLs parsed from the sitemap files) |
| 15 | `inspections.json` | n/a | n/a | n/a | Stage 4 only |

Minimum for a **complete** lane: #1 (or #4) plus #2. Without #2 the lane is **partial** and
decay is blocked. Without #1 and #4 the lane is **not_run**. Pull sort order: impressions
descending. `compare_search_periods` can replace #1 and #2 if it returns both periods per page;
split its output into the two files.

For a run limited to some analyses, pull only what they need (table column 6).

## File format
```json
{
  "meta": {
    "kind": "current_query_page",
    "dimensions": ["query", "page"],
    "start_date": "2026-08-28",
    "end_date": "2026-09-24",
    "search_type": "web",
    "row_limit": 25000,
    "pages_fetched": 2,
    "row_cap_hit": false,
    "paginated_to_end": true,
    "pulled_at": "2026-09-27"
  },
  "rows": [
    {"keys": ["cedar gazebo", "https://example-outdoor.com/products/cedar-gazebo"], "clicks": 30, "impressions": 1500, "ctr": 0.02, "position": 3.0}
  ]
}
```
- `rows` may use the API shape (`keys` matched to `meta.dimensions`) or flat objects
  (`{"query": ..., "page": ..., "clicks": ...}`). CTR may be a fraction or a percent.
- If the MCP answers with a text table, convert it to rows faithfully. Never round, fill in or
  guess values.
- Several files of one kind are merged: name them `<kind>__p1.json`, `<kind>__p2.json`. The part
  after `__` is ignored when choosing the kind.
- `search_type_totals` rows: `{"search_type": "image", "clicks": .., "impressions": .., "position": ..}`.
- `inspections` rows: the inspection result per URL. Keep `url`, `verdict`, `coverageState`,
  `indexingState`, `robotsTxtState`, `pageFetchState`, `googleCanonical`, `userCanonical`,
  `lastCrawlTime` (camelCase or snake_case both work).
- `sitemaps` rows: `path`, `lastSubmitted`, `lastDownloaded`, `isPending`, `errors`, `warnings`,
  `contents[{type, submitted, indexed}]`.

## Pagination (25,000-row cap)
Request `row_limit: 25000`, `start_row: 0`. If exactly 25,000 rows return, request
`start_row: 25000`, then 50,000, and so on, until a page returns fewer. Save each page as
`<kind>__pN.json`, or merge them into one file with `pages_fetched` and `paginated_to_end: true`.
If a pull stops early (budget, time), set `row_cap_hit: true`: the lane lowers confidence and records
the limit. For standard depth on these stores, one or two pages of query/page rows are normal.

## Depth
- **quick:** #1, #2, #4, #6 (28 days only), no inspections.
- **standard (default):** all of #1-#10 and #13, up to 10 inspections.
- **deep:** add #11, #12 (top 50 pages), #14, a 90-day current window as a second run, up to
  25 inspections. Check with the user before running it.

## Caveats to carry into the report
- The last 2-3 days are provisional. The analyzer drops them from the trend windows, and the
  archive keeps re-pulls with the newest pull winning.
- Query-grain totals will not equal page-grain totals, because anonymised queries are withheld.
- Average position is an impression-weighted average, not a rank.
- Detailed groupings (query+page+country) lose more rows than coarse ones. Prefer coarse
  groupings and drill down only on pages that deserve it.
- Every file stays in the run folder and the archive. History past 16 months exists **only**
  because of this archive, so never delete it during cleanups.

File: gsc-audit/references/data-collection.md · Version 1.0 · November 2026
