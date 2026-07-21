---
name: seo-schema
description: "Generate and validate structured data (JSON-LD) for your-project beyond FAQ — Article/BlogPosting, BreadcrumbList, Product, and ItemList. Use when adding rich-result markup to a blog article or product/comparison page, auditing existing schema, or wiring schema into the Shopify theme. Triggers on: add schema to article, JSON-LD for X, breadcrumb schema, product schema, article schema, structured data, rich results, schema markup. Outputs validated JSON-LD plus the Shopify delivery method (theme snippet or jsonld metafield)."
---

# SEO Schema (Structured Data Beyond FAQ)

Wrong schema costs more than no schema. A deprecated type (HowTo, retired Sept 2023) or FAQ markup on
a commercial page (restricted to gov/health authority sites since Aug 2023) gets ignored at best and
flagged in Search Console at worst — while you think you're covered. This skill generates only the
schema types Google still rewards, validates them against current requirements, and ships them the
right way for a Shopify storefront.

It is the sibling of `skills/faq-jsonld/SKILL.md` (which already handles FAQPage). This skill covers
everything else: **Article/BlogPosting, BreadcrumbList, Product, and ItemList**.

---

## The core job

Take an article or product/comparison page and produce **valid JSON-LD** plus the **correct delivery
method** for Shopify. Two delivery mechanisms — pick by whether the data is derivable:

| Schema type | Best delivery | Why |
|---|---|---|
| **Article / BlogPosting** | **Theme snippet** (one-time) | Every field (title, dates, image, author, publisher, URL) is a native Liquid object — the theme can build it for all your articles at once. No per-article work. |
| **BreadcrumbList** | **Theme snippet** (one-time) | The blog → article hierarchy is native (`blog.title`, `article.title`, URLs). Build once for all articles. |
| **Product** | **Theme snippet** (one-time) | Shopify product objects expose price, availability, sku, brand, images. Build once for the product template. Per-product overrides via metafield only when needed. |
| **ItemList** (best-X / roundup / comparison) | **`jsonld` metafield** (per-article) | The list of items is editorial and article-specific — not derivable. Generate per article and upload like FAQ. |
| **FAQPage** | already handled | See `skills/faq-jsonld/SKILL.md`. |

**Rule of thumb:** if Shopify already knows the data, emit it in the theme once. If the data lives only
in the article's editorial content, store it as a `jsonld.*` metafield per article.

---

## Hard rules (read `references/schema-types-2026.md` before generating)

- **Only generate actively supported types.** Do NOT generate HowTo (deprecated Sept 2023),
  SpecialAnnouncement (retired Jul 2025), or other retired types. Full list in the reference.
- **FAQPage is restricted** to government/healthcare authority sites since Aug 2023. For our blog,
  FAQ markup is "nice to have," not a rich-result guarantee — keep using the existing `jsonld.faq`
  metafield, but don't expect FAQ rich results. (This is why FAQ stays in its own skill, unchanged.)
- **Server-render the JSON-LD.** AI crawlers and Google process server-rendered markup reliably;
  JS-injected schema (especially time-sensitive Product/Offer) is processed late or missed. Shopify
  Liquid is server-rendered — emit schema in the theme/`.liquid`, never via a client-side `<script>`
  that builds it in the browser. (Ties to `skills/seo-content/references/geo-checklist.md`.)
- **JSON-LD only.** It's Google's stated preference; never emit Microdata/RDFa.
- **No placeholder text, no relative URLs, valid `@context`.** Every URL absolute
  (`https://example.com/...`), every required field populated.
- **Multiple types on one page → use `@graph` with `@id` references.** Don't ship three separate
  `<script>` blocks with the publisher duplicated in each. Emit the sitewide **Organization** once and
  reference it by `@id` from each BlogPosting. See the `@graph + @id` pattern and the Organization
  object in `references/schema-types-2026.md`. (Incremental — current separate blocks remain valid.)

---

## Delivery method 1 — Theme snippet (Article, Breadcrumb, Product)

These are built once in the Shopify theme and apply to every page of that type. This skill's job is to
(a) supply the JSON-LD template, (b) tell you which Liquid fields map to which schema fields, and
(c) give you the snippet to paste. **This is a one-time theme edit, not per-article.**

### Article / BlogPosting (blog article template)

Template (theme renders the bracketed Liquid values server-side):

```liquid
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": {{ article.title | json }},
  "description": {{ article.excerpt_or_content | strip_html | truncate: 300 | json }},
  "image": {{ article.image | image_url: width: 1200 | prepend: "https:" | json }},
  "datePublished": {{ article.published_at | date: "%Y-%m-%dT%H:%M:%S%z" | json }},
  "dateModified": {{ article.updated_at | date: "%Y-%m-%dT%H:%M:%S%z" | json }},
  "author": { "@type": "Organization", "name": "Your Brand" },
  "publisher": {
    "@type": "Organization",
    "name": "Your Brand",
    "logo": { "@type": "ImageObject", "url": "https://example.com/[logo-path]" }
  },
  "mainEntityOfPage": { "@type": "WebPage", "@id": {{ request.origin | append: article.url | json }} }
}
</script>
```

