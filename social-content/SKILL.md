---
name: social-content
description: "Drafts single social posts for X, X Premium (long posts), Meta Threads and LinkedIn that sound like the person posting, rest on real proof, and skip generic AI polish. Calibrates to the saved voice profile and real voice examples, interviews briefly when the idea is thin (or skips questions in quick mode), keeps a private proof ledger, runs a three-check editing pass, picks one of 12 visual roles with a JSON prompt seed, generates images only with consent through an optional image engine, saves reusable post packets on request, and hands approved drafts to an installed scheduler only when asked. Use when someone says: write a post, write a LinkedIn post, draft a tweet, X post, long X post, Threads post, turn this into X and LinkedIn posts, post about this screenshot, make this sound like me on LinkedIn, quick post, just write it, build my social voice profile, image prompt for this post, queue these drafts. NOT for splitting one long article into many pieces across Instagram, TikTok and YouTube (use content-atomizer), LinkedIn carousel decks, paid ads (use creative), building the brand voice itself (use brand-voice), or humanizing an existing long draft (use content-humanizer)."
metadata:
  version: 1.0.0
  display-name: Social content
  category: marketing
  updated: 2026-09-28
  provenance: "Built in our own words from a social content plugin. Typefully delivery replaced by a platform-neutral scheduler handoff; Zernio is a future adapter."
---

# Social content

The skill writes one strong post per requested platform. The post should sound like the person who will publish it, stand on proof they actually have, and fit the platform's reading habits. Voice files, packets, visuals and schedulers exist to serve the draft; none of them is allowed to take over the run.

Keys: none of its own. Image generation borrows the keys of an optional image engine, `<image-engine>` (it loads them itself). A future Zernio scheduler adapter would use `ZERNIO_API_KEY`; it is not active.

## What it does

- Drafts for X, X Premium, Meta Threads, LinkedIn, or exactly the combination asked for.
- Loads the voice profile and the real voice examples before writing. Examples outrank the profile: the profile states the rules, the examples carry the rhythm.
- Asks two or three focused questions when the source is too thin to publish. Asks nothing in quick mode.
- Builds a private proof ledger before drafting and never lets a post claim more than the ledger allows.
- Runs a three-check editing pass (hook and platform fit, proof, voice and AI cleanup) before anything is shown.
- Decides the visual role before final copy, writes a JSON prompt seed when a visual earns its place, and generates only with consent.
- Saves a reusable social workspace (index, profile, packets) only when that is useful.
- Hands approved drafts to an installed scheduler only when the person asks.

## What it never does

- Invent proof: numbers, quotes, results, screenshots, customers, testimonials, personal stories.
- Write a platform draft nobody asked for, or skip one that was asked for.
- Generate an image just because a key happens to exist.
- Queue drafts in a scheduler before approval, or schedule or publish when only drafts were approved.
- Force hashtags, emojis, or formatting habits the voice evidence does not support. Dashes follow the house rule: zero em dashes, en dashes or spaced hyphens in the copy, unless the person's own examples use them.
- Copy an admired post's wording. The move can be emulated; the sentences cannot.

## Question rule

Every question to the person (interview, platform routing, save location, off-pillar check, X Premium check, scheduler preference, image offer, ambiguous approval) goes through the structured question tool (AskUserQuestion in Claude Code). Ask the fewest questions that unblock the run and bundle them into one call. If the runtime has no such tool, say so once and ask in chat.

## Reference map

Load only what the run needs.

