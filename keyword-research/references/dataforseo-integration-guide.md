# DataForSEO Integration Guide

Complete guide to integrating DataForSEO API with the keyword-research skill.

## Quick Start

### 1. Setup (One-time)

**Create account:**
- Go to dataforseo.com
- Sign up for pay-as-you-go plan
- Get API credentials (login + password)

**Store credentials:**
```powershell
# Create .dataforseo-config.json in project root
{
  "api_login": "your@email.com",
  "api_password": "your-api-password",
  "base_url": "https://api.dataforseo.com/v3"
}
```

**Add to .gitignore:**
```
.dataforseo-config.json
```

### 2. Usage in Keyword Research Workflow

```
Phase 1: Seed (LLM generates seeds)
Phase 2: Expand (6 Circles Method generates 100-200 keywords)

→ Phase 2.5a: Market Discovery
  Use: Get-MarketKeywords function
  Input: Main seed keyword ("[product]")
  Output: 1,000-4,000 market keywords
  Cost: ~$0.40-0.50

→ Phase 2.5c: Merge
  Combine: LLM keywords + Market keywords + ATP questions
  Total: ~1,000-3,500 keywords

→ Phase 2.5d: Enrich
  Use: Invoke-BatchEnrich function
  Input: All merged keywords
  Output: Enriched data (volume, difficulty, core_keyword, intent)
  Cost: ~$0.20-0.50

Phase 3: Cluster (using core_keyword)
Phase 4: Prioritize (using objective scoring)
Phase 5: Map (using volume thresholds)
Phase 6: ROI Dashboard (using traffic projections)
```

---

## API Endpoints Reference

### Endpoint 1: Keyword Ideas (Market Discovery)

**Purpose:** Discover top 1k-4k keyword variations for your seed

**URL:** `POST /v3/dataforseo_labs/google/keyword_ideas/live`

**Cost:** ~$0.40-0.50 per request

**Request:**
```json
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

**Response fields (key ones):**
```json
{
  "keyword": "[product] for [use case]",
  "keyword_info": {
    "search_volume": 2400,
    "competition": 0.45,
    "cpc": 2.15
  }
}
```

**PowerShell usage:**
```powershell
. .\scripts\dataforseo-client.ps1
$keywords = Get-MarketKeywords -SeedKeywords @("[product]") -Limit 2000
```

---

### Endpoint 2: Keyword Overview (Enrichment)

**Purpose:** Add volume, difficulty, core_keyword, intent to ALL keywords

**URL:** `POST /v3/dataforseo_labs/google/keyword_overview/live`

**Cost:** ~$0.10 per 700 keywords

**Request:**
```json
[{
  "keywords": [
    "[product] sizing",
    "how to choose [product]",
    "[option A] vs [option B] [product]"
  ],
  "location_code": 2840,
  "language_code": "en",
  "include_serp_info": true,
  "include_clickstream_data": false
}]
```

**Response fields (critical ones):**
```json
{
  "keyword": "[option A] vs [option B] [product type]",
  "keyword_properties": {
    "core_keyword": "[option A] vs [option B] [product]",  ← PARENT!
    "keyword_difficulty": 34
  },
  "keyword_info": {
    "search_volume": 210,
    "cpc": 1.85,
    "competition": 0.42,
    "monthly_searches": [...]
  },
  "search_intent_info": {
    "main_intent": "informational",
    "foreign_intent": ["commercial"]
  }
}
```

**PowerShell usage:**
```powershell
$enriched = Get-KeywordOverview -Keywords $keywordArray

# Or batch enrich with progress tracking:
$enriched = Invoke-BatchEnrich -Keywords $allKeywords -OutputFile "enriched.csv"
```

---

## Key Data Fields Explained

### core_keyword (THE MOST IMPORTANT FIELD)

**What it is:** The parent keyword that groups semantically related variations

**Example:**
```
Keyword: "[option A] vs [option B] [product type]"
core_keyword: "[option A] vs [option B] [product]"

→ This tells you:
  - These keywords should be ONE article, not two
  - "[option A] vs [option B] [product]" is the article target
  - "[option A] vs [option B] [product type]" is an H2 section
```

**Use cases:**
- Auto-detect semantic duplicates
- Group keywords into articles
- Identify parent keywords you missed
- Prevent keyword cannibalization

**Decision rules:**
```
If keyword.core_keyword != keyword:
  → This keyword should be a SECTION in the core_keyword article

If keyword.core_keyword == keyword:
  → This keyword IS a parent (make it an article)

If keywords share same core_keyword:
  → They belong in the SAME article
