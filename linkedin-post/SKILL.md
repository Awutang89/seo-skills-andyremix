---
name: linkedin-post
description: "Write one LinkedIn feed post for one plan slot of a LinkedIn account, or for an idea a person gives. The post follows the Page records read by name from the records folder (voice rules, layout rules, claims rules, retained gates, [screening-rules], the content type record, link tags, the account strategy): one topic and a clear take, at least five hook variants from 21 formulas with three shown, a cold-reader body, one ask, British spelling, no hashtags, no second person, no contractions. Customer and result claims come only from approved claim rows or approved facts ledger entries; a missing figure becomes a bracketed placeholder. Writes one draft file carrying the content type, the angle, the plan slot and the review copy, keeps the text exactly as written, and reports the score and every flag as evidence. It never submits, schedules or files an approval: the checks, the review decision and the approval are a named person's acts on the draft file. Also covers the short answer-first LinkedIn article shape, posted by hand. Triggers on: write a LinkedIn post for <account>, write the Tuesday LinkedIn post, draft this slot, LinkedIn hook options, rewrite this LinkedIn post, short LinkedIn article. Not for a one-off post across X, Threads and LinkedIn at once (social-content), carousels, newsletters or a spread from one article (content-atomizer), hiring posts or comments and replies (linkedin-engage). Outputs three hook options, one saved draft and a receipt."
---

# LinkedIn post

Write one LinkedIn feed post that sounds like the account that will post it and stands only on
proof the company can publish. One slot, one idea, one ask. This skill drafts and saves. A person
checks, decides and approves.

The rules live in the Page records (files in `./campaigns/linkedin/`). Read them by name and follow them. Do not
copy a rule into the draft, the receipt or a note: a copy goes stale and the record does not.

