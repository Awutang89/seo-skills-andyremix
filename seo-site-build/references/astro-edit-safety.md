# Editing an existing Astro site safely (plus Next.js and Shopify analogues)

Read this before changing content, frontmatter, headings, links or schema on a site that already
builds. It applies to any skill that edits site files: `seo-content` refresh work,
`seo-page-diagnosis` fixes, `internal-linking` passes, `seo-schema` / `faq-jsonld` changes. The
build and rendered checks that close every edit are in `build-verify.md`.

Rule zero: **if the agent cannot identify how a page is built, do not touch its frontmatter or schema.**
Report what could not be identified and stop at a proposal.

---

## Stage 0: know the project (once per session)

Run `python scripts/detect_stack.py [project-path]` first. It prints (and with `--json` writes)
everything below; confirm by reading the files it names.

1. **Find the project root.** Look for `astro.config.mjs|ts|mts` in the working folder, then one
   level down (for example `site/`). None found → this is not an Astro project; ask for
   the right folder instead of guessing.
2. **Site URL.** Read `site` from the config. Missing or `localhost` → ask the user for the live
   URL. Never take it from an env var.
3. **Package manager** from the lockfile at the project root, and use it for every command:

   | Lockfile | Manager | Build |
   |---|---|---|
   | `pnpm-lock.yaml` | pnpm | `pnpm run build` |
   | `yarn.lock` | yarn | `yarn build` |
   | `package-lock.json` | npm | `npm run build` |
   | `bun.lock` / `bun.lockb` | bun | `bun run build` |

   Two lockfiles → report it and use the one that matches `packageManager` in `package.json`.
4. **Content config location.** Astro 5 and later: `src/content.config.ts` (at `src/`, with
   `loader: glob(...)`). Astro 4 and earlier: `src/content/config.ts` (collections declared with
   `type: 'content'`, which later majors removed). Check both. Neither → no schema validation,
   so the layout alone decides which fields matter.
5. **Architecture of the target page.** Read its route file and layout and note: where `<title>`
   comes from and whether a suffix is appended; where the meta description comes from; any SEO
   package (`astro-seo`, `astro-seo-schema`); where the H1 comes from; whether FAQ or other
   schema is built from frontmatter; whether the body is Markdown or the page is driven by
   frontmatter or imported data files.
6. **External CMS.** Integrations in `package.json` such as `@astrojs/storyblok`,
   `@astrojs/contentful`, `astro-sanity`, a WordPress integration (`astro-wordpress`,
   `wp-astrojs-integration` or similar), or routes that fetch entries at build time
   (`getLiveEntry`, `fetch(` to a CMS API) mean the copy lives in the CMS. Analyse and propose;
   the edits happen in the CMS, not in local files. (Shopify analogue: store content lives in
   the admin and changes go through the Admin API or the admin UI.)
7. **Target market.** Location words in titles, the config `i18n` block and the TLD (`.co.uk`,
   `.com.au`) suggest the country. Map it to a DataForSEO `location_code` + `language_code` and
   reuse them for every call in the session. Ambiguous → ask. Default to the US only when
   nothing points elsewhere. On a bilingual site decide per locale (each locale → the market its
   audience actually searches from, confirmed with the user).
8. **Keyword-data preflight** (only if the task needs keyword data): one cheap DataForSEO call
   through an existing DataForSEO client (an optional integration,
   credentials from `.env` as in `.env.example`, never printed). If it
   fails: 401 → wrong or missing credentials file (do not print its contents); timeout or
   refused → network or service issue, retry once; do not continue with guessed volumes.
   GSC data is optional: use it if a GSC tool is connected, never ask the user to set it up here.
9. **Draft and paused pages.** Flag any target whose frontmatter has `draft: true`,
   `status: draft|paused`, `published: false` or `active: false`. Those pages do not ship (or
   are filtered out of `getStaticPaths`), so edits there change nothing live. Work on live pages
   first and say so.

Stage 0 ends with: config path, site URL, package manager, content-config path (or none),
target-page architecture, CMS flag, market codes, draft flags.

---

## Edit preflight (report before the first edit)

