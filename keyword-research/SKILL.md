---
name: keyword-research
version: 8.0
description: "Strategic keyword research combining LLM creativity with market data. Uses 6 Circles Method + AnswerThePublic + DataForSEO to generate 1,000-3,500 validated keywords with search volume, difficulty, and parent keyword relationships. Creates data-driven content plans with ROI forecasting. Triggers on: keyword research for X, content strategy for X, what topics should I cover, SEO strategy, content calendar, topic clusters. Outputs prioritized keyword clusters with traffic/revenue projections and internal linking architecture."
---

# Keyword Research

Most keyword research is backwards. People start with tools, get overwhelmed by data, and end up with a spreadsheet they never use.

This skill starts with strategy. What does your business need? Who are you trying to reach? What would make them find you? Then it validates that strategy with market reality.

**The approach:** Combine three complementary sources:
- **6 Circles Method (LLM)** — Strategic keywords aligned with business positioning
- **AnswerThePublic** — Real questions people actually ask
- **DataForSEO** — Search volume, difficulty, parent keywords, and market validation

Result: 1,000-3,500 keywords with complete data, organized into prioritized clusters with traffic/revenue projections.

**Can be used without API tools:** The 6 Circles Method works standalone. Data enrichment is optional but recommended for data-driven decisions.

---

## The core job

Transform a business context into a **prioritized content plan** with:
- Keyword clusters organized by topic
- Priority ranking based on opportunity
- Content type recommendations
- A clear "start here" action

**Output format:** Clustered keywords mapped to content pieces, prioritized by business value and opportunity.

---

## The process

```
SEED → EXPAND → ENRICH → CLUSTER → PRIORITIZE → MAP → FORECAST
```

1. **Seed** — Generate initial keywords from business context
2. **Expand** — Use the 6 Circles Method to build comprehensive list
3. **Enrich** — (Optional) Add market data via AnswerThePublic + DataForSEO
4. **Cluster** — Group related keywords into content pillars
5. **Prioritize** — Score by opportunity and business value
6. **Map** — Assign clusters to specific content pieces
7. **Forecast** — (Optional) Project traffic/revenue ROI

---

## Brand Memory

On every invocation, load brand context before doing anything else:

```
./brand/
  ├── voice-profile.md      [voice, tone, vocabulary rules]
  ├── positioning.md        [angles, differentiators, audience]
  ├── audience.md           [ICP, segments, pain points]
  └── creative-kit.md       [taglines, proof points, assets]
```

Check each file:
- If it exists → load it silently, confirm with ✓ in context display
- If it's missing → mark with ✗ and note: "Run /brand-voice first to create this"

Display on load:
```
BRAND CONTEXT
✓ voice-profile.md loaded
✓ positioning.md loaded
✗ audience.md — not found (run /brand-voice to create)
✗ creative-kit.md — not found
```

If all files are missing: ask "Should I run /brand-voice first, or do you want to proceed without brand context?"

---

## Iteration Detection

Before generating output, check for existing work:

```
./campaigns/{project-name}/
  ├── copy/          [existing copy files]
  ├── emails/        [existing email sequences]
  └── keywords/      [existing keyword research]
```

If files exist:
- List what's there with a one-line summary of each
- Ask: "I found existing work for this project. Do you want to (R)evise, (A)dd to it, or (S)tart fresh?"
- Wait for response before generating anything new

If no files exist:
- Proceed normally

---

## File Output Protocol

When generating output, save to the appropriate location:

```
./campaigns/{project-name}/
  ├── copy/          → landing pages, CTAs, ad copy
  ├── emails/        → sequences and individual emails
  └── keywords/      → keyword research and content plans
```

**Naming convention:**
- `{project-name}-{type}-v{n}.md` (e.g., `acme-landing-page-v1.md`)
- Increment version number on each revision

**After saving:**
- Confirm the file path
- State what changed vs. previous version (if revision)
- Ask: "Ready to move to the next step?"

---

## Before starting: Gather context

Get these inputs before generating anything:

1. **What do you sell/offer?** (1-2 sentences)
2. **Who are you trying to reach?** (Be specific)
3. **What's your website?** (To understand current content)
4. **Who are 2-3 competitors?** (Or help identify them)
5. **What's the goal?** (Traffic? Leads? Sales? Authority?)
6. **Timeline?** (Quick wins or long-term plays?)

---

## Phase 1: Seed Generation

From the business context, generate 20-30 seed keywords covering:

**Direct terms** — What you actually sell
> "AI marketing automation", "fractional CMO", "marketing workflows"

**Problem terms** — What pain you solve
> "can't keep up with content", "marketing team too small", "don't understand AI"

**Outcome terms** — What results you deliver
> "faster campaign execution", "10x content production", "marketing ROI"

**Category terms** — Broader industry terms
> "marketing automation", "AI marketing", "growth marketing"

---

## Phase 2: Expand (The 6 Circles Method)

For each seed keyword, expand using 6 different lenses:

### Circle 1: What You Sell
Products, services, and solutions you offer directly.
> Example: "AI marketing automation", "marketing workflow templates", "fractional CMO services"

### Circle 2: Problems You Solve
Pain points and challenges your audience faces.
> Example: "marketing team overwhelmed", "can't measure marketing ROI", "content takes too long"

### Circle 3: Outcomes You Deliver
Results and transformations customers achieve.
> Example: "automated lead generation", "consistent content publishing", "marketing that runs itself"

### Circle 4: Your Unique Positioning
What makes you different from alternatives.
> Example: "no-code marketing", "AI-first approach", "community-driven marketing"

### Circle 5: Adjacent Topics
Related areas where your audience spends time.
> Example: "startup growth", "indie hackers", "solopreneur tools", "productivity systems"

### Circle 6: Entities to Associate With
People, tools, frameworks, concepts you want to be connected to.
> Example: "Claude AI", "n8n automation", specific thought leaders, industry frameworks

### Expansion techniques

For each seed, find variations using:

**Question patterns:**
- What is [keyword]?
- How to [keyword]?
- Why [keyword]?
- Best [keyword]?
- [keyword] vs [alternative]?
- [keyword] examples
- [keyword] for [audience]

