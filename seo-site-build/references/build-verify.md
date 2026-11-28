# Build, rendered verification and changed-file hygiene

Every build or edit on a code-based site ends with these four steps. Do not report a change as
done, and never call a run "clean", until each step has a result. If a check could not run, say
exactly which one and why.

---

## 1. Source checks (before building)

- Every touched frontmatter field is defined in the content schema with a matching type
  (`astro-edit-safety.md`, Zod table).
- One H1 source: layout H1 **or** Markdown `#`, never both.
- Internal links: list every link added or changed (from Markdown, frontmatter such as
  `related`, and data files). Each must resolve to an existing, non-draft route in the site's
  `trailingSlash` form. If no link was added or changed, write "no internal links changed" and
  say whether existing links were spot-checked or skipped.
- Next.js: `metadata` and `JsonLd` data come from the same object. Shopify: the metafield
  value validates for its type (`json` parses; `jsonld.faq` has no leading/trailing pipes).

## 2. Build

Run the build with the detected package manager (`detect_stack.py` prints the command, e.g.
`npm run build`). Fix failures before anything else. Also run `astro check` when the project has
it (for example `npm run check`) because type errors in frontmatter usage do not always fail the build.

## 3. Rendered checks (built HTML, not source)

Run `python scripts/verify_build.py <build-dir>` over the whole build, then target the changed
pages:

```
python scripts/verify_build.py dist --page blog/<slug> \
  --expect-h2 "<exact new H2 text>" --expect-link /<linked-path> \
  --expect-type BlogPosting --expect-type FAQPage --expect-text "<new FAQ question>"
```

This script is not included in this repository.

Build dirs: Astro `dist/` (with `build.format: 'file'` a page is `dist/blog/x.html`, otherwise
`dist/blog/x/index.html`; the script finds either), Next.js static export `out/` (or
`.next/server/app/` for prerendered pages), Shopify: no local build; fetch the preview URL of the
unpublished theme and save the HTML, then point the script at that folder.

The report for each changed page must state:

- H1 count (must be 1) and H2 count.
- JSON-LD types present in the DOM (including types inside `@graph`), parse errors, a raw `<`
  inside a JSON-LD script, duplicate FAQPage/Organization nodes.
- Whether each new H2, FAQ question and link is present in the rendered DOM.
- Title display width (CJK counted as 2) and meta description length; canonical present,
  absolute, on the configured host and self-referencing; `noindex` state.
- On multilingual sites: hreflang set complete and reciprocal (`hreflang-i18n.md`).
- Sitewide sweep: pages over ~800 KB (`SKILL.md` §7), duplicate titles, internal links that
  point at no built page.

`verify_build.py` exits non-zero on any failure, so it can gate a deploy. If it cannot run (no
build output, a remote-only platform), do the same checks by hand on the rendered page and list
which ones were not possible.

After deploy, repeat the key checks on the live URL (curl the HTML, validate schema with the
Rich Results Test or validator.schema.org per `seo-schema`) because hosts and CDNs can rewrite
HTML, headers and robots.txt.

## 4. Changed-file hygiene

Before the final summary:

1. `git status --short`, then `git status --short --ignored`. Or run
   `python scripts/git_hygiene.py --allow "<glob>" [--allow "<glob>" ...]`, which runs both and
   classifies every path.
2. **Allowed changes:** the approved target files, shared layout/schema/config files the agent changed
   on purpose and can justify, and the project's notes or change-log files.
3. **Unexpected changes** (build tooling rewrote a tracked file, e.g. `.wrangler/deploy/config.json`,
   a cache, a lockfile the run did not mean to touch, other pages): restore them with
   `git restore <path>` when that is clearly safe; otherwise report them as an unexpected side
   effect and do not call the run clean. (In a repo other sessions also commit to, never run a
   blanket restore, stash or checkout; restore only paths this run created.)
4. **Ignored build and dependency output** (`dist/`, `.astro/`, `.next/`, `node_modules/`,
   `.wrangler/`): not content changes. Remove a temp folder or symlink only if it was created in
   this run. Keep installed dependencies. List what remains under
   "ignored build/dependency output" in the summary.
5. Never write "only target files changed" if either status command shows anything else.
6. New kinds of generated output (a state folder, a report folder, downloaded images that are
   not meant to ship) go into that project's `.gitignore` the same day.

File: seo-site-build/references/build-verify.md · Version 1.0 · November 2026
