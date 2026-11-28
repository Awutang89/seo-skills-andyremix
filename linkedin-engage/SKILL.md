---
name: linkedin-engage
description: "Draft LinkedIn replies and comments for a person to post by hand, for one LinkedIn account, in the voice the Page voice rules record sets (the content type is engagement-reply, draft only, never saved or sent by any tool). Reply mode sorts the comments a person pastes from under the account's own post into lead, substance, peer, support and noise, and drafts replies in that order, each answering with a question rather than thanks, aimed at the first hour and the first 15 minutes. Comment mode drafts two comments of different types (nine types plus Anchor, Add, Ask) on another person's post that someone pastes, written as mini-posts with the account's keywords where natural, never a pitch, and plans the daily round from the three engagement lists with timing about 1.5 hours before and 1 hour after the account's own post. Drafts only: never posts, never saves a draft, never automates, never scrapes LinkedIn. Triggers on: reply to these LinkedIn comments, handle the comments on our post, comment on this LinkedIn post, draft LinkedIn comments, engagement round, who should we comment on today. Not for writing posts (linkedin-post) or DMs and connection notes (deferred). Outputs triaged reply drafts or two labelled comment options, each through the writing checks."
---

# LinkedIn engage

This skill drafts replies and comments. A person reads, edits and posts every one of them by hand. The
first hour of replies decides much of a post's reach, and a comment on the right post can reach more
people than the account's own post. A generic one costs credibility.

