---
name: internal-linking
description: "Automatically insert internal links into published articles using intelligent semantic matching and anchor text variation. Use when adding internal links to existing content, updating link profiles, or implementing internal linking strategy across a content cluster. Triggers on: add internal links to X, insert links in article, internal link article X, link article cluster. Outputs updated article with strategically placed internal links ready for API update."
---

# Internal Linking Automation

Internal linking is critical for SEO and user experience, but doing it manually is tedious and inconsistent. This skill automates the entire process: extracting link targets, mapping to URLs, finding optimal insertion points using semantic matching, varying anchor text, and updating via API.

The goal: Every article gets its internal links placed in the most contextually relevant locations, with anchor text variation that looks natural and avoids over-optimization.

---

## The core job

Transform an article's internal link suggestions into **strategically placed, contextually relevant links** that:
- Are inserted where context best matches the target article's intent
- Use varied anchor text (70% exact match, 20% secondary keywords, 10% miscellaneous)
- Are evenly distributed throughout the article (no clustering)
- Include the correct full URLs
- Are ready to update via Shopify API

---

## The workflow

```
CONFIGURE → IDENTIFY → MAP → ANALYZE → PLACE → PREVIEW → UPDATE
```

---

## Phase 0: Link Strategy Configuration

Before touching any article, gather the user's inputs and preferences. **Do not skip this phase** — the user's answers drive every decision in Phases 1–6.

### Step 0.1 — Collect required files

Ask the user for the following. Do not assume file paths — the user tells you where each one lives:

1. **Article file(s) to process** — Which markdown file(s) need internal links added or updated? Can be a single article or a batch.

2. **Link target pool** — "Where is the full list of link targets I should pull from?" This is the master list of every URL the article could potentially link to. It might be:
   - A URL list file (e.g., `article-urls.txt`)
   - A CSV with slugs and URLs (e.g., `shopify-article-ids.csv`, `KEYWORD-REGISTER.csv`)
   - A combination of files (blog URLs in one file, collection URLs in another, calculator/tool page URLs provided separately)

   **Load the entire pool before analyzing the article.** Every URL in the pool is a candidate — don't limit yourself to links the article already contains or articles in the same pillar.

3. **Keyword register** — File that maps article titles/slugs to primary keywords, secondary keywords, and pillar assignments (e.g., `KEYWORD-REGISTER.csv`). Used for anchor text selection and semantic matching.

4. **Anchor text map** — File that tracks existing anchor text usage per target URL (e.g., `anchor-text-map.csv`). Used to maintain the 70/20/10 distribution and check inbound link counts.

5. **Article ID mapping** — File that maps local filenames to Shopify article IDs and URL handles (e.g., `shopify-article-ids.csv`). Needed because **local filenames often differ from Shopify URL slugs** — slugs are finalized at upload time and may be adjusted based on keyword data.

### Step 0.2 — Ask user preferences

Ask the user the following before starting analysis:

1. **Max links per article** — "How many internal links should each article have?" Provide the default range as a reference:
   - ~1,000 words: 3–5 links
   - ~2,000 words: 6–10 links
   - 3,000+ words: 10–20 links
   - Or: ~1 link per 200–300 words

   The user may set a specific cap (e.g., "no more than 8") or accept the default range.

2. **Priority targets** — "Are there any pages you want to prioritize as link targets?" Examples: new articles that need inbound links, under-performing pages, collection pages, calculator/tool pages. If the user has no preference, default to under-linked articles (1–3 inbound in anchor-text-map.csv).

3. **Mandatory link types** — "Should every article include:"
   - At least 1 collection page link? (default: yes)
   - A link to the pillar hub? (default: yes, if the article belongs to a pillar cluster)
   - A calculator/tool page link where contextually relevant? (default: yes)

4. **Max inbound cap** — "What's the max inbound link cap per target? (default: 10)" The user may override for specific pages. Record any overrides and check `anchor-text-map.csv` before linking to any target that might be near its cap.

