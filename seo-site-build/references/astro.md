# Astro build conventions (new project or rebuild)

Read this when the stack is Astro: scaffolding a new project, adding a page type, or wiring SEO
into a layout. For editing content on an Astro site that already exists, read
`astro-edit-safety.md` instead. For a multilingual setup, read `hreflang-i18n.md`.

**The canonical template is a reference Astro site, not a course scaffold.**
A reference Astro site is the model when it
already implements every rule in `SKILL.md`. When in doubt, copy
its patterns (read them, do not edit that project from this skill):

| File in a reference Astro site | What it shows |
|---|---|
| `astro.config.mjs` | hard-coded `site`, `trailingSlash: 'never'` + `build.format: 'file'`, `compressHTML: false`, i18n, sitemap filter, build hooks |
| `src/layouts/Base.astro` | canonical, hreflang, OG/Twitter, noindex prop, title-suffix strip with CJK width, one `@graph` with a `jsonLd` prop, `<` escaping, font preloads |
| `src/content.config.ts` | Astro 5+ content layer with `glob()` loader, Zod from `zod`, `draft`, `lang`, `translationOf`, `faq` |
| `src/lib/blog-seo.ts` | BlogPosting + BreadcrumbList + FAQPage nodes built from frontmatter |
| `src/pages/robots.txt.ts` | robots route with the sitemap line and no Disallow on noindexed pages |
| `DESIGN.md` | the locked design-system format (tokens with contrast ratios, type, components, bans) |

---

## 1. Baseline stack

- `astro` (current major; check `node_modules/astro/package.json` `engines.node` for the Node
  floor: Astro 7 needs Node >= 22.12, so "Node 18+" in older guides is stale).
- `tailwindcss` v4 + `@tailwindcss/vite` (Vite plugin). Never `@astrojs/tailwind`, which is the
  v3 integration.
- `@astrojs/sitemap` for any indexable site.
- Fonts self-hosted via `@fontsource/*` (static weights, only the weights in use) or
  `@fontsource-variable/*` when the face has a variable build. No Google Fonts `<link>`.
- `zod` imported directly (or `astro/zod`) for content schemas.
- `@astrojs/react` (+ `react`, `react-dom`) **only** when an island actually needs React.
- `@astrojs/mdx` only when content needs components (see `astro-edit-safety.md` §MDX).
- **No adapter** for a pure static site on Cloudflare Pages. Add `@astrojs/cloudflare` only for
  the Workers option (§6) or server routes.

## 2. Scaffold (new, empty folder only)

Hard rule: generate bootstrap files with the CLI. Never hand-write `package.json`,
`astro.config.*`, `tsconfig.json` or `src/env.d.ts` from nothing. If the CLI fails, stop and
report the error; do not fall back to hand-written files.

1. **Empty-folder guard.** Run `python scripts/scaffold_guard.py check` from the target folder.
   It allows only `.claude`, `.git`, `.site-concepts` and the temp scaffold folder, and exits
   non-zero listing up to 12 conflicting entries. Never scaffold over an existing site. For a
   rebuild inside an existing repo, scaffold in a sibling folder (for example `site/`) instead.
2. **Scaffold into a temp folder, non-interactively**, pinning the major so reruns reproduce:
   `npx create-astro@<major> .astro-scaffold --template minimal --no-install --no-git --yes --skip-houston`
   (`--no-git` because git is set up separately: `git init`, then
   `gh repo create <name> --private --source . --push`.)
3. **Move up:** `python scripts/scaffold_guard.py move-up` moves the files into the folder only if
   no destination already exists, then deletes the temp folder.
4. **Install with the CLI** (so versions resolve), never by editing `package.json`:
   `npm install tailwindcss @tailwindcss/vite @astrojs/sitemap` (+ fonts, + `zod`).
   The only hand edit to `package.json` is `name` = the business name in kebab-case.
5. Commit the lockfile. Do not commit `node_modules`, `dist`, `.astro`.

Next.js equivalent: `npx create-next-app@<major>` with the same guard and install rules.
Shopify equivalent: duplicate the live theme (`shopify theme duplicate` or admin → Duplicate) and
work on the unpublished copy; never scaffold a theme from scratch for an existing store.

