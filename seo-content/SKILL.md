---
name: seo-content
description: "Create high-quality, SEO-optimized content that ranks AND reads like a human wrote it. Use when turning keyword research into actual content pieces. Takes a target keyword/cluster and produces a complete article optimized for search while avoiding AI-sounding output. Triggers on: write SEO content for X, create article for keyword, write blog post about X, SEO article, content for keyword cluster, refresh/rewrite an existing article, update outdated outbound links. Outputs publication-ready content with proper structure, optimization, and human voice."
---

# SEO Content Workflow

SEO content has a reputation problem. Most of it is garbage — keyword-stuffed, AI-sounding, says nothing new. It ranks for a month, then dies.

This skill creates content that ranks AND builds trust. Content that sounds like an expert sharing what they know, not a content mill churning out filler.

The goal: Would someone bookmark this? Would they share it? Would they come back?

If yes, Google will reward it. If no, no amount of optimization saves it.

---

## The core job

Transform a keyword target into **publication-ready content** that:
- Answers the search intent completely
- Sounds like a knowledgeable human wrote it
- Is structured for both readers and search engines
- Includes proper on-page optimization
- Passes the "would I actually read this?" test

---

## Required inputs

Before writing, gather:

1. **Target keyword** — Primary keyword to rank for
2. **Keyword cluster** — Related keywords to include naturally
3. **Search intent** — Informational / Commercial / Transactional
4. **Content type** — Pillar guide / How-to / Comparison / Listicle / etc.
5. **Brand voice profile** — (from brand-voice skill, if available)
6. **Unique angle** — What perspective makes this different?

If coming from keyword-research skill, most of this is already defined.

---

## The workflow

```
RESEARCH → STATS/IMAGES → BRIEF → OUTLINE → DRAFT → HUMANIZE → DEEP VOICE PASS → OPTIMIZE → REVIEW
```

---

## Phase 1: Research

Before writing a word, understand what you're competing against.

### SERP Analysis

Search the target keyword (incognito) and analyze top 5 results:

**For each result, note:**
- Content type (guide, listicle, tool page, etc.)
- Approximate word count
- Structure (headers, sections)
- Unique angles or data
- What they do well
- What they miss or get wrong
- How recent (publish/update date)

**Extract from SERP features:**
- People Also Ask questions (answer ALL of these)
- Featured Snippet format (match it to win it)
- AI Overview presence (what it includes/excludes)

### Word Count Analysis (CRITICAL)

Before deciding your target word count, analyze what's actually ranking.

**For each of the top 5 results, determine exact word count:**

Use WebFetch or manual inspection to get accurate counts. Don't guess.

| Position | Source | Word Count | Quality Level |
|----------|--------|------------|---------------|
| #1 | [Site] | ___ words | Comprehensive/Basic |
| #2 | [Site] | ___ words | Comprehensive/Basic |
| #3 | [Site] | ___ words | Comprehensive/Basic |
| #4 | [Site] | ___ words | Comprehensive/Basic |
| #5 | [Site] | ___ words | Comprehensive/Basic |

**Calculate distribution:**
- Shortest: ___ words
- Longest: ___ words
- Average: ___ words
- Median: ___ words

**Determine Optimal Target Length:**

DO NOT pick arbitrary word counts. Base it on SERP data + gap analysis.

**Option A: Match the Leader (2,500 words if leader is 2,500)**
- Use when: Leader is comprehensive, you'll differentiate on angle/quality
- Pros: Competitive parity
- Cons: Doesn't stand out on depth

**Option B: Beat Leader by 30-50% (3,500 words if leader is 2,500)**
- Use when: You've identified 3+ significant content gaps to fill
- Pros: Clearly more comprehensive
- Cons: Must justify extra length with unique value

**Option C: Definitive Guide 2-3× (5,000+ words if leader is 2,500)**
- Use when: Weak competition, major gaps, proprietary knowledge
- Pros: Becomes THE resource
- Cons: Only works if you have genuinely unique insights

**The Gap Test (Do This Before Committing to Length):**

