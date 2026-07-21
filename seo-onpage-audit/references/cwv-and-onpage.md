# Core Web Vitals & On-Page Thresholds Reference

Thresholds for `seo-onpage-audit`. Adapted from the open-source `claude-seo` project (MIT). Verify CWV
thresholds against Google's current `web.dev/vitals` before treating as final.

## Core Web Vitals (current)

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5 s | 2.5–4 s | > 4 s |
| **INP** (Interaction to Next Paint) | < 200 ms | 200–500 ms | > 500 ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1–0.25 | > 0.25 |

- **INP replaced FID** on 2024-03-12; FID was fully removed from Chrome tools 2024-09-09. **Never
  reference FID.**
- Field data (real users) comes from CrUX/PageSpeed Insights — not measurable from HTML alone. Run PSI
  manually per URL for real numbers.
- **Heuristic flags we CAN see from HTML:** images without width/height (CLS risk), oversized images
  (LCP risk — see image-seo-audit size tiers), render-blocking third-party scripts in `<head>`,
  no `loading="lazy"` on below-fold images.

## On-page length & keyword rules

| Element | Rule |
|---|---|
| Title tag | 50–60 chars (≤~600px); primary keyword present + front-loaded; short and descriptive; unique per page (uniqueness verified only by the site-level pass) |
| Meta description | **50–160 chars** (below 50 = thin; Google truncates beyond ~160); primary keyword present; accurately summarizes the page; unique per page |
| H1 | exactly one per page; **40–65 chars**; primary keyword present; matches page intent / search intent |
| H2–H6 | descriptive and meaningful (not "Overview"/"More Info"); carry secondary / long-tail keywords where natural; together cover the subtopics the main query implies |
| Heading hierarchy | H1→H2→H3, no skipped levels, headings descriptive not decorative |
| Keyword coverage | primary keyword should appear in: title, H1, **first 100 words of body**, **at least one H2**, the URL slug, and the meta description; secondary/long-tail terms spread across subheads + body (never stuffed) |
| URL slug | lowercase, hyphen-separated, concise, human-readable (words not IDs — `/red-unicycle/` not `/red-2192734i.html`); **no repeated keywords** in the path; consistent structure across the site (site-level pass); no redirect chains (max 1 hop) |

## Indexability
- Canonical: self-referencing, absolute (full `https://…` matching the live URL incl. trailing
  slash). Serve it in the **raw server-rendered HTML**, not JS-injected — Google honors raw-HTML
  robots/canonical even if JS later changes them.
- `meta robots`: confirm no accidental `noindex`/`nofollow` on pages meant to rank.
- Page should be present in the site's XML sitemap.

## Links
- **Internal:** even spacing — no two links (internal or external) within ~200–300 words of each
  other; anchor text descriptive/informative (flag "click here", "read more", and bare/pasted URLs);
  links point to relevant, appropriate destinations; no duplicate targets; no broken links.
- **External:** link out to authoritative sources where it strengthens the page. `rel` is
  contextual, not blanket — normal editorial links can be followed; **paid/affiliate** links must
  carry `rel="sponsored"`, **user-generated** links `rel="ugc"`, and untrusted links
  `rel="nofollow"`. Flag missing `rel` on affiliate/paid links, and flag broken external links.
- **Orphans / inbound distribution** (a site's most important pages should receive the most internal
  links, and no important page should be orphaned) can only be judged across the whole site — this is
  part of the optional **site-level pass**, not a single-URL check.

## Crawler notes (AI era)
- **Googlebot** crawls for Search indexing **and** AI Overviews.
- **Google-Extended** governs **Gemini training only** — blocking it does **NOT** affect Google Search
  indexing or AI Overviews. Don't block it assuming it controls AI Overviews; it doesn't.
- AI search crawlers to allow if you want citations: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot,
  PerplexityBot (a site-level `robots.txt` decision).
- **Crawl-friendliness heuristics (AI citation):** TTFB < 200 ms; rendered HTML < ~200 KB (very
  large DOMs risk partial extraction — flag egregiously heavy pages only).
- If the site's custom domain is proxied through a CDN/WAF that default-blocks AI bots (e.g.
  Cloudflare's AI-bot block), that block overrides `robots.txt` allow-lists — check it when a site
  wants AI citations.
- `llms.txt` is experimental/unconfirmed — INFO only, never a blocker.

## IndexNow
Optional protocol to ping Bing/Yandex (and others) on publish/update for faster discovery. A
nice-to-have, not required. Note as INFO, not a blocker.