| Need | Read |
|---|---|
| Thin idea, first run, voice setup | `references/interview.md` |
| Saved profile, earlier post, packet, revision | `references/memory.md` |
| Any draft | `references/drafting-guide.md` |
| Editing and AI cleanup | `references/editing-guide.md` |
| Platform choice and fan-out | `references/platform-rules.md` |
| Standard X | `references/platforms/x.md` |
| X Premium or long X post | `references/platforms/x-premium.md` |
| Meta Threads | `references/platforms/threads.md` |
| LinkedIn | `references/platforms/linkedin.md` |
| Visual decision, roles, prompt seeds | `references/visuals.md` |
| Image generation (gate, engine call, fallback) | `references/image-generation.md` |
| Scheduler detection, queueing, schedule or publish | `references/scheduler-handoff.md` |
| Social profile creation or update | `references/social-profile-template.md` |
| Voice examples file and copyright rule | `brand-voice/` (owned there; see `references/memory.md` for how this skill reads it). This file is not included in this repository. |
| Packet, index, seed files | `templates/` |
| Character counts and lint | `scripts/check_post.py` |

Required reads are not theater. A voice profile never stands in for the platform rules, the drafting guide or the editing guide. If a required file cannot be read, say so rather than claiming the workflow ran.

## Workflow

### 1. Load context

For runs with several drafts, fan-out, packets, memory, visuals, image generation, scheduler delivery, or more than one reference to load, open a todo list early (TodoWrite in Claude Code) and tick off: context, platforms, extraction, draft, edit, visual, save, present. Skip it for a tiny one-off.

If the person points at earlier work ("the last post", "yesterday's draft", "my profile"), read `references/memory.md`, resolve `SOCIAL_WORKSPACE`, and read its `index.md` first.

Voice sources, first match wins, and load both profile and examples when both exist:
1. `SOCIAL_WORKSPACE/voice-profile.md` and `SOCIAL_WORKSPACE/voice-examples.md`.
2. The brand folder kept by brand-voice: `<brand>/brand/voice-profile.md` and `<brand>/brand/voice-examples.md`. Never guess the brand when more than one fits; ask.
3. For the user's personal brand: `<personal brand profile>` when posting as themselves.

No profile anywhere: in normal mode read `references/interview.md` and ask the smallest useful set. In quick mode draft from the input, state one temporary voice assumption if it shapes the draft, and never pretend a full profile exists.

Quick mode triggers: `quick`, `quick mode`, `just write`, `skip questions`, `no questions`, or anything that plainly means the same.

During reusable setup, ask where social work should live before writing any file (never create a default folder silently) and run the scheduler check in `references/scheduler-handoff.md`.

### 2. Resolve platforms

Read `references/platform-rules.md`, then only the platform files for the drafts requested.

- One platform named: one draft. Several named: one each. None named and the source does not clearly imply one: one short question.
- Off-pillar or off-audience idea: ask how it connects, or propose a bridge, before drafting.
- X Premium only when the person says they have it, the profile says so, or they ask for a long X post.
- Fan-out shares one source and one proof ledger, but each platform gets its own shape.

### 3. Extract or interview

Thin source and no quick mode: ask two or three questions that surface the reader and the reaction wanted, the proof or concrete example, and the platform and voice (`references/interview.md`).

Rich source: pull only what the post needs.
- Proof that can be used, with numbers, dates and timeframes.
- Named tools, products, people, examples.
- The person's own phrases, quotes, screenshots, charts, photos.
- Claims that need softening, and claims to leave out.

Writing samples or admired posts arrive: save them to the examples file only when the person wants reuse or they clearly matter later. They are voice evidence, never factual support for today's claim.

### 4. Decide on memory

Read `references/memory.md` when memory is in play. Write durable files only when the person asks to save, reuse, continue or build a profile; the run produces durable voice context; reusable examples or brand rules arrive; the proof will be repurposed; or the task depends on saved context. A one-off post stays a one-off. One packet per idea, even with several platform versions. Packet headings: Brief, Source Nuggets, Proof Ledger, Drafts, Visual Brief, Editing Pass, Revision Notes.

### 5. Draft

Read `references/drafting-guide.md`. Build the private proof ledger (claimable, qualified, illustrative, forbidden) and decide whether the post is text-led, artifact-led or generated-visual-led. When voice examples exist, run the Example Pass first. Then write one draft per requested platform.

