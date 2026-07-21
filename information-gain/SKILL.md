---
name: information-gain
description: "Surface rare, citable statistics and primary-source data from PDFs, Google Docs/Sheets, government reports, academic papers, and institutional documents for use in blog content. Use when you need hard numbers that competitors won't have. Triggers on: find statistics for [topic], research data for [article], information gain for [keyword], source data for blog post about [topic]."
---

# Information Gain Researcher

Most blog posts cite the same 5 sources everyone else already found on page 1 of Google. This skill finds what they missed — government reports, academic whitepapers, industry data buried in PDFs and spreadsheets that require deliberate digging to surface.

The goal: arm a blog post with at least 20 citable statistics from primary sources that competitors are not using. That's information gain — the thing that makes Google prefer your article over theirs.

---

## The core job

Execute targeted filetype searches across .gov, .edu, and institutional domains to surface:
- Statistics and survey results from primary research
- Government data and regulatory reports
- Academic whitepapers and study findings
- Industry association data and technical standards documents
- Case study data from NGO and institutional reports

Then compile findings into a structured research dossier the writer can draw from directly.

---

## Phase 1: Clarify the brief

Before searching, ask the user:

1. **Topic** — What is the article's primary keyword or subject?
2. **Angle** — What specific claim or argument does the article need to support? (e.g., "energy savings from [product feature]" vs. "[product] market size")
3. **Document types** — Which do they want prioritized? (PDF / PPT / DOC / XLSX / Google Docs / Google Sheets / all)
4. **Data type** — What kind of evidence is most useful? (statistics, survey results, case studies, technical specs, regulatory data)
5. **Recency** — How recent must sources be? (e.g., last 5 years, last 10 years, any)

Do not begin searching until all five answers are confirmed.

---

## Phase 2: Execute the search battery

Run all applicable searches below. Replace `[topic]` with the specific keyword or phrase. Run variations — use synonyms, abbreviations, and related terms to maximize coverage.

### PDF searches
```
filetype:pdf "[topic]"
filetype:pdf "[topic]" statistics
filetype:pdf "[topic]" data survey
inurl:gov filetype:pdf "[topic]"
site:edu filetype:pdf "[topic]"
site:osha.gov filetype:pdf "[topic]"
site:energy.gov filetype:pdf "[topic]"
site:epa.gov filetype:pdf "[topic]"
site:nist.gov filetype:pdf "[topic]"
```

### PowerPoint / presentation searches
```
filetype:ppt "[topic]"
filetype:pptx "[topic]"
inurl:gov filetype:ppt "[topic]"
site:edu filetype:pptx "[topic]"
```

### Word document searches
```
filetype:doc "[topic]"
filetype:docx "[topic]"
inurl:gov filetype:doc "[topic]"
site:edu filetype:docx "[topic]"
```

### Spreadsheet / data searches
```
filetype:xlsx "[topic]"
filetype:csv "[topic]"
inurl:gov filetype:xlsx "[topic]"
site:edu filetype:xlsx "[topic]"
```

### Google Docs / Sheets searches (public & published-to-web documents)
```
site:docs.google.com "[topic]"
site:docs.google.com/document "[topic]"
site:docs.google.com/spreadsheets "[topic]"
site:drive.google.com "[topic]"
"[topic]" "docs.google.com/spreadsheets"
```

### Institutional and NGO searches (no filetype filter — catches embedded docs)
```
site:eia.gov "[topic]"
site:bls.gov "[topic]"
site:cdc.gov "[topic]"
site:nrel.gov "[topic]"
site:energy.gov "[topic]" report
```

### Execution rules

- Use the WebSearch tool for every search. Do not fabricate results.
- Run at minimum 12 distinct searches before compiling findings.
- If a query returns no useful results, substitute a synonym or related term and run it again. Log what you tried.
- Google Docs and Sheets are not downloadable files — surface them with `site:docs.google.com` / `site:drive.google.com`, not `filetype:`. Only include documents that open without a login or share-request wall.
- If you can access the document via WebFetch, retrieve it and extract the specific data point and surrounding context.
- Do not include blog posts, news articles, or press releases. Primary-source documents only.
- Flag any source that appears to be behind a paywall — note "paywall — preview only."
- Flag any source older than 10 years as "potentially outdated — verify before citing."

---

## Phase 3: Evaluate and curate

For each result found, determine:

| Criterion | Question to ask |
|-----------|----------------|
| Rarity | Is this data available on the first page of a standard Google search? |
| Authority | Is the source a government body, academic institution, or industry standards organization? |
| Specificity | Does it contain a concrete number, percentage, or measurable claim? |
| Recency | Is it dated, and is that date recent enough to be credible? |
| Usability | Can a blogger cite this naturally in a sentence without needing the full document context? |

Discard results that are generic, vague, or easily found by competitors. Keep only sources that clear all five criteria.

**Minimum target: 20 usable statistics from at least 3 different source types.**

If you cannot reach 20 after exhausting all search patterns, report how many you found and why the search ceiling was hit (thin data landscape, paywalled sources, topic too narrow).

---

## Phase 3.5: Score the dossier (research-quality rubric)

Before compiling, score the dossier as a whole on five dimensions (adapted from the `claude-blog`
research-quality rubric, MIT). This catches a dossier that's technically full of citations but weak
where it counts — e.g. 20 stats that all trace back to one upstream press release ("synthesis echo").