**Modifier patterns:**
- [keyword] tools
- [keyword] templates
- [keyword] guide
- [keyword] strategy
- [keyword] 2025
- [keyword] for beginners
- [keyword] for [industry]

**Comparison patterns:**
- [keyword A] vs [keyword B]
- best [category]
- [tool] alternatives
- [tool] review

**Output:** Expanded list of 100-200 keywords from seed terms

---

## Phase 2.5: Data Enrichment (Three-Source Synthesis)

**The limitation of brainstorming alone:** The 6 Circles Method generates strategically aligned keywords based on business context, but it doesn't know what people actually search for or how much demand exists.

**The solution:** Combine LLM creativity with market reality using three complementary data sources.

### The Three-Source Approach

| Source | What It Provides | Why Essential |
|--------|------------------|---------------|
| **6 Circles (LLM)** | Business-aligned strategy, unique positioning, proprietary angles | Strategic foundation - what makes you different |
| **AnswerThePublic** | Question-based queries, conversational search, real user language | Human intent - how people actually ask questions |
| **DataForSEO** | Search volume, difficulty scores, parent keyword relationships, trends | Market validation - quantify opportunity and discover what LLM missed |

**Combined result:** Strategic keywords (LLM) + human questions (ATP) + market data (API) = Complete keyword intelligence

---

### Phase 2.5a: Market Discovery via DataForSEO

**Goal:** Discover the top 1,000-4,000 keyword variations that the market actually searches for around your main seed keyword(s).

**Why this matters:**
The 6 Circles Method might generate "[product] maintenance tips" based on business strategy, but miss that "[product] not working" (2,400 monthly searches) is what people actually search for.

**API Endpoint:** `dataforseo_labs/google/keyword_ideas/live`

**Process:**

1. **Identify main seed keyword(s)** from Phase 1
   - This is your core niche/topic (e.g., "[product]", "marketing automation", "fractional cmo")
   - Can be 1-3 primary seeds if multiple product lines

2. **API Request Structure:**
```json
POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live

Headers:
  Authorization: Basic [base64(login:password)]
  Content-Type: application/json

Body:
[{
  "keywords": ["[product]"],
  "location_code": 2840,
  "language_code": "en",
  "include_seed_keyword": true,
  "include_serp_info": false,
  "limit": 4000,
  "filters": [
    ["keyword_info.search_volume", ">", 50]
  ],
  "order_by": ["keyword_info.search_volume,desc"]
}]
```

**Parameters explained:**
- `keywords`: Your main seed(s)
- `location_code`: 2840 = USA (see DataForSEO docs for other locations)
- `language_code`: "en" for English
- `limit`: 1000-4000 (more = more comprehensive, but review time increases)
- `filters`: Minimum search volume threshold (50+ filters out ultra-long-tail)
- `order_by`: Sort by volume descending (shows biggest opportunities first)

3. **Cost:** ~$0.40-$0.50 per seed keyword

4. **Output:** 1,000-4,000 keywords sorted by search volume with basic metrics

**What you'll discover:**
- High-volume keywords your brainstorm missed
- Problem-solving queries (e.g., "won't start", "not working", "troubleshooting")
- Application-specific searches (e.g., "for [use case]", "for [industry]")
- Comparison terms the market uses
- Seasonal or trending variations

**Save the results:** Export to CSV or JSON for Phase 2.5c merge

---

### Phase 2.5b: Question Mining via AnswerThePublic

**Goal:** Capture how real humans phrase their questions and problems.

**Why this matters:**
Questions reveal search intent and become your article structure (FAQs, H2 sections, content angles).

**Data Source:** AnswerThePublic (answerthepublic.com)

**Options:**
- **Free:** Manual scraping (limit: 2-3 searches per day)
- **Paid:** API access ($99/mo for unlimited)

**Process:**

1. **Enter your main seed keyword** into AnswerThePublic

