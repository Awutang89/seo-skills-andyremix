# Editorial Heuristics (optional independent QA lens)

Ten editorial heuristics adapted from Nielsen's usability principles, scored on a 0–4 ordinal scale with
P0–P4 severity. This is a **different lens** from the Phase 7 gate — Phase 7 checks SEO/voice/E-E-A-T/GEO
compliance (mostly binary PASS/FAIL); these heuristics check whether the article *works for a human
reader*. Use it as an **optional pass** on flagship pillar pages or when an article passes Phase 7 but
still "reads flat." It is not a required gate. (Adapted from the `claude-blog` editorial-heuristics
framework, MIT.)

> **Avoid double-counting.** Several heuristics overlap existing Phase 7 rows. Where they do, the Phase 7
> row is authoritative — don't fail an article twice for the same defect. Overlaps flagged per row below.

---

## Scoring

Rate each heuristic **0–4**: 0 = absent/broken · 1 = poor · 2 = adequate · 3 = good · 4 = excellent.
Then tag the **worst** findings by severity so the fix list is prioritized:

| Severity | Meaning | Action |
|---|---|---|
| **P0** | Blocking — breaks comprehension or trust | Fix before publish |
| **P1** | Ship-blocker — materially weakens the page | Fix before publish |
| **P2** | Publish-then-iterate — real but not urgent | Log, fix in next refresh |
| **P3** | Cosmetic | Optional |
| **P4** | Excellent — a strength worth keeping | Note, don't touch |

Target: no heuristic below **2**, and zero P0/P1 open.

---

## The 10 heuristics

| # | Heuristic | What "good" looks like | Overlaps Phase 7? |
|---|---|---|---|
| 1 | **Visibility of intent** | Within ~5 seconds the reader knows the topic, the payoff, and roughly the depth. TL;DR box + answer-first intro do this. | Yes — TL;DR / first-200-words rows |
| 2 | **Heading–content match** | Each H2/H3 delivers exactly what it promises; no bait headings, no buried answers. | Partial — answer-first H2 row |
| 3 | **Reader control & exit** | Skimmers can navigate and leave with the answer: scannable headings, self-contained sections, tables. | Partial — GEO section-length rows |
| 4 | **Voice & standards consistency** | Terminology, tone, units, and formatting stay stable throughout (e.g. one consistent unit label, not the same unit written two ways). | No — net-new lens |
| 5 | **Fabricated-stat prevention** | Every numeric claim has a named, reachable source. | **Yes — E-E-A-T trust + "no fabricated stats."** Defer to Phase 7. |
| 6 | **Recognition over recall** | Reader never has to backtrack to understand the current section; terms defined where used. | Partial — overlaps cognitive-load forward-refs |
| 7 | **Skimmer vs deep-reader** | Both the 20-second scanner and the close reader get value (summary table + depth). | No — net-new lens |
| 8 | **Information-density discipline** | No padding; paragraphs ≤150 words; every sentence earns its place. | **Yes — paragraph ≤150w + Sentence Contribution Rule.** Defer to Phase 7. |
| 9 | **Failure-recovery copy** | Jargon is defined; abstract claims are backed by a concrete example or number. | Partial — overlaps cognitive-load jargon |
| 10 | **Sources & related docs** | Authoritative outbound sources, woven internal links, visible dates where relevant. | **Yes — internal-link + external-link rows.** Defer to Phase 7. |

The **net-new value** is in heuristics **#4 (consistency)** and **#7 (skimmer/deep-reader dual-mode)** —
the ones with no Phase 7 equivalent. If you only run two, run those. #1/#2/#3/#6/#9 are partial lenses
on existing rules; #5/#8/#10 are already enforced by Phase 7 (listed here for completeness only).

---

## Output format

```
EDITORIAL HEURISTICS — [article]
1 Intent 4 · 2 Heading-match 3 · 3 Control 3 · 4 Consistency 2 · 5 Stats 4
6 Recognition 3 · 7 Skim/deep 2 · 8 Density 3 · 9 Recovery 3 · 10 Sources 4

P1: #7 — no summary table; a skimmer can't get the verdict without reading 600 words. Add a quick-answer
    table after the intro.
P2: #4 — units drift between "[unit]" and "[unit variant]" in the technical section; standardize on "[unit]".
Strengths (P4): #1 intent, #5 sourcing, #10 sources.
```

## How this connects
- `skills/seo-content/SKILL.md` Phase 7 — the authoritative gate; heuristics #5/#8/#10 live there.
- `references/cognitive-load.md` — heuristics #6/#9 overlap the recall/jargon load signals.
- This lens is **optional** — invoke on flagship content, not every article.
