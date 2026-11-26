---
name: linkedin-strategy
description: "Set up or refresh the LinkedIn strategy for one LinkedIn account in Zernio (<account>, or any LinkedIn account added later): interview for audience and ICP, goal, positioning, 3 to 5 pillars, funnel mix as role words (default 40/40/20), one lead magnet or newsletter ask, a recurring series, cadence (default 5, can be 2 to 3), posting zone and slot times with a role word for each slot, weekend slots only if wanted, keywords, positions, a proof bank and an off-limits list, and the three engagement lists, then give the candidate strategy text for the account strategy record in chat for a person to carry into the record. The strategy holds no voice block: voice and layout come from the Page records. The engagement lists stay on a page file that a person approves before it is written. Re-run monthly with the latest review notes. Profile mode scores a profile out of 100 with the video 095 fixes and gives fix-first rewrites. Holds the LinkedIn playbook every LinkedIn skill cites as a prior. Triggers on: LinkedIn strategy, set up LinkedIn for this account, strategy needed for, monthly LinkedIn review of strategy, score my LinkedIn profile, rewrite my headline, LinkedIn playbook. Not for writing posts (linkedin-post), the week's plan (linkedin-weekly-plan), comments (linkedin-engage), weekly results (linkedin-review) or the company voice profile (brand-voice). Outputs a candidate strategy text, a proposed engagement lists page awaiting approval, or a profile score with rewrites."
---

# LinkedIn strategy

Set the strategy for one LinkedIn account and give it as candidate text for the account's strategy
record, which every other LinkedIn skill reads. Each account has its own record. This skill writes
no record: a person carries the candidate text into the record file, and nothing the skill
produces is the strategy until that is done.

## References

| Need | Load |
|---|---|
| Every framework, number and source, as a prior | `references/linkedin-playbook.md` |
| The candidate text's fields and layout | `references/strategy-page-template.md` |
| Profile mode | `references/profile-rubric.md` |

The playbook is a prior, not an authority. Where the Page records differ from it, the records
govern.

## Records

Read each record from the file `./campaigns/linkedin/<record name>.md`.

| Need | Record name |
|---|---|
| The current strategy | `linkedin-account/<alias>/strategy` |
| The account | `linkedin-account/<alias>/accounts` |
| What the strategy may and may not set | `linkedin-page/voice-rules`, `linkedin-page/layout-rules`, `linkedin-page/claims-rules`, `linkedin-page/retained-gates` |
| The compliance marks | `[screening-rules]` |
| The content types | `linkedin-page/type-index` |
| The programmes | `linkedin-page/programmes` |
| Read floors for the monthly refresh | `linkedin-page/measure-floors` |

A name the folder does not hold is reported (list the files in `./campaigns/linkedin/`; a learn
record, when one exists, is listed there). When the strategy record is absent, the page file
`./campaigns/linkedin/<alias>/strategy.md` is read for its audience, pillars, positions and
off-limits topics only.

## Modes

- **Setup:** no strategy exists for the alias. Run the interview, then give the candidate text.
- **Monthly refresh:** a strategy exists. Read it and the last four review notes
  (the page files `./campaigns/linkedin/<alias>/review-<date>.md`, and
  the learn record when one exists). Ask only what the review evidence questions. Keep every section
  that does not change. Give the whole candidate text. Keep a cadence for at least a month before
  changing it (066).
- **Profile:** score a profile and give rewrites (see the profile reference).
- **List:** for each LinkedIn account in Zernio, say
  whether a strategy record or page exists and when it was last reviewed.

## Setup and refresh workflow

### 1. Load context

1. Confirm the alias against the LinkedIn accounts in Zernio. Only LinkedIn accounts.
2. Read the current strategy (record, else page file). Missing means setup mode.
3. Brand context, read per `_system/brand-memory.md`: positioning (`./brand/positioning.md`) and audience
   (`./brand/audience.md`). Read the facts ledger (`./campaigns/linkedin/facts-ledger.md`).
   The company voice profile (`./brand/voice-profile.md`) is not read for a Page strategy: the Page records set voice.
4. Load `references/strategy-page-template.md`. Load sections of the playbook as the interview needs
   them (section 3 for frameworks, section 10 for engagement, section 11 for the profile).