2. **Export all question variations:**
   - What questions (what is, what are, what does, what's the best, etc.)
   - How questions (how to, how much, how many, how does, etc.)
   - Why questions (why is, why does, why do, etc.)
   - Where/when/who questions
   - Comparisons (vs, or, and)
   - Prepositions (with, without, for, near, like, etc.)
   - Alphabetical long-tail variations

3. **Example for "[product]":**
```
What:
- what is a [product] used for
- what size [product] do i need
- what is [attribute] on [product]
- what [component] to use in [product]

How:
- how to size a [product]
- how a [product] works
- how to choose a [product]
- how much [key spec] do i need

Why:
- why is my [product] not working
- why does my [product] keep running
- why is my [product] [common problem]

Comparisons:
- [product] [type A] vs [type B]
- [option A] vs [option B] [product]
- [product type A] vs [product type B]
```

4. **Save the results:** Export to CSV (50-200 question-based keywords)

**Integration value:**
- Questions = ready-made article titles
- Questions = FAQ section content
- Questions = H2 section headers
- Questions reveal what users actually care about vs what you assume they care about

---

### Phase 2.5c: Merge & Deduplicate

**Goal:** Combine all three keyword sources into one master list without duplicates.

**Input sources:**
- Stream 1: 100-200 keywords from 6 Circles (Phase 2)
- Stream 2: 50-200 keywords from AnswerThePublic (Phase 2.5b)
- Stream 3: 1,000-4,000 keywords from DataForSEO (Phase 2.5a)

**Total raw pool:** ~1,150-4,400 keywords

**Merge process:**

**Step 1: Combine all sources**
Create one master list with source tracking:
```
keyword: "[product] sizing"
sources: [6_circles, dataforseo]

keyword: "how to choose [product]"
sources: [answerthepublic, dataforseo]

keyword: "[product type A] advantages"
sources: [6_circles]
```

**Step 2: Remove exact duplicates**
- Normalize: lowercase, trim whitespace
- Remove 100% exact matches
- Keep source attribution for remaining keywords

**Step 3: Flag semantic near-duplicates**
Don't auto-merge these yet - let the API tell us if they share a parent:
- "how to choose a [product]" vs "[product] buying guide"
- "[type A] vs [type B]" vs "[type B] vs [type A]"
- "best [product] for [use case]" vs "top [product]s for [use case]"

**Step 4: Remove irrelevant keywords (optional filter)**
From DataForSEO stream, remove obviously off-topic results:
- Brand-specific manuals (unless you cover those)
- Rental/service queries (unless you offer those)
- Extremely niche technical specs (unless expert audience)

**Output:** ~1,000-3,500 deduplicated unique keywords ready for enrichment

**Source tracking matters because:**
- Keywords found by all 3 sources = highest confidence
- Keywords only from 6_circles = strategic but unvalidated
- Keywords only from DataForSEO = market demand but may not align with strategy
- Keywords only from AnswerThePublic = need volume validation

---

### Phase 2.5d: Enrich with DataForSEO Keyword Overview

**Goal:** Add search volume, difficulty, parent keyword (core_keyword), and intent data to ALL keywords.

**This is the critical validation layer** that transforms your keyword list from "interesting ideas" to "quantified opportunities."

**API Endpoint:** `dataforseo_labs/google/keyword_overview/live`

**Process:**

1. **Batch your keywords** (max 700 per request)
   - 1,000 keywords = 2 requests
   - 2,000 keywords = 3 requests
   - 3,500 keywords = 5 requests

2. **API Request Structure:**
```json
POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live

Headers:
  Authorization: Basic [base64(login:password)]
  Content-Type: application/json

Body:
[{
  "keywords": [
    "[product] sizing",
    "how to choose [product]",
    "[option A] vs [option B] [product]",
    ... up to 700 keywords
  ],
  "location_code": 2840,
  "language_code": "en",
  "include_serp_info": true,
  "include_clickstream_data": false
}]
```

**Set `include_clickstream_data: true` for 2x cost** if you need:
- More accurate search volume
- Age/gender demographics
- Device breakdown

For most projects, `false` is sufficient.

3. **For each keyword, API returns:**

```json
{
  "keyword": "[option A] vs [option B] [product type]",
  "keyword_properties": {
    "core_keyword": "[option A] vs [option B] [product]",
    "keyword_difficulty": 34
  },
  "keyword_info": {
    "search_volume": 210,
    "cpc": 1.85,
    "competition": 0.42,
    "monthly_searches": [
      {"year": 2024, "month": 12, "search_volume": 220},
      {"year": 2024, "month": 11, "search_volume": 200},
      ...
    ]
  },
  "search_intent_info": {
    "main_intent": "informational",
    "foreign_intent": ["commercial"]
  }
}
```

4. **Key fields to extract:**

**core_keyword** - THE PARENT KEYWORD
This is the most important field. It tells you:
- Which keywords should be grouped into one article
- What the main article target should be
- When you've missed a parent keyword entirely

Example:
```
Your keyword: "[option A] vs [option B] [product type]"
core_keyword: "[option A] vs [option B] [product]" ← This is the article to write!

→ If "[option A] vs [option B] [product]" wasn't in your original list, ADD IT
→ Make it the parent article
→ Make your original keyword an H2 section within it
```

**search_volume** - Monthly search volume
- Validates which topics have demand
- Informs content scope (high volume = longer content)
- Enables traffic projections

**keyword_difficulty** - 0-100 score
- 0-30: Low competition (quick wins)
- 30-50: Medium competition (achievable with quality)
- 50-70: High competition (need authority)
- 70-100: Very high competition (long-term play)

**search_intent** - What the searcher wants
- `informational`: Learning, research → Blog post, guide
- `commercial`: Comparison, evaluation → Buying guide, comparison
- `transactional`: Ready to buy → Product page, pricing page
- `navigational`: Looking for specific site → Brand page

**monthly_searches** - 12-month trend
- Identify seasonal patterns
- Spot growing vs declining topics
- Plan content timing

5. **Cost:** ~$0.10 per 700 keywords
   - 1,000 keywords: $0.20
   - 2,000 keywords: $0.30
   - 3,500 keywords: $0.50

6. **Output:** Fully enriched keyword database

**Example enriched keyword:**
```
keyword: "how to choose [product] for [use case]"
sources: [6_circles, dataforseo, answerthepublic]
core_keyword: "how to choose [product]"
search_volume: 880
keyword_difficulty: 28
search_intent: informational
monthly_trend: growing (+15% over 12 months)
confidence: HIGH (all 3 sources)
```

**What you now know:**
- Which keywords are parents vs children
- Exact search demand (no more guessing)
- Competition level (realistic ranking timeline)
- Search intent (right content type)
- Multi-source validation (confidence level)
- Trend direction (prioritize growing topics)

---

### Phase 2.5 Summary

**Investment:**
- DataForSEO Market Discovery: $0.40-$0.50 per seed
- DataForSEO Enrichment: $0.20-$0.50 for full keyword set
- AnswerThePublic: Free (manual) or $99/mo (API)
- **Total per project: $0.60-$1.00 in API costs**

**Time saved:**
- Manual keyword research: 10-20 hours
- Guessing search volume: eliminated
- Keyword cannibalization issues: prevented
- Content scope decisions: data-driven

**Output:**
- 1,000-3,500 unique keywords
- Full data for each: volume, difficulty, parent, intent, trends
- Source attribution: LLM, ATP, API, or combination
- Ready for clustering with objective data

**Next:** Use this enriched data in Phase 3 to create data-driven clusters

---

## Phase 3: Cluster

Group expanded keywords into content pillars using the hub-and-spoke model:

```
                    [PILLAR]
                 Main Topic Area
                      |
        +-------------+-------------+
        |             |             |
   [CLUSTER 1]   [CLUSTER 2]   [CLUSTER 3]
    Subtopic       Subtopic       Subtopic
        |             |             |
    Keywords      Keywords      Keywords
```

### Identifying pillars (5-10 per business)

A pillar is a major topic area that could support:
- One comprehensive guide (3,000-8,000 words)
- 3-7 supporting articles
- Ongoing content expansion

Ask: "Could this be a complete guide that thoroughly covers the topic?"

### Data-Driven Auto-Grouping (If Phase 2.5 was completed)

**If you enriched keywords with DataForSEO**, use the `core_keyword` field to automatically group keywords:

**Step 1: Group by core_keyword**
All keywords that share the same `core_keyword` belong to the same article.

Example:
```
core_keyword: "[option A] vs [option B] [product]"
  ├─ "[option A] vs [option B] [product type]" (210 vol, 6_circles)
  ├─ "[option A] [product] benefits" (390 vol, dataforseo)
  ├─ "should i get [option A] [product]" (180 vol, answerthepublic)
  └─ "[option A] vs [option B] [product] compared" (520 vol, dataforseo)

Total cluster volume: 1,300
Article target: "[option A] vs [option B] [product]"
Content type: Comprehensive guide (3,000-4,000 words)
```

**Step 2: Identify missed parent keywords**
If `core_keyword` doesn't appear in your original keyword list, **add it as the article target**.

Example:
```
Keyword: "[option A] vs [option B] [product type]"
core_keyword: "[option A] vs [option B] [product]" ← NOT in original list

ACTION: Add "[option A] vs [option B] [product]" as primary article target
        Make all child keywords into H2 sections
```

**Step 3: LLM validation of auto-groups**
For each auto-generated cluster, review:
- Does this semantic grouping make sense?
- Are there strategic reasons to split any keywords out?
- Should we combine any core_keywords into a broader pillar?

The API groups by search behavior. You validate with business strategy.

---

### Manual Clustering (If Phase 2.5 was skipped)

If you didn't use DataForSEO enrichment, use the original manual clustering process:

**1. Group by semantic similarity** — Keywords that mean similar things
**2. Group by search intent** — Keywords with same user goal
**3. Identify the pillar keyword** — The broadest term in each group
**4. Identify supporting keywords** — More specific variations

---

### Pillar Validation (Critical Step)

**Before finalizing pillars, run these 4 checks:**

Most keyword research fails because pillars are chosen based on what the business WANTS to talk about, not what the market ACTUALLY searches for.

**1. Search Volume Test (Data-Driven if enriched)**

**With DataForSEO data:**
Sum all `search_volume` values for keywords in this cluster.

```
Pillar: "[Option A] [Product]s"
Keyword volumes in cluster:
- [option A] vs [option B] [product]: 840
- [option A] [product] benefits: 390
- [option A] [product type]: 520
- [option A] [product] vs [option B]: 280
= TOTAL: 2,030 monthly searches → PASS (>1,000)
```

- If cluster total >1,000: Valid pillar
- If cluster total <1,000: Demote to article or remove

**Without DataForSEO data:**
Does this pillar have >1,000 monthly searches? (Manual validation via Google Trends or keyword tools)

- If YES: Valid pillar
- If NO: Not a pillar. It may be a single article or shouldn't be created at all.

Example failure: "Claude marketing" (zero search volume) chosen as pillar because the product uses Claude. Market searches "AI marketing" instead.

**2. Product vs. Market Test**
Is this pillar something the MARKET searches for, or something YOU want to talk about?

| Product-Centric (Wrong) | Market-Centric (Right) |
|-------------------------|------------------------|
| "Our methodology" | "Marketing automation" |
| "[Your tool name] tutorials" | "[Category] tutorials" |
| "Why we're different" | "[Problem] solutions" |
| Features of your product | Outcomes people search for |

The market doesn't search for your product name (unless you're famous). They search for solutions to their problems.

