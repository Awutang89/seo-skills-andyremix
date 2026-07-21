# Cognitive-Load Assessment (long-form sections)

A section can be accurate, sourced, and on-keyword and still lose the reader — because it asks them to
hold too much in working memory at once. Human working memory handles ~4 chunks. When a single ~100-word
stretch piles on new entities, raw numbers, undefined jargon, forward references, and deeply nested
clauses, comprehension collapses and the reader bounces. This check catches that **before** publish.

It is a *pacing* lens, not a "cut the data" lens. Our brand voice is numbers-first — dense figures are a
feature. The fix for an overloaded section is almost never "delete the stats"; it's **break it up**:
add a table/chart, split into sub-points, define the term on first use, or move a tangent out. (Adapted
from the `claude-blog` cognitive-load model, MIT.)

---

## When to run it

Only on long, dense pieces — it's wasted effort on short articles. Apply to:
- Pillar guides and any article **>2,000 words**
- Technical how-to / tutorial sections (setup, sizing, installation, configuration)
- Data-research / cost-analysis sections with stacked figures (TCO tables, payback math)

Spot-check the **2–3 densest sections**, not every paragraph. The densest section is usually a sizing
calculation, a spec comparison, or a standards/regulatory passage.

---

## Thresholds (per ~100 words of body prose)

Measure within a single section's prose (skip tables, lists, and code — those are *relief* from load,
not load). An optional content-metrics helper (tallies burstiness / windowed TTR / structural tics) can
tally these, or estimate by eye on the densest paragraph.

| Signal | Healthy | Watch | Overloaded | Notes |
|---|---|---|---|---|
| **Named entities** (brands, models, standards, place/part names) | 1–3 | 4–6 | **7+** | [Product] content is entity-heavy; 4–6 is normal here — only 7+ in one breath is a problem. |
| **Numeric claims** (figures, %, ranges, prices) | 1–3 | 4–5 | **6+** | We're numbers-first, so expect the high end. 6+ in 100 words = move them into a table. |
| **New jargon** (term used before it's defined) | 0–1 | 2–3 | **4+** | "[jargon term]," "[spec at a condition]," "[option]" — define on first use, then it's free. |
| **Forward references** ("as we'll see below," "more on this later") | 0 | 1 | **2+** | Each one parks an open loop in the reader's head. Prefer answering now or linking. |
| **Clause nesting** (avg subordinate-clause depth per sentence) | <1.5 | 1.5–2.5 | **>2.5** | Deeply nested sentences are the #1 readability killer; split them. |

**Verdict:** a section is **OVERLOADED if ≥2 signals hit the Overloaded column.** One signal alone is a
watch, not a fail.

---

## Fixes (in order of preference)

1. **Add a visual** — a table, chart, or spec list absorbs numeric/entity density and doubles as a GEO
   multi-modal asset (ties to `geo-checklist.md`). This is the highest-leverage fix for our content.
2. **Split the section** — one idea per sub-point / H3. Dense ≠ long; dense = too much per breath.
3. **Define-on-first-use** — introduce each term once, plainly, before leaning on it.
4. **Unnest sentences** — break >2.5-depth sentences into two. (Also lowers AI-slop "three-clause"
   structural tics — see `content-humanizer/references/ai-tells-checklist.md`.)
5. **Close or cut forward references** — answer it here, link to the deep-dive, or drop the promise.

Do **not** fix overload by deleting real figures or named sources — that trades a pacing problem for a
weaker E-E-A-T/information-gain signal.

---

## QA wiring

In the Phase 7 gate, add **one conditional row** (only for articles >2,000 words):

`| Cognitive load: no section is OVERLOADED (≥2 signals at threshold) — densest 2–3 sections checked | PASS / FAIL / N/A |`

A FAIL names the section and which signals tripped, then applies the fix ladder above. For articles
≤2,000 words, mark **N/A** — don't pad the gate.

## How this connects
- `skills/seo-content/SKILL.md` Phase 7 — the conditional QA row lives here.
- `content-humanizer/references/ai-tells-checklist.md` — clause-nesting overlaps the "three-clause
  sentence" structural tic; fixing one usually fixes the other.
- `references/geo-checklist.md` — the preferred fix (add a visual) is also a GEO multi-modal win.
- An optional content-metrics helper — tallies these counts.
