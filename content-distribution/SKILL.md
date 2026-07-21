---
name: content-distribution
description: "Off-site distribution and AI-visibility playbook for a published article — Reddit, YouTube, LinkedIn, email, and review/entity platforms. Use AFTER an article is live to plan where and how to amplify it, build brand-entity presence, and earn AI citations. Triggers on: distribute this article, promote the post, where should I share, off-site SEO, earned media, get cited by AI, brand mentions, content amplification, publish-day plan. This is a strategy skill — it produces a channel plan, not automated posting. Off the per-article critical path."
---

# Content Distribution (off-site amplification & AI visibility)

On-site optimization (the `seo-content` flow) decides whether a page *can* rank and be cited. Off-site
distribution decides whether it actually gets *seen and referenced* — and for AI answer engines that's
most of the battle: AI-search analyses report the large majority of AI citations trace to **off-site**
signals (brand mentions, community discussion, video), not the page itself. This skill turns a finished
article into a distribution plan.

It is **strategy, not automation** — it outputs a per-article channel plan and a publish-day timeline.
It does not post for you, and it is deliberately **off the per-article critical path**: write and ship
the article through `seo-content` first, then invoke this when you want to amplify.

> **Provenance / verify-before-citing:** The channel correlations and growth figures below are adapted
> from the `claude-blog` distribution-playbook (MIT), itself compiled from third-party AI-search
> studies. Treat them as *directional* — use them to prioritize channels, not as facts to quote in a
> published article. Confirm any specific percentage against the primary source before it leaves this
> repo. (Same discipline as `seo-content/references/geo-checklist.md`.)

---

## The reframe: owned vs earned

Most small operators spend ~90% of effort on owned content (the blog) and ~10% on getting it seen. The
modern split that earns AI citations is closer to **40% owned / 60% earned**. For your-project —
a lean, single-operator Shopify store — treat 40/60 as the *direction*, not a quota. Pick the two or
three channels below that fit the topic and your core audience segments and do those consistently.
Half-doing six channels beats fully-doing zero.

---

## Channel playbook

### Reddit — highest reported AI-citation growth
- **The 10/90 rule:** 10% of activity can reference your content; 90% must be genuine community help.
  Link-dropping gets removed and tanks the account.
- Lead with the **insight**, not the link. Answer the actual question; link only when it genuinely adds.
- Relevant subs for this niche: r/[your-niche] and other relevant industry subreddits / niche
  communities/forums where your topic is discussed. Match the article topic to the sub.
- Organic only (post-2023 API changes killed automation). One real, helpful comment > ten drops.

### YouTube — strongest reported citation correlation
- Companion video for how-to / comparison articles. **Mirror the article's H2s as video chapters** —
  AI systems index chapters and transcripts.
- **Upload your own transcript** (don't rely on auto-captions) — it's indexed text.
- How-to format reportedly drives the biggest citation lift. A 3-6 min "how to size / set up X" clip
  that points back to the full article in the description.

### LinkedIn — algorithm penalizes outbound links in-body
- Put the **blog link in the first comment, not the post body** — external URLs in the body suppress
  reach. The post itself: 800-1,200 words, opinion-led, one clear takeaway.
- Best for B2B-leaning topics (cost-of-ownership, ROI, deployment/setup).

### Email — fastest freshness signal
- Send to the list **within ~24 hours of publishing** — early engagement is a freshness signal.
- Format: a TL;DR + the 3 most useful findings + the link. Don't paste the whole article.

### Review & entity platforms (B2B credibility multiplier)
- For the store/brand: maintain presence and respond to reviews on the platforms your buyers check
  (Google Business, marketplace/supplier profiles, trade directories). Volume + recency + fast response
  build the trust signals AI engines weigh.

### Wikipedia / Wikidata — credibility tiebreaker (long game)
- An entity entry acts as a tiebreaker for AI citation, but requires **independent coverage first**
  (multiple third-party mentions). Don't attempt a self-authored page — earn the mentions, and it
  follows. This is a months-to-years signal, not a launch task.

---

## Brand-entity presence (ties to GEO §C)

AI-visibility analyses report **brand mentions across the web correlate more strongly with AI citation
than raw backlinks**. The off-site goal is to get "Your Brand" *named* — in roundups,
manufacturer/supplier pages, trade forums, and Q&A — even **unlinked** mentions count. This is the
strategic throughline behind every channel above and is the same note as
`seo-content/references/geo-checklist.md` §C (brand mentions). Build the entity; citations follow.

---

## Publish-day timeline (template — adapt to capacity)

A realistic cadence for one operator. Skip rows that don't fit the article.

| When | Action |
|---|---|
| **Day 0 (publish)** | Email the list (TL;DR + 3 findings + link). One LinkedIn post if B2B-relevant (link in first comment). |
| **Day 0-1** | If a how-to/comparison: outline the companion YouTube clip (chapters = the H2s). |
| **Day 2-5** | Genuine Reddit/forum participation where the topic is being asked about (10/90 rule). Publish the YouTube clip; description links back. |
| **Week 1-2** | Pitch/insert into any relevant roundup or supplier mention opportunity (entity building). |
| **Quarterly** | Revisit top articles: refresh stats, re-share the still-relevant ones, check review platforms. |

---

## What this skill does NOT do
- No automated posting or API integration — every channel here is organic/manual by design (and several
  platforms actively penalize automation).
- Not part of the article QA gate — it runs after publish, on the articles worth amplifying.
- Doesn't replace on-site GEO work — citability still starts with the structure rules in `seo-content`.

## How this connects
- `skills/seo-content/SKILL.md` — write/ship the article here first; this skill runs after.
- `skills/seo-content/references/geo-checklist.md` §C — brand-mention strategy is the on-ramp to this.
- `skills/content-atomizer/SKILL.md` — for turning the article into the per-channel assets (threads,
  clips, email) this plan calls for.
