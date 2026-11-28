# GSC lane result contract (v1.0)

`gsc-lane.json` is the file a future site audit orchestrator reads as `evidence/gsc.json`.
Scripts own evidence, scoring and validation. The lane never writes a verdict or flagship plays:
the orchestrator does that.

## Shared lane fields (same shape as every lane)

| Field | Type | Meaning |
|---|---|---|
| `lane` | `"gsc"` | |
| `status` | `complete` \| `partial` \| `not_run` | complete = current + previous rows; partial = current only; not_run = no current rows or no access |
| `confidence` | 0-1 | live 0.85, manual 0.70, mixed 0.75, fixture 0.55; -0.15 if the row cap was hit unpaginated; -0.10 without comparison; capped at 0.40 under 100 impressions |
| `summary` | string | one-line counts |
| `evidence[]` | objects | `{id: "gsc-ev-N", claim, proof_type: "gsc_row", subtype?: "url_inspection", source_url, snippet, observed_value, expected_value}` |
| `recommendations[]` | objects | see below |
| `why_not_more` | string | what was not pulled or inspected, and why |
| `inputs_required[]` / `inputs_available[]` | strings | raw kinds |
| `source_type` | `live` \| `fixture` \| `manual` \| `mixed` \| `not_run` | |
| `client_summary` | string | client-safe line |
| `operator_notes[]` | strings | archive result, config notes |
| `blocking_limitations[]` | strings | reasons from open gates |
| `visuals{}` | object | chart-ready series (monthly trend, top URLs, device, search types, country table, appearances) |

## Gates and conflicts
- `dependency_gates[]`: `{id, status: open|cleared|not_applicable, blocks[], reason, rerun_requirement}`.
  - not_run: `missing-gsc`, blocks `traffic_sizing`, `ctr_upside`, `decay_confidence`.
  - partial: `missing-gsc` blocking only what is missing (normally `decay_confidence`).
  - Any open gate means sized numbers elsewhere carry "GSC-gated directional estimate". While
    `traffic_sizing` is blocked, no dollar figure may appear as a standalone forecast.
- `evidence_conflicts[]`: `{source, claim, status: "candidate"}`. Empty from this lane. The
  orchestrator fills it when GSC and DataForSEO disagree (e.g. DataForSEO says we rank #3 for a
  query GSC shows at position 14).

## GSC extension fields
| Field | Content |
|---|---|
| `contract_version`, `property`, `brand`, `generated_at` | |
| `date_ranges` | the windows from config (current, previous, yoy, sixteen_months) |
| `freshness` | `latest_available_date`, `settled_end`, `lag_days`, `provisional_dates_excluded[]` |
| `segments` | `devices[]`, `countries[]` (with `impression_share`), `geo_opportunities[]`, `search_types[]`, `search_appearances[]` |
| `page_query_map[]` | `url_key, page, path, query, query_class, clicks, impressions, ctr, position, source: "gsc", confidence: 0.9` |
| `trend_summary` | windows, `change_vs_previous`, `change_yoy`, labels, `monthly[]`, `anomalies[]`, `seasonality`, `coverage_months`, `beyond_16_months` |
| `ctr_curve` | `mode_used`, `curve{1..20}`, `source_by_position`, `calibration_stats` |
| `ctr_gaps[]`, `decay_candidates[]`, `dead_pages[]`, `striking_distance[]`, `striking_distance_by_page[]`, `cannibalization[]`, `device_gaps[]`, `brand_nonbrand{}` | analysis outputs |
| `url_briefs[]` | one per URL (below) |
| `inspections[]` | interpreted inspection results with `index_status`, `index_risk_score`, `deliberate_possible` |
| `inspection_queue[]` | URLs still to inspect, with reasons |
| `sitemaps[]` | per sitemap: counts, flags, `health` |
| `data_limitations[]` | lag, row cap, average-position and anonymised-query caveats, and anything else |
| `exploration_log[]` | per raw kind: `{surface, status complete|not_available, calls_used, rows_returned, reason, why_not_more}` |
| `handoffs` | `seo_page_diagnosis[]`, `seo_content_refresh[]` (also written to `handoff/`) |

## URL brief
`url, url_key, path, page_type (home|product|product_in_collection|collection|blog_article|blog_index|page|cart|search|other), high_value, metrics, previous_metrics, yoy_metrics, primary_queries[<=5], query_count, position_trend, signals[{type, detail}], scores{ctr_upside, traffic_loss, striking_distance, striking_click_gain, index_risk, device_gap}, trend_label, recommended_action, action_summary, suggested_route, suggested_owner, refresh_outcome_hint, register_match, inspection, proof_level (confirmed|directional), confidence, priority_score, blocking_index_issue, dependencies[]`

`proof_level` is `confirmed` only for live data with 100+ impressions.

## Recommendation
`id, lane, title, why_it_matters, evidence[], evidence_refs[], affected_urls[], impact 1-10, confidence 1-10, effort 1-10, type (quick_win|strategic|research), cluster (content_growth|technical_health|data_trust), suggested_route, suggested_owner (seo|content|catalog|theme-dev), decision_status (ready|validation_required|directional), proof_level, report_visibility (client|operator), directional_click_gain, sizing_label, acceptance_criteria[]`

The top 10 non-monitor URL briefs become recommendations, plus lane-level items for a weak
non-brand share, sitemap problems and country gaps. For not_run there is one `connect-gsc`
recommendation (own site: setup; client: request access).

File: gsc-audit/references/lane-contract.md · Version 1.0 · November 2026
