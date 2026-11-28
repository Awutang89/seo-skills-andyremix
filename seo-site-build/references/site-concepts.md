# Site concepts: kickoff for a new site or redesign (interview → directions → scaffold → prototypes → lock)

Use this before the SEO rules in `SKILL.md` when the user wants a new website, a redesign, or
"to vibe code my site": it produces a brief, a site blueprint, N homepage design directions
built as real pages, and after the pick a locked design system. The SEO rules then apply to
every page built from it.

End state: a running project with N homepage prototypes the user can open side by side
(Astro: `localhost:4321/concepts/direction-1-<slug>`; fresh folder: see Phase 3), and after
feedback, one final homepage plus a `DESIGN.md`.

Load files just in time:

| Phase | Read |
|---|---|
| 1. Interview | `interview.md` |
| 1. Directions | `directions.md` |
| 2. Scaffold | `astro.md` (Next.js/Shopify notes inside) |
| 3. Prototypes | `prototype-brief.md` |
| 5. Lock + build pages | `SKILL.md`, `build-verify.md` |

---

## Hard rules

- **Every question goes through `AskUserQuestion`**, never plain text: interview topics, the
  direction count, approvals, resume offers.
- **One topic per turn**: each turn covers one interview topic with at most 2-3 related
  questions. Never dump the whole questionnaire.
- **Script paths:** this skill's scripts live in `seo-site-build/scripts/`. When the skill
  is loaded, Claude Code prints "Base directory for this skill: …". Set that as the skill root
  before running a bundled script (`$SKILL_DIR` in Git Bash, `$env:SKILL_DIR` in PowerShell) and
  call `python "$SKILL_DIR/scripts/<name>.py"`. Do not guess the root from the repo layout;
  deployed copies (for example on a server) sit elsewhere.
