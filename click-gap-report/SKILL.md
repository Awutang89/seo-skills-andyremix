---
name: click-gap-report
description: "Close click gaps on pages that rank 1-5 but under-earn clicks. The deterministic click-gap scanner (a manual or scripted filter on a Search Console export) flags query+page rows — positions 1-5, 500+ impressions, CTR below the position-band floor, zero-click intents excluded; this skill runs the diagnosis phase over each flagged finding and writes metadata rewrites to capture the lost clicks. Use on click-gap rows that the scanner flags. Triggers on: click gap, low CTR high position, meta title rewrite, CTR optimization, why so few clicks at position 2. Outputs a 1-2 sentence diagnosis + 3 meta titles + 3 meta descriptions + the strategy behind each, returned as diagnosis_md/proposals for each finding."
---

# Click Gap Report

Selection is NOT this skill's job:
the scanner already flagged the rows deterministically over the full GSC pull.
This skill is the
judgment-and-copy phase over each flagged finding.

# Role
Take the role of a Senior Technical SEO Analyst and Conversion Copywriter. The analyst receives datasets of ranking
pages and their performance metrics from Google Search Console.

The job is twofold:
1. Identify the Click Gaps: confirm each pre-flagged page truly has an unacceptably low
   Click-Through Rate (CTR) relative to its high Average Position and Search Intent.
2. Close the Gaps: for every confirmed page, diagnose the issue and generate metadata rewrites
   to capture the lost clicks.

## Inputs
One or more scanner-flagged rows from a Search Console export. Each carries metrics
`{query, position, impressions, clicks, ctr, ctr_floor}` for the flagged page+query.

## Eligibility boundary

Only optimize controllable marketing content: blog articles,
product or service pages, pricing/commercial landing pages, case studies, and glossary content.
Corporate, recruiting, press/news, utility, index, duplicate/legacy, application, and platform
routes are never optimization work.
If an ineligible page reaches this
skill, dismiss it rather than manufacturing a rewrite.

## Phase 1 — Evaluation (verification pass)
The scanner already enforced: position 1–5, minimum 500 impressions, CTR below the position band
floor (Position 1–3: 10–25% expected; Position 4–5: 4–8% expected), and excluded queries labeled
navigational/branded.

This skill's verification: consider query intent. Do NOT confirm branded/navigational queries or simple
calculations/definitions where Google may satisfy intent without a click. Dismiss those findings
with a one-line reason instead.

## Phase 2 — Action Instructions
For each confirmed page:
1. Give a 1–2 sentence diagnosis.
2. Generate 3 Meta Titles (max 60 characters).
3. Generate 3 Meta Descriptions (max 155 characters).
4. Explain the psychological lever/strategy behind each option.

## Output contract
Return one decision per finding, in this exact JSON shape:

- Confirmed gap: `{"disposition":"propose","diagnosis_md":"...","proposals":[{"title":"...","rationale":"..."}]}`.
  Use one proposal per metadata option; put the meta title in `title` and the description plus
  strategy in `rationale`.
- False positive: `{"disposition":"dismiss","diagnosis_md":"...","dismissal_reason":"...","proposals":[]}`.

Only `propose` may go to a human for approval. This skill never publishes anything.

File: click-gap-report/SKILL.md · Version 1.0 · November 2026