Adapted in part from the li-comment and li-reply skills of `linkedin-agent-skill` by Jake
Schincariol (https://github.com/Jakeschincariol/linkedin-agent-skill), MIT licence, Copyright (c)
2026 Jake Schincariol. Sources for every rule: the `linkedin-strategy` playbook reference, section
10 (videos 021, 030, 042, 045, 065, 101).

## What it never does

- Post, like, connect or send anything. No browser automation, no auto-commenting, no auto-replies.
  Automated commenting and posting break LinkedIn's User Agreement.
- Scrape LinkedIn or open a LinkedIn URL to read a post or a thread. A person pastes the text (or a
  screenshot). If only a URL is given, ask for the text.
- Pitch in a comment. Send a person to a DM for an answer that fits in the reply.
- Keep commenter details beyond what the draft needs. Names and headlines of LinkedIn users are
  personal data: use them in the draft, do not save them to any file or page.
- Write a connection note or DM. Those are deferred (Zernio reports that LinkedIn blocks
  third-party DM access).
- Save a draft file. A reply or comment is copy for a person to post, and the
  record holds it only if a person registers it later.
- Use the second person for a company Page, or a contraction. The voice rules record applies to
  every reply and comment the Page gives.

## Before either mode

1. Find the account alias from the request; ask if it is unclear. Read the voice rules (`./brand/voice-profile.md`, read per `_system/brand-memory.md`)
   and the strategy (`./campaigns/linkedin/linkedin-account/<alias>/strategy.md`;
   when that file does not exist, the page file `./campaigns/linkedin/<alias>/strategy.md` for
   keywords and positions only). Read the engagement lists page
   `./campaigns/linkedin/<alias>/engagement-lists.md` for the three lists, or the strategy page
   when that page does not exist yet. For a personal account no voice record exists: ask the person
   for the voice and state the assumption. For the company Page the voice rules record governs
   everything below.
2. Load the writing checks: `linkedin-post/references/humanizer-gate.md`. Every draft goes through them.

"Write them yourself. generated comments are obvious and they undo the whole thing" (101). The
person's own notes make the draft theirs: ask for one line of what they think about the post when
the paste gives nothing to anchor on, and keep their words.

---

## Reply mode (comments under the account's own post)

### 1. Triage

Sort every pasted comment and say the counts.

| Bucket | What it is | What it gets |
|---|---|---|
| LEAD | someone describing the problem the account solves | a real answer in public and a one-sentence open door that offers help, not a pitch |
| SUBSTANCE | adds data, disagrees, extends | the longest reply on the thread |
| PEER | a name worth being seen next to | a reply that gives them something |
| SUPPORT | "great post", an emoji, a tag | a like by the person, and a reply of 3 to 8 words at most, to the first few |
| NOISE | a pitch, spam, bad faith | nothing; replying gives it reach |

Write in that order and stop when the value stops.

### 2. Reply rules

- Ask a question that keeps the thread going instead of only saying thanks (101).
- Answer the actual question in the reply.
- Use the commenter's name once, at the start, never with an exclamation mark.
- Match their length.
- To a critic: concede the true part first, in their words, then hold the line. Never delete, never
  get defensive, never reply twice on one thread.
- No claims beyond the facts ledger (`./campaigns/linkedin/facts-ledger.md`) and the claims rules
  record (`./campaigns/linkedin/linkedin-page/claims-rules.md`). No customer names unless the
  retained gates record allows them.
- Timing: the person on duty posts the replies within the first hour, the first 15 minutes most
  (101, 045).

### 3. Output

```
REPLIES  <alias>  post: <first line>  <n> comments: <n> LEAD, <n> SUBSTANCE, <n> PEER, <n> SUPPORT, <n> NOISE

LEAD
<commenter> - "<their point, short>"
> <reply draft>

SUBSTANCE
...
SUPPORT (like these; reply to the first three)
...
NOISE (<n>) skipped: <why>

Post these by hand within the first hour. Nothing was posted.
```

No company-page comment reading exists yet, so every comment is pasted in and every reply is
posted by hand.

---

## Comment mode (another person's post)

### 1. Pick two types

Pick by what the post actually is. Never default to type 9.

| # | Type | When | Shape |
|---|---|---|---|
| 1 | Add a datum | the post makes a claim an approved number supports | "[company] measured the same thing: {approved figure}..." (an approved figure only; the company speaks as the company) |
| 2 | Add the missing case | right but incomplete | "This holds until {condition}. Then..." |
| 3 | Respectful disagree | genuinely wrong | the real agreement first, then the fork |
| 4 | Extend one line | one sentence is the good one | quote it, then build on it |
| 5 | Ask the real question | the post skipped the hard part | one specific question |
| 6 | The receipt | the account has done the thing | what happened, in two sentences |
| 7 | The correction | a factual error | right, brief, kind, sure |
| 8 | The reframe | right facts, wrong frame | "Another way to read this:" |
| 9 | The one-liner | presence only | under 12 words, funny or true |

Every comment also follows **AAA** (101): **Anchor** on a specific line of their post, **Add**
something they did not say, **Ask** a question. A comment is a mini-post (030): an example, an
anecdote, a counterpoint, a framework or an experience that adds to the conversation.

### 2. Comment rules

- 2 to 4 sentences. Longer reads as a hijack; shorter reads as filler. One idea.
- Never open with "Great post", "Love this", "So true", "Couldn't agree more", "This resonates", or
  the author's first name with an exclamation mark. No emoji opener.
- Never restate the post. Say the specific thing: if the comment could sit under any post on the
  topic, it is noise.
- Use one of the account's keywords where it reads naturally; sounding natural comes first (042).
- No pitch, no link, no offer.
- Claims follow the facts ledger. Apply `[screening-rules]`:
  mark a reference it flags as `[screening-rules]` states, and ask what it is for.
- Company voice: no second person, no contractions, no emoji, British spelling.

### 3. Output

```
COMMENT OPTIONS  <alias>  on <author>'s post about <topic>

[<type number> <type name>]
<comment>

[<type number> <type name>]
<comment>

Post the first: <one-line reason>. Nothing was posted.
```

### Daily round

When asked who to comment on, plan from the strategy's three lists:

- **Owned audience:** people who engage within the first 90 minutes and are online when the account
  posts.
- **Mid-tier creators:** around 100K followers who still reply to comments. Comment early, before
  the post has about 20 comments, or nobody sees it.
- **ICP accounts:** buyers active at the right time. Comment for weeks before any connection
  request; never pitch.
- **Timing:** about 1.5 hours before and 1 hour after the account's own post (042).
- **Budget:** the strategy's daily figure. The sources range from 3 to 5 comments twice a day (030)
  to 20 to 30 a day (065) and about 50 a day (042); 101 suggests 10 to 15 minutes. The strategy
  decides.
- **Rotation:** keep a note in the chat of who was commented on this week, and do not suggest the
  same three people every day.

The person pastes each target post into this mode for the drafts. The lists live on the engagement
lists page.

### Turning commenters into connections

After a few days or weeks of exchanges, a person may send a personalised connection request with no
pitch and something useful in it (101). The person writes and sends it. This skill does not draft
connection notes yet.

File: linkedin-engage/SKILL.md · Version 1.0 · November 2026
