---
name: seo-backlinks
description: "Analyze a domain's backlink profile using free-first data sources — referring domains, anchor-text distribution, toxic-link flags, top linked pages, and competitor link gaps. Use to baseline our link profile, find link opportunities, or spot toxic patterns. Triggers on: backlink analysis, who links to us, referring domains, anchor text profile, toxic links, link gap vs competitor, backlink audit. Outputs a profile summary + health score (or INSUFFICIENT DATA) with prioritized actions."
---

# Backlinks Analysis

Backlinks are the one major SEO input we don't generate from content — and the one most clouded by
paid-tool marketing. This skill gives an honest read of the link profile using **free data first**,
flags the patterns that actually matter (too few referring domains, over-optimized anchors, toxic
sources), and surfaces competitor gaps — without pretending a free Common-Crawl sample is a full
Ahrefs index. It's analysis-only; it doesn't do outreach.

> Lower-priority skill for a content shop (you picked it as optional). Best run occasionally to
> baseline and find opportunities, not per-article.

---

## Data sources (free-first, confidence-weighted)

| Tier | Source | Access | Metrics | Confidence |
|---|---|---|---|---|
| Always-on | **Common Crawl** | Free (public index) | Referring domains (sample), historical snapshots | 0.50 |
| Free signup | **Moz API** | Free key | Domain Authority, referring domains, anchor patterns | 0.85 |
| Free signup | **Bing Webmaster** | Free key | Backlink count, referring domains, anchor text | 0.70 |
| Paid | **DataForSEO** | Paid | Full referring domains, anchors, toxicity, link velocity, competitor gaps | 1.00 |

Common Crawl is always available (no key); Moz/Bing need a free signup; DataForSEO is optional paid.
**Confidence-weight** findings by source and state which source produced each number.

---

## Analysis framework (7 sections)

1. **Profile overview** — referring-domain count, follow ratio, domain diversity, trend.
   - Alert: **referring domains < 20**, or **follow ratio < 40%**.
2. **Anchor-text distribution** — branded / exact-match / partial / generic / naked URL.
   - Alert: **exact-match anchors > 15%** (over-optimization / Penguin risk).
3. **Referring-domain quality** — TLD spread, authority tiers, follow/nofollow mix.
4. **Toxic-link detection** — PBNs, link farms, deindexed domains, directory spam; assign a risk
   level. Flag, don't auto-disavow — recommend review.
5. **Top pages by backlinks** — our link magnets; pages with 0 backlinks that need internal links;
   404s with recoverable equity (redirect them).
6. **Competitor gap** — domains linking to competitors but not us = the opportunity list.
7. **Link velocity** — new/lost links over time (DataForSEO only).

---

## Health score (honest)

Compute a 0–100 score **only when ≥4 of the 7 sections have data**. Otherwise report
**"INSUFFICIENT DATA"** rather than a misleadingly low score (a thin free-tier sample is not a low
profile — it's an unmeasured one). Weight contributing factors by source confidence. Always state the
data basis: e.g. "Common Crawl only (confidence 0.50) — directional, not definitive."

## Output format

```
BACKLINKS — example.com   [Score: 62/100  |  basis: Moz + Common Crawl]
Referring domains: 41 (Moz) · Follow ratio: 71% · Exact-match anchors: 9%

FLAGS
- (none critical)
OPPORTUNITIES (competitor gap, top priority)
- 8 domains link to [competitor] but not us — manufacturer directories + 2 trade blogs. (list)
- 3 of our high-traffic articles have 0 referring domains — candidates for outreach/promotion.
HOUSEKEEPING
- 2 inbound links point to 404s — 301 them to the live equivalents to recover equity.
```

## Honesty rules
- Never present a free-tier sample as a complete profile. Label confidence.
- Don't recommend mass disavow from a free toxic-link sample — flag for manual review.
- No link-buying / PBN advice. Opportunities = legitimate gap targets (directories, trade press,
  manufacturer/distributor pages, genuine resource pages).

## How this connects
- **`skills/seo-content/SKILL.md`** — link magnets worth promoting; internal links to fix 0-backlink pages.
- **`skills/keyword-database-article-map/SKILL.md`** — internal-link routing for orphaned/under-linked pages.
- **`anchor-text-map.csv`** — our internal anchor distribution (different from inbound external anchors,
  but the 70/20/10 discipline rhymes).