### 2. Interview

Ask in short batches, at most four questions a message, and offer a default the person can accept.
Prefill from `./brand/` where it already answers. The order follows the 6-step strategy (083):

1. **Audience:** ICP job titles, industries, company size, responsibilities; two audiences.
2. **Goal:** pipeline, credibility with buyers, investors, brand awareness or recruiting.
3. **Positioning:** the three things a reader should link to the account after about 10 posts, and
   the headline (who the account helps and how).
4. **Pillars:** three to five, each drawn from ICP pain, the account's expertise, the poster's
   passion, and how it ties back to ICP pain (066). Pull the two best stories (034).
5. **Funnel:** the mix as role words (default 40% reach, 40% positioning, 20% conversion); one lead
   magnet or newsletter ask; the conversion link; a recurring series (080 #8).
6. **Schedule:** cadence (default 5 a week; 2 to 3 is fine for some accounts); the audience's time
   zone and slot times, chosen for when the ICP is online and a person can reply for the first 90
   minutes (045); one role word for every slot; who is on duty; weekend slots only if wanted; the
   weekday template (076 by default, or 068, 047, 103).
7. **Keywords and positions:** 5 to 10 keywords to repeat across profile, posts and comments (021,
   042); three to five positions the account holds that some of the audience does not. Voice is not
   asked: for a company Page the voice record governs. For a personal account, note that its voice
   comes from its own record when one exists, and ask the person for the voice only to hold it
   until then.
8. **Engagement lists:** owned audience, mid-tier creators around 100K followers who still reply,
   and ICP accounts (042); the daily commenting budget. Names come from the person. Never scrape.
9. **Proof bank and off limits:** approved ledger entries the account may use, stories the poster
   will sign, topics and customers that are off limits.

Quick mode (`quick`, `just set it up`): fill every field from `./brand/` and the defaults, mark each
assumed field "(default)" or "(assumed)", and ask nothing.

### 3. Checks before giving the text

- No figure or customer in the proof bank unless the facts ledger or a claims record has it with
  status approved.
- Apply `[screening-rules]` to every pillar, story and
  engagement name: a reference it flags is marked as `[screening-rules]` states in the change
  summary, and the person is asked what it is for.
- An engagement list holds names and roles only, as the person gave them. No contact details.
- A pillar or series that `[screening-rules]` covers gets
  the review mark it names in the change summary.
- Nothing in the text sets a voice, a length, a link rule or a count of asks that differs from the
  Page records.

### 4. Show the candidate, then the engagement lists

Show the whole candidate text, with a short before and after (for a refresh: which sections change
and why; which stay at defaults). Say plainly that the text is a candidate: it is not the strategy
until a person carries it into the record `linkedin-account/<alias>/strategy`, and no skill writes
that record.

The engagement lists stay on a page file. Show the page, then write it only after a person approves it:

| Field | Value |
|---|---|
| `path` | `./campaigns/linkedin/<alias>/engagement-lists.md` |
| `markdown` | the lists page |
| `title` | `LinkedIn engagement lists: <alias>` |
| `change_summary` | the before and after, plus any flags |
| `expected_state` | `create` if the page was absent, `replace` if it existed |

If the person does not approve the page, say so plainly and hand
the lists over in chat. Do not work around it. Never propose a page write for the strategy
itself.

### 5. Report

```
CANDIDATE: linkedin-account/<alias>/strategy (text above, not yet a record)
ENGAGEMENT LISTS: ./campaigns/linkedin/<alias>/engagement-lists.md (approval pending | written | handed over in chat)
Defaults used: <fields>
Flags: <flags under `[screening-rules]`, or none>
Next: a person carries the candidate text into the strategy record, then linkedin-weekly-plan can plan for <alias>.
```

Never say the strategy is saved. Never say the lists page is saved before the approval is granted.

## What it never does

- Write the strategy record, write a page file for the strategy, or overwrite the voice profile
  (brand-voice owns it).
- Set or offer a voice block, a second-person setting, a contraction setting or a first-comment
  link practice for a company Page.
- Invent an audience, a number, a customer or a story.
- Add automation: no connection-request quotas, no auto-commenting, no scraping (playbook
  section 17).

File: linkedin-strategy/SKILL.md · Version 1.0 · November 2026
