# Site interview and brief

Goal: enough truth about the business to write a sharp brief and a site blueprint. Act as a
strategist, not a form: ask what matters for this business, skip what is already known, and
challenge vague answers.

## How to run it

- Every question through `AskUserQuestion`. One topic per turn, 2-3 related questions at most.
- Adapt: follow up on what the user said, not on the next line of a script. Cover the topics in
  whatever order the conversation makes natural, and skip any that context already answers.
- Never re-ask a fact the user already gave, or one that exists in `./brand/` (voice profile
  from `brand-voice`, positioning from `positioning-angles`). Show what was found and ask only
  for corrections.
- Recommend instead of listing options: "I'd go with X, because Y."
- Reject empty answers politely: "modern and clean" is not a look; "everyone" is not a customer.
- User is stuck → "Write something honest for now; we can sharpen it later."

## Step 0: new site or redesign

Ask first, it changes everything after it:

- **New site**: blank slate.
- **Redesign, keep the branding**: same colors, fonts and identity, rebuilt.
- **Redesign, new direction**: existing site, fresh look.

Any redesign:
1. Ask for the URL. Run `scripts/extract_brand.py <url> -o .site-concepts/brand-extraction`
   and read `brand-identity.json`. Summarize in one message: the most-used colors (hex + where
   they appear), fonts in use, logo found or not.
   Shopify store: prefer the theme's own settings (`config/settings_data.json` colors and font
   pickers via the Shopify CLI theme pull) over scraping.
2. Keep branding → confirm what is right, ask about tweaks, then lock colors and fonts (skip
   the color/font topic later).
   New direction → treat the extraction as "what we are moving away from" and still run the
   visual topics.
3. Redesign always triggers `SKILL.md` §9: crawl the old URLs now; the redirect map is part of
   the plan.

## Topics

### Business and positioning
Need: a one-sentence description, a specific customer (industry or situation, role, size, the
frustration that brings them), the ONE action a visitor should take, and a concrete
differentiator (smaller claims are fine if true: "you talk to the owner, not a call center").
Then play it back: "Here's what I'm hearing: <2-3 sentences>. What would you change?"
Quality bar: a real person could match the customer description; the differentiator is a fact,
not "we care more".

### Vibe
- "What should someone feel in the first three seconds, before reading anything?"
- "What are you NOT? Not corporate, not edgy, not academic?"
- Vague → offer reactions: trust and authority / warm and approachable / bold and creative /
  clean and minimal / premium / energetic. Push for a reaction, not a pick ("a luxury brand's
  site or a startup's: which feels closer?").

### Inspiration
- 2-3 sites they like, any industry; screenshots of specific elements; any logo or brand
  assets they already have.
- Fetch each URL through a subagent (keeps raw pages out of the main context) and note: palette
  (dominant, secondary, accent), type (serif or sans, weight contrast, heading scale), density
  (whitespace, grid, section rhythm), design family (editorial, minimal, organic, brutalist…).
- Synthesize: "The common thread is <x>. That tells me the site should feel <y>."

### Colors and fonts (constraints only)
Skip if locked by a keep-branding redesign. Ask only: brand hex codes that must stay, colors to
avoid, a font they must use. Record them as anchors. Do not propose palettes or pairings here;
that is the designer's job per direction.

### Site structure
- Launch pages ("Home is a given; what else on day one?" About, Services, Portfolio, Contact,
  Pricing, Blog, FAQ…). Six or more → "Which are truly needed at launch, and which can wait a
  few months until there is content for them?"
- Home page: what must be visible before scrolling; what proof exists **today** (testimonials,
  client logos, case studies, numbers, press), not what is planned; primary and secondary CTA.
- **Build around what exists.** Two testimonials → a section sized for two. No proof → no proof
  section (or a clearly labelled placeholder the user agrees to fill before launch).
- Feed the page list into `SKILL.md` §1: each page gets a target query class there.

### Content (skip for simple brochure sites)
Blog and cadence (hand off to `keyword-research`); content to migrate (feeds the §9 map); lead
magnets (hand off to `lead-magnet`).

## Enough to stop

- [ ] One-sentence business description
- [ ] Specific customer
- [ ] Primary CTA
- [ ] Concrete differentiator
- [ ] Vibe
- [ ] Required and avoided colors (or none)
- [ ] Required fonts (or none)
- [ ] Launch pages
- [ ] Home page sections and which content is ready

## Brief template (`.site-concepts/brief.md`, copied to `./brand/site-brief.md`)

```markdown
# Brief: <business>

## Positioning
- Business:
- Customer:
- Primary CTA:
- Differentiator:
- Positioning statement: (2-3 sentences, as confirmed in the playback)

## Voice
Link to ./brand/voice-profile.md if it exists. Otherwise:
- Personality (2-3 adjectives):
- Tone:
- We are: / We are not:

## Visual identity
- Anchor colors: (hex, or "none: designer's choice per direction")
- Avoid:
- Required font: (or "none")
- Vibe words (3-5):
- Inspiration pattern:
- Do: / Don't:

## Site blueprint
### Launch pages
Per page: purpose (one sentence), target query class (from SKILL.md §1), sections in order,
content status (ready / needs writing / placeholder agreed).
### Later pages
Page + note.
### Home page sections
| Section | Content needed | CTA | Status |
|---|---|---|---|

## Content inventory
- Ready:
- To create:
- Assets on hand: (logo, photos, headshots, client logos with permission)

## CTA plan
- Primary: text → destination
- Secondary: text → destination
- Placement across the site:
```

File: seo-site-build/references/interview.md · Version 1.0 · November 2026
