---
name: keyword-database-article-map
description: "Takes the output of keyword-research and maps every keyword to exactly one article with zero duplication. Use when building or cleaning a content database, planning article writing order, or ensuring no two articles compete for the same keyword. Triggers on: map keywords to articles, keyword database cleanup, content plan with no duplication, article writing roadmap, keyword assignment, cluster to article mapping. Outputs a deduplicated keyword database with every keyword owned by one article, plus a prioritized article writing roadmap."
---

# Keyword Database Article Map

The keyword-research skill finds what to write about. This skill solves the problem that always follows: **every keyword needs exactly one home, and every article needs a clearly unique primary keyword**.

Without this step, you end up with cannibalization — two articles competing for the same search terms, splitting authority, confusing Google, and making it impossible to know which article to improve.

This skill takes keyword research output and produces a clean, deduplicated database where every keyword is assigned to exactly one article, and every article has a clear roadmap for the writer.

---

## The core job

Transform a keyword research database into a **deduplication-clean article map** with:
- Every keyword assigned to exactly one article
- Every article's primary keyword unique across the entire site
- Secondary and longtail keywords consolidated to the most semantically relevant article
- A prioritized writing roadmap showing which articles to write first

**Output format:** Clean keyword database organized by pillar → cluster → article, with a writing roadmap ordered by priority.

---

## When to use this skill

Use this skill when:
- Starting a new content site (build the map before writing anything)
- An existing site has keyword cannibalization problems
- Coming out of the keyword-research skill with a cluster list that needs article-level assignments
- Planning a writing sprint and needing to know what to write in what order
- Adding keywords from a SEMrush/Ahrefs export to an existing database

**This skill sits between keyword-research and seo-content in the workflow:**

```
keyword-research → keyword-database-article-map → seo-content
```

---

## Before starting: Gather inputs

Get these from the keyword-research skill output or the user:

1. **Keyword database or cluster list** — The raw keyword groups from research
2. **Existing articles (if any)** — URLs or titles already published (to check for cannibalization)
3. **Site topic/niche** — To understand semantic relationships between keywords
4. **Priority signals** — Which pillars or keywords are highest commercial value
5. **Audience** — Professional/industrial or consumer? (Affects how to split overlapping topics)

If the user has a CSV or markdown keyword file, read it in full before proceeding.

---

## Phase 1: Deduplication Audit

Before mapping keywords to articles, find every duplicate.

### Step 1.1 — Find exact duplicate primary keywords

Scan the full keyword list. Flag any keyword that appears as a primary keyword in more than one article or cluster.

```
DUPLICATE FOUND:
Keyword: "best [product] for [use case]"
Appears in: Cluster 1D spoke #1 AND Cluster 3A spoke #3
Action needed: Pick one home, redirect the other to link there
```

### Step 1.2 — Find semantic duplicate primary keywords (Enhanced with Data)

Catch keywords that are functionally the same even if worded differently.

**With DataForSEO data:**
Use the `core_keyword` field to auto-detect semantic duplicates:

```
Keyword A: "[product type A] vs [product type B]"
core_keyword: "[product type A] vs [product type B] [product]"

Keyword B: "[product type B] vs [product type A]"
core_keyword: "[product type A] vs [product type B] [product]"

→ SAME core_keyword = SEMANTIC DUPLICATES → Consolidate to one article
```

**Manual examples** (if no data):
- "[product type A] vs [product type B]" AND "[product type B] vs [product type A]" — same article
- "[product] for [use case]" AND "[use case] [product]" — same article
- "[use case A] [key spec] requirements" AND "[use case B] [key spec] requirements" — same article if intent matches

Flag these and consolidate to one primary keyword per article.

**Decision rule with data:**
If keywords share `core_keyword`, pick the one with higher `search_volume` as the primary.

### Step 1.3 — Find misplaced secondary/longtail keywords

A keyword is misplaced when it appears as a secondary or longtail in an article that isn't its most relevant home.

**Test:** "If someone searched this exact phrase and landed on Article A, would they find the most complete answer? Or would Article B be a better match?"

If Article B is better — move the keyword there.

Example:
- "[use case] [key spec] requirements" as a longtail in a general [use case] guide — wrong home
- "[use case] [key spec] requirements" as a secondary in a [key spec] requirements article — correct home

### Step 1.4 — Flag competing clusters

Sometimes entire clusters compete with each other, not just individual keywords. Look for:
- Two clusters that could be the same article with different framing
- Clusters where all primary keywords are already covered in another pillar
- "Type comparisons" clusters that simply duplicate what type guides already cover