## 3. `astro.config.mjs` baseline

Start from the reference site's config. The settings that matter for SEO:

- `site: 'https://{canonical-host}'`, **hard-coded**. Never read it from an env var (a stale
  site-URL env var poisoned every canonical; `SKILL.md` §6).
- `output: 'static'` for marketing, service and content sites.
- **`trailingSlash` + `build.format` must agree with the host.**
  - `trailingSlash` accepts `'always'`, `'never'`, or `'ignore'` (the default, which leaves the
    choice to whoever writes links, so avoid it).
  - Cloudflare Pages 308-redirects a directory path (`/blog/x` served from `blog/x/index.html`)
    to `/blog/x/`. With `trailingSlash: 'never'`, also set `build: { format: 'file' }`
    so Astro emits `blog/x.html`; otherwise every canonical points at a URL that redirects.
  - The reverse pairing (`'always'` + default `format: 'directory'`) is also consistent.
  - Every internal link, canonical, hreflang and sitemap URL uses the same form. A link in the
    wrong form costs a redirect hop on every click and crawl.
- `compressHTML: false` if any inline link starts on a new source line: compression dropped the
  space before it ("and<a>"). The gzip cost is negligible.
- `integrations: [sitemap({ filter })]` where the filter drops every noindexed and utility page
  (`/thanks`, `/404`, each locale's copy). Linked set == sitemap set (`SKILL.md` §6).
- `vite: { plugins: [tailwindcss()] }`, plus
  `build.assetsInlineLimit` returning `false` for `.woff`/`.woff2` so fonts are never inlined
  as base64 into render-blocking CSS.
- i18n block when there is more than one language (`hreflang-i18n.md`).
- Build hooks (`astro:build:done`) for post-processing the built HTML, e.g. per-locale 404
  relocation or a sitewide external-link `rel` policy. Post-processing the output covers
  Markdown and `.astro` links alike.

## 4. Styles, tokens and fonts

- One `src/styles/global.css`: `@import "tailwindcss";` then an `@theme { … }` block of tokens,
  then `@layer base { … }` element defaults (body background/text/font, h1-h4 display font,
  `text-wrap: balance` on headings). Splitting into `theme.css` + `base.css` is fine; keep the
  import order **font imports → tailwindcss → theme → base** (a CSS `@import` after other rules
  is ignored).
- Tokens become utilities: `--color-accent` → `bg-accent`, `text-accent`, `border-accent`,
  `ring-accent`; `--font-display` → `font-display`; `--radius-card` → `rounded-card`. Markup uses
  token utilities; no raw hex in markup.
- **`@theme` vs `@theme static`:** plain `@theme` only emits variables for utilities that are
  used; `@theme static` always emits every variable on `:root`. While several prototypes
  override tokens at runtime (see `site-concepts.md`), use `@theme` with the override on
  `:root`; once one direction is locked, prune and use whatever the locked system needs.
- **Fonts:** import the fontsource CSS either at the top of `global.css` or in the base layout
  frontmatter. Import only the weights in use. Preload only the one or two
  above-the-fold woff2 files (`?url` import + `<link rel="preload" as="font" crossorigin>`).
  Large CJK faces load async (`media="print" onload`), see `hreflang-i18n.md`.
- **Family names must match the @font-face.** `@fontsource-variable/inter` registers the family
  `"Inter Variable"`, not `"Inter"`; `@fontsource/inter` registers `"Inter"`. A token that names
  the wrong family silently falls back to the system font. Check the package's CSS for the
  `font-family:` it declares before writing the token.
- Verify a font package exists on npm before planning around it (`npm view @fontsource-variable/<name> version`).
  Some families have no variable build; use the static `@fontsource/<name>` package then.
- **Tailwind v4 `<style>` gotcha:** a component `<style>` block that uses `@apply` with theme
  tokens needs `@reference "<relative path>/styles/global.css";` at its top. Prefer utilities
  in markup and avoid the problem.
- Contrast floor for every text token: WCAG AA (4.5:1 body, 3:1 large text). Record the ratio
  next to each token in `DESIGN.md`. Every `prefers-reduced-motion: reduce` user gets
  motion removed or reduced.

## 5. Base layout requirements

A minimal `Layout.astro` with only title/description/favicon is not enough. The base layout
must provide:

- Props: `title`, `description` (required, never defaulted to an empty string: an empty meta
  description is worse than none), `canonicalPath`, `noindex`, `jsonLd` (extra nodes), and
  `altPath` on multilingual sites.
- `<title>`: brand only on the homepage. Strip a trailing `| Brand` elsewhere. Count CJK
  characters as width 2 against the 60 budget (`SKILL.md` §3; our rule supersedes the common
  "keep the frontmatter title ≤45 to leave room for a 15-character suffix" advice, because we
  do not use a suffix).
- Self-referencing absolute canonical in the `trailingSlash` form.
- hreflang alternates + `x-default` (multilingual only).
- `<meta name="robots" content="noindex">` when `noindex`.
- OG + Twitter tags with a 1200×630 default image; `og:type` article on posts.
- `<link rel="icon" href="/favicon.svg" type="image/svg+xml">` pointing at a file that exists
  (the minimal template ships `favicon.svg`, not `favicon.ico`).
- One JSON-LD `<script type="application/ld+json" is:inline set:html={…}>` with the sitewide
  `@graph` (Organization, WebSite) + page nodes, serialized with every `<` replaced by `\u003c`.
- Exactly one H1 per page, rendered by the page (or by the layout from `title`, never both).

## 6. Deploy targets

**Default: Cloudflare Pages, static, no adapter.** Project root = the site folder (for example
`site`), build command = the detected package manager's build (`npm run build`), output = `dist`.
A `public/_routes.json` with `"include": ["/api/*"]` keeps Pages Functions off static paths.
Custom domain + the other host redirecting to the canonical one.

**Option: Cloudflare Workers with static assets** (only when the project needs Workers features):
- `npm install @astrojs/cloudflare` and `npm install -D wrangler`.
- Adapter in the config; image service set explicitly (for example `imageService: 'compile'`)
  so it does not default to the binding-based service. **Verify the option names against the
  current `@astrojs/cloudflare` docs**; they change between majors.
- A `wrangler.jsonc` with `name`, a `compatibility_date` set to the day it is created (not a
  copied date), `compatibility_flags: ["nodejs_compat"]`, and `assets` pointing at the built
  client folder with an `ASSETS` binding. Any additional flag (for example one that claims to be
  required for `/_image`) needs a current Cloudflare doc citation before adding it.
- `public/.assetsignore` listing `_worker.js` and `_routes.json` so they are not served as
  assets.
- Read the current Cloudflare `wrangler` documentation for the syntax before running it.

## 7. Verify the scaffold

1. Detect the package manager (`python scripts/detect_stack.py`) and run its dev command. The
   dev server should answer on `localhost:4321`.
2. Typical failures: the v3 `@astrojs/tailwind` integration instead of the Vite plugin; React
   peer versions not matching `@astrojs/react`; a fontsource package name typo; an adapter
   missing for a config that references one; Node below the `engines` floor.
3. Stop the dev server before spawning prototype subagents (they must not share it).
4. Run the build and `python scripts/verify_build.py dist` (see `build-verify.md`) before
   calling the scaffold done. This script is not included in this repository.

## 8. Next.js and Shopify parallels

| Concern | Astro | Next.js | Shopify |
|---|---|---|---|
| Canonical host | `site` in config | `metadataBase` in root layout | Primary domain in admin |
| Title template | layout prop | `metadata.title.template: "%s"` | `theme.liquid` title logic |
| Trailing slash | `trailingSlash` + `build.format` | `trailingSlash` in `next.config` | fixed by Shopify (no slash) |
| Sitemap | `@astrojs/sitemap` + filter | `app/sitemap.ts` | automatic `/sitemap.xml` |
| JSON-LD | layout `@graph` prop | one `JsonLd` component per route | theme snippet + `jsonld.*` metafields |
| Fonts | fontsource, self-hosted | `next/font` (self-hosts) | theme font picker or `assets/` |
| Static build dir to verify | `dist/` | `.next/server/app/` or `out/` | none: verify the live preview URL |

File: seo-site-build/references/astro.md · Version 1.0 · November 2026