**Author note (E-E-A-T fit):** we use an **institutional voice**, so `author` is the Organization, not
a personal byline — consistent with the brand voice profile and the E-E-A-T rubric in seo-content
(no invented author personas). If a genuine bylined expert exists, switch `author` to `{ "@type":
"Person", "name": "...", "url": "[bio page]" }` — but only when the bio page is real.

### BreadcrumbList (blog article template)

```liquid
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
    { "@type": "ListItem", "position": 2, "name": {{ blog.title | json }}, "item": {{ request.origin | append: blog.url | json }} },
    { "@type": "ListItem", "position": 3, "name": {{ article.title | json }} }
  ]
}
</script>
```
(Last item omits `item` per Google guidance — the current page isn't a link.)

### Product (product template)

Use the **Product schema tier rubric** in `references/schema-types-2026.md` — score what fields you can
populate (required → 50/100, +aggregateRating → 65, +sku/gtin/mpn → 75, +shippingDetails → 85,
+merchantReturnPolicy → 90, +3 reviews → 100). Field rules: price as a **number string** (no `$`),
ISO 4217 currency, availability as a full schema.org URL, ISO 8601 dates, non-empty brand.

---

## Delivery method 2 — `jsonld` metafield (ItemList for roundups/comparisons)

For "best X," roundup, or comparison articles, the list of recommended items is editorial. Generate an
**ItemList** (and, where you name specific products with prices, **Product**/**AggregateRating**) and
store it as a per-article metafield, exactly like FAQ.

**Workflow:**
1. Generate the JSON-LD object(s) for the article (see ItemList template in the reference).
2. Save to a sidecar file: `your-project/schema/[article-slug].json` (a JSON array of one or more
   JSON-LD objects).
3. Upload: `python your_metafield_upload.py --single [article-slug]   # your Shopify GraphQL metafield upload` (dry-run first).
   This stores the value as metafield namespace `jsonld`, key by type (`itemlist`/`product`), type
   `json`, using the same Shopify GraphQL metafield upload (metafieldsSet) as the FAQ metafield.
4. The theme renders any present `jsonld.*` json metafields in a `<script type="application/ld+json">`
   block (same mechanism the theme already uses for `jsonld.faq`).

> The comparison-page playbook (`skills/comparison-pages/SKILL.md`) calls this skill to produce the
> ItemList/Product/AggregateRating markup for vs / alternatives / best-X pages.

---

## Workflow (per article or page)

1. **Identify the page type** → pick schema types (article → BlogPosting + Breadcrumb [theme, already
   on]; comparison/roundup → + ItemList/Product [metafield]; product page → Product [theme]).
2. **Check the type is still supported** (`references/schema-types-2026.md`). Never emit a deprecated type.
3. **Theme types:** confirm the theme snippet is installed and rendering (one-time). If not, supply the
   snippet above for the user to add to the theme.
4. **Metafield types:** generate the JSON-LD, save the sidecar, dry-run + upload the metafield.
5. **Validate** (see below) before considering it done.

---

## Validation (always, before "done")

Run every generated block through validation and report a table:

| Check | Result |
|---|---|
| Valid `@context` (`https://schema.org`) and correct `@type` | PASS / FAIL |
| Type is actively supported (not deprecated/restricted) | PASS / FAIL |
| All required fields present for the type (per reference) | PASS / FAIL |
| All URLs absolute (`https://example.com/...`), no relative paths | PASS / FAIL |
| No placeholder text (`[...]`, "example", lorem) | PASS / FAIL |
| Product: price is number-string, ISO 4217 currency, schema.org availability URL, ISO 8601 dates | PASS / FAIL / N/A |
| Server-rendered (theme/`.liquid` or json metafield) — not JS-built in browser | PASS / FAIL |
| Matches visible page content (no schema for content that isn't on the page) | PASS / FAIL |
| Multiple types: one `@graph` block, publisher via `@id` reference (not duplicated per script) | PASS / FAIL / N/A |
| Sitewide Organization present with logo (+ contactPoint/sameAs where real, no invented profiles) | PASS / FAIL |

Then run the block through Google's Rich Results Test before publishing. Schema that doesn't match the
visible page is a manual-action risk — never mark up content the reader can't see.

---

## How this connects
- **`skills/faq-jsonld/SKILL.md`** — FAQPage (unchanged); same metafield + upload mechanism.
- **`skills/comparison-pages/SKILL.md`** — consumes this skill for ItemList/Product/AggregateRating.
- **`skills/seo-content/references/geo-checklist.md`** — server-render requirement (AI citability).
- **Your metafield upload step (Shopify GraphQL metafieldsSet)** — uploads `jsonld.*` json metafields.

## Reference
- `references/schema-types-2026.md` — actively supported vs deprecated/restricted types, required
  fields per type, the Product schema tier rubric, and field-format rules.
