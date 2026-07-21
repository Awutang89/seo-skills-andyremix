# Link Refresh — Outbound-Citation Audit for Refreshes

When you **refresh or rewrite an existing article**, one of the strongest freshness signals is
swapping stale outbound links for newer, more authoritative external sources. A 2021 blog post
cited as your authority quietly ages the whole page; a current `.gov` PDF with a fresher figure
re-dates it. This is the citation-side companion to the freshness work `seo-page-diagnosis` scores
(Authority/sourcing + Freshness) — that skill *finds* the gap and hands off "route to seo-content
(refresh)"; this procedure *closes* it.

> **When this runs:** Refreshes and rewrites only. **Skip entirely for net-new articles** — there
> are no pre-existing outbound links to audit (the QA-gate row reads `N/A`). For net-new sourcing,
> use Phase 1.5 and `/information-gain` as normal.

The engine for finding replacements is the existing **`/information-gain`** skill — do not reinvent
the search. This file is the loop that wraps it.

---

## Step 1 — Scan the existing outbound links

Read the article and list **every external (outbound) link**. For each, record:

| Anchor text | Destination URL | What it supports | Source year |
|---|---|---|---|

- **What it supports:** a stat, a claim, a definition, or a bare source reference.
- **Source year:** the destination's publication/update year. `WebFetch` the destination when the
  year isn't obvious from the URL or anchor — you need it to apply Step 2's threshold.

Internal links are out of scope here (that's the internal-link audit). This is outbound only.

---

## Step 2 — Flag stale or weak citations

Flag a link if **any** of these is true:

1. **Source >2 years old.** This is the SEO freshness threshold — tighter than `/information-gain`'s
   10-year "potentially outdated" flag, because for a *ranking* refresh a 3-year-old statistic reads
   as dated even when it's still roughly correct.
2. **The stat has likely been superseded** by newer data (prices, market size, adoption rates,
   energy figures, failure rates — anything that drifts year to year).
3. **It's a secondary source where a primary exists** — a blog post, news roundup, or aggregator
   standing in for a government report, academic paper, standards body, or manufacturer spec sheet.
4. **It's broken or redirects** — 404, parked domain, or a redirect to a generic homepage.

> **Evergreen exception — do not churn for churn's sake.** Standards (ISO, ASME), regulations, and
> stable definitions don't need swapping just because they're old; a 2015 standard is still the
> standard. Flag an evergreen citation **only** if it's superseded (a newer revision exists) or
> broken. Re-dating a link that points to the correct authoritative source adds no value and risks
> downgrading a Tier 1 source to a worse one.

---

## Step 3 — Find replacements (drive with `/information-gain`)

For each flagged link, find a fresher, more authoritative replacement. Run the **`/information-gain`**
skill for the relevant claim, or — for a one-off swap — a targeted `WebSearch` using the **Phase 1.5
tier rules** (Tier 1: `.gov`/`.edu`/intl orgs · Tier 2: research/academic · Tier 3: major trade ·
Reject: generic blogs/affiliate). Prioritize primary-source filetypes: PDF, PPTX, DOCX, XLSX.

A replacement must:
- be **more recent** than the source it replaces;
- carry a **specific, citable statistic** for the *same* claim (not a vague restatement);
- be a **primary / high-authority** source (prefer ≥ the original's tier, never below Tier 3);
- add **genuine information gain** — different vocabulary or a sharper data point than what the
  article already says, not a synonym swap.

If no fresher primary source exists, **say so and keep the original** — note it as "current source is
still the best available." Don't downgrade a good link just to change the date.

---

## Step 4 — Rewrite the anchor text

Every replacement gets new anchor text that:
- is **descriptively different** from the original — not the same phrase pointing at a new URL;
- **naturally names the new source or weaves in the new stat** (e.g. *"the Department of Energy's
  2025 industrial-efficiency survey"* rather than *"this study"*);
- **reads naturally** in the surrounding sentence — rewrite the sentence around it if needed.

---

## Step 5 — Output: inline approval table, then apply

Present **one compact table** for the user to approve before touching the file:

| Original anchor → URL | Issue | New anchor → URL | New stat | Source / Year / Type | Why better | Suggested rewrite sentence |
|---|---|---|---|---|---|---|

After approval:
1. Edit the article `.md` — swap links, update anchor text, and weave in the new stat/sentence.
2. Regenerate HTML via your post-draft / publish step (nofollow is re-applied automatically).
3. Update `KEYWORD-REGISTER.csv` only if anchors/links changed materially.

**Guardrails — the existing rules still bind after the swap:**
- Stay within **2–4 external links** total, with **≥1 Tier 1–2**.
- Keep **200+ words between any two links** (internal or external) — if a swap bunches links, move
  or drop one.
- Any **anchor / citation-priority stat** (the figure you most want AI engines to quote) must be
  **corroborated across 2+ independent authoritative sources** — same rule as Phase 1.5 Step 3b.
- Re-run the relevant Phase 7 QA-gate rows (external-link tier, link spacing, link freshness) after
  editing.
