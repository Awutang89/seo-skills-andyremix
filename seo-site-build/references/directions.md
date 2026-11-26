# Design directions (brainstorm)

After the interview, propose exactly N directions (N from the user, default 3). The one rule that
matters: **directions differ in structure and feel, not just color.** One layout in three
palettes is one direction.

## Fixed vs open

Fixed for every direction: positioning, voice, CTA plan, anchor colors and fonts, colors to
avoid, and any ban in an existing `DESIGN.md`.

Open per direction: the palette (tokens below), the heading + body font pair, and the contrast
axes. The skill is the designer: present each direction as a finished proposal; do not ask the user to
choose colors.

## Contrast axes

Each direction should differ from each other one on at least four or five of these:

| Axis | Range |
|---|---|
| Density | airy / balanced / packed |
| Type hierarchy | huge contrast / quiet steps / one dominant size / caps labels / expressive display |
| Weight strategy | light vs heavy / even medium / heavy throughout / hairline + black |
| Metaphor | editorial (magazine) / workshop (craft) / layered (depth) / minimal (breathing room) / natural (organic forms, texture) |
| Hero | full-bleed photo / split / type-only / video / illustration |
| Section rhythm | steady grid / alternating / asymmetric / modular blocks |
| Shape | square / rounded / pill / mixed |
| Depth | flat / soft shadow / strong shadow / overlapping layers (a brand that bans shadows keeps this axis at flat or overlap) |
| Proof | numbers first / quotes first / project grid / logo row |
| Whitespace | generous / balanced / tight |

## Palette and fonts

Internally try two or three palettes and pairings per direction, keep the best fit, never show
the discarded ones.

Tokens per direction:
- `primary` (main brand and CTA), `secondary`, `accent`
- `bg` (page), `surface` (cards and alternate sections, a step off `bg`)
- `text`, `muted` (secondary text), `hairline` (borders)
- `accent-ink`: the accent darkened until it passes as text on `bg` and `surface`

Rules:
- Every text/background pair passes WCAG AA (4.5:1; 3:1 for large text). `muted` must pass as
  small text on both `bg` and `surface`. Record the ratios.
- Palettes are clearly different moods across directions, not the same hue shifted.
- Each palette fits its metaphor (earthy for natural, high contrast for bold).
- Anchor colors appear in every direction; supporting colors can change.
- Fonts reinforce the metaphor (editorial → serif heads, precise → geometric sans).
- Each font must exist as an npm package: `@fontsource-variable/<name>` when a variable build
  exists, else `@fontsource/<name>` with only the needed weights. Check with
  `npm view <package> version` before proposing it. Record the exact `font-family` the package
  registers (variable packages add " Variable").
- No face the site's `DESIGN.md` bans.

## How to present each direction

```markdown
## Direction <n>: <Name>

Palette: <name> #hex · <name> #hex · <name> #hex on <name> #hex
Fonts: <heading> + <body>
Approach: 2-3 sentences: layout, hero, spacing, shape, type treatment, color mood, feeling.
Why it fits: 1-2 sentences tied to this brief.
```

Names: 2-4 evocative words tied to the metaphor ("Shop Floor Ledger", "Night Shift Blue").
Never "Direction A", "Minimal", "Dark Theme", "Option 1".

## Worked example (fictional, for format only)

Brief: a mobile diesel repair service for fleet owners; customer = small trucking companies
losing money on every hour a truck sits; CTA = call dispatch; differentiator = the mechanic comes
to the yard.

```markdown
## Direction 1: Shop Floor Ledger
Palette: Diesel Black #1D1F21 · Safety Orange #C4520F · Steel #5B6670 on Paper #F4F2EE
Fonts: IBM Plex Sans Condensed + IBM Plex Sans
Approach: dense, spec-sheet layout; the hero is type-only with the dispatch number as the
largest element; square corners, hairline rules, numbers set tabular like a work order.
Why it fits: fleet owners read invoices and spec sheets all day; this looks like a tool, not an ad.

## Direction 2: Roadside at Dawn
Palette: Night Blue #14263D · Amber #B7791F · Fog #D9DEE3 on White #FFFFFF
Fonts: Barlow Semi Condensed + Source Sans 3
Approach: full-bleed photo hero of the service truck in a yard, split sections alternating photo
and copy, rounded cards, calm spacing, one strong amber CTA per screen.
Why it fits: shows the difference (we come to you) before a word is read.

## Direction 3: Dispatch Board
Palette: Graphite #2B2B2B · Signal Green #2E7D32 · Chalk #EDEDE8 on Chalk
Fonts: Archivo + Archivo Narrow
Approach: modular board of blocks (service area map, response promise, services, call box),
pill buttons, no hero photo; a live-looking "trucks on the road" strip only if real data exists.
Why it fits: puts availability and area first, which is what a stranded fleet manager scans for.
```

(Hex values and pairings above are illustrations of the format, not a recommendation; verify
contrast and packages before using any of them.)

## Pitfalls

- Too alike: all minimal; the same hero three times; color as the only difference.
- Too generic: "bold and modern", "clean and professional", "minimalist" with no specifics.
- Not grounded: a dark moody direction for a children's brand; corporate blue for a spa.
- Palette/font errors: near-identical palettes; a package that does not exist; a family name
  that does not match the package; anchors ignored; contrast not checked.

## `directions.json`

Written after approval.

```json
{
  "total": 3,
  "directions": [
    {
      "id": 1,
      "slug": "shop-floor-ledger",
      "name": "Shop Floor Ledger",
      "description": "One paragraph used on the navigator and in the subagent brief.",
      "rationale": "One or two sentences tied to the brief.",
      "palette": {
        "primary": "#1D1F21", "secondary": "#5B6670", "accent": "#C4520F",
        "accent-ink": "#A34309", "bg": "#F4F2EE", "surface": "#FFFFFF",
        "text": "#1D1F21", "muted": "#4F5962", "hairline": "#DDD8CF"
      },
      "contrast": { "text/bg": "14.8", "muted/bg": "6.4", "accent-ink/bg": "5.6", "white/accent": "4.6" },
      "fonts": {
        "heading": { "package": "@fontsource/ibm-plex-sans-condensed", "weights": [600],
                     "cssFamily": "IBM Plex Sans Condensed", "fallback": "system-ui, sans-serif" },
        "body":    { "package": "@fontsource/ibm-plex-sans", "weights": [400, 600],
                     "cssFamily": "IBM Plex Sans", "fallback": "system-ui, sans-serif" }
      },
      "axes": { "density": "packed", "type": "one dominant size", "hero": "type-only",
                "metaphor": "workshop", "shape": "square", "depth": "flat", "proof": "numbers first" }
    }
  ]
}
```

`contrast` values are computed, never estimated (compute them when writing the file).
File naming: Astro `src/pages/concepts/direction-<id>-<slug>.astro` with components in
`src/components/concepts/direction-<id>/`; Next.js `app/concepts/direction-<id>-<slug>/page.tsx`
with `components/concepts/direction-<id>/`.

File: seo-site-build/references/directions.md · Version 1.0 · November 2026
