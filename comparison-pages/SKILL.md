---
name: comparison-pages
description: "Playbook for comparison content — X vs Y, alternatives-to-X, and best-[category] roundups. Use when writing or refreshing a comparison/versus/buying-guide article. Layers a feature-matrix, fairness, dated-claims, and ItemList/Product schema discipline on top of the standard seo-content workflow. Triggers on: write a vs article, X vs Y comparison, alternatives to X, best [category] guide, brand comparison, comparison table, buying guide roundup. Outputs a comparison article that wins commercial-intent SERPs without misleading readers."
---

# Comparison Pages Playbook

Comparison content is the highest-commercial-intent content we publish — and the easiest to get sued
over or penalized for. A "vs" article that fudges a competitor's spec, quotes a price with no date, or
reads like a hit piece loses trust with both readers and Google. This playbook makes comparison
articles win the SERP **and** stay defensible: every claim verifiable, every price dated, every
competitor described honestly, and the right ItemList/Product schema attached.

This is **not** a replacement for `skills/seo-content/SKILL.md` — it's a specialization layer. Run the
normal seo-content workflow (research → brief → outline → draft → humanize → optimize → QA), and apply
the rules here wherever the article is a comparison. The seo-content **Comparison Structure** (Quick
Verdict → table → deep dives → head-to-head → FAQ → recommendation) is the skeleton; this adds the
discipline.

---

## The three comparison page types

| Type | Keyword pattern | Our examples | Schema |
|---|---|---|---|
| **X vs Y** (type or brand) | `[A] vs [B]`, `[A] or [B]` | [spec-A] vs [spec-B], [size-A] vs [size-B], [type-A] vs [type-B], [Brand A] vs [Brand B] | (none required; Product only if naming specific SKUs) |
| **Alternatives to X** | `[X] alternatives`, `alternative to [X]` | alternatives to a specific brand/model | ItemList |
| **Best [category]** roundup | `best [category]`, `best [category] for [use]` | best [product], best [product] for [use case], best [attribute] [product] | **ItemList** (+ Product/AggregateRating for named picks) |

Pick the type from search intent (use the seo-content Phase 1 SERP analysis + the SERP-overlap test in
`keyword-database-article-map` if it's unclear whether two comparisons should be one article).

---

## Rule 1 — Pick a winner, but earn it

Brand voice is opinionated: when the answer is clear, say so (the brand-voice profile calls for
picking a winner — "[option X] wins for 90% of jobs"). A comparison that ends in "it depends" with no
decision has failed. **But** the verdict must be earned by the comparison body, not asserted. Lead with
a **Quick Verdict** (200–300 words) that states the call and the one variable it hinges on, then prove
it. The [A]-vs-[B] article is the template: the verdict ("[attribute] follows the use case")
is then derived from the [key spec] throughout.

Always include the decision-by-use-case cut: "Choose X if… / Choose Y if…" or a use-case table. The
winner is rarely universal — name the conditions.

---

## Rule 2 — The feature matrix

Every X-vs-Y and best-X article needs a **comparison table** with 8–12 differentiators that actually
decide the purchase (not filler rows). For a given product that's typically: [key spec], [spec @ condition],
[type/mechanism], [attribute], [performance metric], [power/rating], [footprint/dimension], [service life], price range,
best-for. One row per differentiator, one column per option.

- Every cell is a **verifiable fact** from a public source (spec sheet, manufacturer page, standards
  doc) — not a guess.
- Missing data → **"Not publicly available"**, never a fabricated number.
- Keep cells concise; the prose deep-dives explain the *why* behind the table.

---

## Rule 3 — Dated, sourced, fair (non-negotiable for brand comparisons)

This is where comparison content gets dangerous. Apply strictly, especially for brand-vs-brand:

- **Prices and specs get a date:** "as of [Month Year]" plus the source. Prices drift; an undated
  price is a future inaccuracy. (Pairs with the `/schedule` habit — comparison articles with dated
  pricing are legitimate refresh candidates.)
- **Cite every competitive claim** to a public source (manufacturer spec, standards body, an
  independent test). Assertions like "Brand A underperforms on [metric]" need a measured figure with a source.
- **Describe competitors honestly.** State their genuine strengths. No defamation, no aggressive
  sales language in a competitor's description. If we sell the winner, that's fine — but the loser's
  real advantages still get named. (This is also an E-E-A-T Trustworthiness signal.)
- **Disclose affiliation** where we sell one side. Link to the collection naturally (per seo-content
  internal-linking rules), don't astroturf.

The fairness rules are also what make the article *citable* by AI engines and durable against Google's
trust signals — honest comparisons outrank hit pieces.

---

## Rule 4 — Schema (via seo-schema)

- **Best-X / roundup / alternatives:** generate an **ItemList** of the ranked picks; embed
  **Product** (+ **AggregateRating** only if real ratings exist) for any specifically named product
  with a price. Use `skills/seo-schema/SKILL.md` → save the sidecar to
  `your-project/schema/[slug].json` → `python your_metafield_upload.py --single [slug]   # your Shopify GraphQL metafield upload`.
- **Plain type comparisons** ([spec-A] vs [spec-B]) usually need **no extra schema** beyond the theme's
  Article/Breadcrumb — only add Product if you name specific SKUs with prices.
- Never invent ratings or prices for schema (manual-action risk).

---

## Rule 5 — Conversion without sleaze

- **Above the fold:** the Quick Verdict + (for roundups) a summary of the top pick, with one clear
  CTA (the matching collection link).
- After the comparison table and at the natural decision point, place the collection/product link —
  woven in per seo-content link rules, not a banner.
- Trust signals: an "as of [date]" / "last updated" note and the sourcing make the page credible.

---

## Title & meta patterns
- X vs Y: `[A] vs [B]: [Differentiator] ([Year])` — e.g. "[Option A] vs [Option B]: Which Lasts
  Longer?" Keep ≤60 chars (seo-content hard limit).
- Best-X: `Best [Category] for [Use] ([Year])`.
- Meta description still needs a specific stat (seo-content rule) — use the headline differentiator.

---

## Comparison QA (run in addition to the seo-content Phase 7 gate)

| Check | Result |
|---|---|
| Quick Verdict present (200–300w) and names the deciding variable | PASS / FAIL |
| Decision-by-use-case present ("Choose X if…" or use-case table) | PASS / FAIL |
| Feature matrix: 8–12 purchase-deciding rows, every cell verifiable | PASS / FAIL |
| Missing data shown as "Not publicly available" (no fabricated specs) | PASS / FAIL |
| Every price/spec has "as of [date]" + source | PASS / FAIL |
| Each competitor's genuine strengths stated; no defamation/hype | PASS / FAIL |
| Affiliation disclosed where we sell a side | PASS / FAIL |
| Roundup/alternatives: ItemList (+Product/AggregateRating for named picks) generated & validated | PASS / FAIL / N/A |
| No invented ratings or prices in schema | PASS / FAIL |

---

## How this connects
- **`skills/seo-content/SKILL.md`** — the base workflow; this specializes the Comparison content type.
- **`skills/seo-schema/SKILL.md`** — ItemList/Product/AggregateRating generation + upload.
- **`skills/keyword-database-article-map/SKILL.md`** — SERP-overlap test to decide if two comparisons
  should merge; thin-content uniqueness vs the sibling comparison.
- **`your-project/brand/voice-profile.md`** — opinionated, pick-a-winner voice.
