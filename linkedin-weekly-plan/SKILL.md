---
name: linkedin-weekly-plan
description: "Plan next week's LinkedIn posts for one LinkedIn account by writing a plan version to the plan file, and nothing else. It reads the week's plan state, takes the week's team input (company events, numbers that may be shared, sales-call objections and questions, approved customer outcomes, news links) from a person in an attended run, and writes one proposed plan version to the plan file, with the slots built from the accepted ideas and the calendar under the cadence rules. It shows the version: slots, rule results, programme balance and the engagement targets. It drafts no post, saves no draft, sets no time, submits nothing and accepts nothing: a named person accepts, adjusts, returns or skips the version in the plan file, and each post of an accepted slot is then written by linkedin-post on request. A week that already has an accepted or skipped version is not planned again. Triggers on: plan the LinkedIn week, weekly LinkedIn plan for <account>, next week on <account>, what should we post on LinkedIn, LinkedIn content calendar. Not for setting the strategy (linkedin-strategy), a single post (linkedin-post) or posts from one article (content-atomizer). Outputs the plan version table with a FLAGS column, the rule results, needs-input questions and engagement targets."
---

# LinkedIn weekly plan

Plan one account's LinkedIn week by writing a plan version. This skill builds the slots, a
person decides the version, and `linkedin-post` writes a post for a slot only after the version is
accepted and a person asks. This skill drafts nothing.

