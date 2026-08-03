---
name: content-atomizer
description: "Split one long article into multiple linked articles with distinct keywords and entity cores, and/or transform content into platform-optimized assets across LinkedIn, Twitter/X, Instagram, TikTok, and YouTube. Two modes. Mode A (split) takes a very long article, extracts its entities, tests whether its topics are one concept or several, and proposes a split map of child articles with primary/secondary keywords, angles, and an interlink plan. Mode B (atomize) turns content into platform-native social posts, long-form X and LinkedIn posts, broadcast email, and infographic briefs. Triggers on: repurpose this, atomize this content, turn this into social posts, thread from this, LinkedIn post from this, split this article, break this into smaller articles, this article is too long, turn this into a content cluster, what entities does this rank for, entity extraction. Outputs a split map plus article briefs, or platform-specific content ready to publish."
---

# Content Atomizer Skill

One piece of content should become ten. The best creators don't create more—they distribute better.

This skill works in two directions. **On-site**, it splits one very long article into the right number
of smaller articles, each with its own keyword target and entity core. **Off-site**, it transforms
content into platform-native assets that perform.

**The math:** A single blog post can become 1 LinkedIn carousel + 2 LinkedIn text posts + 1 Twitter thread + 3 single tweets + 2 Instagram carousels + 1 Reel script + 2 TikTok scripts + 1 YouTube Short script = 13 pieces of content from one source.

---

## Pick your mode

