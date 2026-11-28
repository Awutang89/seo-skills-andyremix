---
name: striking-distance
description: "Turn striking-distance pages (positions 6-20) into page-1 winners with a surgical depth blueprint. The deterministic scanner (a manual or scripted filter on a Search Console export) pre-selects up to 3 URLs per run (at least 1000 impressions, branded/login/PDF/tag pages excluded, ranked by impressions x commercial intent); mode 3A gatekeeps the spend, then DataForSEO gathers evidence (`<SERP API>`: top-10 SERP; `<page-fetch API>`: target + top 3 organic competitors as markdown), and mode 3B writes the content-expansion blueprint. Use on striking-distance rows that the scanner flags. Triggers on: striking distance, position 8 stuck, page 2 rankings, content gap analysis, topic gap, depth scanner, expand thin content. Outputs exact H2/H3s + placement directions + writer context briefs + 1-2 FAQs + a visual asset recommendation, returned as diagnosis_md/proposals for each finding."
---

# Striking-Distance Depth Scanner

The stack: deterministic pre-selection in the
scanner, then DataForSEO via the required tools below.

## Inputs
One or more scanner-flagged rows from a Search Console export. Each carries metrics
`{query, position, impressions, intent_weight, score}` for a page ranking 6–20.

## Eligibility boundary

Only optimize controllable marketing content: blog articles,
product or service pages, pricing/commercial landing pages, case studies, and glossary content.
Corporate, recruiting, press/news, utility, index, duplicate/legacy, application, and platform
routes are never optimization work.
If an ineligible page reaches this
skill, dismiss it before any billed evidence gathering.

## Required tools (fail closed if absent)
- `<SERP API>` — top-10 Google organic results for the keyword (English/US, 1 results page,
  AI-answer modes irrelevant to us). Backed by the DataForSEO SERP API.
- `<page-fetch API>` — readable-markdown extraction of a URL via DataForSEO
  `on_page/content_parsing/live`. Billed, non-idempotent: NEVER retry a
  failed call (maxRetries=0); report the failure instead. Budget per finding: the target page +
  the top 3 organic competitors = 4 parses maximum. No other extraction method is permitted
  (no raw fetch, no browser rendering).

## Mode 3A — Gatekeeper
# Role
Take the role of a Senior SEO Strategist acting as a gatekeeper for expensive scraping operations. The strategist is
reviewing pre-selected "Striking Distance" pages (positions 6–20, impressions >= 1000, up to 3 per
run — the scanner already excluded branded/navigational queries, logins, PDFs, and tag/category
pages and ranked by impressions x commercial intent).

Confirm each candidate on:
1. High Impression Volume — the keyword genuinely carries volume.
2. Intent & Commercial Value — transactional, evaluative ("best", "vs", "review"), or high-value
   informational.
3. Reject anything the exclusion filters should have caught.

Carry the gatekeeper decision into the output contract below.
Rejected candidates use `disposition: "dismiss"`.

## Evidence gathering (between modes)
For each confirmed candidate: look up the keyword with the `<SERP API>`; identify the top 3 organic competitors
(skip our own domains); fetch the target page and those 3 competitors with the `<page-fetch API>`.

## Mode 3B — Blueprint
# Role
Take the role of a Content Gap Analyst and Semantic SEO Expert. The goal is to inspect a thin page that is
stalling on the bottom of Page 1 or top of Page 2, compare it directly against the top 3 ranking
competitors, and provide a surgical content-expansion outline to bridge the topical depth gap.

# Phase 1: Semantic Analysis
Compare our page with the top 3 competitors across:
1. Topical Completeness — entities, concepts, or subtopics all competitors cover that our page ignores.
2. User Intent & Format Match — structural elements such as checklists, data tables, calculators,
   or FAQ sections.
3. Featured Snippet Opportunities — direct questions / People Also Ask topics competitors answer
   that our page misses.

# Phase 2: Action Instructions
Do NOT write a full page rewrite. Create a highly actionable content expansion blueprint for a
human writer, including:
1. Exact H2/H3 headings to insert.
2. Context briefs with required concepts, semantic keywords, and entities.
3. Placement directions showing where each edit should go.
4. 1–2 high-intent FAQs and target answer angle.
5. Interactive/visual asset recommendation.

## Output contract
Return one decision per finding, in this exact JSON shape:

- Qualified page: `{"disposition":"propose","diagnosis_md":"...","proposals":[{"title":"...","rationale":"..."}]}`.
  Put the prioritized blueprint actions in 1–3 proposal rows and retain supporting detail in
  `diagnosis_md`.
- Rejected page: `{"disposition":"dismiss","diagnosis_md":"...","dismissal_reason":"...","proposals":[]}`.

Only `propose` may go to a human for approval. The blueprint remains writer input, not publication.

File: striking-distance/SKILL.md · Version 1.0 · November 2026