Write this block into the working notes and show it to the user before editing:

- Content schema read: `<path>` or "none found".
- Route and layout read: `<paths>`.
- H1 source: layout, Markdown, or data file.
- Every frontmatter field the edit touches, with "defined in schema: yes/no".
- Schema emission path, if FAQ or JSON-LD changes: layout `@graph` prop, component,
  frontmatter-driven helper, `astro-seo-schema`, or none.

Anything unknown → no frontmatter or schema edit.

**Next.js analogue:** the route's `metadata` / `generateMetadata`, the `JsonLd` component and
its data source, and the MDX or data file holding the copy. **Shopify analogue:** the theme
section/snippet that renders the field, the metafield namespace/key, and whether the value is
admin content (API) or theme code (theme working copy).

---

## Frontmatter and the Zod schema

How Zod treats a key the schema does not declare (this is where many guides are wrong):

| Schema written as | Unknown key in frontmatter |
|---|---|
| `z.object({...})` (default) | **Silently stripped.** The build passes, the value never reaches the page. |
| `.strict()` / `z.strictObject({...})` (Zod 4 form) | Build error. |
| `.passthrough()` (Zod 3) / `.loose()` or `z.looseObject({...})` (Zod 4; `.passthrough()` is deprecated there) | Kept and available to the layout. |

So the danger with a default schema is a silent no-op, not a crash. Decision:

- Field defined in the schema → safe to set or change (respect its type: `z.coerce.date()`,
  enums, `.max()` limits).
- Not defined, schema loose/passthrough → allowed only if the layout actually reads it.
- Not defined, default or strict → do not add it. Tell the user: "the `<collection>` schema in
  `<config path>` has no `<field>` field; add it there first if you want it."

Field names differ per site. Discover them; never assume:

| Purpose | Names seen in the wild |
|---|---|
| Title | `title` |
| Meta description | `description`, `excerpt`, `summary` |
| Social image | `image`, `ogImage`, `heroImage`, `thumbnail`, `cover` |
| Published | `date`, `pubDate`, `publishDate`, `datePublished`, `created` |
| Updated | `updated`, `updatedDate`, `lastmod`, `lastUpdated`, `dateModified`, `modifiedDate` |
| Draft | `draft`, `status`, `published` |
| URL override | `slug` |
| Taxonomy | `tags`, `categories`, `category` |

The layout's `Props` interface is the ground truth for which fields feed SEO tags: if it takes
`ogImage`, that is the field. **Dates:** keep the format the file already uses (date-only, full
ISO, or quoted string). The JSON-LD layer converts to full ISO 8601 with time zone
(`toISOString()`), which the Rich Results Test prefers.

---

## Headings, sections, links

- **H1 source.** If the layout renders `<h1>{title}</h1>` (or a hero component does), the Markdown
  body starts at `##` and must not contain `#`. If the layout only renders `<Content />`, the
  Markdown owns the `#`. Quick check: open a sibling file in the same collection. Layout H1 +
  Markdown `#` = two H1s; check the layout first, every time.
- **Heading renames break `#anchor` links.** Search the site for `#<old-slug>` before renaming
  and warn the user.
- **Insert new sections in plain Markdown only**: between existing sections, never inside a code
  fence or inside an MDX component (between `<X>` and `</X>`, or in a self-closing `<X ... />`).
  If the planned spot is inside one, move to the nearest plain region before or after it. Match
  the surrounding voice and formatting.
- **URL resolution.** `src/content/blog/x.md` usually serves `/blog/x`, but read the route:
  `[slug].astro` vs `[...slug].astro`, and whether `getStaticPaths` uses `entry.id` (the file
  path without extension, which can include a locale folder such as `en/x` that a site can strip),
  a `slug` field, or something else.
- **Internal links:** root-relative (`/blog/x`), in the site's `trailingSlash` form (check the
  config and existing links; `never` → no slash). A wrong form costs a redirect hop.
- **Verify the target exists before linking**: find the content file or page in `src/content/`
  / `src/pages/`, confirm it is not a draft, and confirm the route produces that URL.