**3. Competitive Reality Test (Enhanced with Data)**

Can you actually win here?

**With DataForSEO data:**
Check average `keyword_difficulty` across cluster:

```
Pillar: "[Product type A]"
Avg difficulty: 42
Difficulty range: 28-58

Assessment:
- Avg <30: High opportunity (quick wins possible)
- Avg 30-50: Medium competition (winnable with quality)
- Avg 50-70: High competition (need authority building)
- Avg >70: Very high competition (long-term play only)

VERDICT: Medium competition → Winnable with comprehensive content
```

**Without DataForSEO data:**
Check the top 3 results for the pillar keyword manually:
- All DR 80+ sites (Forbes, HubSpot, etc.)? Find adjacent pillar.
- Mix of authority and smaller sites? Winnable with great content.
- Thin content from unknown sites? High opportunity.

Don't choose pillars where you have no realistic path to page 1.

**4. Proprietary Advantage Test**
Do you have unique content, data, or expertise for this pillar?

| Advantage | Priority |
|-----------|----------|
| Proprietary data others don't have | Prioritize highly |
| Unique methodology or framework | Prioritize highly |
| Practitioner experience (done it, not read about it) | Prioritize |
| Same info everyone else has | Deprioritize |

If you have 2,589 marketing workflows and nobody else does, "marketing workflows" should be a pillar. If you're writing about "AI marketing" with no unique angle, you're competing on equal footing with everyone.

**Validation Output:**

For each proposed pillar, document:

```
Pillar: [Name]
Search volume test: PASS/FAIL — [evidence]
Market-centric test: PASS/FAIL — [evidence]
Competitive test: PASS/FAIL — [evidence]
Proprietary advantage: YES/NO — [what advantage]
VERDICT: VALID PILLAR / DEMOTE TO CLUSTER / REMOVE
```

**If a pillar fails 2+ tests, it's not a pillar.** Either demote it to a single article within another pillar, or remove it entirely.

### Clustering process

1. **Group by semantic similarity** — Keywords that mean similar things
2. **Group by search intent** — Keywords with same user goal
3. **Identify the pillar keyword** — The broadest term in each group
4. **Identify supporting keywords** — More specific variations

### Example cluster

**Pillar:** AI Marketing Automation

**Clusters:**
- What is AI marketing automation (definitional)
- AI marketing tools (commercial/comparison)
- AI marketing examples (proof/validation)
- Building AI marketing workflows (how-to)
- AI vs traditional automation (comparison)

---

## Phase 4: Prioritize

Not all keywords are equal. Score each cluster by:

### Business Value (High / Medium / Low)

**High:** Direct path to revenue
- Commercial intent keywords
- Close to purchase decision
- Your core offering

**Medium:** Indirect path
- Builds trust and authority
- Captures leads
- Educational content

