---
name: google-ads-create
version: 1.0
description: >
  Drafts a complete Google Ads Search campaign as one structured proposal: budget, one or more ad
  groups, responsive search ads, keywords, negatives, sitelinks, callouts, bidding, dates and
  location settings. Runs Google's dry-run check, which creates nothing, and files the draft for a
  human approver. Nothing is created until the approver approves, and the campaign is then created
  PAUSED. Triggers on: create a campaign, launch a search campaign, set up Google Ads for this page,
  write ads for this offer. Also triggers on: new ad group, spin up paid search. Not for: changes to existing
  campaigns (google-ads-optimize), audits (google-ads-audit), Performance Max, Display, Shopping
  or Demand Gen, Meta ads.
---

# Google Ads Create

The other Google Ads skills work on an account that already exists. This one proposes a campaign
that does not exist yet. That difference is the whole risk profile. An audit that is wrong wastes a
reading. A campaign that is wrong spends money on the wrong traffic the moment someone enables it.

**Operating contract (binding):**

- **Draft and check, never create.** Save the draft as a proposal and run Google's
  `validate_only` check, which creates nothing in Google Ads. Nothing is created until the approver
  approves this exact draft. The approver is a named person with authority over the account and
  its spend. The agent never approves its own draft. The approver sends the create. The agent
  never sends it.
- **Every campaign is created PAUSED.** Enabling it is a separate human act inside Google Ads.
  Never write copy, a memo or a summary that implies the campaign starts serving on approval. It
  does not.
- **A budget is a claim that needs a reason.** State the daily amount, what it buys at the ad
  group's expected CPC, and why that number beats half or double it. "Start small" is not a reason.
  A reason reads like this: "`<daily budget>` covers about `<n>` clicks at the `<CPC>` these terms
  show over the last 90 days".
- **Nothing outside Search.** No Performance Max, Display, Shopping or Demand Gen proposals. Those
  spend across surfaces that these skills cannot report on per placement. A proposal for one is
  advice nobody can check.
- **Refuse to guess the landing page.** The final URL is a page that exists and matches the
  keywords. If the page cannot be checked, say which page is needed and stop. A live page is a
  prerequisite, not a detail.

**Keys:** Google Ads API access needs a developer token (`GOOGLE_ADS_DEVELOPER_TOKEN`) and OAuth
credentials in the form the client library expects. An account reached through a manager account
also needs `GOOGLE_ADS_LOGIN_CUSTOMER_ID`. Keep them in the environment or in `.env` (see `.env.example`).
Never ask for a key in chat. The create step also needs write access (see "Approval and create").

## Before drafting

1. **Brand voice.** Read `./brand/` per `_system/brand-memory.md` (voice-profile, positioning). Ad
   copy that ignores the voice profile is a defect, even where it converts.
2. **Standards.** `google-ads-optimize/references/google-ads-standards.md` is the single source for
   RSA limits, asset minimums and structure conventions. Read it. Do not restate its numbers from
   memory.
3. **Keyword evidence.** Use the `keyword-research` skill's output where one exists. For terms the
   account already has data on, use the account's keyword report from the Google Ads API or the
   web interface. A keyword with no evidence behind it is a hypothesis. Label it as one, and keep
   the set small enough for a first run to learn from.
4. **Existing coverage.** Look in the account's campaign and keyword reports for a campaign that
   already targets these terms. A second campaign on the same keywords makes the account bid
   against itself. Say so instead of proposing it.
5. **Political advertising.** This skill does not draft political advertising: a party, candidate,
   election, referendum, legislation or political campaign. If a request is political advertising,
   do not draft it, and tell the person. Google requires every new campaign to declare whether it
   contains EU political advertising. Every create from this skill declares that it does not.