- **Finding related pages:** grep frontmatter titles and `##` headings for the keyword across
  `src/content/**/*.{md,mdx}`; same folder = likely related; two or more shared tags = strong
  candidate. If the site has an explicit `related` frontmatter array, use it instead of inline guesses.
  The full link pass is `internal-linking`.
- **Slugs:** a title change never silently changes a slug. A slug change is a migration
  (`SKILL.md` §9).

---

## MDX

- Leave existing `import` lines and component tags (and their props) untouched. Add Markdown
  before, after or between components. If the change needs a new prop or component variant,
  propose it instead of editing.
- Add a new import only for a component the site already documents or uses elsewhere.
- Escape bare `<` and `>` in prose (`&lt;`, or wrap in code). Other HTML entities and `{`/`}`
  are also parsed; wrap them in code or escape them.
- Relative images need an `import` in MDX; `![alt](./img.jpg)` is only reliable in `.md`.
- Need components or `src/assets/` image imports in a `.md` file? Rename it to `.mdx` **only if
  `@astrojs/mdx` is in the integrations**. Otherwise skip that feature and tell the user.

---

## Schema on Astro pages

Use what the site already does, in this order (details in `seo-schema`):

1. **Layout `@graph` prop** (for example `Base.astro` takes `jsonLd` nodes and merges them into
   the single sitewide `@graph`). Add page nodes through the prop.
2. **`astro-seo-schema`** `<Schema item={...}>` if installed; use the layout's
   `<slot name="schema" />` when there is one.
3. **Frontmatter-driven** (for example a `faq` array → FAQPage node in `lib/blog-seo.ts`). Edit the
   frontmatter; never add a second script for the same type.
4. **Inline script, last resort** (no schema infrastructure and the file is `.mdx`): an
   `is:inline` `<script type="application/ld+json">` whose content is set with `set:html` from
   `JSON.stringify(...).replace(/</g, '\\u003c')`. Never interpolate raw `{JSON.stringify(...)}`
   into a script tag (a `<` in the text can close the tag, and user-sourced text becomes an XSS
   sink). A plain `.md` file cannot carry JSON-LD: flag it and propose a layout change.

Never duplicate the sitewide Organization / WebSite / LocalBusiness the layout already emits.
One FAQPage per page: check that a `Faq` component and a frontmatter helper do not both emit it.

---

## Page-shape edge cases

- **Target is a layout or component**, not a page: find the `.md`/`.mdx` entry or the `.astro`
  page that renders it and edit there.
- **`.astro` page fed by data files** (product, service and sales pages; for example `i18n/ui.ts`,
  `lib/service.ts`): the visible copy lives in imported `.ts` arrays/objects (features, FAQs,
  hero text) and inline markup. Those files ARE the body copy. Follow the imports to find which
  file feeds each section, and edit every locale's copy.
- **Frontmatter-driven pages:** improve the frontmatter fields (title, description, `tldr`,
  `faq`, CTA fields); do not bolt a long Markdown body onto a page the layout does not render
  that way.
- **No content collections:** work with the file structure that exists (`src/pages/*.astro`).
- **External CMS:** analysis and proposals only; any change log records rankings, not edits.
- **Content cache:** after adding or renaming content files, restart the dev server (the content
  layer caches entries).

---

## Facts in new or moved copy

- New sections that state product features, prices, model names, dates or limits need a current
  official source; uncertain → ask the user. Model memory is not a source.
- Moving or repeating an existing claim into a new place (FAQ, title, meta, table, takeaway,
  schema field) republishes it: re-verify it or drop the volatile part. The page itself is not
  evidence for its own claim.
- Before editing, list every volatile claim in each new or changed paragraph, FAQ answer,
  bullet, row, title/meta and schema field with its source. (Comparison pages keep a full claim
  ledger; see `comparison-pages`.)

## After the edit

1. Change summary: numbered list of title, meta, heading, section, link and schema changes, with
   the word-count delta.
2. Build and rendered checks: `build-verify.md` §1-§3.
3. Changed-file hygiene: `build-verify.md` §4.

File: seo-site-build/references/astro-edit-safety.md · Version 1.0 · November 2026
