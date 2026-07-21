# AnswerThePublic Integration Guide

How to use AnswerThePublic (ATP) to capture real user questions for keyword research.

## What AnswerThePublic Provides

**ATP discovers:** How real humans phrase their questions and searches

**Output categories:**
- What questions (what is, what are, what does, etc.)
- How questions (how to, how much, how many, etc.)
- Why questions (why is, why does, etc.)
- Where/when/who questions
- Comparisons (vs, or, and)
- Prepositions (with, without, for, near, etc.)
- Alphabetical variations

**Why this matters:**
- Questions = ready-made article titles
- Questions = FAQ section content
- Questions = H2 section headers
- Questions reveal what users care about vs what you assume they care about

---

## Setup

### Free Tier (Recommended to start)

**Limits:**
- 2-3 searches per day
- Manual CSV export
- No API access

**Best for:**
- Testing the integration
- Small projects (1-3 seed keywords)
- Budget-conscious keyword research

**URL:** https://answerthepublic.com

---

### Paid Plan ($99/mo)

**Benefits:**
- Unlimited searches
- API access
- Bulk export
- Historical data
- Priority support

**Best for:**
- Agencies running multiple client projects
- High-volume keyword research
- Automated workflows

---

## Usage in Keyword Research Workflow

### Phase 2.5b: Question Mining

**Step 1: Enter seed keyword**
```
Seed: "[product]"
```

**Step 2: Export all question categories**

Free tier: Download CSV manually
Paid tier: Use API or bulk export

**Step 3: Filter and organize**

ATP returns 50-200+ questions. Organize by:
- **Article-worthy:** Questions with enough depth for full content
- **FAQ-worthy:** Quick answer questions for FAQ sections
- **H2-worthy:** Questions that become section headers
- **Ignore:** Too niche or off-topic

---

## Question Categories & Use Cases

### "What" Questions → Definitions & Introductions

**Examples:**
```
- what is a [product] used for
- what size [product] do i need
- what is [attribute] on [product]
- what [component] to use in [product]
```

**Use as:**
- Article introductions
- Definition sections
- H2 headers for foundational topics

---

### "How to" Questions → Tutorials & Guides

**Examples:**
```
- how to size a [product]
- how a [product] works
- how to choose a [product]
- how much [key spec] do i need
```

**Use as:**
- Main article topics
- Step-by-step tutorial sections
- H2 headers with detailed instructions

---

### "Why" Questions → Problem-Solving & FAQs

**Examples:**
```
- why is my [product] not working
- why does my [product] keep running
- why is my [product] [common problem]
```

**Use as:**
- FAQ entries
- Troubleshooting sections
- Problem/solution H2 headers

---

### "Best/Top" Questions → Commercial Content

**Examples:**
```
- best [product] for [use case]
- best [product type] for [use case]
- top rated [product] brands
```

**Use as:**
- Separate commercial articles (buying guides)
- Comparison content
- Product recommendation sections

---

### "vs" Questions → Comparison Articles

**Examples:**
```
- [type A] vs [type B] [product]
- [option A] vs [option B] [product]
- [product type A] vs [product type B]
```

**Use as:**
- Standalone comparison articles
- H2 comparison sections
- Decision framework content

---

## Integration with DataForSEO

**The perfect combo:**

1. **ATP discovers questions** (real user language)
2. **DataForSEO validates volume** (which questions people actually search)
3. **Combine for prioritized question list** (real + popular)

**Workflow:**
```
1. Export 150 questions from ATP
2. Add to merged keyword list
3. Enrich with DataForSEO
4. Filter by volume >100
5. Result: Validated question-based keywords
```

**Example:**
```
ATP Question: "why does my [product] keep shutting off"
DataForSEO Data:
  - Volume: 880/month
  - Difficulty: 24
  - Intent: informational

Decision: High-priority FAQ + potential H2 section
```

---

## Question-to-Content Mapping

### Tier 1: Full Article Topics (Volume >500)

```
Question: "how to choose a [product]"
ATP: Discovered in "how to" category
DataForSEO: Volume 2,200, Difficulty 32
Content: Comprehensive guide (3,000-4,000 words)
```

### Tier 2: H2 Sections (Volume 200-500)

```
Question: "what is [attribute] on [product]"
ATP: Discovered in "what" category
DataForSEO: Volume 390, Difficulty 18
Content: H2 section in [attribute] guide (300-400 words)
```

### Tier 3: FAQ Entries (Volume 100-200)

```
Question: "should i buy [option A] [product]"
ATP: Discovered in prepositions
DataForSEO: Volume 150, Difficulty 22
Content: FAQ entry (100-150 words)
```

### Tier 4: Natural Mentions (Volume <100)

```
Question: "when to replace [product] [component]"
ATP: Discovered in "when" category
DataForSEO: Volume 60, Difficulty 15
Content: Natural mention in maintenance section
```

---

## Extraction Templates

### For Free Tier (Manual Process)

**1. Go to AnswerThePublic.com**

**2. Enter seed keyword:** "[product]"

**3. Export data:**
- Click "Download CSV"
- Or manually copy questions by category