List specific gaps you'll fill that justify going longer:
- [ ] Gap 1: [What topic/angle they miss]
- [ ] Gap 2: [What methodology they lack]
- [ ] Gap 3: [What examples/data they don't have]

**If you can't list 3+ significant gaps, match the leader's length.**

Going longer without adding value = bloat. Google rewards comprehensiveness, not word count.

**Example Decision:**

```
Keyword: "how to choose [product]"

SERP Results:
#1: 2,500 words (comprehensive)
#2: 550 words (basic)
#3: 1,500 words (mid-depth)
#4: 100 words (landing page)
#5: 553 words (beginner)

Average: 1,220 words
Median: 1,500 words
Leader: 2,500 words

Gaps Found:
✓ No application-specific sizing ([use case] vs [use case] vs [use case])
✓ No common mistakes section with real examples
✓ Missing workflow-based [key spec] analysis (they just say "add tools")
✓ No [option A] vs [option B] decision framework
✓ No cost analysis of under/oversizing

Decision: 3,500 words (40% longer than leader)
Justification: 5 major gaps to fill, each adding 200-300 words of unique value
```

**Word Count is Determined BY the Research, Not Before It.**

---

### Data-Driven Word Count Formula (If keyword-research provided data)

**If you have search volume + difficulty data** from keyword-research skill, use this supplemental formula:

```
base_word_count = 1,500

If search_volume >2,000: add 1,000 words
If search_volume >5,000: add 1,500 words (total +2,500)

If keyword_difficulty >50: add 1,500 words (need depth to compete)
If keyword_difficulty >70: add 2,000 words (need authority depth)

If cluster has >7 child keywords: add 500 words
If cluster has >12 child keywords: add 1,000 words (total +1,500)
```

**Example:**
```
Keyword: "[product] sizing"
Volume: 2,200
Difficulty: 38
Child keywords in cluster: 9

Calculation:
1,500 (base)
+ 1,000 (volume >2,000)
+ 0 (difficulty <50)
+ 500 (>7 child keywords)
= 3,000 words

Cross-check with SERP leader (2,500 words)
→ Final target: 3,000-3,500 words (justified by data + gaps)
```

**Use both methods:**
- SERP analysis = competitive baseline
- Data formula = content scope guidance
- Final decision = combine both + gap test

---

### Gap Analysis

After reviewing competitors, identify:

1. **What's missing?** — Questions unanswered, angles unexplored
2. **What's outdated?** — Old information, deprecated methods
3. **What's generic?** — Surface-level advice anyone could give
4. **What's your edge?** — Unique data, experience, perspective

Your content should fill these gaps.

---

### SERP Heading Gap Extraction

When fetching each top-ranking URL with WebFetch for the Word Count Analysis above, also extract all H1 and H2 headings from each page.

**For each of the top 3-5 ranking pages:**
- Extract all H1 and H2 headings from the page content
- Compile a heading inventory table:

| Rank | URL | H1 | H2 Headings |
|---|---|---|---|
| #1 | [url] | [h1] | [h2, h2, h2...] |
| #2 | [url] | [h1] | [h2, h2, h2...] |
| #3 | [url] | [h1] | [h2, h2, h2...] |

- Identify headings that appear in 2+ competing articles (high-frequency = must-cover topics)
- Identify unique headings that appear only once but address a clear user question (opportunities)

**Output a Content Gap Summary before moving to Phase 1.5:**

```
Content Gap Summary — [primary keyword]

High-frequency headings (appear in 2+ top pages — must cover):
- [heading]
- [heading]

Gap opportunities (unique angles competitors cover that KEYWORD-DATABASE may have missed):
- [heading] (source: URL)
- [heading] (source: URL)
```

These feed directly into the Phase 3 outline — the H2 structure should incorporate all high-frequency headings and any gap opportunities that fit the article's focus.

---

### Information Gain Research (Optional — Recommended for Data-Heavy Articles)

For articles where citing primary-source statistics will meaningfully differentiate the content — particularly comparison articles, how-to guides with quantified claims, and any topic where competitors rely on vague generalities — run the `/information-gain` skill before moving to Phase 2.

**When to invoke it:**
- The article needs hard numbers competitors don't have (efficiency percentages, cost data, failure rates, regulatory figures)
- The SERP gap analysis revealed competitors are making claims without citing primary sources
- The topic has government or academic bodies that publish relevant data (safety, energy, standards, manufacturing)

**How to use the output:**
- The skill saves a dossier to `[project]/research/[slug]-information-gain.md`
- Pull the top-rated statistics into the Phase 2 brief as "anchor data points"
- Assign each statistic to the section of the outline where it will appear
- Do not dump all statistics into the article — select the 5–8 most relevant and let the rest sit in the dossier for future articles

Skip this step for thin-SERP articles where word count is low and the SERP itself is mostly opinion-based content.

---

### Link Refresh (Refreshing / Rewriting an Existing Article)

**Refresh/rewrite tasks only — skip for net-new articles.** When the job is to refresh or rewrite an existing article (typically handed off from `seo-page-diagnosis` with an Authority/Freshness gap), audit its **existing outbound links before drafting**: swapping stale citations for newer, more authoritative sources is one of the strongest freshness signals you can send. Scan the current external links, flag any that are >2 years old, superseded, secondary-where-a-primary-exists, or broken, then find fresher primary-source replacements — reuse the `/information-gain` skill as the search engine — and rewrite the anchor text. Present the swaps in one approval table, then apply inline. Full procedure: `skills/seo-content/references/link-refresh.md`. (Net-new articles have no pre-existing links to audit — the matching Phase 7 QA row reads `N/A`.)

---

### NeuronWriter Query

Run this after SERP analysis and gap analysis, before moving to Phase 2.

**Credentials and settings:** See `skills/seo-content/references/neuronwriter-config.md`

**Step 1 — Confirm the primary keyword**

Before firing the query, ask the human reviewer:

> "What should the primary keyword be for the NeuronWriter query? I'll use: [your working primary keyword]. Confirm or correct before I submit."

Wait for confirmation. Do not submit the query until the keyword is confirmed.

**Step 2 — Create the query**

```
POST https://app.neuronwriter.com/neuron-api/0.5/writer/new-query

Headers:
  X-API-KEY: [from neuronwriter-config.md]
  Content-Type: application/json

Body:
{
  "project": "[project ID from neuronwriter-config.md]",
  "keyword": "[confirmed primary keyword]",
  "engine": "google.com",
  "language": "English"
}

IMPORTANT: "language" must be "English" (full word), NOT "en". Using "en" causes the API to return an error.
```

Note the `query` ID from the response — you'll need it in Step 3.

**Step 3 — Wait for analysis**

NeuronWriter takes up to 90–120 seconds to process. Wait the full time before calling `/get-query`. If the response status is not "ready", wait another 30 seconds and retry.

**Step 4 — Retrieve recommendations**

```
POST https://app.neuronwriter.com/neuron-api/0.5/writer/get-query

Headers:
  X-API-KEY: [from neuronwriter-config.md]
  Content-Type: application/json

Body:
{
  "query": "[query ID from Step 2]"
}
```

**Step 5 — Save the full query output**

Before extracting terms, save the raw API response to a per-article JSON file:

```
your-project/neuronwriter-queries/[article-slug].json
```

Use a PowerShell script to retrieve and save in one step:

```powershell
$headers = @{
    'X-API-KEY' = '[from neuronwriter-config.md]'
    'Content-Type' = 'application/json'
}
$body = '{"query":"[query ID from Step 2]"}'
$response = Invoke-RestMethod -Uri 'https://app.neuronwriter.com/neuron-api/0.5/writer/get-query' -Method POST -Headers $headers -Body $body
$response | ConvertTo-Json -Depth 10 | Out-File -FilePath 'your-project/neuronwriter-queries/[article-slug].json' -Encoding utf8
```

This file persists the query output so the Phase 6 score check can reuse the same query ID, and so term data is available if the article is updated later without burning another API query.

**Step 6 — Read and extract the term data**

Use the **Read tool** to read the saved JSON file in batches. Do NOT run Python scripts or shell commands to parse the JSON — the Read tool handles the file directly and avoids encoding issues and interpreter path problems on Windows.

Read the full file in one pass (it is typically under 100KB). The JSON structure to look for:

```
competitors[]          → SERP results: rank, url, word_count, content_score, headers
metrics.word_count     → median, target word count
ideas.people_also_ask  → PAA questions (key: "q")
ideas.topic_matrix     → topic importance scores
terms_txt              → plaintext term lists (easiest to read):
  .content_basic_w_ranges  → body terms with frequency ranges e.g. "noise: 3-14x"
  .h2                      → recommended H2 terms
  .title                   → recommended title terms
serp_summary.top_intent → informational / transactional / etc.
```

Extract and present to the human reviewer:

```
NeuronWriter Term Data — [primary keyword]

SERP (top competitors with word counts and content scores)
NW median word count: [X]
PAA questions: [list from ideas.people_also_ask[].q]
H2 terms: [from terms_txt.h2]
Body terms with ranges: [from terms_txt.content_basic_w_ranges]
Extended terms: [from terms_txt.content_extended — supporting vocabulary]
```

These terms are a **research supplement only.** They inform Phase 2 but do not override the secondary keywords derived from SERP analysis. Only use a NW term if it semantically fits the article — do not force terms in to hit a list.

**How to use NeuronWriter term recommendations:**

NeuronWriter provides suggested usage ranges (e.g., "[term]: sugg_usage [1, 6]" means use 1-6 times). These are guides for natural term inclusion, not quotas to hit.

**In practice:**
- Aim for the **middle of the suggested range** (e.g., if NW suggests [1, 6], use 3-4 times naturally)
- Mix terms with synonyms for variety (e.g., alternate "[term]" with "[synonym]" and "[synonym]")
- Never force terms into sentences where they don't fit naturally
- Focus on writing helpful content first, then verify key terms are present

**Example:**
- NW suggests: "[term]" (60% usage, sugg_usage [1, 6])
- ✅ Good: Use "[term]" 3-4 times naturally, use "[synonym]" for variety in other instances
- ❌ Bad: Force "[term]" 6 times to hit the upper range

NW data helps ensure you're using relevant industry terms competitors use, not creating a keyword stuffing checklist.

---

## Phase 1.5: Statistics & Image Research

Run this phase after the NeuronWriter query (Phase 1) and before the Content Brief (Phase 2).

---

### Statistics Research

**Step 1 — Search for statistics:**

Run WebSearch: `[topic keyword] statistics data study 2024 2025 2026`

Find 5-8 statistics, tier-classified as follows:
- **Tier 1**: .gov, .edu, international orgs, Google Search Central
- **Tier 2**: Ahrefs, Semrush, SparkToro, BrightEdge, academic papers
- **Tier 3**: Search Engine Land, SEJ, TechCrunch, major trade publications
- **Reject**: Generic SEO blogs, affiliate sites, round numbers without methodology

**Step 2 — Record candidates:**

For each statistic found, record in a table:

| # | Stat | Source | URL | Tier | Date | Verified |
|---|------|--------|-----|------|------|----------|
| 1 | ...  | ...    | ... | 1    | ...  | Pending  |

**Step 3 — Verify at least 3 stats:**

Fetch the source page with WebFetch to confirm the number appears on the page. Reject any stat that cannot be verified or only appears on Tier 4+ sites.

**Step 3b — Corroborate your citation-priority stats:**

The 1–2 numbers you most want AI engines to quote (the TL;DR stat, the headline figure) should appear in at least 2 independent authoritative sources, not just one. Answer engines score a claim against the other sources retrieved for the query — a figure corroborated across multiple primaries wins; a lone or contrarian figure gets discarded. Note the second corroborating source in the table for your anchor stats. Single-source is fine for supporting numbers — reserve corroboration effort for the claims you build the article around.

**Step 4 — Identify chart candidates:**

Identify 1-2 data sets suitable for a chart (comparative percentages, before/after, ranked factors). Note chart type (bar, table, list) and data source.

**Output before moving to Phase 2:**

```
Statistics Research — [primary keyword]

| # | Stat | Source | URL | Tier | Date | Verified |
|---|------|--------|-----|------|------|----------|
| 1 | ...  | ...    | ... | 1    | ...  | Yes/No   |

Chart candidates:
- [Data set 1]: [chart type suggestion]
- [Data set 2]: [chart type suggestion]  (if applicable)
```

**How it connects downstream:**
- Statistics feed the brief's "Key Points to Cover" and "Unique Angle"
- Chart candidates become `[CHART: ...]` markers in the Phase 3 outline
- All stats used in the draft must come from this pre-verified list
- The QA gate checks "at least 3 specific numbers" — these satisfy that

**Research-quality gate (soft):** If this article leans on the `/information-gain` dossier (a data-heavy
or competitive topic), apply that skill's 5-dimension **research-quality rubric** and **FLOW citation
triple** before drafting — remediate a dossier scoring <70 (usually a Coverage / synthesis-echo
problem). For a light stats pass (the 5–8 above), the verify-3 step here is enough; don't over-gate a
thin-data topic.

---

### Image Research

**Step 1 — Search for images:**

Search in this order:
1. `site:pixabay.com [topic keywords]` (preferred — no attribution required)
2. If no results: `site:unsplash.com [topic keywords]`
3. Fallback: `site:pexels.com [topic keywords]`

**Step 2 — Extract CDN URLs:**

For each candidate image page, fetch with WebFetch and extract the `og:image` meta tag value — this is the direct CDN URL, not the page URL.
- Pixabay CDN pattern: `https://cdn.pixabay.com/photo/YYYY/MM/DD/.../filename.jpg`
- Unsplash CDN pattern: `https://images.unsplash.com/photo-<id>?w=1200&h=630&fit=crop&q=80`

**Step 3 — Verify CDN URLs:**

For each CDN URL: `curl -sI "[url]" | head -1` must return HTTP 200 or 301/302. If 403 or 404: discard and find a replacement.

**Step 4 — Write alt text:**

Write a descriptive alt text sentence for each verified image (10-125 chars, includes topic keywords naturally, describes what the image shows).

**Step 5 — Quantity note:**

Aim for 1-2 verified images. For purely technical content (spec tables, flowcharts) where no photo adds real value, 0 images is acceptable — note this explicitly.

**Output before moving to Phase 2:**

```
Images Research — [primary keyword]

| # | Platform | CDN URL | HTTP Status | Alt Text |
|---|----------|---------|-------------|----------|
| 1 | Pixabay  | https://cdn.pixabay.com/... | 200 ✓ | [alt text] |
| 2 | Unsplash | https://images.unsplash.com/... | 200 ✓ | [alt text] |
```

**How it connects downstream:**
- Verified image URLs become `![alt text](url)` placements in Phase 3 outline markers
- The Phase 4 draft embeds images after the most relevant H2 sections
- Phase 7 QA gate checks "alt text on all images" — these pass because alt text is written at research time

---

## Phase 2: Content Brief

**MANDATORY FIRST STEP — Keyword Register Check**

Before creating the brief, read `your-project/KEYWORD-REGISTER.csv` and check the planned secondary keywords and FAQ questions against it.

**For H2 secondary keywords:**
- Scan the "H2 Secondary Keywords" column for a match or close semantic equivalent
- If a match is found in another article: flag it and ask the user — "This secondary keyword [X] is already used as an H2 in Article #[N] ([Title]). Do you want to keep it here with a different section focus, move it to body copy only, or replace it with a different keyword?"
- Do not proceed past the check without a decision on every conflict
- If no conflicts found: state "No H2 secondary keyword conflicts found" before continuing

**For FAQ questions:**
- Scan the "FAQ Questions" column for a match or close semantic equivalent
- If a match is found: answer in 1-2 sentences max + link to that article. Do not fully answer
- If no conflicts found: state "No FAQ conflicts found" before continuing

**After the article is complete:** append the new row to KEYWORD-REGISTER.csv before moving to the next article.

---

Before drafting, create a brief:

```
# Content Brief: [Title]

## Target Keyword
Primary: [keyword]
Search volume: [if available from keyword-research]
Keyword difficulty: [if available from keyword-research]
Search intent: [if available from keyword-research]
Core keyword (parent): [if different from primary - indicates this is a section topic]

## Data-Driven Scope (If keyword-research provided data)
- Estimated word count (from data formula): [number] words
- Child keywords in cluster: [count]
- Priority tier: [Tier 1/2/3]
- Estimated traffic potential: [if ROI dashboard provided]

## Secondary Keywords (define BEFORE outlining)
List all secondary keywords that will be used in this article. For each one, decide at the brief stage whether it belongs in an H2 or in body copy. This prevents gaps during drafting and makes the keyword extract consistent for duplicate content review.

**Primary source:** Secondary keywords derived from SERP analysis and keyword cluster research.

**NeuronWriter supplement:** Cross-reference the NW header terms and body terms extracted in Phase 1. If any NW term is not already in your list AND it semantically fits the article's scope, add it. If it doesn't naturally fit, skip it — do not force NW terms in to satisfy the tool.

| Secondary Keyword | Placement (H2 / Body) | Target Section | Source |
|---|---|---|---|
| [keyword] | H2 | [section name] | SERP / NW |
| [keyword] | Body | [section name] | SERP / NW |
| [keyword] | H2 | [section name] | SERP / NW |

**Rule:** At least 2-3 secondary keywords must be assigned to H2 headers. The rest go in body copy of the most relevant section. Do not leave secondary keywords unassigned — if it's in the brief, it goes somewhere specific in the outline.

## FAQ Questions (define BEFORE outlining)
List all FAQ questions that will appear in this article. Confirm each one against the FAQ deduplication rule below before locking them in. Questions defined here = questions written — no additions or substitutions during drafting without re-checking deduplication.

**NeuronWriter supplement:** Review the NW question recommendations extracted in Phase 1. If any question is not already in your PAA list AND it's unique to this article (passes deduplication check), add it. If it duplicates another article's primary keyword, apply the standard redirect rule.

**AnswerThePublic supplement (if keyword-research used ATP):** Review ATP questions from keyword-research output. These are pre-validated by real search behavior. Use them to structure FAQ section and H2 headers where natural.

Planned FAQ questions:
1. [Question] — confirmed unique to this article (source: PAA/NW/ATP)
2. [Question] — confirmed unique to this article (source: PAA/NW/ATP)
3. [Question] — confirmed unique to this article (source: PAA/NW/ATP)

## Search Intent
[Informational / Commercial / Transactional]

## Content Type
[Pillar Guide / How-To / Comparison / Listicle / etc.]

## Target Word Count
[Based on competitor analysis]

## Audience
Who is searching this? What do they need?

## Unique Angle
What makes our take different?

## Key Points to Cover
- [Point 1]
- [Point 2]
- [Point 3]

## Questions to Answer (from PAA)
- [Question 1]
- [Question 2]
- [Question 3]

## FAQ Deduplication Check
Before writing FAQ questions, cross-check against the keyword-database-article-map cross-reference table.
A FAQ question that is essentially the primary keyword of another article should NOT appear in this
article's FAQ at all — not as a full answer, not as a redirect. Simply omit it.

Example: If "what is the difference between [option A] and [option B]" is the primary
keyword of a dedicated article, do not include it in this article's FAQ in any form. That question
belongs to that article. Leave it out entirely.

Questions that belong ONLY in this article's FAQ:
- [Question 1] — confirmed not the primary of another article
- [Question 2] — confirmed not the primary of another article

## Competitor Gaps to Fill
- [Gap 1]
- [Gap 2]

## Internal Links
- Link to: [related content on site]
- Link from: [existing content that should link here]

## CTA
What action should readers take?
```

---

## Phase 3: Outline

**Before building the outline, pull from the Content Brief:**
- Secondary keyword table → assign each H2-designated keyword to a specific section header
- FAQ questions list → slot them into the FAQ section as written (no new questions added here)

If a section in your outline has no secondary keyword assigned to it from the brief, check whether a body-copy keyword belongs in that section. Every secondary keyword from the brief must have a home in the outline before drafting starts.

### GEO/AEO Placeholder Markers

As you build the outline, insert these placeholder markers throughout. The outline is generated dynamically from SERP analysis — these markers are added to the generated structure, not to a fixed template.

- **After the intro section:** `> **TL;DR:** [placeholder — write after draft is complete]`
- **Under each H2:** `[ANSWER-FIRST: 40-60 words — stat + source + direct answer]`
- **Under each major H2:** `[CITATION CAPSULE: 40-60 word self-contained quotable passage]`
- **Image placement:** `[IMAGE: verified URL from Phase 1.5 — placed after most relevant H2]`
- **Chart placement:** `[CHART: data set from Phase 1.5 — placed in most relevant section]`

These markers become the targets that Phase 4 draft rules fill in. Do not leave placeholders in the published article — all must be replaced by actual content in the draft phase.

### Outline Approval Gate (mandatory human stop)

**Before drafting, present the full outline to the human reviewer and wait for explicit approval.**

Do not begin Phase 4 until the outline is approved. If the reviewer requests changes, update the outline and re-present before proceeding.

Structure the content based on type:

### Pillar Guide Structure (5,000-8,000 words)

```
1. Hook Intro (150-250 words)
   - Answer the title question immediately
   - Why this matters NOW
   - Who this is for (and who it's not for)

2. Quick Answer Section (200-300 words)
   - Direct answer for Featured Snippet
   - TL;DR for skimmers

3. Core Sections (3-5 major sections)
   - Each 800-1,500 words
   - Each answers a major sub-question
   - H2 headers with keyword variations

4. Implementation / How to Apply (300-500 words)
   - Specific actionable steps
   - Decision framework if applicable

5. FAQ Section (5-10 questions)
   - From PAA research
   - Schema-ready format
   - **Concise answers:** Keep each answer to 2-3 sentences max. If a question requires a longer explanation, give a brief direct answer and link to the relevant article for the full treatment.
   - DEDUPLICATION RULE: Before writing each FAQ question, check whether it is the primary
     keyword of another article in the database. If it is, omit the question entirely — do not
     include it as a full answer or a redirect. Only include questions this article uniquely owns.

6. Conclusion with CTA (150-200 words)
   - Summarize key takeaway
   - Clear next action
```

### How-To Tutorial Structure (2,000-3,000 words)

```
1. What You'll Achieve (150-200 words)
   - End result shown first
   - Time estimate
   - Prerequisites

2. Why This Method (200-300 words)
   - Context and alternatives
   - Why this approach works

3. Step-by-Step Instructions (1,200-2,000 words)
   - Numbered steps
   - One action per step
   - Troubleshooting inline

4. Variations / Advanced Tips (300-400 words)

5. Common Mistakes (200-300 words)

6. Next Steps with CTA (100-150 words)
```

### Comparison Structure (2,500-4,000 words)

```
1. Quick Verdict (200-300 words)
   - Bottom line recommendation
   - "Choose X if... Choose Y if..."

2. Comparison Table
   - 8-12 key differentiators
   - Pricing, best for, key features

3. Deep Dive: Option A (800-1,000 words)
   - What it is
   - Key features
   - Pros/cons
   - Best for
   - Real example

4. Deep Dive: Option B (800-1,000 words)
   - Same structure

5. Head-to-Head Comparison (300-500 words)
   - Specific scenarios
   - When to pick each

6. FAQ (3-5 questions)

7. Final Recommendation with CTA
```

### Listicle Structure (2,000-3,000 words)

```
1. Intro with Context (150-200 words)
   - Why this list matters
   - How items were selected

2. Quick Summary Table/List
   - All items at a glance
   - For skimmers

3. Individual Items (150-300 words each)
   - What it is
   - Why it's included
   - Best for / Use case
   - Limitations (honesty builds trust)

4. How to Choose (200-300 words)
   - Decision framework

5. FAQ (3-5 questions)

6. Conclusion with CTA
```

**Additional content types** (same GEO-marker rules apply — TL;DR, answer-first H2s, citation capsules,
image/chart placement). Use when the article fits one of these better than the four core types above.
(Template set adapted from the `claude-blog` content-templates library, MIT.)

### Data-Research Structure (1,500-2,500 words)

Built around original or hard-to-find data (feeds on the `/information-gain` dossier). The data IS the angle.

```
1. Headline Finding (150-200 words)
   - Lead with the single most striking stat (FLOW triple: year + named source + figure)
   - Why it matters to the reader's decision

2. Methodology / Where the Data Comes From (100-200 words)
   - Sources and how they were selected (primary sources only — builds trust)

3. Findings (3-5 sections, 300-500 words each)
   - One finding per H2, each opening answer-first with its key figure
   - Pair each data-heavy section with a chart/table (GEO multi-modal)

4. What It Means / Implications (200-300 words)
   - Translate the numbers into a decision or action

5. FAQ (3-5 questions)

6. Conclusion with CTA
```

### News-Analysis Structure (1,200-1,800 words)

For an industry development, standard change, or regulatory update. Time-sensitive — date it and anchor
the year in prose. Use only when something genuinely changed.

```
1. What Happened (100-150 words)
   - The development, stated plainly, with the date and source

2. Why It Matters (200-300 words)
   - Impact on the reader ([target audience])

3. The Details (400-600 words)
   - What changed, the specifics, who's affected

4. What To Do About It (300-400 words)
   - Concrete actions or decisions the change forces

5. FAQ (2-4 questions)

6. Bottom Line with CTA
```

### Product-Review Structure (1,500-2,500 words)

Single-product deep review (distinct from a multi-item Listicle/roundup). Institutional voice — assessed
against real specs and use cases, not a personal "I bought this."

```
1. Verdict First (150-250 words)
   - The recommendation up front: who it's for, who should skip it
   - Key specs at a glance ([key spec], [attribute], [attribute], [attribute], price)

2. Specs Table (8-12 rows)
   - The full spec sheet; the snippet/skimmer target

3. Where It Wins (400-600 words)
   - Concrete strengths tied to real jobs/use cases

4. Where It Falls Short (300-500 words)
   - Honest limitations (trust signal; never all-positive)

5. Best For / Alternatives (300-400 words)
   - Who should buy it; what to consider instead (link to comparison/collection)

6. FAQ (3-5 questions)

7. Final Verdict with CTA
```

### Case-Study Structure (1,500-2,200 words)

A real implementation/application (e.g. a business's [product] deployment). Strong E-E-A-T from
operational specifics — use only with real, attributable details; never fabricate a customer story.

```
1. The Situation (150-250 words)
   - Setup, constraints, what was at stake (numbers: [scale], [tools], budget)

2. The Problem (200-300 words)
   - The specific failure or cost being solved

3. The Approach (500-700 words)
   - What was chosen and why; the decision criteria and trade-offs

4. The Result (300-500 words)
   - Measurable outcome (energy / cost / downtime figures, with sourcing)

5. What To Take From It (200-300 words)
   - The transferable lesson for a reader in a similar spot

6. FAQ (2-4 questions)

7. Conclusion with CTA
```

### Thought-Leadership Structure (1,200-1,800 words)

An opinionated POV piece that takes a position (consistent with the brand's "pick a winner" voice).
Institutional POV, not personal memoir. Earn the take with evidence.

```
1. The Take (150-250 words)
   - State the position plainly in the first lines (no hedging)

2. Why The Conventional View Is Incomplete (300-400 words)
   - What most people get wrong, with specifics

3. The Case (500-700 words)
   - 2-3 arguments, each backed by data or operational reality

4. The Honest Counter (200-300 words)
   - Where the take has limits / when it doesn't apply (trust)

5. What It Means For You (150-250 words)
   - The decision the reader should make differently

6. Conclusion with CTA
```

---

## Phase 4: Draft

Write the first draft following these principles:

### The First 200 Words Rule

Within the first 200 words you must accomplish three things:

**1. Use the primary keyword** — naturally, in the first 1-2 sentences. Not forced, not repeated twice. Once, clearly.

**2. Answer the search query** — in the first 2-3 sentences. Don't make them scroll.

**3. State the conclusion** — tell the reader what they'll learn or decide by the end. This is the "so you'll know exactly what to do" sentence. It hooks the reader AND signals to Google that the article delivers on its title.

**Bad intro (fails all three):**
> "In today's rapidly evolving digital landscape, marketers are increasingly turning to artificial intelligence to streamline their workflows and enhance productivity..."

**Good intro (hits all three in ~80 words):**
> "AI marketing tools can automate 60-80% of repetitive marketing tasks. Here are the 10 that actually work, based on testing them across 50+ client accounts. By the end of this guide, you'll know exactly which tools fit your workflow — and which ones to skip."

The conclusion statement doesn't have to be a separate sentence — it can be woven into the hook. But it must be there. Readers who know where they're going stay longer. Readers who don't, bounce.

**Intro checklist (first 200 words):**
- [ ] Primary keyword used once, naturally
- [ ] Query answered directly (no build-up, no preamble)
- [ ] Conclusion stated (what the reader will know/be able to do)
- [ ] No AI preamble phrases ("In today's...", "Whether you're a...")

### TL;DR Box Rule

Immediately after the introduction (before the first H2 body section), write a TL;DR box:
- 40-60 words, self-contained — makes sense without reading the article
- Includes 1 statistic with source name (from Phase 1.5 verified list)
- States the key finding or recommendation
- Format: `> **TL;DR:** [summary]`
- This is a first-class AI citation target — AI systems frequently quote these verbatim

### Answer-First H2 Rule

Every H2 section opens with a 40-60 word paragraph that:
- Contains at least one specific statistic with source attribution (from Phase 1.5 verified list)
- Directly answers the heading's implicit question
- Pattern: `[Stat] ([Source](url), year). [Direct answer in 1-2 more sentences.]`
- If no relevant stat exists for a section, use the closest supporting evidence and note the gap

### Citation Capsule Rule

For each major H2 section, write one citation capsule — a 40-60 word self-contained passage designed so AI systems can extract and quote it directly:
- Must be self-contained (makes sense quoted out of context)
- Contains: one specific claim + one data point + source attribution
- Written in a declarative, quotable style
- Minimum 2 capsules per article; 1 per major H2 is ideal

### Citable Answer Block (GEO)

The 40-60 word answer-first opening wins featured snippets; AI *citation* favors a slightly longer, fully self-contained block. For each section that answers a discrete question, continue past the opening into a **~130-170 word self-contained answer block** — makes complete sense quoted out of context, carries one specific stat with a named source (corroborated across 2+ sources for the article's anchor claims — see Phase 1.5), and ends a thought rather than trailing into the next section. Open with the 40-60 word direct answer, then round the block out to ~130-170 words before the next sub-point.

**Multi-modal pairing:** Place the verified image/chart/table from Phase 1.5 *adjacent to* a citable answer block, not wherever it looks nice. Text-plus-visual passages are selected by AI answer engines at higher rates than text alone.

See `references/geo-checklist.md` for the full GEO methodology, the site-level AI-crawler allow-list (one-time robots.txt setup), and provenance/verify notes on the underlying figures.

### Win the Arbitration (claim sourcing for AI citation)

AI answer engines don't read your article as a document — they score each claim against three things: the model's existing training/consensus, the other sources retrieved for that query, and a source-quality filter. A claim is only cited if it wins that arbitration. Two rules follow:

**Consensus-aligned claims can run light. Contrarian claims need heavy corroboration.** The brand voice picks a winner — keep doing that. But know the cost: a take that *contradicts* the model's priors (e.g. "[option A] outlasts [option B]") gets discarded unless multiple independent authoritative sources back it in the text. A take that *aligns* with consensus needs only one good source. The more contrarian the claim, the more corroboration it carries — never less. Don't soften the opinion; arm it.

**Phrase claims with declarative authority.** State facts the way a primary source (a spec sheet, a standards body, a test report) would — flat and direct — not hedged like an aggregator. "A [specific configuration] delivers [figure] under [condition]" beats "generally, a larger [attribute] may offer more [benefit]." Hedging reads as low-confidence secondary content and loses to the source that just states the number. This is not license to overstate — trade-offs and limits are still acknowledged (E-E-A-T). It means: where you know the number, say it plainly and source it.

### The "So What?" Chain

For every point you make, ask "so what?" until you hit something the reader actually cares about:

> Feature: "Automated email sequences"
> So what? "Sends follow-ups without you remembering"
> So what? "You wake up to replies instead of a blank inbox"
> So what? "Close deals while you sleep"

Write from the bottom of the chain, not the top.

### Specificity Over Generality

**Weak:** "This tool saves time."
**Strong:** "This tool cut our email outreach from 4 hours to 15 minutes per day."

**Weak:** "Many marketers struggle with content."
**Strong:** "73% of marketers publish less than once per week. Here's why."

Numbers, examples, specifics. Always.

### Show Your Work

Don't just make claims. Show how you know:

> "After testing 23 AI writing tools over 6 months, three stood out..."

> "We analyzed 147 high-ranking articles in this space. The pattern was clear..."

> "When I implemented this for [client], the results were..."

Experience signals beat assertions.

### The Sentence Contribution Rule

Every sentence must do one of two things: explain the primary keyword or explain a secondary keyword. If it does neither, delete it.

**Test:** Point to the keyword this sentence serves. If you can't, cut it.

**Delete without hesitation:**
- "The breakdown above is useful." (evaluates content, explains nothing)
- "[Tangential option] is mentioned here purely for completeness." (justifies inclusion, explains nothing)
- "Now that we've covered X, let's move on to Y." (navigates content, explains nothing)
- "This section will help you understand..." (previews content, explains nothing)

The goal is the most concise article that fully answers the query. Every word that doesn't serve the reader's question dilutes the ones that do.

### NeuronWriter Term Usage

As you draft, keep the NW term lists from Phase 1 visible. Work through them section by section:

- **Title terms** — check that at least the strongest 1-2 appear naturally in the article title
- **Header terms** — where a NW header term describes a section you're already writing, use it as or in the H2. If it doesn't describe the section, skip it.
- **Body terms** — as you complete each section, scan the NW body term list. If an unused term is relevant to the section just written, work it in naturally. If it doesn't fit without forcing it, leave it out.

Do not write a sentence just to place a NW term. The term should slot into a sentence that would exist anyway.

---

## Phase 5: Humanize

AI-generated content has tells. Remove them ruthlessly.

The goal isn't "sounds okay." It's "sounds like a specific person wrote this based on real experience."

### The AI Detection Patterns

AI content fails in predictable ways. Learn to spot them:

**1. Word-Level Tells**

See `references/llm-words-to-avoid.md` for the full categorised list (90+ words, 40+ phrases,
sourced from the community-maintained GitHub Gist and multiple research sources).

Quick reference — the core 40 to Ctrl+F before publishing:
```
delve, leverage, utilize, foster, underscore, comprehensive, robust,
crucial, vital, essential, paramount, seamlessly, transformative,
groundbreaking, cutting-edge, revolutionary, innovative, game-changer,
landscape, realm, navigate, tapestry, embark, journey, resonates,
unveil, unlock, unleash, harness, supercharge, streamline, enhance,
empower, nuanced, multifaceted, profound, meticulous, effortlessly,
bolster, beacon
```

**2. Phrase-Level Tells**

These scream "AI wrote this":
- "In today's fast-paced world..."
- "In today's digital age..."
- "It's important to note that..."
- "When it comes to..."
- "In order to..." (just say "to")
- "Whether you're a... or a..."
- "Let's dive in" / "Let's explore"
- "Without further ado"
- "At the end of the day"
- "It goes without saying"
- "In conclusion" (especially at the end)
- "This comprehensive guide will..."
- "Are you looking for..." (fake questions)
- "Look no further"
- "Let's unpack this" / "Let's break it down"
- "Buckle up" / "Picture this"
- "Gone are the days of..."
- "Here's the kicker"
- "The possibilities are endless"
- "The bottom line..." (as a section closer)

Two more to flag on sight:
- **Opening with "So,"** — cut the "So," and start on the point.
- **Ending a section with a rhetorical question** — answer it or delete it; don't leave the reader hanging on a fake question.

**Empty connective transitions** — single words dropped in to glue sentences together, not because the logic needs them: *moreover, furthermore, additionally, notably, ultimately, that said, it's worth noting.* Cut them, or swap for a plain connective ("and," "but," "so") only where the sentence genuinely needs one. Same for stock openers like "in the ever-evolving world of..." and "navigate the world of..." — delete the runway and state the point.

**3. Structure-Level Tells**

AI has recognizable structural patterns:

- **The Triple Pattern**: Everything in threes. Three benefits. Three examples. Three subpoints. Humans are messier.
- **Perfect Parallelism**: Every bullet point same length, same structure. Too clean.
- **The Hedge Stack**: "While X, it's important to consider Y, but also Z." Never commits.
- **Fake Objectivity**: "Some experts say... others believe..." without taking a position.
- **Summary Sandwich**: Intro summarizes, body covers, conclusion summarizes again. Boring.
- **Empty Transitions**: "Now that we've covered X, let's move on to Y." Adds nothing.

**4. Voice-Level Tells**

The hardest to fix:

- **No Opinions**: Everything balanced, nothing claimed. Real experts have takes.
- **No Mistakes Mentioned**: Never wrong about anything, ever. Suspicious.
- **Generic Examples**: "For example, a business might..." instead of a real story.
- **Distance from Subject**: Writing about, not from experience of.
- **Uniform Certainty**: Every statement equally confident. Humans hedge where uncertain, commit where sure.

### Before/After Examples

**AI Version:**
> "Email marketing remains a crucial component of any comprehensive digital marketing strategy. When it comes to improving open rates, it's important to consider several key factors. First, crafting compelling subject lines is essential. Second, segmenting your audience allows for more targeted messaging. Third, timing plays a vital role in engagement."

**Human Version:**
> "I ignored email for two years. Social media was sexier. Then I looked at the numbers: email drove 3x the revenue of all social combined. Here's what actually moves open rates—the stuff that worked when we tested it across 12 client accounts."

---

**AI Version:**
> "In today's fast-paced business landscape, professionals are increasingly turning to automation tools to streamline their workflows and enhance productivity. These comprehensive solutions offer a myriad of benefits for organizations of all sizes."

**Human Version:**
> "Most automation tools are shelfware. You buy them, set them up, use them twice, forget they exist. Here are the three that actually stuck after a year of testing—and the 14 I wasted money on."

---

**AI Version:**
> "Whether you're a seasoned marketer or just starting your journey, understanding SEO fundamentals is crucial for success. Let's dive into the essential strategies that can help you navigate the complex landscape of search engine optimization."

**Human Version:**
> "SEO advice is 90% outdated garbage. The tactics that worked in 2019 will get you penalized now. I'm going to show you what's actually ranking in December 2024—pulled from 300+ sites we analyzed last month."

### Voice Injection Points

Human content has these. AI content doesn't. Add them:

**Personal experience with specifics:**
> "I made this mistake for two years. Cost me roughly $40K in lost revenue before someone on Twitter pointed out what I was doing wrong."

**Opinion with reasoning:**
> "Honestly, most SEO advice is written by people who've never ranked anything. They're regurgitating what they read somewhere else. Here's what I've actually seen work..."

**Admission of limitations:**
> "This won't work for everyone. If you're in YMYL niches, ignore this entirely—different rules apply. If you're B2B enterprise, probably not either."

**Specific examples from real work:**
> "When we implemented this for [specific client—an e-commerce brand in a competitive niche], their organic traffic went from 12K to 89K monthly in four months. Not because of any trick—because we fixed the structural issues killing their crawlability."

**Uncertainty where honest:**
> "I'm not 100% sure why this works. Best guess: the semantic density signals topical authority. But I've seen it work across 40+ sites, so I stopped questioning it."

**Tangents and asides:**
> "This is the part where most guides tell you to 'create quality content.' (Useless advice.) What does that actually mean? Here's the specific bar to clear..."

### Rhythm Variation

AI writes in monotonous rhythm—similar sentence lengths, parallel structures, predictable patterns. Fix it:

- Vary sentence length. Short punch. Then longer explanatory sentences that build out the context and add nuance that couldn't fit in a shorter form.
- Use fragments. For emphasis. Or drama.
- Start sentences with "And" or "But" when natural. Grammar rules exist to serve clarity, not the other way around.
- Include parenthetical asides (the kind of thing you'd say out loud if explaining to a friend).
- Ask questions. Then answer them. Or don't—leave some things hanging.
- One-word paragraphs.

Really.

**Quantified targets (check per paragraph):**
- At least one sentence **under 8 words** in every paragraph — the short punch that breaks the rhythm.
- **Never more than 3 long sentences in a row** — after the third, force a short one.
- **At most 1 em-dash per paragraph** — beyond that, switch to a comma, colon, period, or parentheses.

### The Primary-Source Register (Comparison / Listicle / Product-Review types)

AI models are explicitly instructed to be skeptical of "product recommendations" and heavily-SEO'd pages — the exact category your "best X," comparison, and buying-guide articles fall into. The defense is to read like a primary source, not an affiliate roundup. On these article types, strip the affiliate-listicle tells:

- **Unsourced superlatives** — "the best," "top-rated," "highly recommended" with no figure behind them. Replace with the spec that earns the verdict: "[specific measurable rating]," not "built to last."
- **Roundup filler** — "you can't go wrong with any of these," "there's an option for everyone." Pick a winner and say why, with numbers.
- **Commission-vibe phrasing** — "grab yours today," "check the latest price," manufactured urgency. The institutional voice assesses; it doesn't upsell.
- **Vague "best for"** — every "best for X" ties to a measurable threshold ("best for [use case] with [specific demand] — you need [threshold]"), not a mood.

The test: would a manufacturer's engineer or a trade-standards body write this sentence? If it reads like an Amazon-affiliate caption, rewrite it to the spec underneath.

### The Detection Checklist

Before publishing, run through:

```
[ ] No AI words — Ctrl+F the core 40 in references/llm-words-to-avoid.md
[ ] No AI phrases — check Section 2 of references/llm-words-to-avoid.md
[ ] No em dash overuse (—) — replace with comma, colon, period, or parens based on context
[ ] Not everything in threes
[ ] At least one personal opinion stated directly
[ ] At least one specific number from real experience
[ ] At least one admission of limitation or uncertainty
[ ] Sentence lengths vary (some under 5 words, some over 20)
[ ] Would I say this out loud to a smart friend?
[ ] Does it sound like a specific person, or a committee?
[ ] Can I identify whose voice this is?
[ ] Every sentence explains the primary or a secondary keyword — no meta-commentary, no filler transitions
```

### The Read-Aloud Test

Read your draft out loud. If you stumble, readers will too. If it sounds like a textbook, rewrite it. If you'd be embarrassed to read it to a colleague, it's not ready.

---

## Phase 5B: Deep Voice Pass (content-humanizer)

Phase 5 strips AI tells. This phase makes the article sound like a real person with real opinions wrote it. Run the **content-humanizer** skill (`skills/content-humanizer/SKILL.md`) on the draft.

### What to run

**Step 1 — Score the draft.**
Run `python skills/content-humanizer/scripts/humanizer_scorer.py` on the article file. This gives a 0-100 humanity score across 6 dimensions (AI vocabulary, sentence variance, passive voice, hedging, em-dashes, paragraph variety).

- **85+** → Skip to Phase 6. The draft already reads as human.
- **70-84** → Light pass. Run Mode 2 (Humanize) only — fix the flagged categories.
- **Below 70** → Full pass. Run Mode 2 then Mode 3 (Voice Injection).

**Step 2 — Humanize (Mode 2) if score < 85.**
Using the content-humanizer checklist (`skills/content-humanizer/references/ai-tells-checklist.md`):
- Replace any remaining AI vocabulary the Phase 5 word list missed
- Fix sentence rhythm — break uniform lengths, add short punches, vary cadence
- Replace generic claims with specifics (numbers, named sources, real examples)
- Vary paragraph structure — break SEEB patterns, add single-sentence paragraphs, asides
- Add friction and imperfection — mid-thought direction changes, honest qualifications

**Step 3 — Voice Injection (Mode 3) if score < 70.**
Using the voice techniques reference (`skills/content-humanizer/references/voice-techniques.md`) and the brand voice profile (`your-project/brand/voice-profile.md`):
- Match the brand's voice archetype (for your-project: Direct Expert — consequence-first, opinionated, numbers-backed)
- Inject personal anecdotes where the brand has relevant experience
- Add opinions without apology — pick a winner when the data supports it
- Apply the brand's rhythm signature consistently
- Nail the ending — hard cut or single action, not a summary

### SEO guardrails during this phase

The content-humanizer skill has zero SEO awareness. Protect these while humanizing:
- **Do not remove or rephrase H2s** that contain secondary keywords
- **Do not move the primary keyword** out of the first 1-2 sentences
- **Do not break internal/external links** or change anchor text
- **Do not delete FAQ sections** — rephrase for voice but keep the Q&A structure
- **Do not exceed ±10% of target word count** — tightening prose is fine, wholesale cuts aren't

### Re-score after the pass

Run the scorer again. Target: 80+ for publication. If a section scores low, fix that section rather than rewriting the whole article.

### When to skip this phase

- Article already scored 85+ after Phase 5
- Very short articles (under 800 words) where Phase 5 is sufficient
- Time-sensitive content where speed matters more than voice depth

---

## Phase 6: Optimize

### On-Page SEO Checklist

```
[ ] SEO title generated (≤60 chars, uses NeuronWriter title terms where natural)
[ ] Primary keyword in SEO title (front-loaded if possible)
[ ] Primary keyword in H1 (can match SEO title or differ slightly)
[ ] Primary keyword in first 100 words
[ ] Primary keyword in at least one H2
[ ] Secondary keywords mapped to sections — at least 2-3 used in H2s where natural
[ ] Secondary keywords NOT used in H2s placed in body copy of relevant sections
[ ] Primary keyword in meta description
[ ] Primary keyword in URL slug
[ ] Image alt text includes relevant keywords
[ ] Internal links to related content (4-8 per piece)
[ ] External links to authoritative sources (2-4 per piece) — nofollow applied automatically by step 3 of file output
```

### Title Optimization

Generate an **SEO title** optimized for search engines. This may differ from the H1 title displayed in the article.

**Format:** [Primary Keyword]: [Benefit or Hook] ([Year] if relevant)

**Examples:**
- "AI Marketing Tools: 10 That Actually Work (2025)"
- "What is Agentic AI Marketing? The Complete Guide"
- "n8n vs Zapier: Which Automation Tool is Right for You?"

**Title rules:**
- **Under 60 characters maximum** (hard limit — count before finalizing)
- Front-load the primary keyword
- Include terminology from the **NeuronWriter title terms** extracted in Phase 1 where natural
- Include a hook or differentiator
- Match search intent
- Do not force NW terms if they make the title awkward — clarity beats keyword stuffing

### Meta Description

**Format:** [Direct answer to query]. [Proof/credibility]. [CTA or hook].

**Example:**
> "AI marketing tools can automate 60-80% of repetitive tasks. We tested 23 tools over 6 months to find the 10 that actually deliver. See the results."

**Meta rules:**
- 160 characters maximum (Google truncates anything longer — count characters before finalising)
- Include primary keyword
- Compelling enough to click
- Match what the content delivers

### Header Structure

```
H1: Main title (one per page) — primary keyword front-loaded
  H2: Major section — use secondary keyword variation where it fits naturally
    H3: Subsection
    H3: Subsection
  H2: Major section — use secondary keyword variation where it fits naturally
    H3: Subsection
  H2: FAQ (if included)
    H3: Question 1
    H3: Question 2
```

Use headers for structure, not decoration. Each H2 should be a scannable summary of what follows.

**Do NOT use horizontal rules (`---`) as section dividers in articles.** H2 headers provide sufficient visual separation. The `---` divider renders as `<hr />` in HTML and adds unnecessary visual clutter to the published page.

**Secondary keyword placement in headers:**

Not every H2 needs a secondary keyword — forced keywords in headers read as spam and hurt trust. The rule is: if a secondary keyword naturally describes the section, use it in the H2. If it doesn't fit, leave the H2 as plain descriptive text.

**How to do it:**

1. Take your secondary keyword list (from the keyword-database-article-map or content brief)
2. For each major section in your outline, ask: does any secondary keyword naturally describe this section?
3. If yes — make that secondary keyword the H2 (or a natural part of it)
4. If no — write the H2 as the clearest description of the section, and use the keyword in the body copy instead

**Example:**

```
Article primary keyword: "how to choose [product]"
Secondary keywords: "[product] [key spec] requirements", "[attribute]",
                    "[option A] vs [option B]", "[attribute] selection"

Section about [key spec]:
  Bad H2:  "Understanding [Key Spec]" (keyword buried)
  Good H2: "[Key Spec] Requirements: How Much [Key Spec] Do You Need?"

Section about [attribute]:
  Bad H2:  "Choosing the Right [Attribute]" (keyword absent)
  Good H2: "[Attribute] Selection" (exact secondary keyword — clean and descriptive)

Section about [product] type:
  Bad H2:  "Which Type of [Product] Should You Buy?" (keyword absent)
  Good H2: "[Option A] vs [Option B]: Which Is Right for You?" (secondary keyword used)
```

**Header secondary keyword checklist:**
- [ ] At least 2-3 H2s include a secondary keyword naturally
- [ ] No H2 has a keyword jammed in awkwardly — if it reads forced, remove it
- [ ] Secondary keywords not used in H2s appear in body copy of relevant sections
- [ ] No secondary keyword is used in headers of OTHER articles that own that keyword (check the cross-reference table)

### Featured Snippet Optimization

**For definition snippets:**
- Put definition in first paragraph
- Format: "[Keyword] is [definition in 40-50 words]"

**For list snippets:**
- Use H2 for the question
- Immediately follow with numbered or bulleted list
- Keep list items concise (one line each)

**For table snippets:**
- Use actual HTML tables
- Include clear headers
- Keep data concise

### NeuronWriter Content Score Check (optional)

After completing the draft, you can run a score check against NeuronWriter before moving to Phase 7 QA.

```
POST https://app.neuronwriter.com/neuron-api/0.5/writer/evaluate-content

Headers:
  X-API-KEY: [from neuronwriter-config.md]
  Content-Type: application/json

Body:
{
  "query": "[query ID from Phase 1]",
  "html": "[full article HTML]",
  "title": "[article title]",
  "description": "[meta description]"
}
```

The response returns a content score. Review it to identify any high-priority terms that are still missing. Apply the same filter: only add a term if it fits naturally into an existing sentence or section. Do not pad the article to chase a score.

---

### Internal Linking Strategy

**Link density targets (by article length):**
- Standard articles (~1,000 words): 3–5 internal links
- Long-form content (2,000+ words): 10–20+ internal links
- Rule of thumb: ~1 internal link every 200–300 words

These are targets, not hard caps. Semantic relevance drives every link — never insert a link just to hit a count. If an article only has 4 semantically relevant targets, 4 links is correct. If it has 15 natural opportunities, use all 15.

**Link TO this content from:**
- Related pillar content
- Blog posts on similar topics
- Resource pages

**Link FROM this content to:**
- Deeper dives on subtopics mentioned
- Related tools or resources
- Conversion pages (where appropriate)
- Collection pages matching the article's product category (minimum 1 per article)

**Anchor text:**
- Use descriptive text, not "click here"
- Vary anchor text naturally — 70% exact match (target page's primary keyword) / 20% secondary keyword / 10% misc
- For collection page links: pull anchor text from the collection's secondary keywords in your keyword register (e.g., link to [Category A] collection using "[option A] [product]", link to [Category B] collection using "[option B] [product] system"). For blog article links: use natural variations of the primary keyword (note that your register may store H2 headings separately from secondary keywords — do not use H2 headings as anchor text)
- Anchor must fit grammatically in the sentence — don't force-fit a keyword that reads awkwardly
- Track anchor text per target URL in anchor-text-map.csv

**Link insertion style — no tacked-on cross-references:**

Every internal link must be woven into a sentence that makes its own point. The sentence should read naturally with or without the link — the link adds a path for the curious reader, not a detour from the content.

Banned patterns (tacked-on cross-references):
- "For more on X, see [Article Title]."
- "For a deeper look at X, see [Article Title]."
- "For the full comparison, see [Article Title]."
- "For complete details on X, see [Article Title]."
- "Learn more in our [Article Title] guide."
- "For a side-by-side comparison of X, see [Article Title]."
- "see our [Article Title] guide" (embedded or standalone)
- "see the [Article Title]" (embedded or standalone)
- Any sentence whose only purpose is to point the reader to another article.

Also banned:
- **"Related articles" footers** — lists of article titles at the bottom of the article (e.g., "**Related articles:** Article A | Article B | Article C"). All links belong in the body content, woven into sentences.
- **Plain-text article title references in FAQ answers** — e.g., "For more details, see the How Long Does a [Product] Last guide." Either weave a proper link into the FAQ answer or omit the reference entirely. FAQ answers should be self-contained (2–3 sentences max).

Required pattern: the link sits inside a sentence that already advances the article's argument. The anchor text is a natural phrase within that sentence — typically 2–4 words — not the full article title.

Bad — tacked-on:
> For a side-by-side comparison of installation methods across [material options], see [[Option A] vs. [Option B] for [Use Case]](url).

Bad — tacked-on (uses "see our"):
> For context on how [attribute A], [key spec], and [attribute B] relate, see our [[Attribute] to [Key Spec] guide](url).

Bad — related articles footer:
> **Related articles:** Article A | Article B | Article C

Good — woven in (sentence makes its own point):
> Both ends of any hose joint must be mechanically secured with [rated fittings](url), not friction fits or improvised adapters.

Good — woven in (link is a natural phrase in an argument):
> The [[option A] maintenance schedule](url) is simpler than [option B] — fewer service events, longer intervals — but each missed event carries a higher penalty.

Good — woven in (anchor text is a concept, not a title):
> A correctly sized dedicated circuit also reduces resistive [energy losses](url) over time — undersized wiring adds heat and wasted watts to every [product] cycle.

The test: delete the link and read the sentence aloud. If the sentence collapses into nothing ("For more on X, see ___"), the link was tacked on. If the sentence still makes a complete point, the link is woven in correctly.

**One link per target rule:**
No article should link to the same internal target (blog article, collection page, or calculator) more than once. If the same target URL appears twice in an article, keep the first instance and remove the duplicate. This applies to both body content and FAQ sections.

**Link strategy configuration (ask during Phase 2, before outline):**

Before selecting internal link targets, ask the user the following:

1. **Priority pages** — "Which pages are your highest-priority link targets right now?" These get first consideration when placing links. Examples: new collections, calculator/tool pages, under-performing articles the user wants to boost. If the user has no preference, default to under-linked articles (1–3 inbound in `anchor-text-map.csv`).

2. **Max inbound cap** — "What's your max inbound link cap? (default: 10)" The user may override the default for specific pages (e.g., "15 for the [tool] calculator, 10 for everything else"). Record any overrides and respect them when checking `anchor-text-map.csv`.

3. **Mandatory link types** — "Should every article include:"
   - A collection link? (default: yes — at least 1 collection link per article matching the product category)
   - A calculator/tool page link where contextually relevant? (default: yes)
   - A link to the pillar hub? (default: yes, if the article is a spoke in a pillar cluster)

Store the user's answers and apply them when placing links in Phase 5. If the user skips this step, use the defaults listed above.

**Link spacing rule:**
No two links — internal or external, in any combination — should appear within 200–300 words of each other. Links clustered together signal low-quality writing and dilute the value of each individual link. Distribute links evenly across the full length of the article.

Before finalizing, map out where every link sits and check the word-gap between each adjacent pair. If two links are closer than 200 words, either remove the less important one or move it to a section that currently has no links.

**Link saturation cap:**
No single article should receive more than 10 inbound internal links across the content network (unless the user has set a different cap for specific pages — see link strategy configuration above). Before linking to an article, check `anchor-text-map.csv` for its current `total_inbound` count. If the target is at its cap, find an alternative target with fewer inbound links and similar semantic relevance. Prioritize under-linked articles (1–3 inbound) when multiple relevant targets exist.

---

## Phase 7: Quality Review

### Editorial Line-Edit Audit (flag, don't rewrite)

Run this as the first pass of Phase 7 — a fine-tooth-comb read of the humanized draft that **flags violations without rewriting the article**. Phase 5 stripped the obvious AI tells in bulk; this pass catches what survived, line by line, and proposes surgical replacements for the human reviewer to approve. It is not a rewrite.

**Rules it audits against (defined in Phase 5 — apply them, don't re-list):**
- **Tics and stock phrases** — the Phrase-Level Tells list (incl. "buckle up," "picture this," "the bottom line," opening with "So," ending a section on a rhetorical question).
- **Banned words and empty connectives** — the core-40 (`references/llm-words-to-avoid.md`) plus *moreover, furthermore, additionally, notably, ultimately, that said*.
- **Rhythm** — the quantified targets: ≥1 sentence under 8 words per paragraph, ≤3 long sentences in a row, ≤1 em-dash per paragraph.

**Four audit-only checks (judgments, not bulk rules):**
- **Opening leads with the point** — flag any background, definition, or "in this post we'll cover" setup that delays the substance past the first sentence. (Cross-checks the First 200 Words Rule.)
- **Audience register** — written for a **[target buyer] making a considered purchase decision**; flag where it over-explains what this reader already knows, or formalizes below the brand's plain register.
- **Format that fights the piece** — flag a wall of text that should be broken up, or a list/table/header padding points that would read better as plain sentences. Do **not** impose a word count or restructure the draft.
- **Fact pass** — flag any statistic, name, or quote not traceable to the Phase 1.5 verified list as **unverified**, rather than leaving it in. Do not invent numbers.

**Voice to match:** your-project's institutional **Direct-Expert** voice — consequence-first, numbers-backed, picks a winner when the data is clear (`your-project/brand/voice-profile.md`). Suggested fixes must read in *that* voice, not stiffer or more generic.

**The discipline:** leave anything that already follows the rules exactly as it is — don't list it, don't touch it. A sentence that's fine stays fine. One row per flagged item only.

**Output — a single table, no rewritten draft:**

| Original | Rule broken | Suggested fix |
|---|---|---|
| [exact text from the draft] | [the rule it breaks] | [replacement in the Direct-Expert voice] |

Present the table to the human reviewer, apply the approved fixes to the draft, then run the checklists and QA gate below to confirm.

### Content Quality Checklist

```
[ ] Primary keyword used naturally in first 1-2 sentences
[ ] Conclusion stated within first 200 words (what reader will know/be able to do)
[ ] Answers title question in first 200 words
[ ] At least 3 specific examples or numbers
[ ] At least 1 personal experience or unique insight
[ ] Unique angle present (not just aggregation)
[ ] All claims supported by evidence or experience
[ ] No generic advice (could apply to anyone)
[ ] Would I bookmark this? Would I share it?
[ ] Every sentence explains the primary or a secondary keyword (Sentence Contribution Rule)
```

### Voice Quality Checklist

```
[ ] Reads naturally out loud
[ ] No AI-isms (delve, landscape, comprehensive)
[ ] No corporate speak (leverage, synergy)
[ ] Sentence length varies
[ ] Personality present
[ ] Would I actually say this to someone?
```

### SEO Quality Checklist

```
[ ] SEO title generated and ≤60 chars (hard limit — count before publishing)
[ ] SEO title includes NeuronWriter title terms where natural
[ ] Primary keyword in SEO title, H1, first paragraph
[ ] Secondary keywords mapped to H2s — at least 2-3 placed naturally
[ ] Meta description compelling and ≤160 chars (hard limit — count before publishing)
[ ] Internal links included (~1 per 200–300 words; 3–5 for ~1K words, 10–20+ for 2K+ words)
[ ] External links to authoritative sources (minimum 1, ideally 2-4) — nofollow applied automatically by step 3 of file output
[ ] No two links (internal or external) within 200–300 words of each other — map link positions and check gaps before finalizing
[ ] Alt text on all images
[ ] Headers create logical structure
[ ] FAQ section with schema-ready format
[ ] FAQ deduplication checked — no FAQ question is the primary keyword of another article
[ ] Any question that belongs to another article has been omitted entirely, not redirected
```

---

### Pre-File Generation QA Gate

**This is the hard stop before writing any files. Run every check, then output the full results table below. Do not write the .md or generate the .html until every item shows PASS. Fix the draft for any FAIL, then re-run that check.**

Output this table in full before writing the files — every row, every check, explicit PASS or FAIL. Skipping a row is not allowed.

```
## QA Gate — [Article Title]

### Automated Checks
| Check | Result |
|---|---|
| No metadata in .md file — starts with H1, no YAML/keyword blocks at top or bottom | PASS / FAIL |
| Word count: [actual] vs target [target] (within ±10%) | PASS / FAIL |
| SEO title: [actual char count] chars (≤60) | PASS / FAIL |
| Meta description: [actual char count] chars (≤160) | PASS / FAIL |
| Primary keyword in first 100 words | PASS / FAIL |
| AI phrases scan (core 40) | PASS (none) / FAIL ([phrase found]) |
| NW basic terms — all present | PASS / FAIL (missing: [terms]) |
| NW extended terms — all present | PASS / FAIL (missing: [terms]) |
| External links: [count] found (minimum 1) | PASS / FAIL |
| Avg sentence length: target 15-20 words (estimate from a sample of 10 sentences) | PASS / FAIL |
| Paragraph length: no paragraph exceeds 150 words (hard limit) | PASS / FAIL |
| Passive voice density: ≤10% of sentences (estimate from 2-3 sections) | PASS / FAIL |
| AI trigger word density: ≤5 per 1,000 words (not just presence — count per 1K) | PASS / FAIL |
| Flesch reading ease: estimated 60-70 (scan for long words + sentence length) | PASS / FAIL |
| Slop-v2 (run the content-metrics helper): burstiness ≥0.30 AND windowed TTR ≥0.40 AND <3 structural tics (Category 6) — see content-humanizer/references/ai-tells-checklist.md | PASS / FAIL |
| Cognitive load (articles >2,000 words only): no section OVERLOADED (≥2 signals at threshold), densest 2-3 sections checked — see references/cognitive-load.md | PASS / FAIL / N/A |

### Content Quality
| Check | Result |
|---|---|
| Primary keyword used naturally in first 1-2 sentences | PASS / FAIL |
| Conclusion stated within first 200 words | PASS / FAIL |
| Title question answered within first 200 words | PASS / FAIL |
| At least 3 specific numbers or examples | PASS / FAIL |
| At least 1 unique insight or angle not in competitors | PASS / FAIL |
| Uniqueness vs nearest sibling article: >40% of content is unique to this article (not a near-duplicate of a comparison/cluster/hub sibling) — see references/thin-content.md | PASS / FAIL |
| All claims supported by evidence or experience | PASS / FAIL |
| Arbitration: contrarian claims (those bucking model consensus) carry 2+ independent authoritative sources; claims stated with declarative authority, not hedged | PASS / FAIL |
| No generic advice (advice specific to this topic) | PASS / FAIL |
| Every sentence explains primary or a secondary keyword | PASS / FAIL |
| TL;DR box present (from GEO section — cross-check) | PASS / FAIL |
| Answer-first format: ≥60% of H2 sections open with stat + source | PASS / FAIL |

### Voice Quality
| Check | Result |
|---|---|
| No AI-isms: delve, landscape, comprehensive, robust, etc. | PASS / FAIL |
| No corporate speak: leverage, synergy, utilize, etc. | PASS / FAIL |
| No tics or empty connectives: buckle up, picture this, the bottom line, opening "So,", section-ending rhetorical question, moreover/furthermore/additionally/notably/ultimately/that said | PASS / FAIL |
| No em dash overuse (—) — Ctrl+F for `—`; ≤1 per paragraph, replace extras with comma/colon/period/parens | PASS / FAIL |
| Sentence length varies — ≥1 sentence under 8 words per paragraph, never >3 long sentences in a row | PASS / FAIL |
| Reads naturally out loud (no textbook stiffness) | PASS / FAIL |
| Sounds like a specific person, not a committee | PASS / FAIL |
| Editorial line-edit audit run; every flagged violation fixed or accepted by reviewer (see Editorial Line-Edit Audit) | PASS / FAIL |
| Primary-source register (comparison/listicle/review types): no unsourced superlatives, roundup filler, or commission-vibe phrasing; every "best for" ties to a measurable threshold | PASS / FAIL / N/A |

### SEO Quality
| Check | Result |
|---|---|
| Primary keyword in SEO title, H1, and first paragraph | PASS / FAIL |
| SEO title uses NW title terms where natural | PASS / FAIL |
| At least 2-3 secondary keywords used in H2s naturally | PASS / FAIL |
| Internal links: [count] (~1 per 200–300 words; 3–5 for ~1K, 10–20+ for 2K+) | PASS / FAIL |
| No two links within 200 words of each other | PASS / FAIL |
| No tacked-on cross-reference links ("For more on X, see [Article]") — all links woven into content sentences | PASS / FAIL |
| No duplicate internal link targets — each target URL appears at most once per article | PASS / FAIL |
| No "Related articles" footer — all links are in body content | PASS / FAIL |
| FAQ section present with schema-ready format | PASS / FAIL |
| FAQ questions are H3 headings under an H2 "FAQ" header (not bold, not plain text) | PASS / FAIL |
| FAQ deduplication checked — no question is PK of another article | PASS / FAIL |
| Meta description includes a specific statistic (a number with source/context) | PASS / FAIL |
| External links: at least 1 is Tier 1-2 (gov, edu, major research); remainder Tier 3 max | PASS / FAIL |
| Link freshness (refresh/rewrite only): every pre-existing outbound link audited — none >2yr stale, broken, or secondary where a fresher primary exists; replacements re-anchored — see references/link-refresh.md | PASS / FAIL / N/A |
| Schema: correct types planned (BlogPosting/Breadcrumb are theme-auto; ItemList/Product metafield for roundup/comparison); multi-type pages use one `@graph` with `@id` refs — see skills/seo-schema | PASS / FAIL / N/A |

### E-E-A-T (Who/How/Why gate + scored 4×25 rubric)

**Step 1 — Helpfulness pre-gate (all three must PASS before scoring).** This is Google's
helpfulness heuristic; a weak answer on any line is a content-quality problem, not a polish problem.

| Check | Result |
|---|---|
| WHO: authority is clear — brand/Organization identity established, About/contact reachable. Institutional voice is fine; do NOT invent author personas or fake bylines | PASS / FAIL |
| HOW: process/sourcing is transparent — original data, hands-on testing, or named primary sources are shown, not asserted | PASS / FAIL |
| WHY: written to help the reader decide or do something, not to chase rankings | PASS / FAIL |

**Step 2 — Score each dimension /25, then total.** Score honestly against the criteria; this is a
line item, not a vibe.

| Dimension | Score | Criteria |
|---|---|---|
| Experience /25 | __/25 | First-hand / operational specifics: tested results, real figures, worked examples, proprietary data (institutional voice — "we tested / in the field," not personal memoir) |
| Expertise /25 | __/25 | Accurate, nuanced, technically correct; correct terminology; no hand-waving or generic filler |
| Authoritativeness /25 | __/25 | Authoritative sources cited (gov/edu/standards bodies/manufacturers); consistent with the site's topical authority in this cluster |
| Trustworthiness /25 | __/25 | Claims sourced; dates where relevant; no overstatement; trade-offs and limitations acknowledged |
| **E-E-A-T total ≥70/100 AND no single dimension <13/25** | PASS / FAIL | |
| AI citation readiness: blocks are quotable, sourced, and schema-ready (cross-check GEO section) | PASS / FAIL |

### GEO / AI Citation Readiness
| Check | Result |
|---|---|
| TL;DR box present (40-60 words, includes a stat, standalone) | PASS / FAIL |
| Answer-first format on ≥60% of H2 sections | PASS / FAIL |
| Citation capsules present in major sections (≥2) | PASS / FAIL |
| Section word count: ≥50% of H2 sections are 120-250 words | PASS / FAIL |
| Key sections contain a self-contained ~130-170 word citable answer block (stat + source) | PASS / FAIL |
| Multi-modal: ≥1 citable section paired with a relevant image/chart/table | PASS / FAIL |
| Anchor/citation-priority stats corroborated across 2+ independent authoritative sources (see Phase 1.5) | PASS / FAIL |
| Extraction independence: every H2 self-describing (retrievable verbatim by the query); no section depends on a definition introduced in an earlier section | PASS / FAIL |
```

(Site-level GEO enablement — AI-crawler allow-list, SSR, brand mentions — is one-time setup, not a per-article check. See `references/geo-checklist.md`.)

**Rule:** Every FAIL must be fixed before writing files. After fixing, re-run only the affected checks and update the table. When all rows show PASS — write the .md, generate the HTML, run nofollow.

---

## Output format

The final deliverable is publication-ready content:

```
# [H1 Title — Article Heading]

[Full article content with proper H2/H3 structure]

## FAQ

### [Question 1]
[Answer]

### [Question 2]
[Answer]

<!-- ARTICLE-NOTES
SEO Title: [Max 60 characters — uses NeuronWriter title terms where natural — count before publishing]
Meta Description: [Max 160 characters — count before publishing]
Internal links: [Link 1], [Link 2], ...
Schema: Article + FAQ
FAQ Metafield: [Pipe-separated Q&A pairs: Q1|A1||Q2|A2||Q3|A3 — see skills/faq-jsonld/SKILL.md]
-->
```

Everything above the `<!-- ARTICLE-NOTES` marker is article content that pandoc converts to HTML. Everything inside the comment block is invisible to readers and Shopify. Never place metadata, link lists, or schema notes outside the comment block.

### File output — both formats required

After writing the article, save two files:

**1. Markdown file** — save to the `Written Articles` folder:
```
your-project/Written Articles/[article-slug].md
```

**No metadata in the .md file.** The markdown file must contain ONLY the article content — starting with the H1 heading. Do not include YAML front matter, keyword notes, query IDs, word count targets, pillar labels, or any other planning metadata. All of that is tracked in KEYWORD-REGISTER.csv. Pandoc converts everything in the .md file to visible HTML, so any notes at the top or bottom will appear on the live page.

If you need to leave notes for future reference within the file, use an HTML comment block at the very bottom, after all article content:
```
<!-- ARTICLE-NOTES
primary_keyword: "example keyword"
nw_query_id: abc123
Any other notes here — pandoc passes HTML comments through but they are invisible to readers.
-->
```

**2. HTML + nofollow** — run your publish step, the step you run after saving the draft (converts Markdown→HTML and applies nofollow in one pass):
```
# run your publish step for "[article-slug]"  (MD→HTML, nofollow, word count + link-spacing check)
```

This step: (a) prints word count + link spacing results, (b) runs pandoc with `--wrap=none` so external links are never line-broken, (c) applies nofollow to external links. The `--wrap=none` flag is required — without it pandoc splits `<a` and `href=` across lines and the nofollow regex misses the link.

Keep these steps in a single reusable publish step rather than throwaway one-off scripts.

**3. FAQ metafield** — generate the pipe-separated FAQ value from the article's FAQ section and store it in your keyword register. Upload to Shopify via your metafield upload step (Shopify GraphQL), single or batch. See `skills/faq-jsonld/SKILL.md` for format details.

All steps must complete before the task is marked complete.

---

## Example: Creating SEO content from keyword research

### Input from keyword-research skill:

```
Target: "what is agentic AI marketing"
Cluster: agentic AI, AI marketing agents, autonomous marketing
Intent: Informational
Content type: Pillar guide
Priority: Critical (category definition opportunity)
```

### SERP analysis findings:
- Top results are thin (500-1,000 words)
- No comprehensive guide exists
- PAA questions unanswered well
- Opportunity to define the category

### Content brief created:
- 5,000+ word pillar guide
- Unique angle: Practitioner perspective with real implementations
- Include: Definition, examples, tools, how to implement, future outlook
- Answer all PAA questions
- Target Featured Snippet with clear definition

### Draft following pillar guide structure:
- Hook: "AI agents can now run marketing campaigns without you. Here's what that actually means."
- Quick answer section for snippet
- Deep sections on: What it is, How it works, Real examples, Tools, Implementation
- FAQ from PAA research
- CTA to community/resources

### Humanized with:
- Personal experience running AI marketing campaigns
- Specific metrics from real implementations
- Honest limitations acknowledged
- Conversational tone throughout

### Optimized with:
- Keyword in title, H1, first paragraph
- Secondary keywords in H2s
- Internal links to related content
- FAQ schema ready

---

## How this connects to other skills

**Input from:**
- **keyword-research** → Provides target keyword, cluster, intent, content type
- **positioning-angles** → Provides unique angle for differentiation
- **brand-voice** → Provides voice profile for consistent tone

**Uses:**
- **direct-response-copy** → For CTAs and conversion elements within content
- **content-humanizer** → Deep voice pass after drafting (Phase 5B) — scores humanity 0-100, strips remaining AI patterns, injects brand voice

**The flow:**
1. keyword-research identifies the opportunity
2. positioning-angles finds the unique angle
3. brand-voice defines how it should sound
4. **seo-content creates the actual piece**
5. content-humanizer runs the deep voice pass (Phase 5B)
6. direct-response-copy punches up CTAs

---

## Reference: E-E-A-T Examples

See `references/eeat-examples.md` for 20 best-in-class examples of human-written content across verticals:

**Marketing/Business:**
- Paul Graham, Wait But Why, Stratechery, James Clear, Backlinko, Lenny's Newsletter, Derek Sivers

**Finance/Economics:**
- Matt Levine (Money Stuff), Morgan Housel (Psychology of Money)

**Technical/Engineering:**
- Julia Evans, Dan Luu, Shopify Engineering Blog

**Healthcare/Science:**
- Dr. Peter Attia, Dr. Siddhartha Mukherjee

**Enterprise/B2B:**
- First Round Review, Rosalyn Santa Elena (RevOps)

**Specialized Verticals:**
- Brian Krebs (Cybersecurity), Ken White (Legal), Katrina Kibben (HR/Recruiting), J. Kenji López-Alt (Food Science)

Study these patterns. The goal is content that reads like these writers—not like AI trained on generic web content.

---

## The test

Before publishing, ask:

1. **Does it answer the query better than what's ranking?**
2. **Would an expert in this field approve of the accuracy?**
3. **Would a reader bookmark or share this?**
4. **Does it sound like a person, not a content mill?**
5. **Is there at least one thing here they can't find elsewhere?**
6. **Does it pass the AI detection checklist?** (Phase 5)
7. **Does it match the quality bar of the E-E-A-T examples?**

If any answer is no, revise before publishing.
