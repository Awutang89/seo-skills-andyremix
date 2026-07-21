# Schema Types Reference (2026)

Which structured-data types to use, which to avoid, and the required fields for each. Adapted from the
open-source `claude-seo` project (MIT). **Verify against Google's current "Structured data markup that
Google Search supports" docs before treating any deprecation date as final** — Google changes this list.

---

## Actively supported (safe to generate)

Organization, LocalBusiness, **Article / BlogPosting**, **Product**, **BreadcrumbList**, Review,
**AggregateRating**, **ItemList**, VideoObject, ImageObject, Event, JobPosting, Course, Recipe.

For your-project the relevant set is: **BlogPosting, BreadcrumbList, Product, ItemList,
AggregateRating, ImageObject** (+ Organization sitewide).

## Deprecated / retired — DO NOT generate

| Type | Status |
|---|---|
| HowTo | Deprecated Sept 2023 — no rich result |
| SpecialAnnouncement | Retired Jul 2025 |
| CourseInfo, EstimatedSalary, ClaimReview, VehicleListing, Practice Problem, Dataset | Deprecated/retired mid-2025 |

## Restricted

| Type | Restriction |
|---|---|
| **FAQPage** | Rich result limited to government & healthcare authority sites (since Aug 2023). For a commercial blog it's allowed markup but won't earn FAQ rich results — keep the existing `jsonld.faq` metafield, but treat FAQ rich results as not guaranteed. Flag as INFO priority, never Critical. |
| HowTo | (see above — gone entirely) |

---

## Required fields per type

### BlogPosting (Article)
Required: `headline`, `image`, `datePublished`, `author`, `publisher` (with `logo`).
Recommended: `dateModified`, `description`, `mainEntityOfPage`.
Notes: `headline` ≤110 chars; image ideally ≥1200px wide; dates ISO 8601 with timezone.

### BreadcrumbList
Required: `itemListElement` array of `ListItem`, each with `position`, `name`; `item` (absolute URL)
on every element **except the last** (current page).

### Product
Required: `name`, `image` (array), `description`, `brand`, `offers`.
`offers` (Offer) required: `price` (number string, no currency symbol), `priceCurrency` (ISO 4217),
`availability` (full schema.org URL, e.g. `https://schema.org/InStock`), `url`.
Field-format rules (hard):
- `price`: `"129.00"` not `"$129"` and not a number-with-symbol.
- `priceCurrency`: ISO 4217 (`"USD"`).
- `availability`: full URL form (`https://schema.org/InStock` / `OutOfStock` / `PreOrder`).
- dates (e.g. `priceValidUntil`): ISO 8601 (`"2026-12-31"`).
- `brand`: non-empty `{ "@type": "Brand", "name": "..." }`.

#### Product schema tier rubric (score completeness)
| Fields present | Score |
|---|---|
| Required only (name, image, description, brand, offers) | 50/100 |
| + `aggregateRating` | 65/100 |
| + `sku` / `gtin` / `mpn` | 75/100 |
| + `shippingDetails` | 85/100 |
| + `merchantReturnPolicy` | 90/100 |
| + ≥3 `review` objects | 100/100 |
Aim for ≥75 on real product pages; ≥85 where shipping/returns data exists.

### ItemList (best-X / roundup / comparison)
Required: `itemListElement` array. Each element either a `ListItem` with `position` + `name` (+ `url`),
or — when you name a specific product with price — an embedded `Product` (with its required fields).
Use `ItemList` for the ranking and embed `Product`/`AggregateRating` for the named items.

Minimal ItemList template:
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Item A", "url": "https://example.com/..." },
    { "@type": "ListItem", "position": 2, "name": "Item B", "url": "https://example.com/..." }
  ]
}
```

### AggregateRating (inside Product/ItemList items)
Required: `ratingValue`, `reviewCount` (or `ratingCount`), `bestRating` (default 5). Only use real,
on-page ratings — never invent ratings (manual-action risk).

### Organization (sitewide publisher — referenced by every BlogPosting)
Emit **once** sitewide (theme `<head>`), then reference it by `@id` from each article instead of
re-embedding the publisher block. Required: `name`, `url`, `logo` (ImageObject, ≥112×112). Recommended
for E-E-A-T/trust: `contactPoint` (or a link to a real contact page) and `sameAs` (array of the brand's
**real** profile URLs — manufacturer/marketplace pages, YouTube, LinkedIn). Never invent profiles.

```json
{
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Your Brand",
  "url": "https://example.com/",
  "logo": { "@type": "ImageObject", "url": "https://example.com/[logo-path]", "width": 112, "height": 112 },
  "sameAs": ["https://www.youtube.com/@...", "https://www.linkedin.com/company/..."]
}
```

This is our **institutional-voice E-E-A-T anchor**: authority is carried by the Organization (plus
named primary sources in the body), not a personal byline. Keep `author` as the Organization unless a
real bylined expert with a real bio page exists. (See the author note in `SKILL.md`.)

### VideoObject (only when a real video is embedded on the page)
Use **only** if the article actually embeds a video (e.g. a YouTube how-to). Required: `name`,
`description`, `thumbnailUrl`, `uploadDate` (ISO 8601), plus one of `contentUrl`/`embedUrl`. Give it a
stable `@id` (`#video-1`). Do **not** add VideoObject to a page with no video — schema must match
visible content. (We currently embed no video; this entry is here for when we do.)

---

## The @graph + @id pattern (combine multiple types on one page)

A blog article legitimately carries several types — BlogPosting + BreadcrumbList, plus the sitewide
Organization. Instead of three separate `<script>` blocks with the publisher duplicated in each, emit
**one** `<script type="application/ld+json">` whose top level is `@graph` (an array of entities),
connected by stable `@id`s:

- **Organization** → `@id: "{site}/#organization"` (emitted sitewide; articles reference it).
- **BlogPosting** → `@id: "{site}/blog/{slug}#article"`; its `publisher` is
  `{ "@id": "{site}/#organization" }` — a *reference*, not a re-embed; `mainEntityOfPage` is the page URL.
- **BreadcrumbList** → `@id: "{site}/blog/{slug}#breadcrumb"`.

Benefits: no duplicated publisher block, entities are linked (Google/AI engines build one connected
graph), and Organization updates happen in one place. Keep it server-rendered (Liquid), same as today.

Minimal shape:
```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "https://example.com/#organization", "name": "Your Brand", "url": "https://example.com/", "logo": { "@type": "ImageObject", "url": "https://example.com/[logo-path]" } },
    { "@type": "BlogPosting", "@id": "https://example.com/blog/[slug]#article", "headline": "...", "publisher": { "@id": "https://example.com/#organization" }, "mainEntityOfPage": "https://example.com/blog/[slug]" },
    { "@type": "BreadcrumbList", "@id": "https://example.com/blog/[slug]#breadcrumb", "itemListElement": [ "..." ] }
  ]
}
```

Adopt **incrementally**: the current separate-block snippets are still valid. Move to `@graph` the next
time the theme schema is touched — it's a consolidation, not a fix for anything broken. The per-article
ItemList metafield (roundups) can stay its own block or join the graph. (@graph/@id/Organization/
VideoObject guidance adapted from the `claude-blog` schema-stack, MIT.)

---

## Universal rules
- `@context`: always `https://schema.org`.
- All URLs absolute and `https`.
- Markup must match content visible on the page. No schema for off-page or hidden content.
- Server-rendered (Liquid/json metafield), not browser-built JS.
- Prefer JSON-LD; never Microdata/RDFa.