When a full cluster competes with existing content:
- Option A: Remove the cluster entirely, add internal linking notes
- Option B: Reframe every article with a unique angle (sizing vs tools-used, [key spec] vs full requirements)
- Option C: Merge the cluster into the competing cluster

### Step 1.5 — SERP-Overlap Test (empirical merge/split decision)

Steps 1.2–1.4 rely on judgment ("are these the same intent?"). When the call is genuinely
ambiguous, don't guess — check how many URLs the two keywords **actually share** in Google's top 10.
Google's own ranking tells you whether it treats them as the same query.

Search each keyword (incognito, or pull via DataForSEO) and list the top 10 organic URLs. Count how
many appear in BOTH lists:

| Shared top-10 URLs | What it means | Action |
|---|---|---|
| 7–10 | Google treats them as the same query | **Merge** — one article; higher-volume phrasing is primary, the other becomes a secondary |
| 4–6 | Same topic cluster | Same cluster; separate articles only with a documented angle (see Phase 2 + Rule 4) |
| 2–3 | Adjacent topics | Separate articles, cross-link them |
| 0–1 | Distinct topics | Separate articles, separate clusters |

This is the data-backed way to settle Step 1.2 (semantic duplicate?) and Step 1.4 (competing
clusters?). Pre-group candidates by intent first so you only test plausible pairs. Record the
shared-URL count in the article's NOTE so the decision is auditable. Full method and worked example:
`references/deduplication-rules.md` (Rule 9).

---

## Phase 2: The One-Home Rule

Every keyword gets assigned to exactly one article. This is the core rule this skill enforces.

### Assigning keyword homes

For each keyword, ask in order:

**1. Is there already an article that primarily covers this topic?**
- YES → Assign keyword to that article as secondary/longtail
- NO → This keyword may need its own article

**2. Could this keyword be covered naturally inside a broader article without being the primary focus?**
- YES → Assign as secondary/longtail in the broader article
- NO → Create a dedicated article

**3. If two articles could both claim this keyword, which one is semantically closer?**
- Use the "closest match wins" rule
- The article whose primary keyword has the most semantic overlap with this keyword gets it
- If closeness is genuinely ambiguous, run the **SERP-Overlap Test** (Phase 1, Step 1.5) — the count of shared top-10 URLs settles merge vs. separate empirically instead of by judgment

### The angle differentiation technique

When two articles legitimately need to exist on related topics, give each a different angle so their primary keywords can't be confused:

| Overlapping Topic | Article A Angle | Article B Angle |
|---|---|---|
| [Product] for [use case] | Sizing/[key spec] selection | Tools used + workflow setup |
| [Use case] requirements | [Key spec] number specifically | Total requirements ([spec B] + [key spec] + [component]) |
| [Attribute] [product] | [Product type A] with [attribute] specifically | [Attribute] energy savings broadly |
| [Component] sizing | Sizing formula/calculation | System design selection criteria |
| [Spec A] to [key spec] | Conversion chart | Efficiency ratio concept |

When you use angle differentiation, document it clearly with a NOTE in the database so writers know what angle to take.

### One-Home Cross-Reference Table

After assigning all keywords, produce a cross-reference table:

```
| Keyword | Home Article | Articles That Link Here |
|---|---|---|
| [Spec A] vs [spec B] | [Article X] | [Article Y], [Article Z] |
| [product] sizing | [Article A] | [Article B] |
```

This table is the map every writer and editor uses to avoid duplication going forward.

---

## Phase 3: Article-Level Keyword Structure

Every article in the database must have this structure before a writer touches it:

### Required for each article

```
Article Title: [Proposed title]
Cluster: [Pillar name > Cluster name]
Content Type: [Pillar Guide / How-To / Comparison / Use Case / Definition]
Word Count Target: [number]
Priority: [Tier 1 / Tier 2 / Tier 3]
Intent: [Informational / Commercial / Transactional / Problem-Solving]

PRIMARY KEYWORD: [one keyword only]
  Search intent: [what the searcher wants]
  Search volume: [if available from DataForSEO]
  Keyword difficulty: [if available from DataForSEO]
  Core keyword (parent): [if different from primary - indicates this should be a section, not separate article]

SECONDARY KEYWORDS (3-6):
  - [keyword] (volume: [if available])
  - [keyword] (volume: [if available])
  - [keyword] (volume: [if available])

LONGTAIL KEYWORDS (3-8):
  - [keyword phrase] (volume: [if available])
  - [keyword phrase] (volume: [if available])
  - [keyword phrase] (volume: [if available])

ANGLE NOTE: [What makes this article unique vs related articles]

INTERNAL LINKS TO:
  - [Article name] (upward to cluster hub / core_keyword parent)
  - [Article name] (horizontal to related spoke)
  - [Article name] (cross-cluster to related pillar)

INTERNAL LINKS FROM:
  - [Article name that should link here]
```

