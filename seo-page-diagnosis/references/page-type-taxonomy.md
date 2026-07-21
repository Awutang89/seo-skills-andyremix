# Page-Type Taxonomy & Mismatch Reference

Used by `seo-page-diagnosis` to classify SERP results and detect page-type mismatch. Adapted from the
SXO approach in the open-source `claude-seo` project (MIT).

## Page types & their signals

| Page type | Intent | SERP/page signals | Our typical home |
|---|---|---|---|
| **Informational guide** | Learn / understand | Long-form, H2 sub-questions, no buy CTA, Article schema | Most blog articles |
| **How-to / tutorial** | Do a task | Numbered steps, tools/time, step images | How-to articles |
| **Listicle / roundup ("best X")** | Choose among options | Ranked items, comparison table, ItemList schema, "best/top" in titles | Best-X buying guides |
| **Comparison ("X vs Y")** | Decide between 2 | Verdict + feature table, two deep-dives, vs/or in titles | Type & brand comparisons |
| **Product / category** | Buy | Price, add-to-cart, Product schema, shopping pack in SERP | Shopify collections/products |
| **Calculator / tool** | Compute a number | Interactive widget, minimal prose | [key spec]/sizing calculators |
| **Definition** | Quick answer | Short, featured-snippet-shaped, "what is X" | Glossary/definition posts |

## How to read consensus (top 10)
1. Classify each of the top 10 by the table above.
2. Count the most common type.
   - **>60%** one type → strong consensus; our page must be that type.
   - **40–60%** → mixed; two types coexist — match the stronger/more-represented one.
   - **<40%** → fragmented; intent unsettled — depth, authority, and freshness decide, type matters less.
3. Also note SERP features: a shopping/product pack or AI Overview shifts intent toward
   transactional/answer formats even if blue links look informational.

## Mismatch severity matrix

| Situation | Severity | Action |
|---|---|---|
| Our type = the >60% consensus type | ALIGNED | Type is fine; diagnose depth/authority/media/schema/freshness |
| Our type ≠ consensus, but consensus is mixed (40–60%) | WARNING | A ranking format exists; assess whether to switch or strengthen |
| Our type ≠ a strong (>60%) consensus | CRITICAL | Wrong page type — reformat or build the correct type; on-page polish won't fix it |

## Common real mismatches for an e-commerce blog
- Informational guide targeting a keyword whose SERP is product/category pages → CRITICAL; point the
  keyword at a collection (or add a buying-guide roundup), don't expand the guide.
- A thin definition post targeting a keyword whose SERP wants comprehensive guides → upgrade to a guide.
- A guide targeting a "best X" keyword whose SERP is all roundups → reformat to a roundup
  (hand to `comparison-pages`) or re-target the guide to an informational sibling keyword
  (resolve via the SERP-overlap test in `keyword-database-article-map`).