**4. Organize in spreadsheet:**
```
| Question | Category | Priority | Planned Use |
|----------|----------|----------|-------------|
| how to choose [product] | How | High | Article |
| what is [attribute] | What | Medium | H2 Section |
| why is it not working | Why | Medium | FAQ |
```

---

### For Paid Tier (API Access)

**API endpoint documentation:** Available in ATP account

**Example automation:**
```powershell
# Pseudo-code (ATP API structure varies)
$seedKeywords = @("[product]", "[product type A]")

foreach ($seed in $seedKeywords) {
    $questions = Invoke-ATPQuery -Keyword $seed -Categories @("what", "how", "why")
    $allQuestions += $questions
}

# Filter duplicates
$uniqueQuestions = $allQuestions | Select-Object -Unique

# Export for DataForSEO enrichment
$uniqueQuestions | Export-Csv "atp-questions.csv"
```

---

## ATP + DataForSEO Workflow Example

### Input: Seed keyword "[product]"

**Step 1: ATP Discovery**
```
ATP returns:
- 45 "what" questions
- 62 "how" questions
- 38 "why" questions
- 27 comparison questions
- 18 "best" questions
= 190 total questions
```

**Step 2: Merge with other sources**
```
6 Circles Method: 180 keywords
ATP: 190 questions
DataForSEO Market Discovery: 3,200 keywords
= 3,570 raw keywords
```

**Step 3: Deduplicate**
```
Remove exact duplicates: -280
Remove irrelevant: -120
= 3,170 unique keywords
```

**Step 4: Enrich with DataForSEO**
```
Batch enrich all 3,170 keywords
Cost: $0.50 (5 batches)
Output: Volume, difficulty, core_keyword, intent for each
```

**Step 5: Filter ATP questions by volume**
```
ATP questions with volume >100: 78 questions
ATP questions with volume 50-100: 42 questions
ATP questions with volume <50: 70 questions (discard)

Validated ATP questions: 120
```

**Step 6: Map to content**
```
Full articles: 8 ATP questions (volume >500)
H2 sections: 24 ATP questions (volume 200-500)
FAQ entries: 46 ATP questions (volume 100-200)
Natural mentions: 42 ATP questions (volume 50-100)
```

---

## Question Quality Filters

### Keep if:
- ✓ Volume >50 (validated search demand)
- ✓ Relevant to business offering
- ✓ Can provide authoritative answer
- ✓ Not already covered in existing content
- ✓ Fits target audience knowledge level

### Discard if:
- ✗ Volume <50 (too niche)
- ✗ Off-topic or irrelevant
- ✗ Duplicate of existing FAQ
- ✗ Question you can't answer with authority
- ✗ Outside business scope

---

## ATP as FAQ Generator

**Perfect for creating FAQ sections:**

```markdown
## Frequently Asked Questions

### What size [product] do I need?
[Answer with volume data + internal link to sizing guide]

### How does a [product] work?
[Answer with internal link to how-it-works article]

### Why does my [product] keep shutting off?
[Answer with troubleshooting steps]

### Should I buy [option A] or [option B]?
[Answer with comparison + internal link]
```

**All questions = pre-validated by ATP + DataForSEO volume data**

---

## Integration Checklist

```
[ ] ATP account created (free or paid)
[ ] Understand free tier limits (2-3 searches/day)
[ ] Can export CSV from ATP
[ ] Know how to categorize questions (article vs FAQ vs section)
[ ] Ready to merge ATP questions with LLM + DataForSEO keywords
[ ] Understand volume thresholds for content decisions
[ ] Can map questions to H2 headers and FAQ entries
```

---

## Best Practices

1. **Use ATP early** - Run ATP queries right after Phase 2 (6 Circles)
2. **Don't skip validation** - Always enrich ATP questions with DataForSEO volume data
3. **Respect limits** - Free tier = 2-3 seeds max per day
4. **Filter aggressively** - Not every ATP question deserves content
5. **Map to structure** - Questions become your article skeleton
6. **Update FAQ sections** - ATP questions = ready-made FAQ content
7. **Track source** - Label keywords with ATP source for attribution

---

## Common Mistakes

**Mistake 1: Using all ATP questions without validation**
→ Many ATP questions have <10 monthly searches
→ Always validate with DataForSEO volume data

**Mistake 2: Creating separate article for every question**
→ Most questions should be FAQ entries or H2 sections
→ Only volume >500 questions justify full articles

**Mistake 3: Ignoring question structure**
→ ATP gives you the exact phrasing users search
→ Use it verbatim in titles/headers when possible

**Mistake 4: Forgetting commercial questions**
→ "best" and "top" questions have commercial intent
→ Map these to buying guides, not informational content

---

## ATP Value Summary

**What ATP does that others don't:**
- Real user language (not SEO-speak)
- Question format (perfect for FAQ/H2 headers)
- Conversational phrasing (matches voice search)
- Problem-focused (reveals pain points)

**Best combined with:**
- 6 Circles Method (strategic business alignment)
- DataForSEO (volume validation)

**Result:** Strategic + Human + Validated keyword research