### Content Scope Decisions (If DataForSEO data available)

Use search volume to determine if keyword deserves separate article or should be a section:

```
If parent keyword volume >500:
  → Separate article

If parent keyword volume 200-500:
  → Separate focused article OR H2 section in broader article (business decision)

If parent keyword volume <200:
  → H3 subsection or FAQ entry in broader article

If core_keyword differs from keyword AND keyword volume <500:
  → This should be an H2 section in the core_keyword article, not a separate page
```

If any article is missing a primary keyword, secondary keywords, or longtail keywords — the map is incomplete. Fill every field before handing to writers.

---

## Phase 4: Writing Roadmap

With every article mapped, produce a prioritized writing order.

### Priority scoring

**With DataForSEO data** (use objective scoring from keyword-research skill):

```
opportunity_score = (
  search_volume ×
  intent_multiplier ×
  source_confidence_bonus ×
  (100 - keyword_difficulty)
) / 100

Tiers:
- Score >1,500: Tier 1 (Write first)
- Score 800-1,500: Tier 2 (Write second)
- Score 300-800: Tier 3 (Backlog)
- Score <300: Consider removing
```

Use the scores from keyword-research output directly.

---

**Without DataForSEO data** (manual qualitative scoring):

Score each article on 3 factors:

**Commercial Value (1-3)**
- 3 = Direct purchase intent, "best X" or "X for [application]"
- 2 = Research/comparison intent, builds toward conversion
- 1 = Informational, authority-building only

**Search Volume Potential (1-3)**
- 3 = Core category-defining keyword (10K+ monthly searches)
- 2 = Solid volume with clear audience (1K-10K)
- 1 = Long-tail, niche, or technical (under 1K)

**Competition Opportunity (1-3)**
- 3 = Thin or outdated content dominates SERP
- 2 = Mix of good and weak content
- 1 = Strong authoritative content already exists

**Total Score = Commercial Value + Search Volume + Competition**
**Range: 3 (lowest) to 9 (highest)**

### Writing order tiers

```
Tier 1 (Score 7-9): Write first — foundation and money pages
Tier 2 (Score 5-6): Write second — supporting authority
Tier 3 (Score 3-4): Write when Tier 1 and 2 are complete
```

### Cluster-first rule

Within the same priority tier, write in cluster order: **hub before spokes**.

Reason: The hub article needs to exist before spoke articles can link up to it. Publishing spokes before the hub wastes the internal linking equity.

```
CORRECT ORDER:
1. [Key Spec] Requirements Hub (Tier 1)
2. [Spec A] vs [spec B] spoke (Tier 1)
3. [Product] [Key Spec] Chart spoke (Tier 1)
4. [Use Case] [Key Spec] spoke (Tier 2)

WRONG ORDER:
1. [Use Case] [Key Spec] spoke (orphaned — no hub to link to)
2. [Product] [Key Spec] Chart spoke (orphaned)
3. [Key Spec] Requirements Hub
```

### Roadmap output format

```
## WRITING ROADMAP

### Tier 1: Foundation (Write First)
These are the money pages and category-defining guides. Everything else builds from these.

| # | Article | Primary Keyword | Score | Word Count | Notes |
|---|---|---|---|---|---|
| 1 | [Key Spec] Requirements Guide | [product] [key spec] requirements | 9 | 6,500 | Pillar hub — write before all [key spec] spokes |
| 2 | Sizing Guide | how to size [product] | 9 | 6,500 | Pillar hub — central resource |
| 3 | Buying Guide | [product] buying guide | 8 | 7,500 | Hub — links out to everything |

### Tier 2: Authority (Write Second)
Core application guides and type comparisons.

| # | Article | Primary Keyword | Score | Word Count | Notes |
|---|---|---|---|---|---|
| 4 | [Use Case] Sizing | [product] for [use case] | 7 | 3,500 | Cluster 2C spoke |
...

### Tier 3: Depth (Write When Tier 1+2 Complete)
Technical depth, longtail, and supporting content.
```

---

## Phase 5: Validation Checks

Before finalizing the database, run these checks:

### Check 1: No duplicate primaries
Scan every PRIMARY KEYWORD field across all articles. Each should appear exactly once.

```
PASS: Every primary keyword is unique
FAIL: [keyword] appears in [Article A] and [Article B] — resolve before writing
```