- **Real proof only.** No invented testimonials, client names, stats, logos or verdicts. Where
  proof is missing, the prototype shows a visibly labelled placeholder ("Illustrative: your
  review goes here") or omits the section.
- **Never overwrite a live home page.** In an existing repo, prototypes live under a noindexed
  `/concepts/` route that is excluded from the sitemap and deleted after the pick.
- Optional design layer: if `impeccable`, `taste-skill` or `ui-ux-pro-max` is installed, load
  one at Phase 1 and Phase 2 for taste; if none is, continue with `prototype-brief.md` alone.
  Never stop because a design skill is missing. A site's own `DESIGN.md` bans always win over
  any design skill's defaults.

## Prerequisites

- Node at or above the scaffolded framework's `engines.node` (Astro 7: 22.12+).
- Python 3 (stdlib only; the bundled scripts need no pip installs).
- The current top model for prototype subagents (design quality); do not hard-code a model name.

## State and resume

Working files live in the target project under `.site-concepts/` (add `.site-concepts/` to that
project's `.gitignore` the same day; the brief also gets copied to `./brand/site-brief.md` so
other skills read it).

`.site-concepts/state.json` always holds the full object:

```json
{ "phase": "interview_complete", "direction_count": 3, "is_redesign": true,
  "source_url": "https://example.com", "platform": "astro", "concepts_route": "/concepts" }
```

| `phase` | Written when | Resume offer | Validate first |
|---|---|---|---|
| `interview_complete` | brief + directions approved and written | review the plan, then scaffold | `brief.md`, `directions.json` exist |
| `scaffold_complete` | project installed, first commit made | build the prototypes | platform sentinel exists: Astro `src/layouts/*.astro`, Next `app/layout.tsx`, Shopify `layout/theme.liquid` |
| `prototypes_complete` | all direction pages built and verified | show the completion message | each direction page exists |
| `locked` | final homepage + `DESIGN.md` done | build the remaining pages | `DESIGN.md` exists |

If the state file names files that no longer exist, treat it as absent and start over (tell the
user). To start fresh deliberately, delete `.site-concepts/`.

---

## Phase 1: interview and directions (approval gate)

1. Check state; offer to resume if valid.
2. Run the interview (`interview.md`). Redesign → brand extraction with
   `python "$SKILL_DIR/scripts/extract_brand.py" <url> -o .site-concepts/brand-extraction`.
3. Ask how many directions: recommend 3 (range without overload), allow 4 or 5, default 3.
4. Brainstorm exactly N directions (`directions.md`) and present them.
5. **Approval gate.** Show the plan (below) and wait for an explicit yes. In plan mode the plan
   lives in the plan text only; the files are written **after** approval, because plan mode
   allows no file writes. Change requests → revise the directions and show the plan again.
6. After approval, write `.site-concepts/brief.md`, `.site-concepts/directions.json`,
   `.site-concepts/plan.md`, and `state.json` (`interview_complete`).

Plan layout:

```markdown
# Site plan: <business>
## Brand brief         one paragraph: business, customer, CTA, differentiator, positioning
## Visual direction    constraints (anchor colors, avoid, must-use fonts, or "none") + 3-5 vibe words
## Site blueprint      launch pages with purpose, sections, content status; v2 pages
## Concept directions  N directions: name, palette summary, fonts, approach, why it fits
## What gets built     stack (per astro.md), N prototypes at <route>, git repo + first commit
## How to view         dev command + one URL per direction
```

## Phase 2: scaffold

- **Fresh empty folder:** follow `astro.md` §2 (guard, CLI scaffold, CLI installs), then
  install the union of all directions' font packages once (dedupe), set up `global.css` tokens
  named after the `directions.json` palette keys (`--color-primary` … `--color-hairline`,
  `--font-heading`, `--font-body`, so the prototype override block matches) with Direction 1's
  values as defaults, and a base layout that already meets `astro.md` §5.
  Do not add radius/shadow/spacing systems or component classes yet; each direction decides
  those, and the real system is built after the pick.
- **Existing site:** no scaffold. Add a `src/pages/concepts/` route (Next: `app/concepts/`),
  every page `noindex`, excluded from the sitemap filter.
- **Shopify:** one unpublished duplicate theme per direction, or a static prototype folder
  outside the theme when the direction changes layout radically. Never edit the live theme.
- **Redesign images:** `python "$SKILL_DIR/scripts/download_site_images.py" <url> --project-dir . --manifest .site-concepts/site-images.json --max 15`.
  Files land in `public/images/redesign/` (Astro and Next.js). Tell the user how many were
  saved. Only use the client's own images; stock or third-party images found on their site need
  a license check before they ship. For Shopify, upload chosen images to Files instead.
- Git: `git init`, first commit, private remote. Then write
  `scaffold_complete`.
- Verify the dev server starts (`astro.md` §7), then stop it before Phase 3.

## Phase 3: prototypes (parallel subagents)

1. Fill one brief per direction from `prototype-brief.md`: number, name, slug, description,
   business name, and the token override values copied from `directions.json` (the subagent
   never chooses hex values or fonts itself).
2. Spawn all N subagents **in one message** (parallel), current top model. They write code only:
   no browser, screenshots or dev server (parallel sessions collide), and only inside their own
   namespace.
3. When they finish, check files without a browser: the page file exists, its components folder
   exists, every import resolves. Re-spawn only a failed direction.
4. Run the build and `verify_build.py` (each prototype: one H1, `noindex`, parses). Fix or
   re-spawn failures. This script is not included in this repository.
5. Navigator: in a fresh project, `src/pages/index.astro` becomes a plain list of the directions
   (label, name, one-line description, link) until the pick. In an existing project the list is
   `/concepts/index` (noindex). One navigator only; no separate static HTML hub.
6. Write `prototypes_complete`.

## Phase 4: review with the user

Tell the user, in plain words:

- Run the dev command, open the navigator, and scroll each direction top to bottom before
  judging.
- Notice reactions, not analysis: which one makes them lean in, which looks like their business,
  which they would be proud to send a customer.
- Note the parts they like from each ("hero from 1, type from 2, colors from 3").
- Come back with those notes; the final homepage and design system are built from them.

## Phase 5: lock

1. Build the final homepage from the mix-and-match feedback.
2. Write the locked system as `DESIGN.md` in this format: token table with hex, utility, use
   and contrast ratio; type (faces, weights, scale, tracking); radii and spacing; components;
   bans.
3. Clean up: remove font packages and imports no direction uses anymore (`npm uninstall`), drop
   unused tokens, delete the direction pages, their components and the `/concepts` route, and
   restore the real home page.
4. Hand over to `SKILL.md`: page-type table (§1, fed by the blueprint), URLs (§5), templates,
   then the launch checklist (§10). Redesign → the §9 redirect map is mandatory.
5. Write `locked`.

## Troubleshooting

| Problem | Fix |
|---|---|
| Dev server will not start | `node --version` against `engines.node`; reinstall with the detected package manager |
| Fonts fall back to system fonts | family name in the token does not match the package's `@font-face` (`"Inter Variable"` vs `"Inter"`), or the package is not installed |
| A script errors on fetch | the site blocks non-browser clients; retry once, else ask the user for screenshots and hex codes |
| One direction is broken | re-spawn that direction only |
| Start over | delete `.site-concepts/` (and the concept pages) and rerun |

## Tips to give the user

- Be specific: "everyone" is not a customer and "modern and clean" is not a direction.
- Bring 2-3 sites they like, from any industry.
- Three directions is usually enough.

## Files

| File | Purpose |
|---|---|
| `references/site-concepts.md` | this workflow |
| `references/interview.md` | interview topics, quality bars, brief template |
| `references/directions.md` | contrast axes, palette/font rules, directions.json |
| `references/prototype-brief.md` | subagent prompt template and done checklist |
| `scripts/extract_brand.py` | colors, fonts, CSS variables and logo from a live site |
| `scripts/download_site_images.py` | content images from a live page into `public/images/redesign/` |
| `scripts/scaffold_guard.py` | empty-folder check and temp-scaffold move-up |

File: seo-site-build/references/site-concepts.md · Version 1.0 · November 2026