| | **Mode A — Split** | **Mode B — Atomize** |
|---|---|---|
| **Input** | One very long article (5,000+ words) | Any finished content |
| **Output** | N linked child articles: keywords, angles, entity cores, interlink map | Platform-native posts, scripts, email, image briefs |
| **Direction** | On-site SEO | Off-site distribution |
| **Produces** | Article briefs → your content skill writes them | Publishable copy |
| **Jump to** | [Mode A](#mode-a--article-splitting) | [Mode B](#mode-b--platform-atomization) |

They chain: split first, then atomize each child. Either runs alone.

## Before you start: load the brand context

Read `./brand/` per `_system/brand-memory.md`.

**Reads:** `voice-profile.md` (required for Mode B), `positioning.md` (optional)

Every platform template in Mode B adapts *format*, not voice. The energy shifts between platforms —
LinkedIn is more formal than TikTok — but the underlying voice, vocabulary rules, and forbidden
phrasings come from the voice profile and stay constant across every asset. Without it, output
defaults to generic-marketer and each platform drifts in a different direction.

If no voice profile exists, say so and offer to run `brand-voice` first. Don't silently invent a
voice — inconsistent voice across a distribution push is more damaging than delaying it.

Mode A doesn't need the voice profile (it produces briefs, not prose), but it should pass the profile
path through to each child brief so the writing step inherits it.

**Routing:** if the source is under ~5,000 words, Mode A will almost certainly tell you not to split
it — go straight to Mode B. If the source is 20,000+ words, run Mode A first; atomizing a 70-page
document as a single unit produces mush.

---

## The Core Job

**Mode A** — decide whether a long article is one concept or several, and if several, produce a split
map that separates them cleanly without cannibalisation.

**Mode B** — transform source content into **platform-native assets** that:
- Match each platform's algorithm signals
- Use format-specific best practices
- Include hooks proven to stop the scroll
- Feel native, not repurposed

---

# MODE A — Article Splitting

Full method: `references/article-splitting.md`. Entity procedure:
`references/entity-extraction.md`. Read both before proposing a split.

## The governing bias: consolidate

A false split costs you two thin pages that cannibalise each other. A missed split costs you one
article that runs long. **The first error is much more expensive.** When evidence is ambiguous, keep
it together — unless length forces the issue.

## Length tiers (the bias is scale-dependent)

| Tier | Source length | Default posture |
|---|---|---|
| **T1** | < 2,500 words | Don't split |
| **T2** | 2,500–5,000 | Consolidate hard |
| **T3** | 5,000–10,000 | Consolidate; partial carve often right |
| **T4** | 10,000–20,000 | Split expected — question is shape |
| **T5** | 20,000+ (≈66+ pages) | Split mandatory — related concepts become a chaptered series |

At T4/T5 the consolidate bias stops deciding *whether* to split and starts deciding **which shape**.
Related concepts that must separate for length become a chaptered series under one hub, which is how
you split without cannibalising: the hub owns the head term, the parts own distinct longtails.

## The ruleset is presented, not applied silently

**Step 0 is mandatory: show the user the thresholds and the detected length tier, and invite
overrides.** These defaults come from general SEO practice, not from the user's niche or content —
they are debatable by design and tunable over time. Full table in `references/article-splitting.md`.

## The decision cascade

For each candidate pair, use the strongest evidence *available*:

| Tier | Test | Works when | Blind spot |
|---|---|---|---|
| **1** | SERP overlap — shared URLs in top 10 | Both keywords have real volume | **Fails silently on novel content.** No SERP to measure. |
| **2** | Entity overlap — shared central entities | Always (reads your text) | Needs careful central/incidental classification |
| **3** | Structured Q&A with the user | Always | Costs user attention — use only on genuinely ambiguous pairs |

**Tier 1 fails on original material.** Proprietary research, in-house test data, and genuinely new
concepts have no SERP and no presence in training data. Absence of search data is not evidence that
concepts are separate — it's absence of signal. For novel content, Tier 2 is primary and Tier 3
decides.

**Tier 2 blocks.** When Tier 1 says separate and Tier 2 says ≥60% shared entities, the split is
blocked. Distinct keywords with a shared entity core means the same article wearing two hats.

**Tier 3 asks in domain terms, never SEO terms** — co-consumption, dependency, audience,
satisfaction, decision-count. The user knows the subject; they shouldn't need SEO knowledge to
answer. Present your read and confidence first so they're correcting, not originating. Log every
answer so no pair is ever asked twice.

## The eight steps

1. **Viability gate** — most long articles shouldn't split. "Don't split this, here's why" is a valid output.
2. **Section inventory** — every H2/H3 → words, query answered, independent demand, existing owner
3. **2.5 Entity extraction** — inventory, section→entity map, ranking evidence, gaps. **Before grouping**, because entity distribution drives it.
4. **Candidate children** — each needs a distinct primary, an angle, real material, and its own entity core
5. **Run the cascade** — every pair, including each candidate against the retained source
6. **Choose the shape** — present options with trade-offs and a recommendation
7. **Interlink map** — hub down to spokes, spokes up and across, no orphans
8. **Validate + hand off** — approved map → each child through your content skill's full write flow

## The five shapes

| Shape | What happens | Use when | Redirects |
|---|---|---|---|
| **A — Hub & spoke** | Source becomes trimmed pillar; spokes become independent articles | Source ranks; carved topics have separate intent | None |
| **B — Full replacement** | Source retires, 301 to strongest child | Source is a grab-bag with no coherent centre | Required |
| **C — Partial carve** | 1–2 sections leave; source ~90% intact | Mostly coherent, one section wants its own page | None |
| **D — Chaptered series** | Hub owns head term; Parts 1–N own longtails, sequential nav | **T4/T5 related concepts** — too long for one page, too connected to separate | None |
| **E — Don't split** | Nothing changes | Viability gate fails, or cascade says consolidate | None |

A 70-page source usually produces a **mix** — some clusters become independent articles, others
become a chaptered series.

## Entity extraction outputs

Four deliverables, detailed in `references/entity-extraction.md`:

1. **Entity inventory** — type, mentions, central/incidental, resolvable?, ranked for?
2. **Entity→child assignment** — every child needs an entity *core*, not just a keyword
3. **Entity overlap matrix** — the Tier-2 block test, per child pair
4. **Entity gap list** — what competitors treat as central that you don't cover

"What are we ranking for" uses three evidence sources: existing query data, entity+modifier SERP
checks, and a competitor entity diff. **For novel content two of the three are usually unavailable —
say so rather than quietly omitting them.**

## Never split in order to

1. Publish more — article count isn't the goal
2. Hit a word-count target — padding a child to clear the minimum manufactures thin content
3. Create a child whose primary is a longtail variant of the source primary — that *is* cannibalisation
4. Carve out context — sections that set up the main argument die when separated
5. Break a ranking page — position ≤5 means the current structure works

---

# MODE B — Platform Atomization

---

## Input Types

### What Can Be Atomized

| Source Type | Best Outputs | Atomization Potential |
|-------------|--------------|----------------------|
| **Blog Post** | All platforms | High (lots of material) |
| **Newsletter** | LinkedIn, Twitter, Instagram | High |
| **Podcast Episode** | Short-form video, threads, carousels | Very High |
| **Long-form Video** | Shorts, Reels, TikToks, carousels | Very High |
| **Webinar/Talk** | All platforms | Very High |
| **Case Study** | LinkedIn, Twitter threads | High |
| **Data/Research** | Carousels, threads, single posts | Medium-High |
| **Framework/Process** | Carousels, threads, video scripts | High |

### What to Extract

From any source, identify:

1. **The Core Insight** — The one thing someone should remember
2. **Supporting Points** — 3-7 sub-points that build the argument
3. **Stories/Examples** — Concrete illustrations
4. **Data Points** — Stats, numbers, proof
5. **Contrarian Takes** — Opinions that challenge conventional wisdom
6. **Actionable Steps** — What someone can do with this
7. **Quotable Lines** — Punchy phrases that stand alone

---

## Platform Playbooks

### LinkedIn

**Algorithm Signals (December 2025):**
- **Dwell time** — How long people spend reading (still #1)
- **Topic authority** — Consistent niche posting builds algorithmic trust
- **Golden hour** — First 60 minutes determines reach to 2nd/3rd-degree connections
- **Relevance over recency** — Mid-2025 update shows older posts (2-3 weeks) if highly relevant
- **Authentic engagement** — AI detects engagement pods via comment velocity and patterns
- **Native content** — Posts without links get significantly more reach

**2025 Reality Check:** Organic views down ~50%, engagement down ~25% as LinkedIn prioritizes quality over quantity. Post 2-3x/week max, not daily.

**Optimal Specs:**

| Format | Specs | Notes |
|--------|-------|-------|
| Carousel | 5-10 slides, 1080x1350px | Highest dwell time, save-worthy |
| Text Post | 1,200-1,500 chars recommended (**3,000 cap**) | Depth over frequency |
| **Long text post** | 2,000-3,000 chars | Full argument in-feed; still fights the "see more" fold |
| **Article** | No practical length limit, headers + images | Google-indexable, permanent URL, low feed reach |
| **Newsletter** | Article + subscriber notification | **Highest-leverage format on the platform** — pushes to subscribers |
| **Post series** | 3-7 posts over 1-3 weeks | The "thread" equivalent; compounding, builds topic authority |
| Document | PDF, 10-15 pages max | Good for frameworks |
| Video | 30-90 seconds, captions required | Lower reach than text/carousels |

> **Verify limits before relying on them.** Character caps, newsletter eligibility, and article
> features change. The selection logic below is stable; the numbers aren't.

#### It doesn't have to be a short post: choosing the LinkedIn format

| Source content looks like | Use | Why |
|---|---|---|
| One insight with a story | **Text post** | Native, highest reach, lowest effort |
| A full argument that needs room | **Long text post** | Stays in-feed (no click-out penalty) while going deep |
| A visual framework or process | **Carousel** | Forces dwell time; each swipe is a signal |
| Reference content you want indexed and linkable | **Article** | Permanent URL, Google-indexable, headers |
| Reference content **and** you want distribution | **Newsletter** | Everything Articles give you, plus a notification to every subscriber |
| A long article with 4+ separable points | **Post series** | Each post is a fresh entry point; the sequence compounds authority |
| Anything with an external link | **Post + link in first comment** | External URLs in the post body suppress reach |

**The Newsletter is the most under-used format here.** An Article and a Newsletter edition are nearly
the same artifact, but the Newsletter notifies every subscriber on publish. If you're publishing
long-form to LinkedIn at all, publishing it as a Newsletter instead of an Article costs nothing extra
and adds a push channel. Set the newsletter up once; every long-form piece afterward uses it.

**Post series is the LinkedIn analogue of a thread** — but distributed across days, not minutes.
Where an X thread is consumed in one sitting, a LinkedIn series gets a separate algorithmic roll of
the dice per post, and each one can reference the last. This is the right destination for a long
source article that has 4+ genuinely separable points.

#### LinkedIn Post Series Template

```
POST 1 — The thesis (day 1)
  [Full hook + the core claim]
  [Preview: "Over the next [N] posts I'll break down each of these."]
  [Do NOT list all N points — that gives away the series]

POSTS 2 to N-1 — One point each (every 2-3 days)
  [Callback: "This is part [X] of [N] on [topic]."]
  [ONE point, treated fully — this must stand alone for
   people who never saw post 1]
  [Forward hook: "Next: [the specific next point]"]

POST N — The synthesis (final)
  [Recap all N as a scannable list]
  [The meta-insight that only appears once you see all of them]
  [CTA — this is where the offer/link goes, not in post 1]
```

**Series rules:** every post must satisfy a cold reader who never saw the others; the callback line is
one line, not a recap paragraph; and the CTA waits for the final post.

#### LinkedIn Newsletter / Article Template

```
TITLE: [Specific and searchable — this one gets indexed by Google,
        so it follows SEO title logic, not feed-hook logic]

SUBTITLE / opening line:
[The promise, in one sentence]

[OPENING — 2-3 short paragraphs. Unlike a feed post, you're not
fighting for a scroll-stop; the reader already opted in. Lead with
the conclusion instead of a hook.]

## [Section header]
[Full treatment — this is the format where depth is rewarded]

## [Section header]
[Images where they carry information]

## [Section header]

## What to do with this
[Concrete next actions]

---
[Subscribe CTA — for Newsletters, this compounds every edition]
```

**Accompany every Newsletter/Article with a feed post** pointing to it — the article itself gets
little feed reach on its own. Post the single best insight natively as a text post, with the article
link in the first comment.

#### LinkedIn Carousel Template

**Slide 1: Hook Slide**
```
[BOLD CLAIM OR QUESTION]

(That challenges what they think they know)

Swipe → to learn [specific outcome]
```

**Slide 2-6: Content Slides**
```
[NUMBER]. [POINT HEADLINE]

[2-3 sentences of explanation]

[Visual element or example if possible]
```

**Slide 7: Summary Slide**
```
Quick recap:

1. [Point 1 - 5 words max]
2. [Point 2 - 5 words max]
3. [Point 3 - 5 words max]
4. [Point 4 - 5 words max]
5. [Point 5 - 5 words max]
```

**Final Slide: CTA Slide**
```
Found this useful?

→ Follow for more [topic]
→ Repost to help others
→ Save for later

[Your name/handle]
```

#### LinkedIn Text Post Template

```
[HOOK - First line must stop the scroll]

[Line break]

[CONTEXT - Why this matters, 2-3 lines]

[Line break]

Here's what I learned:

[Line break]

1. [Point with brief explanation]

2. [Point with brief explanation]

3. [Point with brief explanation]

4. [Point with brief explanation]

5. [Point with brief explanation]

[Line break]

[TAKEAWAY - The "so what"]

[Line break]

[CTA - Question or action]

---

[Hashtags - 3-5 max, at the bottom]
```

#### LinkedIn Hook Formulas

**Pattern 1: Contrarian Statement**
> "Stop [thing everyone does]. It's killing your [result]."

**Pattern 2: Story Hook**
> "Last week, I [did something]. What happened next changed how I think about [topic]."

**Pattern 3: List Preview**
> "[Number] [things] that [outcome]. (Number [X] is the one no one talks about.)"

**Pattern 4: Credibility + Insight**
> "After [impressive stat/experience], here's what I know for sure about [topic]:"

**Pattern 5: Question Hook**
> "Why do [surprising thing happen]? I finally figured it out."

**Pattern 6: Bold Claim**
> "[Counterintuitive claim]. Here's the proof:"

---

### Twitter/X

**Algorithm Signals (December 2025):**
- **Replies** — Highest weight, especially from accounts you engage with
- **Quote tweets** — 2x engagement value vs plain retweet
- **Time spent** — On tweet and clicked links
- **Profile clicks** — Curiosity driven by tweet
- **Media boost** — Images/videos/GIFs increase visibility scores
- **Early engagement** — First hours critical for amplification

**2025 Changes:** Following feed now uses **Grok AI** for ranking (based on past interactions and topics)—no longer purely chronological. Users default to For You feed.

**Optimal Specs:**

| Format | Specs | Performance |
|--------|-------|-------------|
| Single Tweet | <100 characters optimal | Highest engagement rate |
| Thread | 8-15 tweets | Best for depth + followers |
| **Long post** | Essay-length, single unit (paid tiers) | Best dwell time + profile clicks; lower raw reach |
| **Article** | Rich text, headers, embedded images (higher paid tier) | Canonical on-platform reference; lowest reach, longest life |
| Quote Tweet | Add value to original | 2x engagement vs retweet |
| Image Tweet | 1200x675px | 35% more engagement |

> **Verify limits before relying on them.** Character caps, which formats sit behind which paid tier,
> and what the composer exposes all change frequently on this platform. The *selection logic* below
> is stable; the specific numbers are not. Check current limits at time of use.

#### It doesn't have to be a tweet: choosing the X format

The most common mistake is defaulting to a thread. Threads are one option of four, and they're the
wrong one for a lot of source material.

| Source content looks like | Use | Why |
|---|---|---|
| Sequential steps, a listicle, N discrete tips | **Thread** | Each unit stands alone; every tweet is a re-entry point; maximises impressions |
| An argument where each step depends on the last | **Long post** | Chopping dependent reasoning into 280-char units destroys the chain |
| Technical explanation with setup, math, caveats | **Long post** | Caveats stranded in tweet 9 get read as standalone claims and quote-tweeted out of context |
| Reference material you want to be *the* link | **Article** | Formatting, headers, longest shelf life |
| One counterintuitive claim | **Single tweet** | Compression is the payload; don't dilute it |
| Reacting to someone else's take | **Quote tweet** | 2x engagement vs. retweet, and it borrows their audience |

**The rule for technical content:** if the argument has dependencies — "this only holds when X", "the
number changes if Y" — a thread will get you misquoted. Every tweet is independently
screenshot-able, and the qualifying tweet never travels with the claim. Use a long post.

**The hook doesn't disappear in a long post.** Only the first ~280 characters render before the
"Show more" fold. Everything you know about hook writing still applies to that opening block — it's
just that the payoff lives below the fold instead of in tweet 2.

#### X Long Post Template

```
[HOOK BLOCK — first ~280 chars, this is all that shows before "Show more"]
[Must work as a standalone tweet. Bold claim or specific promise.]
[Do NOT open with "A thread:" or "Let me explain" — you have one unit, use it]

[FOLD]

[CONTEXT — why this matters, 2-4 sentences]

[BODY — the argument, in full, with dependencies intact]

  Sub-point framing works here. Line breaks are your only
  formatting, so use them deliberately. Dense blocks don't
  get read.

[THE QUALIFIER — the "this only holds when..." that would have been
stranded in tweet 9. It belongs next to the claim it qualifies.]

[TAKEAWAY — the one line worth screenshotting]

[CTA — one, at the end]
```

#### X Article Template

```
HEADLINE: [Specific, no clickbait — this is reference content]

[Opening: the conclusion first. Readers who came from a post
already know the hook; don't re-sell them.]

## [Section header]
[Full treatment. Headers make it scannable and skimmable —
the one X format where structure is available. Use it.]

## [Section header]
[Embedded images where they carry information, not decoration]

## [Section header]

[Closing: what to do with this]
```

#### The hybrid: hook tweet → long post reply

Post the hook as a standalone tweet, then reply to yourself with the long post. You get the reach
profile of a short tweet and the depth of an essay, and the long post inherits the hook tweet's
engagement.

```
Tweet 1 (standalone, <100 chars):
  [The single most surprising claim from the source]

Reply (long post):
  [The full argument, dependencies intact]
```

Use when the source has one genuinely arresting claim and a long tail of necessary nuance.

#### Twitter Thread Template

**Tweet 1: Hook Tweet**
```
[BOLD CLAIM OR PROMISE]

[What they'll learn in one line]

🧵 Thread:
```

**Tweets 2-X: Content Tweets**
```
[NUMBER]. [POINT]

[2-3 sentences of explanation]

[Example or proof if fits]
```

**Final Tweet: Wrap + CTA**
```
TL;DR:

• [Point 1]
• [Point 2]
• [Point 3]
• [Point 4]
• [Point 5]

If this was useful:
1. Follow @[handle] for more
2. RT the first tweet

[Link if relevant]
```

#### Single Tweet Templates

**The Insight Tweet:**
```
[Counterintuitive observation about industry/topic]

Most people think [X].

But [Y] is actually true because [Z].
```

**The List Tweet:**
```
[Number] [things] that [outcome]:

• [Item 1]
• [Item 2]
• [Item 3]
• [Item 4]
• [Item 5]

Which one hits different?
```

**The Hot Take:**
```
Unpopular opinion:

[Contrarian statement]

Here's why: [One-line reasoning]
```

**The Question Tweet:**
```
[Provocative question about industry/topic]?

Genuine question. Reply with your take.
```

**The Proof Tweet:**
```
[Impressive result/stat]

Here's exactly how:

[3-5 bullet points of method]
```

#### Twitter Hook Formulas

**Pattern 1: Bold Opener**
> "[Thing] is dead. Here's what's replacing it:"

**Pattern 2: Numbers + Outcome**
> "I [did X] for [time period]. Here's what happened:"

**Pattern 3: Controversial Take**
> "This will piss off [group], but [claim]."

**Pattern 4: Curiosity Gap**
> "The [industry] secret no one talks about:"

**Pattern 5: Specific Proof**
> "[Specific result] in [timeframe]. No [common excuse]. Here's the playbook:"

---

### Instagram

**Algorithm Signals (December 2025):**
- **DM shares ("sends per reach")** — Now one of the STRONGEST discovery signals
- **Saves** — Still critical for Feed and Explore
- **Watch time & retention** — For Reels, completion rate is king
- **Likes per reach** — Quality signal (not raw likes)
- **Early velocity** — First 30-90 minutes determines push to wider audience
- **Relationship signals** — DMs, profile taps, comment history with account

**2025 Changes:** Photos getting more support in Feed again (Adam Mosseri). Carousels expanded to 20 slides in some regions. Hashtag weighting significantly reduced. New "Your Algorithm" feature lets users see why they're seeing content.

**Optimal Specs:**

| Format | Specs | Performance |
|--------|-------|-------------|
| Carousel | 6-10 slides (up to 20), 1080x1350px | Highest engagement, save-worthy |
| Reel | 7-15 sec (viral), 30-45 sec (tutorials) | Best for discovery/reach |
| Single Image | 1080x1350px | Getting more support in 2025 |
| Story | 1080x1920px, <15 sec | Best for DM engagement |

#### Instagram Carousel Template

**Slide 1: Cover (The Hook)**
```
[BOLD STATEMENT OR QUESTION]

in [large, readable font]

[Minimal design, high contrast]
```

**Slide 2: The Problem/Setup**
```
[Why this matters]

or

[What most people get wrong]
```

**Slides 3-8: The Content**
```
[ONE point per slide]

[Large text, minimal words]

[Visual hierarchy: headline + 1-2 supporting lines]
```

**Slide 9: Summary (Optional)**
```
Quick recap:

✓ [Point 1]
✓ [Point 2]
✓ [Point 3]
✓ [Point 4]
✓ [Point 5]
```

**Slide 10: CTA**
```
Save this for later 📌

Follow @[handle] for more

Share with someone who needs this
```

#### Instagram Caption Template

```
[HOOK - First line must work in preview]

.
.
.

[BODY - The value/story/insight]

[2-4 paragraphs max]

[Each paragraph 2-3 sentences]

---

💾 Save this for later
📤 Share with a friend who needs it
💬 Drop a [emoji] if this resonated

---

#[niche hashtag] #[broader hashtag] #[topic hashtag]
```

#### Instagram Reel Script Template (15-30 seconds)

```
[SECONDS 0-3: HOOK]
"[Pattern interrupt or bold claim that stops scroll]"

[SECONDS 3-20: VALUE]
"Here's [what/why/how]:
Point one: [brief]
Point two: [brief]
Point three: [brief]"

[SECONDS 20-30: CTA]
"Follow for more [topic]"
OR
"Save this for later"
OR
"Send to someone who needs this"
```

#### Instagram Story Sequence Template

**Story 1: Hook**
```
[Poll or question sticker]

"Quick question..."
[Poll: Option A / Option B]
```

**Story 2: Setup**
```
"Here's why I ask..."

[Brief context]
```

**Story 3-5: Value**
```
[One point per story]

[Use text animation or stickers for engagement]
```

**Story 6: CTA**
```
"Want the full breakdown?"

[Link sticker to content]

OR

"DM me [word] for [resource]"
```

---

### TikTok

**Algorithm Signals (December 2025):**
- **Watch time (first seconds)** — Completion rate still #1, but early seconds weighted heavily
- **Rewatch rate** — Multiple views = strong signal
- **Shares** — Especially to DMs
- **Niche community alignment** — 2025 favors specialized audiences over broad virality
- **Contextual categorization** — AI distinguishes humor, education, emotion to match interests
- **Video quality** — Lighting, sound, editing now integrated into ranking

**2025 Changes:** Algorithm now favors **longer content (30-60+ seconds) if retention is high**. Niche communities (#BookTok, etc.) get boosted over generic viral attempts. Deeper AI personalization analyzes watch duration, replays, and cross-platform habits.

**Optimal Specs:**

| Format | Specs | Performance |
|--------|-------|-------------|
| Short-form | 15-30 seconds | Highest completion rate |
| Medium | 30-60 seconds | Now favored if retention is strong |
| Long-form | 1-3 minutes | Good for depth with engaged audiences |
| Vertical | 1080x1920px (9:16) | Required |

#### TikTok Script Template (15-30 seconds)

```
[HOOK - 0-3 seconds]
"[Visual hook + verbal hook simultaneously]"

Options:
- "Stop scrolling if you [identifier]"
- "POV: You just realized [insight]"
- "The [industry] secret no one tells you:"
- "[Controversial statement]—let me explain"
- "I'm about to save you [time/money/pain]"

[BODY - 3-25 seconds]
"Here's the thing:

[Point 1 - delivered fast]

[Point 2 - keep momentum]

[Point 3 - the payoff]"

[CTA - 25-30 seconds]
"Follow for more [topic]"
OR
"Part 2?" [to boost comments]
OR
"Save this" [drives saves]
```

#### TikTok Hook Formulas

**Pattern 1: Pattern Interrupt**
> "[Unexpected visual or statement that breaks scroll pattern]"

**Pattern 2: Identity Call-Out**
> "This is for my [specific group] who [specific situation]"

**Pattern 3: Proof First**
> "[Show the result immediately, then explain how]"

**Pattern 4: Controversy Spark**
> "I'm going to get hate for this but [take]"

**Pattern 5: Curiosity Gap**
> "I can't believe [industry/brand] doesn't want you to know this"

**Pattern 6: Tutorial Promise**
> "In 30 seconds I'll show you how to [specific outcome]"

#### TikTok Content Patterns That Work

1. **Before/After** — Show transformation immediately
2. **Green Screen** — You + content behind you (tweets, articles, data)
3. **Stitch/Duet** — React to trending content in your niche
4. **Day in the Life** — Niche-specific (day in the life of a marketer, etc.)
5. **POV** — "POV: You're [scenario]" with relatable insight
6. **Listicle** — "3 things [outcome]" with fast delivery
7. **Myth Busting** — "Stop believing [common misconception]"

---

### YouTube

**Algorithm Signals (December 2025):**
- **Click-through rate (CTR)** — How often people click when shown your video
- **Average view duration & % watched** — Raw watch time AND completion percentage
- **Session impact** — Does your video keep people on YouTube longer?
- **Viewer satisfaction** — YouTube now uses surveys + behavior to estimate quality
- **Negative feedback** — "Not interested," skips, very low retention hurt you
- **Topical authority** — Channels focused on clear topics get recommended more

**2025 Changes:** AI-driven hyper-personalization (device, time of day, habits). Older evergreen videos get revived when topics trend again. Stronger emphasis on authority, depth, and "entity-rich" content (aligned with Google Search updates).

**Optimal Specs:**

| Format | Specs | Performance |
|--------|-------|-------------|
| Shorts | 10-35 sec (discovery), up to 60 sec | Highest reach, lower depth |
| Long-form | 8-12 minutes (sweet spot) | Best for monetization + depth |
| Thumbnail | 1280x720px | CTR target: 4-10% (Home), 6-12% strong |

#### YouTube Shorts Script Template

```
[HOOK - 0-2 seconds]
"[Immediate value promise or pattern interrupt]"

Examples:
- "Here's why [common belief] is wrong"
- "[Number] second [topic] lesson"
- "The [industry] hack that changed everything"

[BODY - 2-50 seconds]
[Deliver value fast]

[Each point: 5-10 seconds max]

[Keep visual movement—don't stand still]

[CTA - 50-60 seconds]
"Subscribe for more [topic]"
OR
"Full video on my channel"
OR
End abruptly (drives rewatch for missed content)
```

#### YouTube Long-Form Framework (HIVES)

**H - Hook (0-30 seconds)**
```
[Pattern interrupt or bold claim]
[Quick credibility if needed]
[Preview of what they'll learn]
"By the end of this video, you'll know exactly how to [outcome]"
```

**I - Intro (30 seconds - 1 minute)**
```
[Brief context on why this matters]
[Who this is for]
[What you'll cover]
"Let's dive in"
```

**V - Value (Main content)**
```
[Deliver on the promise]
[Clear sections with verbal signposting]
"First... Second... Third..."
[Examples and proof for each point]
```

**E - Engagement Prompts (Throughout)**
```
[Every 2-3 minutes, insert:]
"Let me know in the comments if [question]"
"Hit like if [relatable statement]"
"If you're finding this useful, subscribe"
```

**S - Strong CTA (Final 30 seconds)**
```
[Summarize key points]
[Clear next action]
"If you want to go deeper on [topic], watch this video next"
[End screen with subscribe + related video]
```

#### YouTube Thumbnail + Title Patterns

**Thumbnail Principles:**
- 3 elements max (face, text, object)
- High contrast colors
- Readable at small size
- Emotion on face (if showing face)
- Curiosity gap (show outcome, not process)

**Title Formulas:**

| Pattern | Example |
|---------|---------|
| How I [result] | "How I Built a 6-Figure Newsletter in 8 Months" |
| [Number] [Things] That [Outcome] | "7 LinkedIn Mistakes Killing Your Reach" |
| Why [Thing] Doesn't Work | "Why Your Content Strategy Isn't Working" |
| The [Adjective] [Thing] | "The Boring Marketing Strategy That Actually Works" |
| I [Did X] For [Time]. Here's What Happened | "I Posted Daily for 90 Days. Here's What Happened" |
| [Year] Guide to [Topic] | "2024 Guide to Growing on LinkedIn" |
| [Thing] vs [Thing] | "Threads vs Twitter: Which One Should You Use?" |

---

### Email — the broadcast

Atomization produces a **broadcast**: a short email whose only job is to earn the click through to the
article. That is a different artifact from a newsletter edition, which is standalone value the reader
consumes in the inbox and may never click out of.

| | Broadcast (this skill) | Newsletter edition (`newsletter` skill) |
|---|---|---|
| **Job** | Sell the click | Be the value |
| **Length** | 120-250 words | 800-3,000 words |
| **Success** | Click-through rate | Read-through, replies, forwards |
| **Timing** | Within ~24h of publish — early engagement is a freshness signal | On its own schedule |

**If the goal is a full edition, hand off to the `newsletter` skill.** Don't rewrite it here.

#### Broadcast Template

```
SUBJECT: [The specific finding, not the article title]
         [4-7 words. No "New post:" prefix — it reads as a bulletin
          and gets ignored.]

PREVIEW TEXT: [The second-most interesting thing. Do not repeat
               the subject — you get two lines of attention, use both.]

---

[ONE-LINE SETUP — why you looked into this]

Three things worth knowing:

1. [Finding — the number or the surprise, stated plainly]
2. [Finding]
3. [Finding]

[THE ONE THAT MATTERS — 2-3 sentences on the most useful of the three,
with the caveat. This is the paragraph that earns the click.]

→ [Full breakdown: link]

[Sign-off]
```

**Rules:** lead with the finding, not the fact that you published. Give away the three best things —
withholding them to force a click suppresses clicks. Link once, plus the sign-off.

### Infographics — the brief, not the render

This skill **specifies** the visual and hands off. It does not generate images — that's
`seo-image-gen` (article-embedded, OG cards, data infographics) or `creative` (social graphics at
campaign scale).

Producing a brief instead of a vague "make an infographic" request is what makes the handoff work.

#### Infographic Brief Template

```
PURPOSE:      [Which citable section this pairs with — a data visual
               that isn't anchored to a specific claim is decoration]

DATA:         [The exact values, with units and the source for each.
               Never hand off data the generator has to invent.]

STRUCTURE:    [Comparison table / process flow / ranked bars /
               before-after / decision tree / annotated diagram]

HIERARCHY:    1. [The number that has to land first]
              2. [Supporting context]
              3. [Source attribution — always visible]

ASPECT:       [4:5 for feed and article embed · 16:9 for OG ·
               9:16 for stories/shorts]

TEXT IN IMAGE: [Every word that must render, verbatim. Generators
               get typography wrong when it's left implied.]

CONSTRAINTS:  [Legibility floor at thumbnail size; brand palette;
               anything that must NOT appear]
```

**Which visuals actually earn the effort:** a data infographic paired with a citable section (it
supports the claim *and* satisfies the multi-modal signal), a process flow when the source explains a
sequence, and a comparison table when the source compares 3+ options. Quote cards and generic
"tips" graphics rarely justify production time.

---

## The Atomization Workflow

### Step 1: Extract

From your source content, pull out:

```
CORE INSIGHT:
[One sentence that captures the main point]

SUPPORTING POINTS:
1. [Point + brief explanation]
2. [Point + brief explanation]
3. [Point + brief explanation]
4. [Point + brief explanation]
5. [Point + brief explanation]

STORIES/EXAMPLES:
- [Story 1]
- [Story 2]

DATA/PROOF:
- [Stat 1]
- [Stat 2]

QUOTABLE LINES:
- "[Quote 1]"
- "[Quote 2]"

CONTRARIAN TAKES:
- [Take 1]
- [Take 2]
```

### Step 2: Map to Platforms

| Content Element | Best Platforms | Best Formats |
|-----------------|----------------|--------------|
| Core insight | All | Single posts, hooks, broadcast subject line |
| Supporting points (together) | LinkedIn, Twitter | Carousel, thread, post series |
| Individual points | All | Single posts |
| **Dependent argument** (each step needs the last) | Twitter/X, LinkedIn | **Long post, Article — never a thread** |
| **Reference-grade depth** | LinkedIn, Twitter/X | **Newsletter, Article** |
| Stories | Instagram, TikTok | Reels, Stories |
| Data points | LinkedIn, Twitter | Image posts, carousels, **infographic brief** |
| Quotable lines | Twitter, Instagram | Quote graphics |
| Contrarian takes | Twitter, TikTok | Single tweets, video hooks |
| **The 3 best findings** | Email | **Broadcast** (within 24h of publish) |

### Step 3: Transform

For each platform, apply:

1. **Format** — Use the templates above
2. **Hook** — Platform-specific hook formula
3. **Length** — Match platform norms
4. **CTA** — Platform-appropriate action
5. **Voice** — Adjust formality (LinkedIn > Instagram > TikTok)

### Step 4: Sequence

**Optimal posting sequence:**

1. **LinkedIn carousel** — Day 1 (longest shelf life)
2. **Twitter thread** — Day 1-2 (good for discussion)
3. **Instagram carousel** — Day 2-3 (repurpose LinkedIn design)
4. **TikTok/Reel** — Day 3-4 (needs video production)
5. **YouTube Short** — Day 4-5 (can repurpose TikTok)
6. **Single posts** — Ongoing (extract individual points)

---

## Anti-Patterns: What Not to Do

### Don't:

1. **Copy-paste across platforms**
   - Each platform has different norms
   - Cross-posted content performs 40-60% worse

2. **Use the same hook everywhere**
   - LinkedIn hooks ≠ TikTok hooks
   - Adjust energy and format per platform

3. **Ignore platform-native features**
   - No hashtags on LinkedIn carousels
   - Always use captions on video
   - Instagram needs visual-first thinking

4. **Post everything at once**
   - Stagger across days/weeks
   - Gives each piece room to perform

5. **Forget the CTA**
   - Every platform piece needs a clear next action
   - But make it platform-appropriate

### Do:

1. **Lead with the best hook per platform**
2. **Adapt length to platform norms**
3. **Use native formatting (threads, carousels, etc.)**
4. **Front-load value (especially for video)**
5. **Create platform-specific visuals when possible**

---

## Transformation Examples

### Example: Blog Post → Multi-Platform

**Source:** 2,000-word blog post on "5 Pricing Mistakes That Kill SaaS Growth"

**Atomization:**

| Platform | Format | Content |
|----------|--------|---------|
| LinkedIn | Carousel | 8 slides: Hook + 5 mistakes + recap + CTA |
| LinkedIn | Text Post | Deep dive on mistake #1 with personal story |
| Twitter | Thread | 7 tweets: Hook + 5 mistakes + wrap |
| Twitter | Single | Just mistake #3 (most contrarian) as hot take |
| Instagram | Carousel | Visual version of LinkedIn carousel |
| Instagram | Reel | 30-sec: "Stop making these pricing mistakes" |
| TikTok | Video | 20-sec: Most controversial mistake, hot take style |
| YouTube Short | Video | 45-sec: All 5 mistakes, rapid fire |

### Example: Podcast Episode → Multi-Platform

**Source:** 45-minute podcast interview with actionable insights

**Atomization:**

| Platform | Format | Content |
|----------|--------|---------|
| LinkedIn | Text Post | Best quote + context + your take |
| LinkedIn | Carousel | Key framework from interview |
| Twitter | Thread | 10 best insights from the episode |
| Twitter | Single | Best quote as standalone insight |
| Instagram | Carousel | Visual quotes from guest |
| Instagram | Reel | Best 30-second clip with captions |
| TikTok | Video | Spiciest take from interview |
| YouTube Short | Video | Best insight with visual hook |
| YouTube | Long-form | Full episode or highlights compilation |

---

## Platform Voice Adjustments

The same insight needs different energy per platform:

| Platform | Voice | Example (same insight) |
|----------|-------|----------------------|
| LinkedIn | Professional, thoughtful | "After 10 years in marketing, I've learned that simplicity beats complexity. Here's why:" |
| Twitter | Punchy, direct | "Hot take: Simple marketing > 'sophisticated' marketing. Every time." |
| Instagram | Visual, inspirational | [Image with text: "Simple > Sophisticated" + story in caption] |
| TikTok | Casual, energetic | "Y'all I need to talk about why everyone's overcomplicating their marketing..." |
| YouTube | Conversational, thorough | "If you've been in marketing for any length of time, you've probably noticed something..." |

---

## Quick Reference: Platform Specs (December 2025)

| Platform | Optimal Length | Best Format | Hook Window | Top Signal |
|----------|---------------|-------------|-------------|------------|
| LinkedIn | 1,200-1,500 chars (3,000 cap) | Carousel | First 3 lines | Dwell time + topic authority |
| LinkedIn (long-form) | No practical limit | **Newsletter** > Article | Title + first 2 lines | Subscriber push + Google indexing |
| Twitter/X | <100 chars (single) | Thread (8-15) | First tweet | Replies + early engagement |
| Twitter/X (long-form) | Essay-length | **Long post** for dependent arguments | First ~280 chars (pre-fold) | Dwell time + profile clicks |
| Instagram | 6-10 slides | Carousel | First slide | DM shares ("sends per reach") |
| TikTok | 30-60 seconds (if retention high) | Short video | First 3 seconds | Completion + niche alignment |
| YouTube (Shorts) | 10-35 seconds | Vertical video | First 2 seconds | Completion rate |
| YouTube (Long) | 8-12 minutes | Horizontal | First 30 seconds | Satisfaction + session time |
| Email | 120-250 words | Broadcast | Subject + preview text | Click-through rate |

Platform mechanics change frequently. Treat the dated algorithm notes and the specific caps above as
**directional** — verify current limits before relying on them.

---

## The Test

**Mode B (atomization) is good when:**

1. **Each piece stands alone** — Makes sense without the source
2. **Each piece feels native** — Doesn't feel "repurposed"
3. **Hooks match the platform** — Right energy, right format
4. **Format matches the content** — A dependent argument didn't get chopped into a thread
5. **Value is front-loaded** — Best stuff first
6. **CTAs are appropriate** — Platform-native actions
7. **Quality over quantity** — 5 great pieces > 15 mediocre ones

**Mode A (splitting) is good when:**

1. **It was willing to say no** — a splitter that always finds a split is manufacturing thin content
2. **Every child has an entity core**, not just a keyword
3. **No child's primary is a longtail variant of the source's**
4. **The retained hub still reads as a complete argument** — not leftovers
5. **The evidence tier is stated** — including which tiers were unavailable and why
6. **Every ambiguous pair was asked about, not guessed at**

---

## How This Connects to Other Skills

**Mode A — splitting:**

| Skill | Relationship |
|---|---|
| `keyword-database-article-map` | Owns the SERP-Overlap Test, One-Home Rule, and angle differentiation. Mode A **drives** that logic — it doesn't re-implement it. |
| `seo-content` | Receives each approved child brief and writes it through the full flow, gates included |
| `information-gain` | Consumes the entity gap list — gaps become research targets |
| `internal-linking` | Executes the interlink map Mode A produces |

**Mode B — atomization:**

| Skill | Relationship |
|---|---|
| `seo-content` | **Input** — published articles to atomize |
| `brand-voice` | **Input** — produces `./brand/voice-profile.md`, loaded at start (see *Before you start*). Run it first if absent. |
| `direct-response-copy` | **Input** — landing page insights to distribute |
| `newsletter` | **Output** — hand off when the goal is a full edition, not a broadcast |
| `seo-image-gen` | **Output** — receives infographic briefs and renders them |
| `creative` | **Output** — receives social graphic specs at campaign scale |
| `content-distribution` | **Wraps this** — decides which channels and when; this skill makes the assets that plan calls for |

**The flow:**

```
Very long article
   │
   ├─ MODE A ─→ split map ─→ child briefs ─→ seo-content ─→ published articles
   │                                                             │
   └─────────────────────────────────────────────────────────────┘
                                                                 │
                                                            MODE B
                                                                 │
        ┌──────────────┬──────────────┬─────────────┬────────────┴───────┐
     social         long-form      broadcast     infographic          series
      posts        X / LinkedIn      email          brief            (LinkedIn)
                                                       │
                                                 seo-image-gen
```

1. Long source → **Mode A** decides whether it's one concept or several
2. Approved children → your content skill writes them
3. Each published article → **Mode B** produces platform assets
4. `content-distribution` sequences the release across channels
