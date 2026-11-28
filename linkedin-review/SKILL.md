---
name: linkedin-review
description: "Weekly results review for one LinkedIn account: rank the week's posts by engagement rate and reach multiple, not impressions; track comment ratio, saves, sends, long comments and profile visits when a person supplies them; find the best content type, angle, format, hook, length and media from the top and bottom posts; check whether the fifth post of the week was weak; apply the read windows and floors of the measure floors record (no read inside the 48-hour lag, no conclusion from one post, a role read only at three or more posts at 28 days); and propose the note ./campaigns/linkedin/<alias>/review-<date>.md for a person's approval, for the plan and the monthly strategy refresh to read. Zernio gives no saves or profile visits for LinkedIn, so those come from a person's paste. Do more of what works, less of what does not, and keep a cadence for a month before changing it. Triggers on: LinkedIn weekly review, how did our LinkedIn posts do, what is working on LinkedIn, LinkedIn post-mortem, review <account> this week. Not for changing the strategy (linkedin-strategy, which reads these notes monthly) or for site analytics. Outputs a ranked table, findings with confidence, STOP and DO MORE lines, and a proposed review note."
---

# LinkedIn review

This skill reads one account's results for the week and writes the note the next weekly plan follows. The
account's own posts are the evidence. Every rule in every LinkedIn guide, the playbook included, is
only a prior.

Adapted in part from the li-audit skill of `linkedin-agent-skill` by Jake Schincariol
(https://github.com/Jakeschincariol/linkedin-agent-skill), MIT licence, Copyright (c) 2026 Jake
Schincariol. Sources: the `linkedin-strategy` playbook reference, section 13 (videos 022, 066, 078,
083 and repo li-audit).

## Inputs

1. **Alias** and **week** (Monday to Sunday, the strategy's posting zone; with no week named, the
   last full week). Read the strategy
   (`./campaigns/linkedin/linkedin-account/<alias>/strategy.md`; when the
   file does not exist, the page file `./campaigns/linkedin/<alias>/strategy.md`) for the
   follower count if recorded, the cadence and the funnel mix. Read the record `./campaigns/linkedin/linkedin-page/measure-floors.md`
   for the read windows and floors; if the file
   does not exist, say so and apply only the lines of the Floors section.
2. **The week's posts:** the week's plan file and the draft files
   (`./campaigns/linkedin/<alias>/drafts/`) with status `posted`, for this account: body, hook
   number, role word, media and time. For a post saved with a content type, read its draft file
   for its content type,
   angle, plan slot and state.
3. **Numbers.** Ask a person
   to paste, per post: impressions, reactions, comments, reposts, and where LinkedIn shows them,
   saves, sends and profile visits; plus the follower count on the posting day. A screenshot per
   post is fine. Zernio analytics cover all company-page posts but only Zernio-sent posts on a
   personal profile, run up to 48 hours behind, and give **no saves and no profile visits for
   LinkedIn**: those always come from the person's paste. Say which source each figure has.
4. **Previous review notes** (the page files `./campaigns/linkedin/<alias>/review-<date>.md`) to compare against.

Never scrape LinkedIn for numbers.

## Measure

Show the working.

| Metric | How | What it tells |
|---|---|---|
| Engagement rate | (reactions + comments + reposts) / impressions | whether the post earned its reach |
| Comment ratio | comments / reactions | whether it started a conversation |
| Reach multiple | impressions / follower count | whether it travelled past the existing audience |
| Save and send rate | (saves + sends) / impressions, when pasted | the strongest single signal of future reach (021, 045) |
| Long comments | count of comments over about 15 words (a working threshold of this pack; the sources give none), when the thread is pasted | weighted far above likes (021, 045) |
| Profile visits | when pasted | whether posts drive interest in the account (022, 078) |
| First-hour replies | did the account reply within the hour | whether the reply routine ran (101) |

Rank by engagement rate and reach multiple, not by impressions. A post with 900 impressions and 40
comments beat one with 12,000 impressions and 6.

## Floors

Apply the measure floors record before any finding. Where its wording differs from the lines below,
the record governs.

- No read inside the lag window (48 hours after the post). A post inside it is listed as `too early`
  and is not ranked.
- No conclusion from one post. One post is an observation, and a finding needs the number of posts
  the record names.
- A role word (reach, positioning, conversion) is read only when the record's post count is met at
  28 days. Below it, say `below the floor` and carry nothing forward as a rule.
- A per-1,000-followers figure only when a followers read for the posting day was supplied.
- Clicks are attributed only for a link with its tags; an untagged link has no click figure.
- A recommendation to change the plan or a rule is a proposal for a named person to accept. This
  skill changes none.

## Find the pattern

Compare the top and bottom posts (top and bottom 5 from ten posts up; with fewer, the top two and
the bottom two) on, in this order:

1. Hook formula number.
2. Content type, angle and role word.
3. Format and media.
4. Length.
5. Topic or pillar.
6. First-hour replies.
7. Day and time, **last**, and only if nothing else explains the gap. It is rarely the cause.

Also check:

- **The fifth post:** with a cadence of 5, was the fifth post of the week the weakest? Say so when it
  was (li-plan's warning).
- **Funnel mix:** did the week match the strategy's mix?
- **Convert post:** link clicks are not in Zernio's LinkedIn data; report what the person pasted.

State each finding as a claim with its evidence and a confidence. One week of five posts is too few
to call a pattern: say "early signal" and carry it forward. Compare with the last four notes before
calling anything a trend.

## Rules for recommendations

- Do more of what works and less of what does not (022).
- Keep a cadence for at least a month before changing it (066). A cadence or schedule change goes to
  the monthly `linkedin-strategy` refresh, not the weekly plan.
- Never recommend automation, pods, connection quotas or scraping.

## The note

Propose `./campaigns/linkedin/<alias>/review-<YYYY-MM-DD>.md` (the Monday of the reviewed week).
Show it, then write it only after a person approves it:

| Field | Value |
|---|---|
| `path` | `./campaigns/linkedin/<alias>/review-<YYYY-MM-DD>.md` |
| `markdown` | the note below |
| `title` | `LinkedIn review: <alias>, week of <YYYY-MM-DD>` |
| `change_summary` | one line: the top finding and the STOP and DO MORE lines |
| `expected_state` | `create` (or `replace` if a note for that week exists) |

```markdown
# LinkedIn review: <alias>, week of <YYYY-MM-DD>

Posts: <n> of <cadence> planned. Followers: <n>. Numbers supplied by: <person paste | Zernio>.

## Ranked
| Post | Role word | Content type | Angle | Hook | Media | Length | Impr. | Eng. rate | Reach x | Comments/Reactions | Saves+sends | Profile visits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## What the data says
1. <claim>, evidence <...>, confidence <low | medium | high>.

## Fifth post
<weak | not weak | n/a>

## STOP
<one line>

## DO MORE
<one line>

## For the next plan
- <angle, hook or content type to repeat or drop, each marked early signal or above the floor>
```

Store post first lines and numbers only. Do not store commenter names or headlines in the note.

If the person does not approve the note, say so and hand the note over in chat. Never say the note is
saved before the approval is granted. Then tell the person the next `linkedin-weekly-plan` run and
the monthly `linkedin-strategy` refresh will read it once approved. The note stays a page file
because no agent tool writes a learn record; a person moves a finding into the learn record.

File: linkedin-review/SKILL.md · Version 1.0 · November 2026
