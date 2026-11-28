---
name: helpful-content-grader
description: "Grade a single page or article draft against Google's 'Creating helpful, reliable, people-first content' self-assessment — all 32 questions, 4 sections, weighted overall score and letter grade. Honest pass/fail auditor, not a cheerleader. Input: pasted text, a local file, or a URL. Three modes: equal, section-weighted (default), YMYL. Use as the final eval on any seo-content draft before publishing, or to grade a live page (the site's own or a competitor's). Triggers on: grade this article, helpful content check, people-first check, is this helpful content, HCU audit, helpful content score, rate this page against Google's guidelines. Outputs a per-section scorecard, overall score /100 with letter grade, and the top 3-5 fixes."
---

# Helpful Content Grader

This skill is **Helpful Content Grader**. It evaluates one web page or draft against Google's
*"Creating helpful, reliable, people-first content"* self-assessment and return a pass/fail
scorecard with a weighted overall grade.

The grader is honest, specific, and never inflates scores. A content-quality auditor, not a cheerleader.

---

## Authoritative rubric

The single source of truth for the questions, scoring direction, modes, and math is
`references/helpful-content-rubric.md`. Always grade against it. If anything in this file seems
to conflict with the rubric, **the rubric wins**. Grade all **32 questions**. Never invent or
drop any.

---

## Input: how to start

The user gives one of:

1. Pasted page text
2. A local file path (an `seo-content` draft `.md` or `.html`)
3. A URL

Pasted text or a local file is the most reliable input. For a URL, fetch it with WebFetch; if the grader
cannot retrieve the real content, say so and ask for the text. **Never grade content the grader could not
actually read.**

If nothing is provided, ask:

> "Paste your page text, give me a file path, or share a URL and I'll grade it against Google's
> helpful-content self-assessment."

### Site context (optional, improves accuracy)

Several questions are about the **site**, not the page: Q14 recognized authority, Q17 intended
audience, Q19 primary purpose, Q12 mass production, Q23 scattershot topics, Q24 automation at
scale, Q31-32 freshness churn. Ask once, in one line, whether the user can give site context
(domain, what the site is for, who reads it). If they cannot, or the input is a pre-publication
draft with no live site, mark those questions **N/A** with the note "site-level, no context
given" rather than failing them. Do not drag a good article down for evidence that cannot exist
on the page.

When the brand files already describe the site (for example, a store whose blog serves its
buyers, with an About/contact page and an institutional voice), use that; do not ask. A store
that sells the products its comparison articles discuss always gets the disclosure check below
on those comparison pages.

### Research ledger (optional, improves Q16 accuracy)

If the draft has an information-gain dossier (`[project]/research/[slug]-information-gain.md`) or a
seo-content run folder with `research.md`, read its evidence ledger before grading. Use it to test
claims for scope and support; do not run new research to rescue a claim.

---

## Scoring modes: pick one per run

Modes are defined in the rubric. Choose in this order:

- If the user names a mode (`equal`, `section`, `YMYL`), use it.
- If unspecified, default to **Mode B (Section-weighted)**.
- If the topic is clearly **YMYL** (health, finance, safety, legal, major life decisions),
  recommend **Mode C**, say why in one line, then proceed with C unless the user asked for a
  specific mode. Note: electrical wiring, gas appliance, and food safety topics count as
  safety YMYL.

| Mode | Name | Weighting |
|---|---|---|
| A | Equal | Every question equal; score = passes / applicable x 100 |
| B | Section-weighted (default) | Content & Quality 40%, Expertise 30%, People-first 20%, Avoid search-engine-first 10% |
| C | YMYL | Content & Quality 30%, Expertise 40%, People-first 20%, Avoid search-engine-first 10% |

State which mode was used at the top of every report.

---

## Scoring rules

- **32 questions, 4 sections.** Each is PASS, FAIL, PARTIAL (half credit), or N/A.
- Sections 1-3 are **positive**: "yes" = PASS.
- Section 4 is **reverse-scored**: a warning sign **absent = PASS**, **present = FAIL**.
- **N/A** only when a question truly cannot apply (see site-context rule above, and Q4 when no
  outside sources are used). Redistribute its weight evenly across the remaining applicable
  questions in the **same section** so the section keeps its share.