| Dimension | Weight | Scored well when… |
|---|---|---|
| **Groundedness** | 30 | Every claim ties to a named, reachable primary source (never "studies show"). |
| **Specificity** | 25 | Concrete figures/percentages/ranges, not directional generalizations. |
| **Coverage** | 20 | Multiple *independent* sources — no synthesis echo (5 pages citing 1 upstream = 1 source). |
| **Actionability** | 15 | Each finding has a concrete "Blog use" — where it deploys in the article. |
| **Format compliance** | 10 | Each entry carries the FLOW triple (year + publisher/title + full URL); drop-in ready. |

Score /100. **Remediate below 70** before handing off: run more searches for the weakest dimension
(usually Coverage — go find independent corroboration), or downgrade single-sourced claims to "verify
before citing." Report the score in the Phase 5 debrief.

### Synthesis-echo check (the one most dossiers fail)
For any striking statistic, ask: do my "multiple sources" actually trace to **one** original study or
press release? If yes, it counts as a **single** source — find a genuinely independent one or flag it. A
high stat count built on one upstream claim is fragile, and competitors already have it.

---

## Phase 4: Compile the research dossier

Save the completed dossier to:

```
[project-folder]/research/[article-slug]-information-gain.md
```

For example: `your-project/research/[product]-efficiency-information-gain.md`

If the `research/` subfolder does not exist, create it.

---

### Dossier format

```markdown
# Information Gain Research: [Article Topic]

**Target keyword:** [primary keyword]
**Article angle:** [specific claim or argument this research supports]
**Research date:** [YYYY-MM-DD]
**Total sources found:** [N]
**Source types:** [PDF / PPT / DOC / XLSX / Google Doc / Google Sheet / institutional page]

---

## Statistics & Findings

### 1. [One-sentence statement of the finding]

- **Source:** [Full document name]
- **Author/Publisher:** [Government body / University / Organization]
- **Year:** [Publication year]
- **URL:** [Full URL — written out in plain text]
- **File type:** [PDF / PPTX / DOCX / XLSX / Google Doc / Google Sheet / web page]
- **Direct quote or data point:** "[Exact quote or figure from the document]"
- **Context:** [1–2 sentences explaining what the document is and why this finding appears in it]
- **Reliability flag:** [None / Potentially outdated / Paywall — preview only]
- **Blog use:** [Specific recommendation — e.g., "Use in the introduction as an anchor statistic" / "Cite in the efficiency section to quantify energy savings" / "Use as a pull quote in an H3 callout box"]

---

### 2. [Next finding]

[Same structure repeated]

---

## Searches run

| Search query | Results useful? |
|---|---|
| filetype:pdf "[topic]" | Yes / No — [note if no: why] |
| inurl:gov filetype:pdf "[topic]" | Yes / No |
| [etc.] | |

---

## Summary table

| # | Statistic (short) | Source name | Year | URL | File type | Blog use |
|---|---|---|---|---|---|---|
| 1 | [brief stat] | [source] | [year] | [URL] | [type] | [use] |
| 2 | | | | | | |
[continue for all findings]

---

## Coverage gaps

[Note any sub-topics where data was thin or unavailable, and why. This helps the writer know where they may need to rely on secondary sources or acknowledge uncertainty.]
```

---

## Phase 5: Debrief to user

After saving the file, report back in this format:

```
Research dossier saved: [file path]

Found: [N] statistics from [N] sources
Source breakdown: [N] PDFs, [N] institutional pages, [N] PPTs, etc.

Top 3 most valuable findings:
1. [One sentence — what it says and why it's rare]
2. [One sentence]
3. [One sentence]

Coverage gaps:
- [Any topics where data was thin]

Suggested next step: Feed the dossier into Phase 2 of /seo-content when drafting the article. Prioritize the top-rated statistics for the introduction and any comparison or data-heavy H2 sections.
```

---

## FLOW citation triple (how each stat is rendered in the article)

When the writer deploys a dossier stat in the draft, render it as a **FLOW triple** so it's verifiable
and AI-citable (adapted from the `claude-blog` FLOW-alignment model, MIT):

1. **Year anchor in the prose** — "In 2024, …" / "A 2023 DOE study …" (never "recently," "studies show").
2. **Inline citation at first mention** — `[Publisher or document title](URL)`, woven into the sentence
   (no tacked-on "see X" — follow the link rules in `seo-content/SKILL.md`).
3. **Traceable source** — the URL resolves to the primary document; keep the full URL + access date in
   the dossier so the claim can be re-verified on refresh.

Example: "In 2024, the [U.S. Department of Energy](https://energy.gov/...) reported [a specific statistic
about your product category]." One sentence — year + named source + live link — which is
exactly what answer engines quote. This is the format the **Format-compliance** dimension scores above.

---

## Quality rules

**DO:**
- Cite every statistic with full source attribution before moving on
- Explain in "Blog use" exactly where and how to deploy each finding
- Prioritize government, NGO, and academic sources over industry association self-reporting
- Include the document's full name, not just the domain
- Note if a statistic is part of a larger dataset that might have a more current edition

**DON'T:**
- Include blog posts, news articles, or op-eds — primary documents only
- Summarize information that's already in the top 5 Google results
- Present vague claims without a specific number (e.g., "studies show efficiency improves" without a percentage)
- Fabricate or assume URLs — only report sources that were actually returned by search
- Skip the "Blog use" field — every finding must have a concrete deployment recommendation
