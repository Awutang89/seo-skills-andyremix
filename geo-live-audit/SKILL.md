---
name: geo-live-audit
description: "Interpret an LLM-readiness audit of our own live pages — heading structure, boilerplate-stripped content volume, and whether content survives without JavaScript — and turn the measurements into a ranked fix list. Use when reviewing site-audit findings, or asking whether our pages are machine-readable for AI answer engines. Triggers on: llm readiness, geo audit, ai citation readiness, is our content server rendered, heading structure audit, empty headings, h1 mismatch, site audit findings, why is this page not being cited. Outputs a ranked fix list per page, grounded in the measured numbers."
---

# GEO Live Audit

The live-page counterpart to `seo-content/references/geo-checklist.md`. That file
states the GEO rules; its enforcement is a PASS/FAIL gate applied to **drafts**
at write time. This skill reads what the
measurements below find on real pages and says what to do about it.

Do not fetch anything. The readiness scanner (`<readiness-scanner>`, an optional integration)
has already fetched our pages,
parsed them deterministically, and written the
numbers. This skill's job is interpretation and ranking.

---

## Scope

**Our own pages only.** Competitor-page extraction is out of scope here.
If asked to run this against a competitor,
decline and point at `striking-distance`, which owns that path.

**This is not the classic technical audit.** Broken links, redirect chains,
orphan pages, cross-page duplicate titles and sitemap problems belong to
`seo-onpage-audit` and its site-level pass, which crawls. Two of the checks here — empty
headings and h1-vs-title mismatch — sit here.

---

## Inputs

1. The page measurements taken as above — one set per page,
   with the numbers in the table below.
2. The run list — the rollup, including pages that could not
   be read.
3. The saved measurements from prior runs, for trend.

---

## What the numbers mean

| Metric | Reading it |
|---|---|
| `score` (0-100) | Composite. **Uncalibrated** — see the caveat below. Use it to compare a page against its own past, never as a grade |
| `fit_words` | Real content words after nav, header, footer and forms are stripped. This is the honest length of the page |
| `raw_words` | All visible text including furniture. `fit_words / raw_words` is the signal ratio |
| `fit_ratio` | Below ~0.10 the page is mostly furniture — usually a thin page on a heavy template |
| `text_to_html` | Visible text as a share of served bytes. Very low means the content is not in the HTML |
| `h1_count` | 0 or above 1 both matter, for different reasons |
| `empty_headings` | Headings occupying an outline slot while describing nothing |
| `skipped_levels` | h2 followed by h4. Only descents count; climbing back up is legal |

### The score is a tracker, not a grade

Its thresholds ("1200 words scores 25") are engineering judgment, not a fit
against measured AI-citation outcomes. Never present it as authoritative, never
put it in front of the operator as a verdict, and never rank work by it alone.
Rank by the individual findings, which are exact. Say "this page improved from
54 to 71" — never "this page scores 71, which is good."

---

## How to rank fixes

Order by what actually blocks an answer engine, not by severity label alone:

1. **`js_dependent_content`** — the page has almost no text in the served HTML
   and a large script payload. AI crawlers generally do not run JavaScript, so
   the page reads as empty. Nothing else on the page matters until this is
   fixed. This is `geo-checklist.md` §B, finally measured.
2. **`low_server_rendered_text`** — same failure, milder. Confirm what is
   server-rendered before treating any content finding on this page as real.
3. **`thin_content` with a low `fit_ratio`** — there is less here than the
   template implies. Decide: expand it, merge it, or retire it.
4. **`no_headings` / `missing_h1`** — nothing states the topic.
5. **`multiple_h1`** — usually a template marking a logo or strapline as a
   heading. Check whether it is site-wide before filing per-page work; one
   template fix can clear every page at once.
6. **`empty_heading` / `skipped_level`** — the outline is broken, which is how
   answer engines segment a page.
7. **`h1_title_mismatch`** — the page presents two different topics. Decide
   which one is true.
8. **`html_too_heavy`** — only worth raising if a page is egregious
   (`geo-checklist.md` §E).
9. Title and meta-description length findings — real, but never the reason a
   page is not cited.

### Look for template patterns first

Before writing per-page tasks, check whether a finding repeats across most
scanned pages. `multiple_h1`, `low_server_rendered_text` and
`html_too_heavy` are usually template-level. One template fix beats twenty page
tasks, and filing the twenty hides the actual cause.

---

## Measurement notes not to ignore

The scanner reports `notes` alongside the score. They change how much an auditor can
trust the numbers:

- **`topic_too_generic`** / **`fit_fell_back`** — the page's title and h1 were
  too thin to score content against, so boilerplate filtering was bypassed.
  `fit_words` is then an over-estimate: treat the content-volume reading as
  unreliable and say so. (This guards a real failure in the reference algorithm,
  which once reduced a long page to a few words because the title was
  site-wide.)
- **`html_truncated`** — the page exceeded 1 MiB and was cut. Findings about
  what is *missing* may be artefacts of the cut.
- **`script_heavy`** — over half the served bytes are script.
- **`no_body_text`** — nothing visible at all; check for a redirect or a gate.

A page that could not be read at all appears in the report's error section, not
as a finding. Say so plainly rather than reporting it as clean.

---

## Output

For each page, in priority order:

```
PAGE https://example.com/pricing — readiness 42/100 (was 54 on <YYYY-MM-DD>)

BLOCKING
1. [js_dependent_content] Only 0.4% of served bytes are visible text with 210KB
   of script. The page reads as empty to AI crawlers. Server-render the pricing
   table and the JSON-LD.

STRUCTURE
2. [multiple_h1] Two h1 elements — the site logo is marked up as one. Present on
   9 of 10 scanned pages, so fix the template, not the page.
3. [empty_heading] An empty h2 sits between the plan tiers.

CONTENT
4. [thin_content] 96 content words against 1,240 raw words (ratio 0.08) — the
   page is mostly template.

NOT ASSESSED
- Content volume is unreliable here: topic_too_generic fired, so boilerplate
  filtering was bypassed.
```

Close with what changed since the previous run, if a snapshot exists. If a clean
page has no findings, say so in one line — this skill treats a
clean audit as a valid result, and inventing work to look busy is worse than
reporting nothing.

---

## How this connects

- **`seo-content/references/geo-checklist.md`** — the rules this
  measures. §B (server-side rendering) and §E (HTML weight) are the site-level
  cousins of `text_to_html` and `html_too_heavy`. Its Phase 7 PASS/FAIL gate
  stays authoritative for drafts; this owns live pages.
- **`seo-page-diagnosis/SKILL.md`** — the other question entirely: why a
  page loses to competitors, which needs a keyword and the SERP. If the ask is
  "why won't this rank", route there. If it is "is this page well-built", stay
  here.
- **`image-seo-audit/SKILL.md`** — images, including alt text, which this
  skill does not check.
- **`seo-schema/SKILL.md`** — when `json_ld_blocks` is zero and the page
  warrants structured data.
- **`seo-onpage-audit` site-level pass** — the crawl-wide technical audit. When the
  pass has run, prefer its findings for broken links, redirects,
  canonicals and cross-page duplicates rather than reasoning about them here.

File: geo-live-audit/SKILL.md · Version 1.0 · November 2026