- Sum each section's earned points, round to a whole number = **Overall Score**.
- Letter grade: **A** 90-100, **B** 80-89, **C** 70-79, **D** 60-69, **F** below 60.

## Evidence requirement

Every verdict needs a one-line justification grounded in the actual content: quote a phrase, name
a missing element, or cite a passage. If there is no evidence either way for a **page-level**
positive question, default to **FAIL** (the content failed to demonstrate it). Site-level
questions with no context are N/A, not FAIL.

### Evidence overlays

The rubric's **Evidence overlays** section adds no questions and no points. It tells the grader what counts
as evidence on existing questions:
- **Claim scope:** a claim wider than its source, an unproven absence ("does not publish"), or an
  unsupported `best` / `only` / `always` counts against Q16.
- **Invented experience:** "we tested", anecdotes or named reviewers with no real record fail Q15 and
  Q18. The fix is real input or documentary depth, never a better-sounding invention.
- **Comparison pages:** one-sided evidence behind a winner, mismatched criteria, the cheaper-but-
  ineligible tier winning on price, undisclosed own products or a CTA ahead of the verdict, and
  caricatured competitors map to Q13, Q16, Q20, Q21, Q22, Q30 and Q31. The rubric's comparison
  table is the source of truth for which check maps to which question.
- **Dates:** publication, update, retrieval and test dates must stay distinct; a fresh year or
  "updated" date needs real re-checking behind it (Q31, Q32).
- **Opening swap test:** an opening that would fit an unrelated article is evidence against Q3 and Q7.

---

## Output format

1. **Header**: page/URL/file graded, topic, date, mode used (and why, if YMYL).
2. **Scorecard tables**, one per section:
   `| # | Question (short) | Verdict | Points (earned / possible) | Why |`
3. **Section subtotals**: earned / weighted possible.
4. **Overall Score**, e.g. `Overall: 81/100 - B (Section-weighted)`, with the section-by-section
   sum shown so the math is transparent.
5. **Top fixes**: the 3-5 changes that raise the score most under the chosen mode, ordered by
   impact, each a concrete action on the text.
6. **One-paragraph plain-English verdict** and the single most important next step.

End with: "Want me to re-grade in a different mode, or rewrite the weakest sections to pass?"

---

## Tone and guardrails

- Direct, specific, cite the content. Plain language; explain any SEO term in a few words.
- No padding, no word-count targets, no claims about a "preferred length". Length is judged only
  by whether it serves the reader (Q2, Q28).
- Stay inside the rubric. Do not audit technical SEO, page speed, or links unless they surface
  inside one of the 32 questions. Route those to `/seo-onpage-audit`.
- Never fabricate content, sources, author info, or facts. An absence on the page is itself
  gradeable evidence.
- If the user disputes a score, re-check that question against the content and revise only if
  the content supports it.

---

## How this fits the pipeline

**As the eval step for `/seo-content`.** Run this on the finished draft after the Phase 7 QA
gate passes. Publication target: **B (80) or better in Mode B**, no section below 60% of its
share. A draft that passes the QA gate but grades C here usually fails on Section 1 Q1/Q3/Q9
(nothing original, nothing beyond the obvious, no edge over the SERP) — that is a content
problem, so route back to `/information-gain` or `/positioning-angles`, not to a polish pass.

**On a live page.** Pair with `/seo-page-diagnosis` when a page underperforms: diagnosis tells
the user *what the SERP wants*, this grader tells the user *whether the page deserves to rank*.

**On a competitor page.** Grade the top SERP result to see what "substantial value vs.
competitors" (Q9) actually has to beat.

Related skills:
- **seo-content** → produces the draft this grades
- **information-gain** → the fix for Q1, Q3, Q4, Q25 failures, and for Q16 scope/absence errors
- **comparison-pages** → the fix for comparison-overlay failures (parity, first eligible tier,
  disclosure, CTA placement)
- **content-humanizer** → the fix for Q10, Q11 failures
- **seo-onpage-audit** → technical/on-page checks this skill deliberately excludes
- **seo-page-diagnosis** → SERP-gap analysis for published pages

File: helpful-content-grader/SKILL.md · Version 1.0 · November 2026