6. **Ask before drafting.** These choices belong to the person. Ask the ones the person did not
   answer yet in this conversation, in one short question block, before writing the draft:
   - **Ad groups:** one ad group, or 2 to 10? With more than one, what are the themes, and which
     landing page does each one use?
   - **Pins:** pin a headline or description to a position? The default is no pins.
   - **Bidding:** Maximize clicks with an optional maximum CPC? Or Manual CPC, with a default bid
     per ad group and optional bids per keyword?
   - **Dates:** a start date and an end date? Or no dates, so the campaign runs from the day a
     person enables it, with no end?
   - **Location option:** presence only (people in, or regularly in, the locations)? Or presence or
     interest (also people searching about them)?
   - **Location exclusions:** any locations to exclude?
   - **Shared negative list:** create a new shared list, attach an existing one by its ID, or use
     none?

   Language targeting is not offered. Google is removing language targeting from Search campaigns
   (https://developers.google.com/ads/blog/posts/2026/08/google-ads-language-targeting-changes).
   If the person asks for a language, explain this. The draft still carries `language_id` (1000 =
   English).

## The draft

One ad group, one responsive search ad, one tight keyword set. A first campaign that tries to cover
four themes learns nothing about any of them. If the person wants several themes, give each theme
its own ad group (`ad_groups`) with its own landing page.

- **Name:** `<site>-<objective>-<theme>`, per the standards file, readable in a campaign list six
  months from now.
- **Daily budget:** in micros (currency × 1,000,000). The owner sets a ceiling,
  `<MAX_DAILY_BUDGET>`, before the first run. Without a ceiling, file nothing and ask the owner to
  set one. Refuse a draft above it. A draft that needs more is a conversation with the operator, not
  a larger number quietly filed.
- **Final URL:** https, a real page, matching the keyword intent. Paths (`path1`, `path2`, ≤ 15
  characters each) are display text, not routing.
- **Headlines:** 8 minimum (the house minimum, per the standards file), aim for 8 to 12 distinct
  ones, ≤ 30 characters each. Distinct means
  different angles (offer, outcome, proof, differentiator, brand), not synonyms. At least one
  carries the primary keyword. At least one carries a concrete differentiator from positioning.
- **Descriptions:** 3 minimum (the house minimum, per the standards file), up to 4, ≤ 90
  characters each.
- **Keywords:** 1 to 50, each with a match type (`EXACT`, `PHRASE`, `BROAD`). Prefer exact and
  phrase for a first campaign. Broad match on a new account with no conversion history spends the
  budget teaching Google, not the advertiser.
- **Targeting:** geo target constant IDs (`2840` = United States) and a language ID (`1000` =
  English). Name why the geo set is what it is.
- **Sitelinks:** `sitelinks`, up to 20, each `{link_text, final_url, description1?, description2?}`.
  Link text ≤ 25 characters, final URL https, descriptions ≤ 35 characters each, both or neither.
- **Callouts:** `callouts`, up to 20, each `{text}` ≤ 25 characters. Every new Search campaign has
  at least 4 sitelinks and at least 4 callouts, per the standards file.
- **Negative keywords:** `negative_keywords`, up to 100, campaign level, same shape as `keywords`.
  A new campaign has no search terms report yet. Add only negatives the person asked for, or ones
  backed by evidence in this draft. Example: keyword research shows an unrelated meaning of a brand
  term, such as a brand name that is also a common word. Name the evidence in the proposal.
  Never add a generic starter list. After the campaign runs, negatives follow the `google-ads-optimize`
  rules.
- **Ad groups:** `ad_groups`, 2 to 10, each `{name, final_url, headlines, descriptions, path1?,
  path2?, keywords, cpc_bid_micros?}` with the same limits as above. With `ad_groups`, leave out
  the top-level `final_url`, `path1`, `path2`, `headlines`, `descriptions`, `keywords` and
  `cpc_bid_micros`. A draft with both is invalid. Give each ad group a different name.
- **Pins:** a headline or description is a plain string, or `{text, pin}` to pin it. Headline pins
  are `HEADLINE_1`, `HEADLINE_2` and `HEADLINE_3`. Description pins are `DESCRIPTION_1` and
  `DESCRIPTION_2`. Pin only what the person asked for. Leave enough assets unpinned: Google refuses
  an ad whose pins leave too few combinations.
- **Bidding:** `bidding` is `{strategy: "MAXIMIZE_CLICKS", cpc_bid_ceiling_micros?}` (the default)
  or `{strategy: "MANUAL_CPC"}`. Under Manual CPC, every ad group needs a default bid in
  `cpc_bid_micros`. For one ad group it is a top-level field. With `ad_groups` it sits inside each
  group. A keyword can also have its own `cpc_bid_micros`. Under Maximize clicks, refuse any bid.
  Google ignores it, and the approver believes it applies.
- **Dates:** `start_date` and `end_date` as `YYYY-MM-DD` in the account's time zone. The end date
  is on or after the start date. Google refuses a start date in the past.
- **Location option:** `location_option` is `PRESENCE` or `PRESENCE_OR_INTEREST`. Leave it out to
  keep Google's default.
- **Location exclusions:** `excluded_geo_target_ids`, up to 100, same ID format as
  `geo_target_ids`. Never target and exclude the same ID.
- **Shared negative list:** `shared_negative_list` is `{name, keywords}` to create a new list, with
  1 to 5,000 keywords in the shape of `negative_keywords`. Or it is `{existing_shared_set_id}` to
  attach a list the account already has. The evidence rule for negatives applies to a new list too.

Count every character before filing. Over-limit copy is a defect. Google rejects the whole request
rather than trim it.

## The proposal

Save the proposal in `./campaigns/google-ads/<campaign-slug>/`:

- `draft.json`: the machine-readable draft, with exactly the fields shown below.
- `proposal.md`: what the approver reads before approving (template below).

Add one entry to the recommendation log, `./campaigns/google-ads/recommendations.md`. It carries
an entry number, the date, `source: google-ads-create`, `kind: other`, the customer ID, the proposal
folder, the draft key and `status: proposed`.
Its summary is one line: what the campaign is and what it costs per day. The draft key is a
SHA-256 hash of the customer ID, the campaign name and the final URL, one per line. With
`ad_groups`, the first ad group's final URL counts.

Money fields are integers in micros. The `<..._MICROS>` placeholders below stand for those
integers. A single ad group:

```json
{
  "customer_id": "<CUSTOMER_ID>",
  "name": "store-leads-[product]",
  "summary": "Search campaign for [product] terms, <daily budget>/day.",
  "daily_budget_micros": "<DAILY_BUDGET_MICROS>",
  "final_url": "https://example.com/[product]",
  "path1": "[category]",
  "headlines": ["...", "...", "...", "...", "...", "...", "...", "..."],
  "descriptions": ["...", "...", "..."],
  "keywords": [{ "text": "[product keyword]", "match_type": "PHRASE" }],
  "negative_keywords": [{ "text": "[brand] [unrelated meaning]", "match_type": "PHRASE" }],
  "sitelinks": [
    { "link_text": "Pricing", "final_url": "https://example.com/pricing",
      "description1": "[pricing point]", "description2": "[pricing point]" },
    { "link_text": "Contact sales", "final_url": "https://example.com/contact" },
    { "link_text": "Docs", "final_url": "https://example.com/docs" },
    { "link_text": "Case studies", "final_url": "https://example.com/customers" }
  ],
  "callouts": [
    { "text": "[benefit 1]" }, { "text": "[benefit 2]" },
    { "text": "[benefit 3]" }, { "text": "[benefit 4]" }
  ],
  "bidding": { "strategy": "MAXIMIZE_CLICKS", "cpc_bid_ceiling_micros": "<MAX_CPC_MICROS>" },
  "start_date": "<YYYY-MM-DD>",
  "location_option": "PRESENCE",
  "excluded_geo_target_ids": ["<GEO_TARGET_ID>"],
  "geo_target_ids": ["2840"],
  "language_id": "1000"
}
```

With two or more ad groups, the single-ad-group fields move into `ad_groups`. Manual CPC bids sit
on each group and keyword:

```json
{
  "customer_id": "<CUSTOMER_ID>",
  "name": "store-leads-[category]",
  "summary": "Search campaign for [product] and [category] terms, <daily budget>/day.",
  "daily_budget_micros": "<DAILY_BUDGET_MICROS>",
  "ad_groups": [
    {
      "name": "[product]",
      "final_url": "https://example.com/[product]",
      "path1": "[product]",
      "headlines": [{ "text": "[brand] [product]", "pin": "HEADLINE_1" }, "...", "...", "...", "...",
        "...", "...", "..."],
      "descriptions": ["...", "...", "..."],
      "keywords": [{ "text": "[product keyword]", "match_type": "PHRASE", "cpc_bid_micros": "<KEYWORD_BID_MICROS>" }],
      "cpc_bid_micros": "<AD_GROUP_BID_MICROS>"
    },
    {
      "name": "[category]",
      "final_url": "https://example.com/[category]",
      "headlines": ["...", "...", "...", "...", "...", "...", "...", "..."],
      "descriptions": ["...", "...", "..."],
      "keywords": [{ "text": "[category keyword]", "match_type": "EXACT" }],
      "cpc_bid_micros": "<AD_GROUP_BID_MICROS>"
    }
  ],
  "bidding": { "strategy": "MANUAL_CPC" },
  "shared_negative_list": {
    "name": "Brand homonyms",
    "keywords": [{ "text": "[brand] [unrelated meaning]", "match_type": "PHRASE" }]
  },
  "geo_target_ids": ["2840"],
  "language_id": "1000"
}
```

The draft never sets `status`, a key or a check result. The request builder adds those. Refuse a
draft that sets any of them, and never rewrite it silently. A silent rewrite of ENABLED to PAUSED
tells someone the campaign is launching. It is not.

`proposal.md` is what the approver reads before approving:

```
## What this is
[the offer, the audience, and the page it sends them to]

## Why this budget
[the amount, the expected CPC and the click volume it buys, and the evidence]

## Keywords
| Keyword | Match | Why |

## Ad copy
| # | Headline (chars) |
| # | Description (chars) |

## Sitelinks and callouts
| Sitelink text (chars) | URL | Descriptions (chars) |
| Callout (chars) |

## Negative keywords
| Negative | Match | Evidence (the person's request or the research that shows it) |

## What I could not verify
[anything assumed, such as CPC estimates, page content or seasonality, named plainly]
```

## Check with Google (creates nothing)

1. Check `draft.json` against every rule in "The draft" and the draft limits in
   `references/create-request.md`. On any failure, refuse the draft, name the rule and send nothing
   to Google.
2. Build the full create request from `draft.json`, as `references/create-request.md` describes.
   The builder sets `status` to PAUSED and adds the draft key.
3. Send it once with `validate_only` set to true. Google checks every operation and creates
   nothing. Without API access, build the campaign in Google Ads Editor with the campaign status
   Paused, and run Check changes. Do not post.
4. Report the log entry number, the proposal folder, and whether Google passed the check. If the
   check was skipped, say why.
5. Build the approval summary from the request itself, not from memory of the draft. It names the
   operation: "Create Search campaign, PAUSED". It lists the budget, bidding, locations,
   exclusions, location option, language and dates. For each ad group it lists the final URL, the
   keyword count by match type, and the headline and description counts. It also lists any default
   bid, keyword bids and pinned assets. It lists the negatives, sitelinks, callouts and any new
   shared list, under the name Google receives.
6. Compare the summary with the draft the person agreed to. Name every difference before the
   approver decides.

If Google rejects the request, the error names Google's code, message and field path. For example:
`REQUIRED: The required field was not present.
(mutate_operations[1].campaign_operation.create.contains_eu_political_advertising)`. If the field
is one this draft controls, fix the draft and check again. Otherwise report the exact error text.
Do not guess at a cause.

## Approval and create

1. The approver reads `proposal.md` and the approval summary, then approves or rejects in writing.
   Record the approver, the date and the decision in the log entry.
2. Before anything is sent, four gates apply. Each one stops the send on its own:
   - **Write access is off by default.** Reading reports needs no write access. The owner turns
     write access on for the account on purpose, in the tool that sends the request. Accept only
     one exact value as "on". Anything else counts as off.
   - **Check again at send time.** Check the draft against every rule in this skill again. It sat
     in a file between approval and send.
   - **Replay guard.** Search the log for the draft key. A key already marked
     `created (PAUSED)` stops the send, so a second send cannot create a second campaign.
   - **Credentials fail closed.** For an API send, missing or malformed credentials stop the run.
     There is no silent fallback to another account or key.
3. After approval, the approver creates the campaign. The agent does not send it. Either the
   approver sends the approved request once, with `validate_only` false and partial failure off.
   Or the approver posts the checked Google Ads Editor changes with the campaign status still
   Paused.
4. Record the created resource names (budget, campaign, ad groups, ads, keywords, shared list) in
   the log entry, with `status: created (PAUSED)`.
5. Enabling the campaign stays a separate human act in the Google Ads web interface.

## Never

- Never propose `status: ENABLED`, and never describe approval as "launching" the campaign.
- Never propose changes to billing, payment methods, account-level settings, conversion actions or
  an existing campaign. That is the ground of `google-ads-optimize`, which files its own recommendations.
- Never invent performance numbers. A CPC or volume estimate without a source goes under
  `What I could not verify` as an assumption, or it stays out.
- Never file the same draft twice to "make sure it went through". The draft key catches a
  duplicate, but a duplicate in the log is still noise for the approver.

File: google-ads-create/SKILL.md · Version 1.0 · November 2026