Adapted in part from the li-plan skill of the linkedin-agent-skill repository by Jake Schincariol
(https://github.com/Jakeschincariol/linkedin-agent-skill), MIT licence, Copyright (c) 2026 Jake
Schincariol.

## What it never does

- Draft, save, schedule or submit a post. No draft file, no schedule or submit step in Zernio,
  and no call to `linkedin-post` from inside a plan run.
- Accept, adjust, return or skip a plan version. Those are a named person's acts.
- Edit a plan version. A version is written once; a change is a new version a person makes with the
  adjust action.
- File the approval to post.
- Invent an event, a result, a customer or a number to fill a slot.
- Fetch news. A news take uses only a link the person supplied this week.
- Plan comments for posting by the agent. Engagement targets are a list for a person.
- Plan around a screened reference without a flag: `[screening-rules]` decides
  what is flagged, and the flag is shown in the FLAGS column.

## Records and references

Read each record from the file `./campaigns/linkedin/<record name>.md`.

| Need | Source |
|---|---|
| The account's cadence, slot times, pillars, funnel mix and positions | `linkedin-account/<alias>/strategy`; when that file does not exist, the page file `./campaigns/linkedin/<alias>/strategy.md` for those fields only |
| The programmes in the plan | `linkedin-page/programmes`, when the file exists |
| Which content types are founded | `linkedin-page/type-index` |
| Read windows and floors | `linkedin-page/measure-floors` |
| The last review note | the newest `./campaigns/linkedin/<alias>/review-<date>.md`, and the learn record when one exists |
| Angle names (background) | `references/post-type-bank.md` and `references/weekday-templates.md`, only to name an angle when a person asks |

A name the store does not hold is reported, not hidden.

---

## Workflow

### 1. Inputs

1. **Alias:** from the request, or ask. Confirm it is a LinkedIn account in Zernio.
2. **Week:** the Monday of the week to plan, as `YYYY-MM-DD`. The default is next Monday. A date
   that is not a Monday is refused.
3. **Strategy and last review:** read as the table says. No strategy anywhere: say "Strategy needed
   for <alias>. Run linkedin-strategy first." and write nothing.
4. **The week's state:** the plan file
   `./campaigns/linkedin/<alias>/plan-<Monday>.md`. Read `situation`, `runs` and `versions`. The `situation` says
   whether the week has no plan because none was generated, generation failed, or there were no
   ideas. Stop here, report the state and the next action, and skip step 5 and step 2 when:
   - the week has an accepted or skipped version (a person adjusts it, and that writes a new
     version);
   - the week has a proposed version that is not returned: show it as step 3 does and ask whether
     a person wants a new one; write none unprompted.
5. **The week's input.** An attended run (a person is in the chat) asks one batched message and
   waits for the reply before step 2:
   - real company events this week (shipped, decided, hired, a milestone, a mistake);
   - numbers that may be shared;
   - objections and questions heard on sales calls;
   - customer outcomes, from approved claim rows or the approved facts ledger only;
   - news links, each with its date, for a news slot.

   Team input is what the person gives. Brand files, published articles and the strategy are
   background and never count as team input. This skill cannot file ideas: ideas are filed and
   accepted by people in the plan file. Tell the person which of their replies still need to be
   filed as ideas before the plan can use them, and generate only after the person says they are
   filed or says to plan from the ideas already accepted. An unattended run (no person in the
   chat) asks nothing and uses what the accepted ideas already hold.

### 2. Write the plan version

When the week has no version, or its latest version was returned, and the `situation` is not
`no accepted ideas` (that state ends the run: report it and ask the person to accept ideas in the
plan file), build
one proposed version and a
run row from the accepted ideas and the calendar under the cadence rules, and write both to the plan file. The run accepts nothing, files no approval and schedules
no post. Do this once for a week; a second run only adds a proposal. Report the run result:
`generated`, or the reason it did not generate. A failed generation is reported with its
reason and is not retried in the same run.

Then read the plan file again and read the new version: its id, version number, hash,
`created_by`, `slots`, `rules_result` and `programme_balance`.

### 3. Show the version

Show the person the version in one message, as stored. Every figure is read from the version, never
recomputed.

```
LINKEDIN WEEK  <alias>  week of <Monday DD Mon>  (<zone>)
Plan version #<id>, v<n>, hash <first 12 characters>, state <state>, written by <created_by>
Strategy: <record version | page file, date>   Review applied: <date | none>
Cadence rules: <each rule result as returned: ok or flag, with its text>
Programme balance: <as returned>

DAY  TIME   PROGRAMME       CONTENT TYPE     ANGLE          SLOT ID                 FLAGS
...
NEEDS INPUT
<slot or idea>: <the one question that would unblock it>

ENGAGEMENT
Replies: <person on duty> within 1 hour of each post (first 15 minutes most).
Comments: <budget from the strategy> a day; this week's names: <owned>, <mid-tier>, <ICP>.

NEXT
A named person accepts, adjusts, returns or skips version #<id> in the plan file. Nothing is
drafted, scheduled or submitted. After acceptance, ask linkedin-post for any slot's post.
```

Compliance and `[screening-rules]` flags the version carries are shown by slot in the FLAGS column,
with the mark as the version states it. Do not add an angle or a content type the version does not
carry.

### 4. Engagement targets

From the engagement lists page `./campaigns/linkedin/<alias>/engagement-lists.md` (the strategy
page when that page does not exist yet), the strategy's zone, person on duty and daily budget:

- **Replies:** on each post day, the person on duty replies to every comment within the first hour,
  the first 15 minutes most (101). `linkedin-engage` drafts the replies from a paste.
- **Comments:** a daily budget from the strategy, spread across the owned audience, mid-tier
  creators and ICP accounts, about 1.5 hours before and 1 hour after the account's own post (042).
  Do not list the same three people every day.
- **Pick about 10 names for the week** from the lists (the person can swap them). Names only.

### 5. After acceptance

When a person says a version is accepted and asks for a slot's post, run `linkedin-post` for that
one slot, passing the slot id, the content type and the angle from the version. It saves one typed
draft and stops. Never run it for a slot of a version that is not accepted.

---

## Output when nothing is written

A week that already holds an accepted or skipped version, a missing strategy, a refused date, or a
`situation` that says there are no accepted ideas each end with the stated reason and the question or
action a person must take. Write nothing in those cases. A needs-input line in the version table
comes only from the version itself or from a reply the person gave; never from a guess.

File: linkedin-weekly-plan/SKILL.md · Version 1.0 · November 2026
