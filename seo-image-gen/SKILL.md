---
name: seo-image-gen
description: "Generate SEO-ready images for articles and products — OG/social cards, blog heroes, product shots, and infographics — then apply alt text, WebP conversion, descriptive filenames, and ImageObject schema. Use when an article needs an image and no suitable stock/CDN image exists, or for branded OG cards and data infographics. Triggers on: generate an image, make a blog hero, OG image, social card, infographic, product image, create graphics. Outputs the generated asset(s) plus their SEO metadata. Requires a connected image-generation backend (see setup gate)."
---

# SEO Image Generation

We currently source images from free-stock CDNs. That covers generic shots but not two things we keep
needing: **branded OG/social cards** (so shared links look intentional) and **data infographics** (the
multi-modal pairing the GEO rules reward — a chart next to a citable answer block). This skill
generates those on demand and ships them SEO-ready, rather than leaving placeholders.

> **SETUP GATE — read before first use.** Image generation needs an external backend, which is **not
> yet wired up**. claude-seo uses Gemini via the `banana` MCP server; alternatives are any image API
> or a connected MCP image tool. **Before generating anything, confirm with the user which backend to
> use and connect it.** Until then, this skill defines the briefs and SEO post-processing but cannot
> render. This is the one ported skill with an unresolved external dependency.

---

## Generation modes

| Mode | Aspect ratio | Use case |
|---|---|---|
| OG / social card | 16:9 (1200×630) | Link previews for an article — branded, title legible |
| Blog hero | 16:9 widescreen | Article header image when no stock fit exists |
| Product shot | square / as needed | Clean-background product image (studio look) |
| Infographic / chart | vertical or 4:3 | Data visualization to pair with a citable section (GEO) |
| Batch | per mode | Multiple variants to choose from (default 3) |

---

## Workflow
1. **Confirm backend is connected** (setup gate). If not, stop and ask the user.
2. **Identify the mode + target** (which article/section, what it must show).
3. **Build the creative brief** — subject, style (clean/technical, matches the [product/brand]
   register, not consumer-retail glitz), composition, palette, text-on-image (for OG cards: the
   article's hook/title), what to avoid.
4. **Set aspect ratio** per the mode table.
5. **Generate** (batch of 3 for heroes/OG so there's a choice).
6. **Post-process for SEO** (always — this is the part that makes it count):
   - **Alt text**: descriptive, 10–125 chars, keyword only where it genuinely describes the image
     (see `skills/image-seo-audit/SKILL.md`).
   - **Filename**: descriptive-hyphenated (`[option-a]-vs-[option-b]-[key-spec]-chart.webp`), never `gen_001`.
   - **Format/size**: export/convert to **WebP**, respect the size tiers (hero < 200 KB).
   - **Schema**: add ImageObject / ensure the image is in the article's BlogPosting image field
     (`skills/seo-schema/SKILL.md`).
   - **OG**: wire the card into the page's `og:image` (theme/metafield) if it's a social card.
7. **Place it** adjacent to the relevant citable block (GEO multi-modal rule).

---

## Cost awareness
Generation is metered (claude-seo cites ~$0.02–$0.16/image depending on resolution/backend). Before a
batch, state the rough cost and the count. Don't silently generate 20 variants.

## Honesty rules
- **Label AI-generated images** where required (e.g. Merchant Center / `DigitalSourceType`
  `trainedAlgorithmicMedia` metadata) so product/marketplace use stays compliant.
- Don't generate fake product photos that misrepresent a real SKU we sell — use real product imagery
  for actual products; reserve generation for heroes, OG cards, and infographics.

## How this connects
- **`skills/image-seo-audit/SKILL.md`** — when an audit gap is "no suitable image," generate one here;
  alt/size/format rules are shared.
- **`skills/seo-content/SKILL.md`** — Phase 1.5 image research (use this when stock fails) + GEO
  multi-modal pairing.
- **`skills/seo-schema/SKILL.md`** — ImageObject and BlogPosting/Product image fields.