5. **Articles to skip** — "Are any articles locked / off-limits for editing?" (e.g., live articles that shouldn't be modified). These articles still count as link targets but their source content won't be changed.

### Step 0.3 — Build the working link pool

After collecting files and preferences:

1. Load the full target pool into memory — every URL the article could link to
2. Cross-reference against the anchor text map to tag each target with its current inbound count
3. Flag any targets already at or above the inbound cap
4. Mark the user's priority targets for preferential placement
5. Note any locked/skip articles

Present a summary to the user before proceeding:

```
Link target pool: [X] total URLs
  - Blog articles: [X]
  - Collection pages: [X]
  - Other (calculators, tools): [X]
At inbound cap (≥10): [X] targets
Priority targets: [list or "none specified"]
Locked articles (read-only): [list or "none"]
```

Confirm with the user, then proceed to Phase 1.

---

## Phase 1: Identify Link Targets

Using the link target pool and preferences from Phase 0, identify which targets belong in this article.

### Step 1.1 — Catalog existing links

Read the article markdown file and list every internal link already present:
- Scan for markdown links: `[anchor text](https://example.com/...)`
- Note the line number, anchor text, and target URL for each
- Cross-reference against the anchor text map for completeness

### Step 1.2 — Find new link opportunities from the full pool

Scan the **entire link target pool** (from Phase 0) against the article's content. For each target in the pool, check whether the article discusses a topic that's semantically relevant to that target. Don't limit candidates to links the article already contains — the goal is to find every natural opportunity.

Sources for matching:
- The target's primary keyword and secondary keywords (from the keyword register)
- Semantic overlap between the article's sections and the target's topic
- The user's priority targets (from Phase 0) — give these extra weight
- Under-linked targets (1–3 inbound) that fit the article's content

### Step 1.3 — Respect constraints

Before adding any target to the candidate list, verify:
- The target is not already at its inbound cap (from Phase 0 pool summary)
- The target is not already linked in this article (one link per target rule)
- The article is not on the skip/locked list (if processing a batch)

### Step 1.4 — Clean up legacy patterns

If the article contains any of these, flag them for removal:
- **"Related articles" footers** — lists of article titles at the bottom. Remove the footer and weave any relevant links into the body.
- **Tacked-on cross-references** — "see our [guide]", "For more on X, see [Article]", etc. Rewrite as woven-in links or remove entirely.
- **Plain-text article references** — unlinked mentions of article titles (e.g., "see the How to Choose [Product] guide"). Either convert to a proper woven-in link or delete.

---

## Phase 2: Map Titles to URLs (Enhanced with Parent-Child Data)

For each article title extracted in Phase 1, you need to determine:
1. The target article's filename/slug
2. The full URL to link to
3. The target article's primary keyword
4. The target article's secondary keywords
5. **NEW:** The target article's core_keyword (parent) if available from keyword-research data

### Step 2.1 — Map title to primary keyword

Read `KEYWORD-REGISTER.csv` and find the row where the article title (or a close match) appears.

Extract:
- Primary keyword
- H2 secondary keywords
- Filename (if available in your tracking)

**Example:**
```
Title in article: "How to Choose [Product]"
KEYWORD-REGISTER match: Primary keyword = "how to choose [product]"
```

### Step 2.2 — Map to URL

Use the primary keyword or title to find the article handle in `shopify-article-ids.csv`.

Then look up the full URL in `article-urls.txt`.

**Example:**
```
Title: "How to Choose [Product]"
→ Match in shopify-article-ids.csv: filename = "how-to-choose-product"
→ Match in article-urls.txt: https://example.com/blog/how-to-choose-product
```

**Build a link map:**
```
| Target Title | Primary Keyword | Secondary Keywords | Full URL |
|---|---|---|---|
| How to Choose [Product] | how to choose [product] | [product] [attribute], [product] calculator | https://example.com/blog/how-to-choose-product |
| [Option A] vs [Option B] | [option A] vs [option B] | [attribute] comparison, cost analysis | https://example.com/blog/option-a-vs-option-b |
```

---

## Phase 3: Analyze Article Content (Enhanced with Parent-Child Priority)

For each link target, you need to find the best place in the current article to insert the link.

**NEW - Parent-Child Priority:**
If keyword-research provided core_keyword data, prioritize linking to parent (core_keyword) pages:

```
Priority 1: Links to this article's core_keyword parent (upward linking)
Priority 2: Links to related pillar pages (cross-cluster)
Priority 3: Links to sibling articles (same parent)
```

**Why this matters:**
- Parent pages (high volume keywords) should receive more link equity
- Proper hierarchy signals topical authority to Google
- Prevents linking to spoke pages when pillar exists

### Step 3.1 — Identify candidate locations

Read the article content (excluding the intro, FAQ, and conclusion sections — links should go in the body content only).

For each link target, search the article for mentions of:
- The target article's primary keyword (exact or partial match)
- The target article's secondary keywords
- Semantically related terms

**Example:**
```
Link target: "How to Choose [Product]"
Primary keyword: "how to choose [product]"
Secondary keywords: "[product] [attribute]", "[product] calculator"

Scan article for:
- "choose" + "[product]"
- "[attribute] requirements"
- "choosing"
- "calculate [attribute]"
```

### Step 3.2 — Evaluate context quality

For each candidate location, evaluate the surrounding context (±2 sentences).

**Good context:**
- The paragraph is discussing a topic directly related to the target article's intent
- The sentence makes its own point with or without the link — the link adds a path for the curious reader
- The anchor text is a natural 2–4 word phrase within the sentence, not the full article title

**Bad context:**
- The mention is tangential or brief
- The link would interrupt the flow
- The paragraph already has another link (violates spacing rule)
- The sentence exists only to point to another article (tacked-on cross-reference)

### Step 3.3 — Select best location per link

Choose the single best location for each link based on:
1. **Semantic relevance** — How well does the context match the target article's intent?
2. **Flow** — Does the link feel natural in the sentence?
3. **Distribution** — Is this location far enough from other links?

**Distribution rule:** No two links should appear in the same paragraph. Aim for at least 200-300 words between links.

**One link per target rule:** An article should link to any given internal target (blog post, collection, or calculator) no more than once. If the target is already linked somewhere in the article, do not add a second link to the same URL — even with different anchor text.

---

## Phase 4: Select Anchor Text

For each link, select the anchor text based on the **anchor text variation strategy.**

**CRITICAL:** The 70/20/10 distribution applies **per target URL across your entire website**, not per article being edited.

If "how-to-choose-product" receives 10 internal links from various articles, those 10 anchor texts should collectively be:
- **70% Exact Match** (7 links) — Use the target article's PRIMARY keyword
- **20% Secondary Keywords** (2 links) — Use one of the target article's H2 SECONDARY KEYWORDS from KEYWORD-REGISTER.csv
- **10% Miscellaneous** (1 link) — Use a descriptive phrase (not from keyword lists)

### Step 4.1 — Look up target article keywords

For each link being inserted, look up the **target article** in KEYWORD-REGISTER.csv:

Extract:
- **Primary Keyword** — For exact match anchor text
- **H2 Secondary Keywords** — For secondary anchor text options (pipe-separated list)

**Example:**
```
Target article: "How to Choose [Product]"
Primary keyword: "how to choose [product]"
H2 Secondary Keywords: "[Attribute] Requirements | [Product] [Key Spec] | [Product] [Attribute] | [Key Spec] | Selection Chart"
```

### Step 4.2 — Check anchor text map for target URL

Read `your-project/anchor-text-map.csv` and filter for all rows matching the **target URL**.

Count anchor types for that specific URL:
```csv
target_url,anchor_text,usage_count,anchor_type,last_used_date
https://example.com/blog/how-to-choose-product,how to choose [product],3,exact,2026-02-20
https://example.com/blog/how-to-choose-product,[attribute] requirements,1,secondary,2026-02-19
https://example.com/blog/how-to-choose-product,this guide,1,misc,2026-02-18
```

Calculate current distribution for this URL:
- Total links to this URL: 5 (3 exact + 1 secondary + 1 misc)
- Exact: 3/5 = 60%
- Secondary: 1/5 = 20%
- Misc: 1/5 = 20%

### Step 4.3 — Determine next anchor type needed

Based on the current distribution for this specific target URL:
- If exact match % is < 70% → use **exact match** (primary keyword)
- Else if secondary % is < 20% → use **secondary keyword** (from H2 Secondary Keywords list)
- Else if misc % is < 10% → use **miscellaneous**
- Else → use exact match (to maintain 70/20/10 balance)

**In the example above:** Exact is 60%, so the next link should use exact match to move toward 70%.

### Step 4.4 — Select specific anchor text

Once you know the anchor type needed:

**For Exact Match:**
- Use the target article's primary keyword from KEYWORD-REGISTER.csv
- Example: "how to choose [product]"

**For Secondary:**
- Choose from the target article's H2 Secondary Keywords from KEYWORD-REGISTER.csv
- Pick one that hasn't been used recently AND fits naturally in the context
- Example: "[attribute] requirements", "[attribute] selection", "[key spec]"

**For Miscellaneous:**
- Use a descriptive phrase that's NOT in the keyword lists
- Examples: "this guide", "complete methodology", "detailed comparison", "read more"

**Choose the anchor text that:**
1. Moves the distribution toward 70/20/10 for this target URL
2. **Fits grammatically into the sentence** — The anchor text MUST make grammatical sense when inserted. Never break sentence structure to insert a keyword.
3. Appears naturally in the candidate location (or can be inserted naturally)
4. Hasn't been used recently for this URL (prefer variety within each type)

**CRITICAL RULE:** Anchor text must fit naturally into the sentence grammar. If the exact primary keyword doesn't fit grammatically, use a natural variation from the secondary keywords list OR adjust the insertion location.

**Bad example:**
```
Before: "Most [product] types come in [option E] and [option F] configurations."
Wrong: "Most [product] types come in [[option E] vs [option F]] configurations." ❌
```

**Good example:**
```
Before: "Most [product] types come in [option E] and [option F] configurations."
Correct: "Most [product] types come in [[option E] and [option F]](URL) configurations." ✓
```

### Step 4.5 — Determine insertion method

Two insertion methods:

**Method A: Replace existing text**
If the exact anchor text or a close match already appears in the candidate sentence, replace it with the link.

Example:
```
Before: "You'll need to calculate your [attribute] requirements before buying."
After: "You'll need to calculate your [[attribute] requirements](URL) before buying."
```

**Method B: Extend sentence with a clause containing the link**
If the anchor text doesn't appear naturally, extend an existing sentence with a clause that makes its own point and contains the link as a natural phrase.

**CRITICAL:** Never use tacked-on patterns like "see our [guide]", "For more on X, see [Article]", or "Learn more in our [Article]." The sentence must make a point even without the link.

Example:
```
Before: "Choosing is the first step."
After: "The [selection process](URL) is the first step — getting the [attribute] wrong by even 20% means the [product] underperforms under load."
```

Bad (banned — tacked-on):
```
After: "Choosing is the first step — see our guide on [how to choose [product]](URL) for the complete methodology."
```

---

## Phase 5: Preview Changes

Before making any updates, present the proposed changes to the user for approval.

**Format:**
```
Article: product-types.md
Total links to insert: 7

Link 1: How to Choose [Product]
  URL: https://example.com/blog/how-to-choose-product
  Anchor text: "[attribute] requirements" (secondary keyword)
  Location: Paragraph 12 (line ~150)

  Context before:
  "Most [use case] setups need the right [attribute] with a matching [key spec]."

  Context after:
  "Most [use case] setups need the right [[attribute] requirements](https://example.com/blog/how-to-choose-product) with a matching [key spec]."

---

Link 2: [Option A] vs [Option B]
  URL: https://example.com/blog/option-a-vs-option-b
  Anchor text: "[option A] vs [option B]" (exact match)
  Location: Paragraph 8 (line ~95)

  Context before:
  "Choose based on whether your demand is continuous or intermittent."

  Context after:
  "The [[option A] vs [option B]](https://example.com/blog/option-a-vs-option-b) decision hinges on whether your demand is continuous or intermittent."

---

[Continue for all links...]
```

**Ask user:** "Approve these link placements? (yes/no)"

Wait for user confirmation before proceeding.

---

## Phase 6: Update Article

Once approved, update the article content with the links.

### Step 6.1 — Insert links into markdown

Read the original article markdown file.

Insert each link at the specified location using markdown link format:
```
[anchor text](full URL)
```

**Preserve all other content** — only add links, don't modify existing text unless you're replacing text with the anchor text.

### Step 6.2 — Regenerate HTML

After updating the markdown, regenerate the HTML file using pandoc:

Run your publish step (the step you run after saving the draft), which converts Markdown→HTML (pandoc with `--wrap=none` so external links are never line-broken), checks word count and link spacing, and applies nofollow to external links — in one pass:

```powershell
# run your publish step for "[article-slug]"  (MD→HTML with pandoc --wrap=none, nofollow, word count + link-spacing check)
```

This ensures the HTML version has the updated links with correct line wrapping and nofollow on external links.

### Step 6.3 — Upload to Shopify

Run your Shopify push step (Admin API) to push the updated HTML to Shopify. This step reads your slug→article-ID map (`your-project/shopify-article-ids.csv`) to map the slug to the correct article ID:

```powershell
# run your Shopify push step (Admin API) for "[article-slug]"  (reads your-project/shopify-article-ids.csv to map slug → article ID)
```

### Step 6.4 — Update anchor text map

After successful update, append new rows to `your-project/anchor-text-map.csv` for each link inserted:

```csv
target_url,anchor_text,usage_count,anchor_type,last_used_date
https://example.com/blog/how-to-choose-product,[attribute] requirements,1,secondary,2026-02-20
https://example.com/blog/option-a-vs-option-b,[option A] vs [option B],1,exact,2026-02-20
```

If an anchor text already exists in the map, increment the `usage_count` and update `last_used_date`.

---

## Quality checks

Before finalizing, verify:

```
[ ] All link targets from the article have been mapped to URLs
[ ] No two links appear in the same paragraph
[ ] Links are evenly distributed across the article body (200+ words between links)
[ ] Anchor text variation follows 70/20/10 distribution (tracked in anchor-text-map.csv)
[ ] All URLs are complete and correct (https://example.com/blog/...)
[ ] No tacked-on links — every linked sentence makes its own point without the link
[ ] No duplicate link targets — each internal URL appears at most once per article
[ ] No "Related articles" footer — all links are woven into body content
[ ] FAQ questions use H3 headings (### Question?), not bold (**Question?**)
[ ] HTML file regenerated via your publish step
[ ] Shopify upload successful via your Shopify push step (Admin API)
[ ] Anchor text map updated
```

### Additional checks (if keyword-research provided core_keyword data):

```
[ ] This article links UP to its core_keyword parent (if it has one)
[ ] Parent pages receive more internal links than child pages (volume-weighted)
[ ] No spoke-to-spoke cross-cluster links (only parent-to-parent)
[ ] Article with core_keyword ≠ primary keyword confirms it's appropriately scoped
```

**Parent-child validation:**
If the current article's primary keyword has a different `core_keyword`:
- Verify at least 1 contextual link to the core_keyword parent article
- Example: Article on "[option C] vs [option D] (narrow variant)" must link to "[option C] vs [option D]" (its parent)

**Volume-weighted validation:**
If search volume data available:
- Articles with volume >2,000 should have 5-8 inbound links
- Articles with volume 1,000-2,000 should have 3-5 inbound links
- Articles with volume <1,000 should have 1-3 inbound links

---

## Example: Processing one article

### Input:
Article: `product-types.md`

Internal links found in body content and/or identified from KEYWORD-REGISTER cross-reference:
- How to Choose [Product]
- [Option A] vs [Option B]
- What is [Option A]
- [Option B]: Complete Guide
- [Option C] vs [Option D]
- [Option E] vs [Option F]
- [Option G] vs [Option H] vs [Option I]

### Phase 1: Extract
✓ Extracted 7 link targets

### Phase 2: Map
✓ Mapped all 7 titles to URLs using shopify-article-ids.csv + article-urls.txt
✓ Mapped all 7 titles to primary/secondary keywords using KEYWORD-REGISTER.csv

### Phase 3: Analyze
✓ Scanned article for mentions of each target's keywords
✓ Identified 12 candidate locations across 7 targets
✓ Selected best location for each based on context quality and distribution

### Phase 4: Select anchor text
✓ Checked anchor-text-map.csv for existing usage
✓ Selected anchor text following 70/20/10 strategy:
  - 5 exact match (71%)
  - 1 secondary keyword (14%)
  - 1 miscellaneous (14%)

### Phase 5: Preview
✓ Presented all 7 proposed links with context to user
✓ User approved

### Phase 6: Update
✓ Inserted 7 links into markdown file
✓ Regenerated HTML with pandoc
✓ Updated Shopify via API
✓ Updated anchor-text-map.csv with 7 new entries

---

## How this connects to other skills

**Depends on:**
- **seo-content** → Articles must be written first with internal link suggestions included
- **keyword-database-article-map** → Provides the keyword-to-article mapping

**Outputs to:**
- Shopify (via API)
- anchor-text-map.csv (for future link variation tracking)

**The flow:**
1. seo-content creates articles with internal link suggestions
2. Articles are uploaded to Shopify
3. **internal-linking processes each article** to insert links
4. Updated articles are pushed back to Shopify with links in place

---

## Reference files

**Input files:**
- `your-project/Written Articles/[article-slug].md` — Source article
- `your-project/KEYWORD-REGISTER.csv` — Keyword mapping
- `your-project/shopify-article-ids.csv` — Article ID and handle mapping
- `your-project/article-urls.txt` — Complete URL list
- `your-project/anchor-text-map.csv` — Anchor text usage tracking

**Output files:**
- `your-project/Written Articles/[article-slug].md` — Updated with links
- `your-project/Written Articles/[article-slug].html` — Regenerated HTML
- `your-project/anchor-text-map.csv` — Updated with new anchor text usage

---

## The test

Before updating via API, ask:

1. **Do all links point to the correct URLs?**
2. **Are the links contextually relevant to their insertion points?**
3. **Is the distribution even (no clustering)?**
4. **Does the anchor text variation look natural?**
5. **Has the anchor text map been updated correctly?**

If any answer is no, fix before proceeding with the update.
