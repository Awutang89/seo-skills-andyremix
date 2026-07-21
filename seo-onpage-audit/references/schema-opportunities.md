# Schema Opportunities — content signal → recommend missing schema

Used by the audit's "Schema opportunities" step. The audit already reports which JSON-LD types are
**present + valid**; this file is the map for recommending types the page **qualifies for but is
missing**. Self-contained — the gate below is baked in, so no external data is needed. (If a
`seo-schema` skill is present in the library, hand the recommendation to it for implementation.)

## How to use it
1. Detect the content signals in the parsed page (below).
2. For each signal, check whether the matching schema type is **already** in the page's JSON-LD.
3. If missing AND the type is not deprecated, recommend it — at the priority shown.
4. Only recommend a type the page genuinely qualifies for. Do not suggest schema for content that
   isn't actually on the page.

## Signal → schema map

| Content signal on the page | Recommend (if missing) | Priority |
|---|---|---|
| Editorial article / blog post (author-ish byline, dateline, long body) | **Article / BlogPosting** | HIGH |
| Breadcrumb trail in the UI, or a clear section hierarchy in the URL | **BreadcrumbList** | HIGH |
| Ranked list / roundup ("best X", "top N"), or a comparison table | **ItemList** (+ **Product** / **AggregateRating** per item where prices/ratings exist) | HIGH |
| Single product with price / SKU / add-to-cart / spec table | **Product** (+ **AggregateRating**/**Review** if ratings shown) | HIGH |
| Standalone review of one product/service with a verdict/rating | **Review** (+ **AggregateRating** if aggregate shown) | MED |
| A **video is actually embedded** on the page (not just linked) | **VideoObject** | MED |
| Q&A block / a section literally headed "FAQ" / "Frequently Asked Questions" | **FAQPage** | **INFO only** (see gate) |
| Business name/address/phone (NAP), hours, a physical location | **LocalBusiness** (or **Organization** sitewide) | MED |
| Site/brand identity, logo, social profiles (usually sitewide, not per page) | **Organization** | LOW |
| A primary content image worth featuring (hero/diagram) | **ImageObject** (or the image field inside Article/Product) | LOW |
| Dated event with a start time / venue | **Event** | MED |
| Job posting (title, location, comp) | **JobPosting** | MED |
| Structured recipe (ingredients + steps) | **Recipe** | MED |

## The gate — supported / restricted / deprecated

**Supported (safe to recommend when the signal is present):** Organization, LocalBusiness,
Article / BlogPosting, Product, BreadcrumbList, Review, AggregateRating, ItemList, VideoObject,
ImageObject, Event, JobPosting, Course, Recipe.

**Restricted — recommend as INFO only, never HIGH/Critical:**
- **FAQPage** — since Aug 2023 the FAQ *rich result* is limited to authoritative government and
  health sites. Adding valid FAQPage markup is still fine (helps AI/parse), but do NOT promise a
  rich result. Always flag it INFO.

**Deprecated / DO NOT recommend (even if the content seems to fit):**
- **HowTo** — deprecated Sept 2023; the rich result is gone. A page with numbered steps must **NOT**
  be told to add HowTo. Recommend a clear step layout in the body instead, not the schema.
- SpecialAnnouncement, ClaimReview, CourseInfo, EstimatedSalary, VehicleListing, Practice Problem,
  Dataset — do not recommend.

## Conditions & don'ts
- **VideoObject only if a video is truly embedded.** Never add VideoObject to a page with no video.
- **Match markup to visible content.** FAQPage must correspond to a real, visible FAQ; Product to a
  real product; Review to a real review. Mismatched/invisible markup risks a manual action.
- **Multi-type pages:** if you recommend more than one type (e.g. Article + Breadcrumb + FAQPage),
  note they should share one `@graph` with `@id` cross-references rather than separate blocks.
- Output recommendations under a **"SCHEMA OPPORTUNITIES"** heading in the audit, each line naming
  the signal, the recommended type, and the priority.