- Hashtags only when the voice evidence or the brief supports them. Off by default.
- Emojis only when the voice evidence supports them.
- Profile bans, tone moves and formatting habits override the generic rules here, except where following them would create fake proof, engagement bait, or a platform break.

### 6. Edit

Read `references/editing-guide.md` and run the three checks. Go deeper (two real versions, keep the stronger) for high-stakes posts, long LinkedIn posts, real-voice emulation, weak first drafts, or when polish is requested. Keep the texture that makes the person's examples sound like them. Run `scripts/check_post.py post` on every final draft: it counts characters the way each platform does and flags dashes, hashtags, bait, banned phrases and limit breaks. Never report a character count that was not checked.

A saved packet gets an Editing Pass section with two to four concrete notes on what was actually checked or changed. Never claim an edit, a tightening or a reference read that did not happen.

### 7. Visuals and image generation

Read `references/visuals.md` when a visual might help or an image is requested.

- Pick the role before final copy: `none`, `raw-screenshot`, `annotated-screenshot`, `receipt-strip`, `chart`, `diagram`, `checklist`, `teardown-crop`, `stat-card`, `meme`, `lo-fi-photo`, `generated-scene`. Text-only is the default.
- A visual that carries proof shortens the post: the text interprets, it does not repeat.
- The best visual is a screenshot or receipt they have not supplied: issue a capture request (what to capture, what to blur). Never generate a fake screenshot, dashboard, receipt, testimonial or product state.
- A generated visual that helps: give a concept plus a JSON prompt seed (`templates/prompt-seed.json`, worked seeds in `templates/seeds/`) and validate it with `scripts/check_post.py seed`.
- Generation follows `references/image-generation.md`: consent gate, cost note, the optional image engine at `<image-engine>`, prompt-only fallback. Never print a key, never say where one was found, never claim an image that was not saved.

### 8. Present

Default: platform label, draft, checked character count, and the visual concept or seed when useful. Add proof, voice, editing or saved-packet notes only when they build trust, the topic is risky, or memory was used. For fan-out, one short line on how the shapes differ. No lab report of private steps.

### 9. Scheduler handoff

Read `references/scheduler-handoff.md` when a scheduler is installed, the profile opts in, or the person says "queue it", "schedule it", "post it", "save as drafts". Drafts only after approval, one scheduler draft per idea carrying every requested platform version, schedule or publish only on an explicit ask, and silence about queueing when no scheduler is installed.

## Hard gates

Do not present a final draft if any of these fail:

- Invented proof, metric, quote, customer, screenshot or result.
- A number or claim pinned to the wrong entity.
- A platform draft nobody asked for, or a requested platform missing.
- Voice profile or real examples ignored when they exist.
- Engagement bait: "Agree?", "Thoughts?", "Comment below", "Hope this helps", and relatives.
- A visual recommended on a text-only request, or a decorative visual that adds no proof, context, personality or scroll-stop value.
- An image claimed without a saved artifact, or generation attempted without a visible generation path plus a request or approval.
- A secret printed or copied anywhere.
- Fan-out versions that are only reworded copies of each other.
- Scheduler queueing before approval, or schedule or publish when only drafts were approved.
- A dash in the copy when the voice evidence does not use dashes.
- Questions asked in plain chat when the structured question tool is available.

## What to give this skill

- The idea, notes, transcript, article, screenshot or other source.
- The platforms: X, X Premium, Threads, LinkedIn, or a mix.
- Any voice examples, banned phrases, audience notes, proof, numbers or screenshots that must be used.
- Whether this is a one-off or reusable work to save.

Sensitive screenshots and receipts (profit-and-loss reports, order data, customer emails) get private details blurred before they are shared, or the person gets a capture brief telling them what to blur.

File: social-content/SKILL.md · Version 1.0.0 · November 2026
