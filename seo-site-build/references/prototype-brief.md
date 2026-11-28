# Prototype subagent brief

One subagent per direction, all spawned in a single message. Fill every `<…>` before spawning;
the subagent must not choose colors or fonts itself. Paths below are Astro; for Next.js use
`app/concepts/direction-<n>-<slug>/page.tsx` and `components/concepts/direction-<n>/`.

---

## Template

```text
Build homepage prototype <n> of <N> for <business>: direction "<name>".

Read, in this order:
1. If a design skill is installed (impeccable, taste-skill, ui-ux-pro-max), load it. If not,
   continue with the standards below.
2. .site-concepts/brief.md (the whole brief).
3. .site-concepts/directions.json, direction <n> only.
4. .site-concepts/state.json. If is_redesign is true, read .site-concepts/site-images.json and
   prefer those real images (use each entry's public_path) over placeholders.
5. DESIGN.md at the project root, if it exists: its bans override everything below.

Direction description: <description from directions.json>

## Limits
- Code only. Do not open a browser, take screenshots, use browser/devtools tools or start the
  dev server; other subagents are running in parallel.
- Write ONLY: src/pages/concepts/direction-<n>-<slug>.astro and src/components/concepts/direction-<n>/.
  Do not touch other directions, the shared layout, global.css or theme files.

## Page shell
Use the shared layout and mark the page noindex:
  import Base from '<relative path>/layouts/<Base>.astro';
  <Base title="<name> | concept for <business>" description="<one line>" canonicalPath="/concepts/direction-<n>-<slug>" noindex>
First child inside the layout, the token override (values pre-filled):
  <style is:global>
    :root {
      --color-primary: <primary>; --color-secondary: <secondary>; --color-accent: <accent>;
      --color-accent-ink: <accent-ink>; --color-bg: <bg>; --color-surface: <surface>;
      --color-text: <text>; --color-muted: <muted>; --color-hairline: <hairline>;
      --font-heading: "<heading cssFamily>", <fallback>;
      --font-body: "<body cssFamily>", <fallback>;
    }
  </style>
Style with the token utilities (bg-primary, text-muted, font-heading...), opacity steps
(bg-primary/10), gradients built from tokens, and arbitrary values for size, tracking and
leading (text-[88px], tracking-[-0.03em]). No raw hex in markup. A component <style> that uses
@apply with tokens needs @reference to the global stylesheet; prefer utilities.

## Quality bar
Design it as a senior designer at a top studio would for a paying client: finished, specific to
this business, not a template with colors swapped. Match the tone of the brand; match the craft
of an expensive custom build.

1. Signature motif: one custom element drawn from the brand (a shape, a line treatment, a
   typographic device) that recurs in at least five places: nav, section transitions, cards,
   backgrounds, CTAs, footer. Not an icon-library glyph.
2. Authored motion: a staggered hero entrance; scroll reveals that vary by element type;
   number reveals only for real numbers; hover curves that suit the brand (a small overshoot for
   playful brands, a smooth ease-out for serious ones); a nav that reacts to scroll; at most one
   element with gentle ambient motion. EVERYTHING respects prefers-reduced-motion: reduce
   (no movement, content visible immediately). No animation may hide content from users
   without JavaScript.
3. Layout tension: uneven column splits, staggered card heights, at least one element crossing a
   section boundary, at least one non-straight section edge or a full-bleed moment. Reserve
   space for every image (width/height) so nothing shifts on load.
4. Type as a tool: a deliberate weight strategy, an accent treatment on key words in headings,
   negative tracking on display sizes, fluid sizes with clamp(). Small tracked labels above
   headings only if the brand allows them.
5. Craft details that fit the brand: a drawn underline or mark, a considered image mask,
   connecting lines, a very low-opacity texture, per-item variation, a designed mobile menu
   (a no-JS <details> menu is fine), a footer sign-off with the motif.
6. Rhythm: backgrounds alternate on purpose; at least one contrasting band (dark or brand-color,
   or a tint band if the brand bans dark sections); transitions between sections, not hard cuts.

Tone guide (blend; one deliberate exception is good):
| Personality | Motion | Decoration | Layout |
| playful / warm | springy, floaty | drawn shapes, organic forms | broken grid, tilted cards |
| refined / premium | slow eases, subtle depth | fine lines, geometry | generous space, editorial asymmetry |
| bold / modern | fast, scale-based | hard geometry, high contrast | dense grid, layered full-bleed |
| professional / trust | measured fades | clean rules, structure | ordered grid, restrained breaks |

## Content
- Voice and language from the brief; no lorem ipsum.
- Proof only from the brief's content inventory. Missing testimonials, logos, stats or case
  studies are either left out or shown as a visibly labelled placeholder ("Illustrative: add a
  real customer quote here"). Never invent names, quotes, numbers or clients.
- Sections (order and grouping are the subagent's call; include a section only if the inventory supports
  it or it is a labelled placeholder the user agreed to): nav with character; hero; services or
  offer; work or proof; three concrete reasons to choose them; social proof; closing CTA;
  footer with navigation, contact, social links and a tagline.

## Done means
- [ ] Exactly one H1; headings in order; buttons are not inside headings
- [ ] Motif appears in 5+ places
- [ ] 3+ distinct motion types, all disabled under prefers-reduced-motion
- [ ] 1+ grid break (overlap, asymmetry or bleed)
- [ ] 1+ contrasting band within the brand's rules
- [ ] 3+ distinct type size/weight combinations
- [ ] Text contrast AA on every background used; visible focus states on every control
- [ ] Works at 375 px wide: layout and motion adapt, not just stack
- [ ] No fabricated proof; placeholders are labelled
- [ ] Feels finished, and nobody would call it generic AI output
```

---

## Spawning

- All N in one message, parallel. Current top model.
- List the mapping in the orchestrator message, e.g.
  `1 "Tuning Ledger" → src/pages/concepts/direction-1-tuning-ledger.astro`.
- Afterwards: file-level checks (page, components folder, imports resolve), then build +
  `verify_build.py`; re-spawn only failures. No browser review inside subagents; the user or the
  main thread reviews visually. This script is not included in this repository.

File: seo-site-build/references/prototype-brief.md · Version 1.0 · November 2026
