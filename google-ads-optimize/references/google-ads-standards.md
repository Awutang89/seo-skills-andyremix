# Google Ads standards: limits, minimums and floors

The numbers the Google Ads skills check against. Platform limits are Google's. Volume floors and
conventions are house rules. When Google changes a limit, update this file. The skills cite this
file and do not hardcode its numbers.

Skills that use this file: `google-ads-audit`, `google-ads-monitor`, `google-ads-optimize`,
`google-ads-create`.

## Responsive search ads (RSA)

| Element | Google limit | House minimum |
|---|---|---|
| Headlines | up to 15, ≤ 30 characters each | 8 distinct angles |
| Descriptions | up to 4, ≤ 90 characters each | 3 distinct |
| Final URL paths | 2 × ≤ 15 characters | use both where they carry meaning |

- Google's hard minimum is 3 headlines and 2 descriptions. The house minimum exists because thin
  RSAs throttle themselves.
- "Distinct" means a different persuasion angle: offer, outcome, proof, urgency, brand or
  keyword-literal. A paraphrase does not count.
- Pin a headline only for a reason, such as compliance text or a brand rule. Every pin reduces the
  combinations the auction can test.
- Character counts include spaces. Count before filing. Review rejects over-limit copy.

## Assets (extensions)

| Asset | Google limit | House rule |
|---|---|---|
| Sitelinks | link text ≤ 25 characters, 2 descriptions ≤ 35 characters each | at least 4 per campaign, on every Search campaign |
| Callouts | ≤ 25 characters | at least 4 per campaign |
| Structured snippets | a header and at least 3 values | add one where a category fits |
| Call asset | a verified number | required where phone leads matter to the account objective |
| Image assets | current Google specs | propose them where images exist |

Sitelinks and callouts are not optional decoration. Ad rank rewards asset coverage. A campaign
without them is a standing `warn` finding in audits.

## Structure conventions

- One theme per ad group. The ad group's primary keyword appears in at least one headline of each
  of its RSAs.
- Campaign naming: `<site>-<objective>-<theme>`, for example `store-leads-[category]`. Consistent
  names keep reports readable at campaign level.
- Audit Search and Performance Max separately. Their metrics are not comparable and must not share
  a benchmark.
- Every campaign has a conversion goal wired to a real conversion action. Its location targeting is
  reviewed: presence only, or presence or interest. Its budget is one the operator recognizes.

## Volume floors (before any performance claim)

| Claim | Floor |
|---|---|
| CTR comparison | ≥ 500 impressions per side |
| CVR or CPA judgment | ≥ 30 clicks, and past the conversion lag |
| ROAS judgment | ≥ 15 conversions in the window |
| Creative fatigue | ≥ 2,000 impressions a week, for 3 or more weeks |
| Pause proposal | all of the above, plus spend material to the account |

Below the floor, the honest statement is "not enough data". It is the required statement.

## Copy compliance

- No claims the site cannot back up. No superlatives without proof on the landing page.
- No excessive capitals, no exclamation abuse and no phone numbers in headline text. Use the call
  asset for a phone number.
- Trademark rules apply to competitor terms. Propose competitor-term copy only after the operator
  states that the use is permitted.
- Destination policy: the final URL delivers what the copy promises. A mismatch between copy and
  landing page is a CVR diagnosis and a policy risk at the same time.

File: google-ads-optimize/references/google-ads-standards.md · Version 1.0 · November 2026
