# Profile rubric

Profile mode of `linkedin-strategy`. A 100-point score merged with the video 095 fixes. Use it for a
personal profile; for a company page, score only the items that exist (headline or tagline, about,
featured, banner, logo, activity, contact) and say which were skipped.

Adapted from the li-profile skill and its rubric in
`linkedin-agent-skill` by Jake Schincariol
(https://github.com/Jakeschincariol/linkedin-agent-skill), MIT licence, Copyright (c) 2026 Jake
Schincariol. Merged with 095 (@aleckremins, 2026-10-22, https://www.instagram.com/reel/DezM_eKlCHm/).

## Input

A person pastes the headline, about section, current role, the last two experience entries, and
says whether there is a banner and a featured section. A screenshot of the top card is enough for a
first pass. Never log in to LinkedIn and never scrape the profile.

## The score

Score every item honestly. Most first-pass profiles land in the 30s and 40s. A generous score is
useless.

| Item | Points | Full marks (rubric) | 095 addition |
|---|---|---|---|
| headline | 12 | States who the account helps and what changes for them, carries one piece of proof, is not the job title, uses the 220 characters | The most important fix: it follows the person into every comment; role and value clearly stated |
| about_open | 10 | The first two lines (all that shows before "see more") name the reader's problem; no "passionate about", no third-person bio, no opening with the name | Treat the two or three visible lines as a hook: who is helped, their problem, how it is fixed |
| about_body | 10 | Problem, what is done, one number as proof, what to do next; under 1,400 characters | Lead with how others are helped, not the person; as many trust factors as possible, case studies especially |
| featured | 8 | Three items: best post, a proof asset, the way to make contact; nothing empty or stale | Two or three at most; one must be a way to make contact (book a call or the newsletter); the second a funding announcement or case study |
| banner | 6 | One line of positioning and one way to reach the person; not the default gradient or a stock skyline | A billboard: what the person does and who they help; text kept right or centre, because the photo covers the left |
| photo | 6 | Face fills about 60% of the frame, eyes visible, shot in the last two years, plain background | Friendly and approachable, with a smile; people decide whether to trust a face in a tenth of a second |
| current_role | 10 | One line of scope, then two or three outcome bullets with numbers | Kept up to date |
| experience_depth | 8 | Last two roles detailed, roles older than ten years one line each | Education kept up to date too |
| skills | 6 | Top three skills are the three to be hired for, and endorsed | |
| recommendations | 8 | At least three in the last two years, each naming an outcome | |
| activity | 10 | Posted or commented in the last seven days | |
| contact | 6 | Custom URL, a working email or booking link, the same handle as other platforms | |

**Adaptation (second person):** the rubric asks for an about body "written to one person in
second person". An organisation-wide rule for external material bars the second person, and the Page
voice record applies it to the company Page: write the about body in the first person or the third
person, addressed to the role ("For [role] who...").

**Featured conflict:** the rubric wants three items; 095 wants two or three at most. Score full
marks for two or three items when one is a way to make contact and one is proof.

## Rewrite order

Fix in descending order of points lost. The person pastes each section in, so do not rewrite
everything at once.

1. Headline: `{what the account does for whom} | {proof} | {how to start}`. Give three options. Not
   the job title, and not "Helping X do Y" as the first three words.
2. About, first two lines: who is helped and what changes.
3. About body: problem, what is done, one approved number, what to do next; under 1,400 characters.
4. Featured: two or three items, one a way to make contact.
5. Experience: one line of scope and two or three outcome bullets with approved numbers.
6. Banner: one sentence of positioning, one way to make contact, text right or centre.
7. Photo and banner are made by a person; give a brief, never a generated likeness.

Every rewrite goes through the humaniser gate (`linkedin-post`, `references/humanizer-gate.md`). Use
the account's keywords (the same words as the posts and comments, 021). Claims and numbers come only
from approved facts ledger entries.

## Output

```
PROFILE SCORE  <n>/100  (<alias>, <date>)
  headline            <n>/12   <why>
  about first lines   <n>/10   <why>
  ...
REWRITES (fix-first order, copy-ready)
  ...
RE-SCORE  <n>/100 (+<delta>). Remaining points need: <recommendations, a real banner, posting
history; none of which a rewrite can create>.
CHECK  Send the finished profile to a colleague for blunt feedback before changing it (095).
```

Nothing is saved to LinkedIn by this skill. The person pastes each section in. Record the score and
the open fixes in the strategy page's Profile section on the next proposal.

File: linkedin-strategy/references/profile-rubric.md · Version 1.0 · November 2026