Adapted in part from the li-post skill of the linkedin-agent-skill repository by Jake Schincariol
(https://github.com/Jakeschincariol/linkedin-agent-skill), MIT licence, Copyright (c) 2026 Jake
Schincariol.

## What it never does

- Post, publish, schedule or submit anything. There is no submit step here and no call to
  Zernio to submit or schedule. Approval is filed by a named person at the
  approve step, after the review decision on the draft file.
- File the approval to post.
- Invent or default a post date or time.
- Invent a number, customer, quote, result, screenshot or story. A missing figure becomes a
  bracketed placeholder such as `[figure to confirm]` and is named in the receipt.
- Remove, replace or hide any character in the text, or claim the draft passes or evades an AI
  detector. The text is saved exactly as written.
- Put a compliance mark, flag or note in `body`.

## Records

Read each record from the file `./campaigns/linkedin/<record name>.md`.

| Need | Record name |
|---|---|
| Voice | `./brand/voice-profile.md` (read per `_system/brand-memory.md`) |
| Layout and length | `linkedin-page/layout-rules` |
| What a post may claim | `linkedin-page/claims-rules`, and the claims record the type record names (`linkedin-page/claims/<programme>`) |
| Gates that hold a post | `linkedin-page/retained-gates` |
| Compliance screen and marks | `[screening-rules]` |
| Held and lifted wording | `[fence-list]` |
| The content type | `linkedin-page/type-index`, then `linkedin-page/type-<content type id>` |
| Link tags | `linkedin-page/utm-scheme` |
| Visuals | `linkedin-page/visual-spec` |
| Overrides of the playbook | `linkedin-page/playbook` |
| The account | `linkedin-account/<alias>/accounts` and `linkedin-account/<alias>/strategy` |

A name the folder does not hold is not an error to hide. List the names (the files in
`./campaigns/linkedin/`), say which record is missing in the receipt, and carry on without it, except for the
strategy: when `linkedin-account/<alias>/strategy` is absent, read the strategy page
`./campaigns/linkedin/<alias>/strategy.md` for audience, pillars, positions and off-limits topics
only. Its voice block, second person setting, contraction setting, link rule and length rule are not
read. If neither exists, say so, offer `linkedin-strategy`, and stop unless the person asks for a
one-off draft.

A personal account (a person's own alias) has no voice record yet. Ask the person for the voice,
state the assumption in the receipt, and apply every rule of the voice and layout records that rests
on an organisation-wide rule.

## References

| Need | Load |
|---|---|
| The 21 hook formulas and hook craft | `references/hooks.md` |
| The self-check list, structures by type, media matching | `references/post-checklists.md` |
| The AI-pattern checks and the score | `references/humanizer-gate.md` |
| Source detail, as a prior only | `linkedin-strategy/references/linkedin-playbook.md` |

If a reference does not load, say so. Do not claim the step ran. Where a reference and a record
differ, the record governs.

---

## Workflow

### 1. Load the account and the records

1. Find the alias: from the plan slot, the request, or the LinkedIn accounts in Zernio
   (LinkedIn accounts only). If unclear, ask.
2. Read the account records and every record in the table that the post needs. Write down each
   record's name and version.

### 2. Fix the slot

1. The plan slot id. A slot of an accepted plan: take the date of the request's day (the coming
   Tuesday, say, stated in the receipt as a date), find that week's Monday, and read the week's plan file
   `./campaigns/linkedin/<alias>/plan-<Monday>.md`, with the Monday as `YYYY-MM-DD`;
   the id has the form `<programme>:<year>-W<week>:<n>`. Use a slot only from an accepted
   version; a proposed one is shown and not used. A one-off request, or a day the plan has no
   slot for: `adhoc:<alias>:<YYYY-MM-DD>:<n>`.
2. The content type id, from the slot or the request, checked against `linkedin-page/type-index`.
   A type the index marks as not founded is not drafted: say so and stop.
3. The angle (the bank type name the slot carries, or the one the person chose), the funnel role
   word, the audience, and the day and time the slot names (for the receipt only).
4. If the angle is not a real event, result or opinion the account holds, it is not a post yet.
   Attended (a person is in the chat): ask one batched question (what happened, to whom, with what
   result). Unattended: save nothing for that slot and report it as `needs input` with the
   question. A new feature named in a request still needs its facts from the person or an approved
   claim row before it is drafted.

### 3. Topic and take

One topic, one clear take, framed for the audience the strategy names. Decide what the reader should
believe after reading, and what does not belong in the post. Read the type record for its shape, its
required checks and what the type must not do.

### 4. Hooks

Load `references/hooks.md`. Write at least five hook variants from different formulas that fit the
angle. Choose three to show and name the one to ship, with one sentence of why. The first line
follows the layout record.

### 5. Body

Hook, context, substance, takeaway, written for a cold reader, in the shape the type record gives.
Voice, layout, length, links and the ask follow the records. The company speaks as the company:
no second person, no contractions, no hashtags, no emoji, British spelling.

Claims:

- A customer name, customer result, metric or product fact appears only when an approved row of the
  claims record, or an approved entry of the facts ledger (`./campaigns/linkedin/facts-ledger.md`),
  supports it. State the support in the receipt.
- A needed figure the sources lack becomes a bracketed placeholder, never an invented number, and
  never a word addressed to the reader.
- Apply `[screening-rules]`: each mark it calls for goes on its own line in the review
  copy (step 8), never in `body`. Ask what a flagged reference is for before keeping it.
- A post that names a customer, deal partner or party the retained gates record covers is held for
  a named person's decision on the draft file; say so in the receipt.

### 6. Link and media

The link and its tags follow the layout record and `linkedin-page/utm-scheme`; the type record says
whether the type carries one. Pick media from the matching table in `references/post-checklists.md`
and the visual record. A person supplies photographs and screenshots: write the capture request
(what to capture, what to blur). Never claim an image exists.

### 7. Self-check and the score

Run the self-check in `references/post-checklists.md` and the written checks in
`references/humanizer-gate.md`. Fix what fails by hand. The optional score run scores the text exactly as written;
the score and every flag are evidence for the approver, not a gate, and no step chases a passing
score.

### 8. Save

Write the draft file `./campaigns/linkedin/<alias>/drafts/<slot id>.md` (colons in the slot id become hyphens) with these fields:

| Field | Value |
|---|---|
| `source_ref` | the article's path or URL when the post comes from a published article; otherwise the strategy record name `linkedin-account/<alias>/strategy` (or the strategy page path when only the page exists), with `#angle=<angle name>;bank=<bank>` appended when a plan slot names them |
| `channel` | `linkedin` |
| `format` | `single` (a document post follows its type record) |
| `account` | the alias |
| `body` | the text exactly as it should be published, with no mark, flag or note |
| `review_copy` | the same text with the compliance mark lines the screen called for, each on its own line; leave the field out when there are none |
| `link` | the one link the layout and type records allow, with its tags; otherwise none |
| `content_type` | the content type id |
| `angle` | the angle name |
| `plan_slot` | the slot id of step 2 |
| `replaces_draft_id` | on a rewrite of this slot's own earlier unsubmitted draft: its id |

Read the score run's result. The `humaniser` entry holds the score, the verdict, the checks, the structural
tells and `found`: the invisible and typographic items left in place. Report each of them in the
receipt. Fix a found item or a flagged structure by editing the text and saving once more with
`replaces_draft_id`, at most one rewrite for a score. Read `replaces` in the result: a refused entry
(the old draft was submitted, scheduled, sent or is on another account) is left as it is and
reported, not retried. A refusal that names a secret or personal data is a stop: nothing was stored,
remove the item and save again.

Then read the draft file back. Report
its content hash and the state of each stage cell as returned. Do not describe a stage as done that
the read shows as pending.

### 9. Hand over

Say plainly: the draft is saved as draft `#<id>`, with the record state read back. The checks, the
review decision and the approval are a named person's acts, on the draft file.
Nothing is submitted, scheduled or posted. A post for an accepted plan slot is written on a
person's request, one slot at a time, and ends the same way.

### 10. Receipt

```
HOOKS
1. #<n> <name>   <hook>
2. #<n> <name>   <hook>
3. #<n> <name>   <hook>
Shipping #<n>: <one sentence why>.

POST
<the draft as saved>

RECEIPT
account:     <alias>
slot:        <slot id>, <content type id>, angle <angle name> (bank <id>), <Day DD Mon HH:mm zone | none>
length:      <counted> characters
link:        none | <url with tags>
media:       <type>, capture request: <what, what to blur>
self-check:  <n> of <n> pass, flags: <list>
score:       <human_score> <verdict>, weakest <check> <score>; tells: <list> | none; found and left in place: <list> | none; saves: <n>; superseded draft ids: <ids> | none | not scored: <error>
claims:      <each figure or name and its claim row or ledger entry> | none
placeholders: <where> | none
compliance:  <marks and flags, or none>
records:     <name, version> for each record read; missing: <names> | none
saved:       draft #<id>; record state <as read back>
next:        a named person runs the checks and records the review decision on the draft file; nothing is submitted
```

When the post names a customer or a result, the receipt also carries this line:

`<the review mark that [screening-rules] names for customer data in public posts>`

Compliance marks and flags go in the receipt and the review copy only, never in `body`.

---

## The short LinkedIn article shape

A separate shape, mainly for the company Page.

- Under 330 words. The answer to one query in the first line. A searchable title that names the
  query.
- The same voice, spelling and claim rules as a post.
- Zernio sends only single-body posts and PDF carousels, so a person publishes the article by hand.
  Do not write it as a draft file. Give it in chat, labelled, with a one-line note that it
  is posted by hand.
- A longer article or newsletter has no fixed length and belongs to `content-atomizer`.

## Hold, never save

Do not save a draft when any of these is true:

- It carries an invented claim, number, customer, quote or screenshot.
- It names the reader in the second person.
- It holds a secret or personal data.
- A reference that `[screening-rules]` flags and the person has not explained is in it.
- It claims that this skill posted, approved or submitted it.

A draft with a placeholder, a needs-input gap, a claim without support or an open compliance flag is
saved, because saving is never refused for a flag, and the receipt names what a person must settle
before the review decision.

File: linkedin-post/SKILL.md · Version 1.0 · November 2026