**Low:** Brand awareness only
- Top of funnel
- Tangentially related
- Nice to have

### Opportunity (High / Medium / Low)

**High opportunity signals:**
- No good content exists (you'd define the category)
- Existing content is outdated (2+ years old)
- Existing content is thin (surface-level, generic)
- You have unique angle competitors miss
- Growing trend (check Google Trends)

**Low opportunity signals:**
- Dominated by major authority sites
- Excellent comprehensive content already exists
- Highly competitive commercial terms
- Declining interest

### Speed to Win (Fast / Medium / Long)

**Fast (3 months):**
- Low competition
- You have unique expertise/data
- Content gap is clear

**Medium (6 months):**
- Moderate competition
- Requires comprehensive content
- Differentiation path exists

**Long (9-12 months):**
- High competition
- Requires authority building
- May need link building

### Priority Matrix

| Business Value | Opportunity | Speed | Priority |
|---------------|-------------|-------|----------|
| High | High | Fast | **DO FIRST** |
| High | High | Medium | **DO SECOND** |
| High | Medium | Fast | **DO THIRD** |
| Medium | High | Fast | **QUICK WIN** |
| High | Low | Any | **LONG PLAY** |
| Low | Any | Any | **BACKLOG** |

---

### Objective Scoring Formula (If Phase 2.5 was completed)

**If you have DataForSEO data**, supplement qualitative assessment with quantitative scoring:

**Formula:**
```
opportunity_score = (
  search_volume ×
  intent_multiplier ×
  source_confidence_bonus ×
  (100 - keyword_difficulty)
) / 100
```

**Intent multipliers:**
```
transactional: 5    (ready to buy = highest value)
commercial: 3       (comparison/evaluation = high value)
informational: 1    (learning/research = baseline)
navigational: 0.5   (brand search = low priority for new content)
```

**Source confidence bonus:**
```
Found by all 3 sources (LLM + ATP + DataForSEO): 1.3x
Found by 2 sources: 1.15x
Found by DataForSEO only: 1.0x (market-driven)
Found by 6_circles only: 1.2x (strategic bet, higher risk/reward)
Found by AnswerThePublic only: 0.9x (needs volume validation)
```

**Scoring examples:**

```
Keyword: "best [product type A] [product] for [use case]"
- Volume: 880
- Difficulty: 42
- Intent: commercial (3x)
- Sources: 6_circles + dataforseo (1.15x)
Score: (880 × 3 × 1.15 × 58) / 100 = 1,763
Priority: HIGH

Keyword: "what is [attribute] on [product]"
- Volume: 2,400
- Difficulty: 28
- Intent: informational (1x)
- Sources: answerthepublic + dataforseo (1.15x)
Score: (2,400 × 1 × 1.15 × 72) / 100 = 1,987
Priority: HIGH

Keyword: "ai-powered predictive maintenance for [product]s"
- Volume: 20
- Difficulty: 18
- Intent: informational (1x)
- Sources: 6_circles only (1.2x)
Score: (20 × 1 × 1.2 × 82) / 100 = 19
Priority: LOW (strategic but no proven demand)
```

**Priority tiers:**
- **Score >1,500:** Tier 1 (DO FIRST)
- **Score 800-1,500:** Tier 2 (DO SECOND)
- **Score 300-800:** Tier 3 (BACKLOG)
- **Score <300:** Consider removing (unless strong strategic reason)

**Insight categories:**

Tag clusters by dominant source pattern:

- **Strategic Bets:** High scores from 6_circles-only = business sees opportunity market doesn't yet
- **Proven Demand:** High scores from dataforseo = market-validated opportunities
- **Question Goldmine:** High scores from answerthepublic = FAQ/how-to content opportunities
- **Validated Wins:** High scores from all 3 sources = highest confidence plays

**Use both qualitative + quantitative:**
- Objective score = data-driven baseline
- Qualitative factors (unique data, proprietary advantage) = override for strategic importance
- Final decision = combine both perspectives

---

## Phase 5: Map to Content

For each priority cluster, assign:

### Content type

| Type | When to Use | Word Count |
|------|-------------|------------|
| **Pillar Guide** | Comprehensive topic coverage | 5,000-8,000 |
| **How-To Tutorial** | Step-by-step instructions | 2,000-3,000 |
| **Comparison** | X vs Y, Best [category] | 2,500-4,000 |
| **Listicle** | Tools, examples, tips | 2,000-3,000 |
| **Use Case** | Industry or scenario specific | 1,500-2,500 |
| **Definition** | What is [term] | 1,500-2,500 |

### Intent matching

| Intent | Keyword Signals | Content Approach | CTA Type |
|--------|-----------------|------------------|----------|
| **Informational** | what, how, why, guide | Educate thoroughly | Newsletter, resource |
| **Commercial** | best, vs, review, compare | Help them decide | Free trial, demo |
| **Transactional** | buy, pricing, get, hire | Make it easy | Purchase, contact |

### Content calendar placement

**Tier 1 (Publish in weeks 1-4):** Highest priority, category-defining
**Tier 2 (Publish in weeks 5-8):** High priority, supporting pillars
**Tier 3 (Publish in weeks 9-12):** Medium priority, depth content
**Tier 4 (Backlog):** Lower priority, future opportunities

---

### Volume-Based Content Scope Decisions (If Phase 2.5 was completed)

**If you have DataForSEO data**, use search volume to determine content structure and scope:

**Cluster-level decisions (parent keyword volume):**

```
If cluster total volume >3,000:
  → Pillar Guide (5,000-8,000 words)
  → Include all child keywords as H2 sections

If cluster total volume 1,000-3,000:
  → Comprehensive Guide (3,000-5,000 words)
  → Include top 5-7 child keywords as H2 sections

If parent keyword volume >500:
  → Standard Article (2,000-3,000 words)
  → Include top 3-5 child keywords as H2 sections

If parent keyword volume 200-500:
  → Focused Article (1,500-2,500 words)
  → Include top 2-3 child keywords as H2 sections

If parent keyword volume <200:
  → FAQ entry or section within broader article
```

**Child keyword scope decisions:**

```
For each child keyword in a cluster:

If child volume >800 AND different search_intent than parent:
  → Create separate article (link back to parent)
  Example: Parent is informational, child is commercial

If child volume >500:
  → Dedicated H2 section (300-500 words)

If child volume 200-500:
  → H3 subsection or FAQ entry (150-250 words)

If child volume <200:
  → Natural mention in body copy (no dedicated section)
```

**Example mapping:**

```
Cluster: "[Product] Sizing"
Parent keyword: "how to choose [product]" (volume: 2,200)
Cluster total volume: 4,100

Content decision: Comprehensive Guide (4,000 words)

Child keyword mapping:
- "[product] [key spec] requirements" (880 vol) → H2 section (400 words)
- "how to calculate [key spec] for [product]" (520 vol) → H2 section (350 words)
- "[product] [attribute] chart" (390 vol) → H2 section (300 words)
- "choosing [product] for [use case]" (620 vol) → H2 section (400 words)
- "[product] [spec A] to [spec B]" (290 vol) → H3 subsection (200 words)
- "should I oversize my [product]" (180 vol) → FAQ entry (100 words)
- "[product] sizing mistakes" (120 vol) → Natural mentions in content
```

---

### AnswerThePublic Question Integration

**If you used AnswerThePublic in Phase 2.5b**, map questions to article structure:

**Question → Content mapping:**

```
"What" questions → Definition sections, introductions
  Example: "what is [attribute] on [product]" → Intro or H2 definition

"How to" questions → Main H2 sections with step-by-step
  Example: "how to choose [product] for [use case]" → H2 tutorial section

"Why" questions → FAQ entries or problem/solution H2s
  Example: "why does [product] keep running" → FAQ entry

"Best/Top" questions → Comparison sections or separate articles
  Example: "best [product] for [use case]" → Separate commercial article

"vs" questions → Comparison H2 sections or separate articles
  Example: "[type A] vs [type B] [product]" → H2 comparison or separate article
```

**ATP Questions as FAQ section:**

All question-based keywords from AnswerThePublic become your FAQ section:

```
## FAQ

### What size [product] do I need for [use case]?
[Answer based on keyword data + search intent]

### How do I calculate [key spec] requirements?
[Answer]

### Should I oversize my [product]?
[Answer]

### Why does my [product] keep [common problem]?
[Answer]
```

**ATP value:** Questions are pre-validated by real search behavior, giving you article structure that matches how users actually search.

---

### Content calendar placement (enhanced)

**Consider difficulty scores when sequencing:**

If you have DataForSEO data, publish easier content first to build authority:

```
Month 1: Low difficulty (<30) supporting articles
  → Build topical authority signals
  → Establish site credibility
  → Generate initial traffic

Month 2-3: Medium difficulty (30-50) comprehensive guides
  → Now have some authority
  → Can compete better

Month 4+: High difficulty (50+) pillar guides
  → Maximum authority built
  → Best chance of ranking
```

**Tier 1 (Publish in weeks 1-4):** Highest score + low/medium difficulty
**Tier 2 (Publish in weeks 5-8):** High score + medium difficulty
**Tier 3 (Publish in weeks 9-12):** Medium score or high difficulty
**Tier 4 (Backlog):** Lower scores or very high difficulty

---

## Output format

### Executive Summary

```
# Keyword Research: [Business Name]

## Top Opportunities
1. [Keyword/cluster] — [Why it's an opportunity]
2. [Keyword/cluster] — [Why it's an opportunity]
3. [Keyword/cluster] — [Why it's an opportunity]

## Quick Wins (3-month potential)
- [Keyword] — [Why quick]
- [Keyword] — [Why quick]

## Long-Term Plays (6-12 months)
- [Keyword] — [Strategy needed]

## Start Here
[Specific first piece of content to create and why]
```

### Pillar Overview

```
## Pillar: [Topic Name]
**Priority:** [Critical / High / Medium / Low]
**Content pieces:** [Number]

| Cluster | Priority | Intent | Content Type | Target |
|---------|----------|--------|--------------|--------|
| [name]  | [H/M/L]  | [type] | [format]     | [date] |
```

### 90-Day Content Calendar

```
## Month 1
- Week 1-2: [Flagship piece] — [Target keyword cluster]
- Week 3: [Supporting piece] — [Target keyword cluster]
- Week 4: [Supporting piece] — [Target keyword cluster]

## Month 2
- Week 5-6: [Second pillar piece] — [Target keyword cluster]
...
```

---

## Phase 6: ROI Dashboard (If Phase 2.5 was completed)

**If you have DataForSEO data**, create traffic and revenue projections for each cluster.

### Traffic Projection Formula

```javascript
estimated_monthly_traffic = sum_across_cluster(
  keyword.search_volume ×
  ctr_by_estimated_position[keyword.difficulty] ×
  intent_ctr_multiplier[keyword.intent]
)
```

**CTR by estimated ranking position:**
Based on keyword difficulty and your domain authority:

```
If keyword_difficulty <30 (low competition):
  Estimated position: 3-5
  CTR range: 5-10%

If keyword_difficulty 30-50 (medium competition):
  Estimated position: 5-8
  CTR range: 3-5%

If keyword_difficulty 50-70 (high competition):
  Estimated position: 8-15
  CTR range: 1-3%

If keyword_difficulty >70 (very high competition):
  Estimated position: 15-20
  CTR range: 0.5-1%
```

**Intent CTR multipliers:**
```
informational: 0.8    (lower CTR due to featured snippets answering query)
commercial: 1.2       (higher CTR, comparison intent drives clicks)
transactional: 1.5    (highest CTR, buying intent)
```

### Revenue Projection Formula

```javascript
estimated_monthly_value = (
  estimated_monthly_traffic ×
  conversion_rate_by_intent ×
  average_customer_value
)
```

**Conversion rates by intent:**
```
informational: 0.2-0.5%   (newsletter signups, downloads)
commercial: 1-3%          (demo requests, trials)
transactional: 2-5%       (direct purchases, contact)
```

### ROI Dashboard Output

```
## ROI Dashboard

### Cluster: "[Product type A] for [Use Case]"

**Keyword metrics:**
- Total keywords: 23
- Total cluster volume: 3,800/month
- Avg difficulty: 38
- Primary intent: commercial (65%), informational (35%)
- Source validation: 18 from DataForSEO, 8 from 6_circles, 12 from ATP, 5 from all 3

**Traffic projection (assuming ranks 5-8 avg):**
- Conservative: 140-180 visits/month
- Optimistic: 220-280 visits/month

**Revenue projection:**
- Avg customer value: $150
- Est. conversion rate: 2% (commercial intent)
- Conservative value: $420-540/month = $5,040-$6,480/year
- Optimistic value: $660-840/month = $7,920-$10,080/year

**Investment required:**
- Content creation: $1,200 (1 pillar + 2 supporting articles)
- Promotion: $300
- Total: $1,500

**ROI projection:**
- First month: 0.28-0.56x (content investment phase)
- Month 6: 1.5-2.5x (rankings stabilizing)
- Year 1: 3.4-6.7x (compounding traffic)

**Confidence level: HIGH**
- 5 keywords validated by all 3 sources
- Mix of strategic positioning + market demand
- Clear commercial intent signals
- Manageable competition (avg difficulty 38)

**Prioritization: TIER 1 (Do First)**
```

### Multi-Cluster Summary

```
## Portfolio ROI Summary

| Cluster | Volume | Score | Est. Traffic | Est. Value/yr | Investment | ROI (Yr 1) | Priority |
|---------|--------|-------|--------------|---------------|------------|------------|----------|
| [Product type A] for [Use Case] | 3,800 | 1,890 | 220/mo | $7,900 | $1,500 | 5.3x | Tier 1 |
| [Key spec] Requirements | 4,200 | 2,100 | 320/mo | $3,800 | $1,200 | 3.2x | Tier 1 |
| [Product] Sizing | 2,100 | 1,650 | 180/mo | $2,200 | $800 | 2.8x | Tier 1 |
| Maintenance Guide | 1,800 | 980 | 95/mo | $1,100 | $600 | 1.8x | Tier 2 |

**Total Tier 1 investment:** $3,500
**Total Tier 1 projected value (Year 1):** $13,900
**Portfolio ROI:** 4.0x
```

**Use ROI dashboard to:**
- Justify content budget to stakeholders
- Allocate resources to highest-ROI clusters
- Set realistic traffic/revenue expectations
- Track actual performance vs projections

---

## Phase 7: Internal Linking Architecture (If Phase 2.5 was completed)

**If you have DataForSEO data**, use parent-child relationships to create linking hierarchy.

### Parent-Child Linking Map

Based on `core_keyword` groupings, create explicit link architecture:

```
## Internal Linking Architecture

### Pillar: [Product type A]

**Parent page:** "What is a [Product type A]" (core_keyword, 2,100 vol)

**Child pages that link UP to parent:**
1. "[Product type A] vs [Product type B]" (1,200 vol)
   - Link anchor: "learn more about [product type A]"
   - Placement: Intro paragraph

2. "[Option A] vs [Option B] [Product type A]" (840 vol)
   - Link anchor: "[product type A] fundamentals"
   - Placement: Background section

3. "[Product type A] Maintenance" (620 vol)
   - Link anchor: "how [product type A] works"
   - Placement: Before maintenance steps

**Parent page links DOWN to children:**
- Section "Types of [Product type A]" → links to [option A] vs [option B] article
- Section "Maintenance Requirements" → links to maintenance guide article
- Section "Comparison to Other Types" → links to vs [product type B] article

**Cross-cluster links:**
- "[Product type A] vs [Product type B]" also links to "[Key spec] Requirements" pillar
- "[Product type A] Maintenance" also links to "[Product] Sizing" (related topic)
```

### Linking Rules

**1. All child keywords link to their core_keyword parent**
- Required: At least 1 contextual link per child page
- Anchor text: Varied (70% exact match to parent, 20% secondary, 10% misc)

**2. Parent pages link to all children**
- Required: Link from relevant section
- Context: Where child topic is naturally mentioned
- Value: Distributes authority to supporting content

**3. Volume-weighted link priority**
Higher volume parents receive more inbound links:

```
If parent volume >2,000: Target 5-8 inbound links
If parent volume 1,000-2,000: Target 3-5 inbound links
If parent volume 500-1,000: Target 2-3 inbound links
If parent volume <500: Target 1-2 inbound links
```

**4. Cross-cluster linking**
Only link between PARENT pages across clusters, not spoke-to-spoke:

```
CORRECT:
Pillar A parent → Pillar B parent

INCORRECT:
Pillar A spoke → Pillar B spoke (orphans the connection, wastes equity)
```

### Linking Map Output

```
## Content Piece: "How to Choose [Product] for [Use Case]"

**This article's parent:** "How to Choose [Product]" (core_keyword)

**Required links TO (upward):**
- "How to Choose [Product]" (parent) - 1 contextual link

**Recommended links TO (cross-cluster):**
- "[Product] [Key spec] Requirements" (related pillar)
- "[Product type A] vs [Product type B]" (product type decision)

**Expected links FROM:**
- None (this is a child/spoke article)

**Anchor text strategy for parent link:**
- Primary: "sizing methodology" or "[product] sizing"
- Context: "For a detailed explanation of the [sizing methodology], see our complete guide."
```

**Benefit:** Every writer knows exactly what to link, where to link, and what anchor text to use. Zero guesswork.

---

## Example: Keyword research for "AI Marketing Consultant"

### Context gathered
- **Business:** AI marketing consulting for startups
- **Audience:** Funded startups, 10-50 employees, no marketing hire yet
- **Goal:** Leads for consulting engagements
- **Timeline:** Mix of quick wins and authority building

### Seed keywords generated
- AI marketing consultant
- AI marketing strategy
- Marketing automation
- Startup marketing
- Fractional CMO
- AI marketing tools

### Expanded via 6 Circles (sample)

**Circle 1 (What you sell):** AI marketing consultant, AI marketing strategy, AI marketing audit, marketing automation setup

**Circle 2 (Problems):** startup marketing overwhelm, no time for marketing, marketing not working, can't hire marketing team

**Circle 3 (Outcomes):** automated lead generation, consistent content, marketing ROI, scalable marketing

**Circle 4 (Positioning):** AI-first marketing, no-code marketing, startup-focused marketing

**Circle 5 (Adjacent):** startup growth strategies, product-led growth, indie hacker marketing

**Circle 6 (Entities):** Claude AI marketing, n8n marketing automation, HubSpot alternatives

### Clustered into pillars

**Pillar 1: AI Marketing Strategy** (Priority: Critical)
- What is AI marketing
- AI marketing examples
- AI marketing tools
- AI marketing for startups

**Pillar 2: Marketing Automation** (Priority: High)
- Marketing automation for startups
- No-code marketing automation
- n8n vs Zapier for marketing
- Marketing workflow templates

**Pillar 3: Fractional Marketing** (Priority: Medium)
- What is a fractional CMO
- Fractional CMO vs agency
- When to hire fractional marketing

### Top 3 recommendations

**1. "What is AI Marketing?" (Do First)**
- Category definition opportunity
- Growing search trend
- Weak competition (thin content dominates)
- You have practitioner expertise
- Pillar guide, 5,000+ words

**2. "AI Marketing Tools 2025" (Do Second)**
- Commercial intent, close to purchase
- Existing content is generic/outdated
- Unique angle: practitioner reviews
- Comparison listicle, 3,000+ words

**3. "Marketing Automation for Startups" (Quick Win)**
- Specific audience match
- Less competitive than broad term
- Clear differentiation path
- How-to guide, 2,500+ words

---

## What this skill does NOT do

This skill provides **strategic direction**, not:
- Live search volume data (use free tools if needed)
- Automated SERP analysis (manual review required)
- Content writing (use direct-response-copy skill)
- Technical SEO audits (different skill set)

The output is a prioritized plan. Execution is separate.

---

## Data Sources & API Setup

### Three-Source Integration (Recommended)

**1. DataForSEO API**
- **Purpose:** Search volume, keyword difficulty, parent keywords (core_keyword), search intent
- **Cost:** ~$0.60-$1.00 per project (pay-as-you-go)
- **Setup:** Account at dataforseo.com, API credentials stored in `.dataforseo-config.json`
- **Endpoints used:**
  - `keyword_ideas/live` — Market discovery (1k-4k keywords)
  - `keyword_overview/live` — Enrichment with full data
- **Documentation:** Phase 2.5 above for detailed instructions

**2. AnswerThePublic**
- **Purpose:** Question-based keywords, real user language patterns
- **Cost:** Free (2-3 searches/day) or $99/mo (unlimited API)
- **Setup:** answerthepublic.com
- **Use:** Export question data for main seed keywords
- **Integration:** Questions become FAQ sections and H2 headers

**3. 6 Circles Method (LLM)**
- **Purpose:** Strategic keywords aligned with business positioning
- **Cost:** Free (LLM processing time)
- **Always included:** This is the foundation method

### Free Alternatives (No API required)

If you skip Phase 2.5 data enrichment, these free tools help validate:

- **Google Trends** (trends.google.com) — Trend direction, seasonality
- **Google Search** — SERP analysis, autocomplete, "People Also Ask"
- **AnswerThePublic** (free tier) — Manual question export
- **AlsoAsked** (free tier) — PAA relationship mapping
- **Reddit/Quora search** — Real user questions and language

**When to skip API enrichment:**
- Budget constraints
- Quick brainstorming phase
- Internal/proprietary topics with no search demand data
- Very new/emerging topics not yet in search data

**When API enrichment is worth it:**
- Building comprehensive content strategy
- Need traffic/revenue projections
- Want to prevent keyword cannibalization
- Competitive niche requiring data-driven decisions

---

## How this connects to other skills

**keyword-research** identifies WHAT to write about and provides data for downstream decisions.

**Outputs to:**

- **keyword-database-article-map** →
  - Enriched keywords with volume/difficulty data
  - Parent-child relationships (core_keyword mappings)
  - Source validation flags
  - Enables data-driven deduplication and article assignment

- **seo-content** →
  - Target keyword with search volume + difficulty
  - Secondary keywords with volumes (for H2 prioritization)
  - AnswerThePublic questions (for FAQ sections)
  - Content scope guidance (word count based on volume)

- **internal-linking** →
  - Parent-child keyword relationships
  - Volume-weighted linking priorities
  - Core_keyword groupings for hierarchical architecture

- **positioning-angles** → finds the angle for each piece
- **brand-voice** → ensures consistent voice across content

**The flow:**
1. **keyword-research** creates data-driven content strategy
2. **keyword-database-article-map** assigns keywords to articles (no cannibalization)
3. **seo-content** writes articles with data-informed briefs
4. **internal-linking** connects articles using parent-child hierarchy

---

## The test

A good keyword research output:

1. **Actionable** — Clear "start here" recommendation
2. **Prioritized** — Not just a list, but ranked by opportunity
3. **Realistic** — Acknowledges competition and timelines
4. **Strategic** — Connects to business goals, not just traffic
5. **Specific** — Content types and angles, not just keywords

If the output is "here's 500 keywords, good luck" — it failed.

---

## Output Summary Format

End every output with this summary block:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SKILL: keyword-research | PROJECT: [project-name] | v[n]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLETED: [What was produced — 1 line]
SAVED TO:  [File path if saved]
NEXT STEP: [Recommended next action]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## What to run next

Keywords define what to create. Once the register is built:

- **Positioning:** Run `/positioning-angles` to shape how content is angled for the audience
- **Content:** Run `/seo-content` to write articles against these keywords
- **Copy:** Run `/direct-response-copy` to write landing pages targeting priority terms

---

## Feedback

After every output, ask:

> "Before we move on — did this hit the mark?
> - (Y) Yes, this works
> - (T) Tweak it — [tell me what to change]
> - (R) Redo — different direction entirely"

If (T): make the requested change and re-deliver.
If (R): ask one clarifying question, then regenerate.
If no response: proceed to next step.
