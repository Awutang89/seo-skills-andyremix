---
name: google-ads-optimize
version: 1.0
description: >
  Diagnoses an underperforming Google Ads campaign, ad group or ad with causal evidence, then
  drafts concrete changes for human sign-off. Changes cover RSA headline and description
  alternatives in brand voice, asset coverage, budget shifts and pause candidates. Outputs
  recommendation entries with explicit IDs and readable before and after diffs, and never touches
  the account. Triggers on: this ad is not performing, improve the ads, change the headline,
  optimize campaigns, budget recommendations, write new ad copy. Not for: a whole-account audit
  (google-ads-audit), anomaly checks (google-ads-monitor), new campaigns (google-ads-create).
---

# Google Ads Optimize

Optimization is a diagnosis with a proposed change attached. A fixed CPA multiple, a budget ratio
or a benchmark is never, on its own, authorization to change an account. A recommendation earns
its place by naming the causal evidence and what "better" will measurably look like.

**Operating contract (binding):**

- **Recommendations only.** Add every proposed change to the recommendation log,
  `./campaigns/google-ads/recommendations.md`. Each entry carries an entry number, the date,
  `source: google-ads-optimize`, a `kind`
  (budget, headline, pause, keyword or other) and explicit resource IDs. The IDs are the customer
  ID, campaign ID, ad group ID and ad ID. The entry also holds a readable before → after diff.
- **One key per change.** Give each entry a key built the same way every time from the target IDs
  and the change. Before adding an entry, search the log for its key. A re-run then cannot file the
  same change twice.
- **Approval is a human act.** A named approver accepts or rejects each entry. Applying an accepted
  change is a separate step: a person makes it in the Google Ads web interface or Google Ads
  Editor. This skill sends no change to the Google Ads API. Its API use is read-only.
- **Nothing destructive, ever.** No deleting campaigns, ad groups, ads, audiences or conversion
  actions. Pausing is the strongest change this skill proposes, and only with evidence.
- **Three options, always considered:** keep as is (the default), test (the evidence is suggestive
  but not conclusive) or change (the evidence is causal). The memo says which one won and why the
  other two lost.
- **Negative keywords** need a search terms report, a business relevance review and an overblocking
  check. If any of the three is missing, withhold the recommendation and say in the memo what is
  missing. This rule covers existing campaigns. A new campaign's negatives follow `google-ads-create`.

**Keys:** Google Ads API access needs a developer token (`GOOGLE_ADS_DEVELOPER_TOKEN`) and OAuth
credentials in the form the client library expects. An account reached through a manager account
also needs `GOOGLE_ADS_LOGIN_CUSTOMER_ID`. Keep them in the environment or in `.env` (see `.env.example`).
Never ask for a key in chat. Without API access, work from report downloads out of the Google Ads
web interface.

## Data

- **Performance** at campaign and ad group level, and per ad where available. Use the GAQL report
  queries in `google-ads-audit/SKILL.md` or the same reports from the Google Ads web interface.
  API cost arrives in micros: divide by 1,000,000 for currency. Web interface downloads show
  currency already.
- **Brand voice:** read `./brand/` per `_system/brand-memory.md` (voice-profile, positioning) before
  drafting any copy. Copy that ignores the voice profile is a defect, even where it converts in
  theory.
- **Standards:** `references/google-ads-standards.md` holds the RSA limits, asset minimums,
  structure conventions and volume floors. Check all drafted copy against it before filing.

## Diagnosis process

1. **Frame.** What is underperforming, against what expectation, over what window? Check that the
   window clears the conversion lag and the volume floors. Otherwise the honest answer is "too
   early to tell", delivered as such.
2. **Localize.** Account → campaign → ad group → ad. A bad account number is usually two bad
   campaigns. A bad campaign is usually one bad ad group. Name the level where the problem lives.
3. **Attribute.** A CTR problem points at a message or audience mismatch. A CVR problem points at
   the landing page or the offer. A cost problem points at competition or bidding. A delivery
   problem points at budget, rank or policy. Different causes need different fixes. A headline
   rewrite cannot fix a landing page problem, and the memo must not pretend it can.
4. **Decide.** Keep, test or change. Attach success criteria to any change: metric, target and
   review date.

## Drafting RSA copy

For a creative fix, follow `references/google-ads-standards.md`:

- Headlines ≤ 30 characters, descriptions ≤ 90. Count before filing. Over-limit copy is a defect.
- Draft toward full slot usage: aim for 8 to 12 distinct headlines and 3 to 4 descriptions per RSA,
  so the auction has material to work with. Distinct means different angles (offer, outcome, proof,
  urgency, brand), not synonyms of one angle.
- At least one headline carries the ad group's primary keyword. At least one carries a concrete
  differentiator from positioning.
- Write the copy in brand voice and check it against the voice profile.
- The diff lists current assets against proposed assets line by line, so the approver reads exactly
  what changes.
- Asset coverage counts as creative work. Where a campaign lacks sitelinks, callouts or (where phone
  leads matter) a call asset, propose them with concrete text. Sitelink link text is ≤ 25
  characters, per the standards file.

## Budget and bidding recommendations

- Propose budget shifts as explicit amounts, for example "campaign `<campaign ID>`:
  `<current>`/day → `<proposed>`/day". Justify them by marginal performance, never by ratios alone.
- Weigh learning effects. A bid strategy change resets learning. The recommendation weighs the
  reset cost against the expected gain and says so.
- A pause proposal needs a mature window past the conversion lag, volume above the floor, spend that
  is material to the account, and no seasonal explanation.

## Filing format

The detail block of each entry:

```
## Evidence
[the rows and metrics that prove the diagnosis, with the window]

## Diagnosis
[the cause, at the level it lives]

## Proposed change
[before → after, line by line]

## Success criteria
[metric, target, review date]
```

## The test

An approver who knows nothing about this account reads one recommendation and decides in under a
minute. The evidence, the change and the success criteria are all in front of them.

File: google-ads-optimize/SKILL.md · Version 1.0 · November 2026
