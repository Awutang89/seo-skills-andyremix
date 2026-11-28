---
name: content-decay-audit
description: "Catch quiet traffic decay before rankings collapse. The deterministic decay scanner (a manual or scripted filter on a Search Console export) compares each page's last 14 days against days 15-28 and flags pages whose clicks fell 15%+ while average position stayed stable (drop under 2) with 100+ historical clicks; this skill diagnoses each flagged page across the four decay vectors and prescribes recovery actions. Use on decay rows that the scanner flags. Triggers on: content decay, traffic dropping but rankings stable, quiet decline, page losing clicks, refresh audit. Outputs a diagnostic summary + freshness/UX/internal-linking/cannibalization recovery actions returned as diagnosis_md/proposals for each finding."
---

# Content Decay Audit

Phase 0 (data alignment) and
Phase 1 (evaluation) run deterministically in the scanner over the full GSC
pull — URL-by-URL alignment with missing periods treated as 0. This skill is the forensic
diagnosis phase over each flagged finding.

# Role
Take the role of an Advanced SEO Forensics Analyst. The task is to examine pages where recent 14-day
performance fell against the previous 14-day period — "Traffic Decay": a quiet, steady loss of
clicks and engagement that happens before ranking drops become catastrophic.

## Inputs
One or more scanner-flagged rows from a Search Console export. Each carries metrics
`{clicks_current, clicks_prior, delta_pct, position_current, position_prior}` for the flagged page.

## Eligibility boundary

Only optimize controllable marketing content: blog articles,
product or service pages, pricing/commercial landing pages, case studies, and glossary content.
Corporate, recruiting, press/news, utility, index, duplicate/legacy, application, and platform
routes are never optimization work.
If an ineligible page reaches this
skill, dismiss it rather than manufacturing recovery work.

## Phase 1 — Evaluation rules (already enforced by the scanner)
- Clicks dropped by 15% or more.
- Average Position remained relatively stable (drop of less than 2 spots, or unchanged).
- If position dropped by 5+ spots, it is NOT quiet decay — the scanner never flags those.
- Historical period had at least 100 clicks.
This skill's verification: sanity-check for seasonality or known events (check any annotations for a
send/publish/experiment near the inflection). Mark explainable declines `dismissed` with the reason.

## Phase 2 — Diagnose Four Decay Vectors
For each confirmed page, assess and rank the likely vectors:
1. Freshness & Temporal Decay — dated content, stale year references, outdated screenshots/stats.
2. Intent Shift / Competitor Leapfrogging — SERP composition changed or a competitor now answers
   the intent better (use the `<SERP API>` for the page's top query when available).
3. Cannibalization / Internal Conflicts — another of our pages now competes for the same queries
   (check the article map from `keyword-database-article-map`: two rows should never share a primary keyword — if they do in effect,
   say so).
4. On-Page Experience / Friction — slow loads, intrusive elements, buried answers.

## Output contract
Return one decision per finding, in this exact JSON shape:

- Confirmed decay: `{"disposition":"propose","diagnosis_md":"...","proposals":[{"title":"...","rationale":"..."}]}`.
- Explainable or ineligible decline: `{"disposition":"dismiss","diagnosis_md":"...","dismissal_reason":"...","proposals":[]}`.

Only `propose` may go to a human for approval. Recovery execution remains a human decision.

File: content-decay-audit/SKILL.md · Version 1.0 · November 2026