```

---

### search_volume

**What it is:** Average monthly searches (12-month average)

**Use cases:**
- Validate pillar topics (cluster total >1,000)
- Determine content scope (>500 = separate article, <200 = FAQ)
- Prioritize content creation
- ROI forecasting

**Volume tiers:**
```
>5,000: High-value pillar content
1,000-5,000: Standard pillar or comprehensive guide
500-1,000: Focused article
200-500: Short article or H2 section
<200: FAQ or natural mention
```

---

### keyword_difficulty (0-100)

**What it is:** Ranking difficulty score based on SERP competition

**Use cases:**
- Set realistic ranking timelines
- Sequence content (easy first → build authority → tackle hard)
- Adjust word count (higher difficulty = more depth needed)
- Opportunity identification (high volume + low difficulty = quick win)

**Difficulty interpretation:**
```
0-30: Low competition (rank in 3 months)
30-50: Medium competition (rank in 6 months)
50-70: High competition (rank in 9-12 months)
70-100: Very high competition (long-term authority building)
```

---

### search_intent

**What it is:** Primary user intent category

**Values:**
- `informational` - Learning, research (blog post, guide)
- `commercial` - Comparison, evaluation (buying guide)
- `transactional` - Ready to buy (product page)
- `navigational` - Looking for specific brand/site

**Use cases:**
- Match content type to intent
- CTA selection
- Conversion rate estimation
- Prioritization (transactional = highest value)

---

## Cost Analysis

### Per Project Costs

| Project Size | Keywords | Market Discovery | Enrichment | Total |
|--------------|----------|------------------|------------|-------|
| Small | 500 | $0.40 | $0.10 | **$0.50** |
| Medium | 1,500 | $0.40 | $0.30 | **$0.70** |
| Large | 3,500 | $0.40 | $0.50 | **$0.90** |

### Annual Budget (10 projects/year)

- Small projects: $5/year
- Medium projects: $7/year
- Large projects: $9/year

**Conclusion:** Even comprehensive keyword research costs less than $1 per project.

---

## Rate Limits

- **Max calls/minute:** 2,000
- **Max keywords per Keyword Overview request:** 700
- **Recommended:** 1 second delay between batch requests

**The PowerShell script handles this automatically.**

---

## Common Patterns

### Pattern 1: Parent Keyword Discovery

**Problem:** You generate "[option A] vs [option B] [product type]" but miss the broader parent.

**Solution:**
```powershell
$enriched = Get-KeywordOverview -Keywords @("[option A] vs [option B] [product type]")

$parent = $enriched[0].keyword_properties.core_keyword
# Returns: "[option A] vs [option B] [product]"

# Add parent to keyword list if not already present
if ($parent -notin $allKeywords) {
    $allKeywords += $parent
}
```

---

### Pattern 2: Cluster by Parent

**Problem:** Need to group 3,000 keywords into articles.

**Solution:**
```powershell
$enriched = Invoke-BatchEnrich -Keywords $allKeywords

# Group by core_keyword
$clusters = $enriched | Group-Object { $_.keyword_properties.core_keyword }

# Show cluster summary
$clusters | ForEach-Object {
    $parent = $_.Name
    $children = $_.Group
    $totalVolume = ($children | Measure-Object -Property {$_.keyword_info.search_volume} -Sum).Sum

    [PSCustomObject]@{
        Parent = $parent
        ChildCount = $children.Count
        TotalVolume = $totalVolume
        AvgDifficulty = ($children | Measure-Object -Property {$_.keyword_properties.keyword_difficulty} -Average).Average
    }
} | Sort-Object TotalVolume -Descending
```

---

### Pattern 3: Priority Scoring

**Problem:** Need to objectively prioritize 150 articles.

**Solution:**
```powershell
$enriched | ForEach-Object {
    $volume = $_.keyword_info.search_volume
    $difficulty = $_.keyword_properties.keyword_difficulty
    $intent = $_.search_intent_info.main_intent

    $intentMultiplier = switch ($intent) {
        "transactional" { 5 }
        "commercial" { 3 }
        "informational" { 1 }
        default { 0.5 }
    }

    $score = ($volume * $intentMultiplier * (100 - $difficulty)) / 100

    [PSCustomObject]@{
        Keyword = $_.keyword
        Volume = $volume
        Difficulty = $difficulty
        Intent = $intent
        Score = [Math]::Round($score, 0)
        Tier = if ($score -gt 1500) { "Tier 1" }
               elseif ($score -gt 800) { "Tier 2" }
               else { "Tier 3" }
    }
} | Sort-Object Score -Descending
```

---

## Troubleshooting

### Error: "Config file not found"

**Solution:**
```powershell
# Create .dataforseo-config.json in project root
@{
    api_login = "your@email.com"
    api_password = "your-password"
    base_url = "https://api.dataforseo.com/v3"
} | ConvertTo-Json | Out-File ".dataforseo-config.json"
```

### Error: "Invalid credentials"

Check that credentials in `.dataforseo-config.json` match your DataForSEO account.

### Warning: "Maximum 700 keywords per request"

This is expected. The Invoke-BatchEnrich function automatically handles batching.

### Cost higher than expected

- Check `include_clickstream_data` (2x cost if true)
- Verify batch count (each batch = $0.10)
- Review location_code (non-US may cost more)

---

## Best Practices

1. **Always start with market discovery** - Don't skip Phase 2.5a
2. **Merge before enriching** - Dedupe first to save API costs
3. **Use core_keyword religiously** - It prevents cannibalization
4. **Export enriched data** - Save CSV for future reference
5. **Track API spend** - Log costs per project for ROI calculation
6. **Validate parent keywords** - If core_keyword ≠ keyword, verify it makes sense
7. **Batch large lists** - Use Invoke-BatchEnrich for >700 keywords
8. **Wait between batches** - Script includes 1-second delay

---

## Integration Checklist

Before using DataForSEO in production:

```
[ ] DataForSEO account created
[ ] API credentials stored in .dataforseo-config.json
[ ] .gitignore updated to exclude credentials
[ ] PowerShell script tested with small keyword list
[ ] Understand cost per project ($0.60-$1.00)
[ ] Know how to interpret core_keyword field
[ ] Can group keywords by parent
[ ] Can calculate priority scores
[ ] Familiar with volume thresholds for content scope
[ ] Ready to integrate data into downstream skills
```

---

## Support

**DataForSEO Docs:** https://docs.dataforseo.com/v3/
**API Status:** https://status.dataforseo.com/
**Pricing:** https://dataforseo.com/pricing
**Support:** support@dataforseo.com
