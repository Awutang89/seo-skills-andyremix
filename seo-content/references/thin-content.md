# Thin-Content Guardrails

Quality gates that keep content above Google's thin/scaled-content line. Adapted from the
open-source `claude-seo` project's programmatic-SEO guardrails (MIT). We hand-write long-form
articles, so the raw word-count floor is almost never the binding constraint — **for us the real
risk is two of our own articles being near-duplicates** (comparison pairs, hub vs spoke, two
articles in the same cluster). This guardrail is the article-level companion to the dedup work in
`keyword-database-article-map` and the SERP-overlap test there.

> **Context:** Google's Scaled Content Abuse policy escalated enforcement through 2025 (notably a
> June-2025 wave against AI content farms). The thresholds below are the published rule-of-thumb
> lines; verify specifics against Google's current guidance before treating any number as exact.

---

## The thresholds

| Metric | Threshold | Action |
|---|---|---|
| Word count of unique substance | < 300 words | Review flag (trivially passed by our long-form articles) |
| Content unique to this page | < 40% | **Flag as thin** — investigate vs. the nearest sibling |
| Content unique to this page | < 30% | **Hard stop** — do not publish; merge or re-angle first |

### Uniqueness %
```
unique % = (words unique to this article) / (total article words) × 100
```
- **Exclude** shared site furniture (nav, header, footer, boilerplate CTA) — for our `.md` files
  the body is all content, so this is straightforward.
- **Include** any templated/boilerplate passages you reuse across articles.
- Compare against this article's **nearest sibling** — the most similar existing article in
  `KEYWORD-REGISTER.csv` (the other half of a comparison pair, the hub if this is a spoke, or the
  closest same-cluster article). Not the whole site — the closest neighbor.

---

## How to apply (hand-written site)

1. Identify the nearest sibling from the register (same cluster / comparison counterpart / hub).
   If the SERP-overlap test in `keyword-database-article-map` already flagged a near-duplicate, that
   is your sibling.
2. Eyeball: does this draft repeat the sibling's sections, examples, tables, and figures, or does it
   carry its own angle, its own data, and its own examples? The angle note in the article map says
   what should make it distinct — confirm the draft actually delivers that.
3. If <40% feels unique → strengthen the distinct angle (different data, scenarios, examples) before
   publishing. If <30% → it shouldn't be a separate article; merge into the sibling or re-scope.

## Safe vs. penalty-risk patterns
- **Safe:** articles with real, distinct data/specs, genuine comparisons backed by figures, original
  testing or operational detail. (This is our normal output.)
- **Penalty risk:** spinning a near-identical second comparison with only the product names swapped;
  a "best X" with no real selection criteria; padding to a word count with filler. The Sentence
  Contribution Rule in `SKILL.md` already guards against filler — this guards against *duplication*.

## How this connects
- Structural dedup (which articles should exist at all): `keyword-database-article-map` +
  its SERP-overlap test.
- Article-level enforcement: the Content Quality row in the `SKILL.md` Phase 7 QA gate.
