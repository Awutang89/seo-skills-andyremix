---
name: seo-page-diagnosis
description: "Diagnose why a published article underperforms in search — before rewriting it. Runs a SERP-backwards analysis to detect page-type mismatch, scores the gap across 7 dimensions, and outputs a prioritized refresh action list. Use when an existing article won't rank, lost rankings, or you're deciding whether to refresh it. Triggers on: why isn't this ranking, page not ranking, diagnose this article, SXO, page-type mismatch, content refresh decision, why did we drop rankings. Outputs a diagnosis + ranked fixes that feed seo-content (refresh) or comparison-pages."
---

# SEO Page Diagnosis (SXO)

A page can be technically perfect and still never rank — because it's the **wrong type of page** for
the query. Before you rewrite an underperforming article on instinct, diagnose it: read what Google
actually rewards for that keyword, find the gap, and fix the specific thing. This skill answers "why
isn't this ranking?" with evidence instead of a guess, then hands a concrete refresh list to
`seo-content`.

It is diagnostic, not generative. It does not rewrite the article — it tells you what to change.

---

## Inputs
1. The article — slug or URL (read the local `.md`/`.html` in `your-project/Written Articles/`,
   or WebFetch the live page).
2. Target keyword + secondaries — from `KEYWORD-REGISTER.csv`.
3. (Optional) GSC/rank signal — what position it's stuck at, or that it dropped.

---

## Step 1 — Read our page
Extract: page type, H1/H2 structure, word count, schema present, media (images/tables/charts), CTAs,
TL;DR/answer-first presence, last-updated date. (Reuse the seo-content Phase 1 lens — you already know
this article's keyword targets from the register.)

## Step 2 — SERP-backwards analysis
Pull the top 10 organic results for the target keyword (WebFetch incognito, or DataForSEO). For each,
record: page type, format (guide/listicle/comparison/product/tool/definition), approx word count,
schema signals, media richness, domain tier. Note SERP features present: featured snippet, PAA, AI
Overview, shopping/product pack, video.

**Page-type consensus** (the key signal):
- **>60%** of the top 10 are the same page type → **strong consensus** — you must match it.
- **40–60%** → **mixed** — two formats can rank; pick the stronger fit.
- **<40%** → **fragmented** — intent is unsettled; depth/authority decide.

See `references/page-type-taxonomy.md` for the type definitions and signals.

## Step 3 — Page-type mismatch detection (highest-value check)
Compare our page type to the SERP consensus. Severity:

| Our type vs SERP consensus | Severity | Meaning |
|---|---|---|
| Matches the >60% consensus type | ALIGNED | Type is not the problem — look at Steps 5–6 |
| Differs, but consensus is mixed (40–60%) | WARNING | A ranking format exists; we may be the weaker one |
| Differs from a strong (>60%) consensus | **CRITICAL** | Wrong page type — no amount of on-page polish fixes this; reformat or re-scope |

Example: a 1,500-word informational guide targeting a keyword whose top 10 are 8 product/category
pages = CRITICAL mismatch. The fix is structural (build/point at a collection or comparison), not a
rewrite of the guide.

## Step 4 — Derive the user stories
From PAA questions, featured-snippet format, related searches, and ad copy themes, write 2–4 user
stories: "As a [persona], I want to [goal], because [driver], but I'm blocked by [barrier]." These
tell you what the ranking pages satisfy that ours doesn't.

## Step 5 — Gap scorecard (0–100)
Score our page against the SERP winners on seven dimensions:

| Dimension | Max | What it measures |
|---|---|---|
| Page type fit | 15 | Match to SERP consensus (from Step 3) |
| Content depth | 15 | Coverage vs winners (subtopics, word count, PAA answered) |
| UX / structure | 15 | Scannability, tables, answer-first, no walls of text |
| Schema | 15 | Right types present and valid (see seo-schema) |
| Media richness | 15 | Images/charts/tables vs winners; multi-modal for GEO |
| Authority / sourcing | 15 | External authoritative citations, E-E-A-T signals |
| Freshness | 10 | Last-updated recency vs winners |
| **Total** | **100** | |

Below ~70 means the page has real, fixable gaps. The lowest-scoring dimension is the priority.

## Step 6 — Quick persona check (lightweight)
Pick the 2–3 personas implied by the SERP and rate the page on Relevance / Clarity / Trust / Action
(each weak/ok/strong). The weakest dimension on the most important persona is usually the conversion
or trust fix. (Keep this fast — it's a sanity check, not a full audit.)

## Step 7 — Output: prioritized refresh action list
Produce a ranked, concrete list — each item names the dimension, the gap, and the fix, e.g.:

```
DIAGNOSIS — [article] for "[keyword]" (stuck at #14)
Page-type: ALIGNED (informational guide matches 70% consensus)
Gap score: 58/100 — weakest: Authority/sourcing (4/15), Media (6/15)

FIXES (priority order):
1. [Authority] Add 3–4 external authoritative citations (gov/standards/manufacturer) — currently zero.
2. [Media] Add the [key spec] comparison chart from Phase 1.5 next to the requirements section (GEO multi-modal).
3. [Depth] Answer 2 unanswered PAAs: "[Q1]", "[Q2]".
4. [Freshness] Add a real last-updated date; refresh the 2023 price figures.
HANDOFF: route to seo-content (refresh) — or comparison-pages if reformatting to a roundup.
```

If Step 3 returned **CRITICAL**, say so first and loudly: the fix is to change the page type (or build
the right page type), not to polish the existing one.

---

## How this connects
- **`skills/seo-content/SKILL.md`** — receives the refresh action list; the GEO/E-E-A-T/uniqueness QA
  rows define many of the gaps this skill scores. For an Authority/Freshness gap, route specifically
  to its outbound-link audit (`seo-content/references/link-refresh.md`) — swap stale/secondary
  citations for fresher primary sources, not just "add a date."
- **`skills/comparison-pages/SKILL.md`** — the handoff when a CRITICAL mismatch means reformatting to
  a comparison/roundup.
- **`skills/seo-schema/SKILL.md`** — for the Schema dimension fixes.
- **`skills/keyword-database-article-map/SKILL.md`** — if the diagnosis is actually cannibalization
  (two of our pages competing), resolve it there with the SERP-overlap test, not by refreshing one.

## Reference
- `references/page-type-taxonomy.md` — page-type definitions, SERP signals, and the mismatch matrix.