### Check 2: No orphaned articles
Every article should have at least:
- 1 internal link TO its cluster hub
- 1 internal link FROM another article

```
PASS: All articles have at least 1 inbound link mapped
FAIL: [Article X] has no inbound links mapped — add to at least one article's "links to" list
```

### Check 3: All longtail keywords have a home
Every longtail keyword in the original research should appear in at least one article's keyword structure.

```
PASS: All keywords accounted for
FAIL: [keyword] appears in research but has no article home — assign or remove
```

### Check 4: Angle differentiation is documented
Every pair of articles covering related topics must have a documented angle difference.

```
PASS: All overlapping topic pairs have distinct angle notes
FAIL: [Article A] and [Article B] cover similar topics with no documented angle differentiation
```

---

## Output format

### Section 1: Deduplication Audit Results

```
## Deduplication Audit

### Duplicate Primary Keywords Found: [N]
[List of duplicates and resolution decisions]

### Misplaced Keywords Moved: [N]
[List of keywords moved to new homes]

### Clusters Removed or Merged: [N]
[List with rationale]

### Articles Renamed to Avoid Overlap: [N]
[List with old and new primary keywords]
```

### Section 2: Master Keyword Database

Organized by Pillar → Cluster → Article, with full keyword structure for each article.

```
# PILLAR [N]: [Name]

## [Cluster Name]

### [Hub Article Title]
Primary: [keyword]
Secondary: [keyword], [keyword], [keyword]
Longtail: [keyword phrase], [keyword phrase], [keyword phrase]
Intent: [type]
Content Type: [type]
Word Count: [number]
Links to: [article], [article]
Links from: [article], [article]
Angle note: [what makes this distinct]

### [Spoke Article 1]
...
```

### Section 3: Cross-Reference Table

```
## One-Home Cross-Reference Table
| Keyword | Home Article | Clusters That Link Here |
|---|---|---|
```

### Section 4: Writing Roadmap

Tier 1, Tier 2, Tier 3 tables as described in Phase 4.

### Section 5: Monthly Writing Calendar

Map Tier 1 articles to Month 1, Tier 2 to Month 2, and Tier 3 to Month 3+.

```
## Month 1 (Tier 1 Foundation)
Week 1-2: [Article 1] + [Article 2]
Week 3-4: [Article 3] + [Article 4]
...
```

---

## How this skill connects to others

**Receives from:** keyword-research
- The 6 Circles keyword list
- Content pillar structure
- Priority clusters

**Sends to:** seo-content
- The completed article-level keyword structure
- Primary keyword, secondary keywords, longtail keywords
- Angle note
- Internal linking instructions
- Word count target and content type

**Also references:**
- brand-voice — for voice consistency reminders in roadmap notes
- positioning-angles — for angle differentiation when two articles cover similar ground

---

## Common mistakes this skill prevents

**Keyword cannibalization**
Two articles targeting the same primary keyword. Google can't decide which to rank, so it ranks neither well. This skill makes it structurally impossible — one keyword, one home, no exceptions.

**Orphaned spokes**
Spoke articles published before the hub exists, with no article linking to them. This skill enforces cluster-first writing order.

**Misplaced longtails**
Specific keywords buried in the wrong article because they were "close enough" to the topic. This skill tests every longtail against semantic closeness, not just topic similarity.

**Duplicate clusters**
Entire clusters of articles that compete with each other because the topic was approached from two different angles without differentiating the primaries. This skill catches competing clusters at the structural level before any writing happens.

**Missing keyword structure**
Articles handed to writers with only a primary keyword and no secondary/longtail list. Writers then guess what to include, often duplicating keywords from other articles. This skill requires a complete keyword structure for every article before writing starts.

---

## Reference files

See the `references/` folder for:

- **deduplication-rules.md** — Full rules for keyword conflict resolution with worked examples
- **article-roadmap-template.md** — Ready-to-fill roadmap template for any niche

---

## The test

A good keyword database article map output:

1. **Zero duplicate primaries** — Run a search for any keyword — it appears in exactly one article
2. **Every article has all keyword tiers** — Primary, secondary, longtail all filled
3. **Angle differentiation documented** — Every pair of related articles has a written angle note
4. **Writing order is clear** — Writer opens the roadmap and knows exactly which article to write next
5. **Hub-before-spoke order** — No spoke appears in Tier 1 without its hub also being Tier 1 or earlier
6. **Cross-reference table exists** — Any editor can look up any keyword and immediately find its home article

If the output is "here's a list of articles in no order with some keywords attached" — it failed.
