# Strategy text template

The candidate text `linkedin-strategy` gives for the account strategy record
`linkedin-account/<alias>/strategy`, one per LinkedIn account in Zernio. `linkedin-weekly-plan`,
`linkedin-post`, `linkedin-engage` and `linkedin-review` read the record. The skill gives the
candidate in chat; a person carries it into the record. Fields marked (default) take the default
when the interview gives no answer; say so with the candidate.

The strategy holds no voice block. Voice and layout are set by the Page records (voice rules and
layout rules), and a personal account's voice is set by its own record when one exists. The strategy
holds what the account chooses: audience, goal, positioning, pillars, funnel, schedule, keywords and
positions.

Sources for each field are in `references/linkedin-playbook.md`: audience and goal (083), positioning
(083, 034), pillars (066, 034), funnel (066, 068, 080 #8, 034), schedule (045, 066, li-plan),
keywords (021, 042, repo voice.md), proof bank and off limits (repo voice.md). The engagement lists
(042) are kept on their own page file, `./campaigns/linkedin/<alias>/engagement-lists.md`.

Adapted in part from `templates/voice.md` in `linkedin-agent-skill` by Jake Schincariol
(https://github.com/Jakeschincariol/linkedin-agent-skill), MIT licence, Copyright (c) 2026 Jake
Schincariol.

```markdown
# LinkedIn strategy: <alias>

Last reviewed: <YYYY-MM-DD>. Next review: <YYYY-MM-DD, one month on>.
Account: <alias> (<company page | personal profile of NAME>), Zernio account alias <alias>.

## Audience
- ICP: <job titles>; <industries>; <company size or headcount>; <responsibilities>.
- Audience 1: <who, what they care about, current versus desired state, pain points>.
- Audience 2: <who, same fields>.

## Goal
<one of: pipeline | credibility with buyers | investors | brand awareness | recruiting>, with a
one-line reason.

## Positioning
- Three things a reader links to this account after about 10 posts:
  1. <...>
  2. <...>
  3. <...>
- Headline (who the account helps and how): <...>

## Pillars
| Pillar | ICP pain | Our expertise | Passion | Ties back to |
|---|---|---|---|---|
| <3 to 5 rows> | | | | |

## Funnel
- Mix as role words: reach <40>% / positioning <40>% / conversion <20>% (default 40/40/20; trust
  is positioning and convert is conversion).
- Lead magnet or newsletter CTA (one): <name, what it is, where it lives>.
- Conversion link: <url> | none yet. The layout and content type records decide where a link may
  sit.
- Recurring series: <name, format, cadence> | none yet.

## Schedule
- Cadence: <n> posts a week (default 5; 2 to 3 is allowed).
- Posting zone: <IANA zone of the audience>.
- Slots: <Mon HH:mm role word, Tue HH:mm role word, ...> (weekend slots only if listed here).
  Every slot names one role word.
- Weekday template: <076 perfect week (default) | 068 TMBTT | 047 Send & Sell | 103 Plan a month>.
- On duty for the first 90 minutes: <person or role per slot>.
- Daily cap: <n> posts per day in the posting zone (default 1).

## Keywords and positions
- Account kind: <company Page | personal profile>. A company Page takes its voice from the Page
  voice record; a personal profile's voice comes from its own record, when one exists.
- Keywords to repeat across profile, posts and comments: <5 to 10>.
- Positions the account holds that some of the audience does not: <3 to 5>.
- Daily commenting budget: <minutes or count> (the lists themselves are on the engagement lists
  page).

## Proof bank
Approved facts ledger entries this account may use, with their ledger reference. Stories and
numbers the poster is happy to sign. Empty means drafts carry a bracketed placeholder.
- <claim> (ledger: <ref>, status approved)

## Off limits
- Topics: <...>.
- Customers or numbers that cannot be named: <...>.
- Claims not allowed: <...>.

## Profile
Last profile score: <n>/100 on <date> | not scored. Open fixes: <list>.

## Change log
- <YYYY-MM-DD>: <what changed and why>.
```

File: linkedin-strategy/references/strategy-page-template.md · Version 1.0 · November 2026
