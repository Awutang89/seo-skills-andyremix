# Create request: Google Ads API and Google Ads Editor

How an approved draft becomes one create request. Field names follow the Google Ads API as of
v23. The REST JSON form uses camelCase for the same fields. When Google renames a field, update
this file.

## One atomic request

- Send every operation in one mutate call: `POST customers/<CUSTOMER_ID>/googleAds:mutate`.
- Set partial failure off. A half-built campaign (a budget and a campaign but no ad) is worse than a
  clean failure that a person can retry.
- Set `validate_only` to true for the check before approval. Set it to false only for the approved
  create. The approver sends that request.
- For an account reached through a manager account, send the manager ID in the
  `login-customer-id` header.
- Temporary resource names with negative IDs (for example `customers/<CUSTOMER_ID>/campaigns/-2`)
  let later operations name resources that the same request creates. Every temporary ID in one
  request is unique across all resource types. Create each resource earlier in the request than any
  operation that names it.
- Keep operations of one type together. Google processes contiguous runs of one operation type
  together.

## Operation order

| # | Operation | Fields |
|---|---|---|
| 1 | `campaign_budget_operation` | name with the key suffix, `amount_micros`, `delivery_method: STANDARD`, `explicitly_shared: false` |
| 2 | `campaign_operation` | `status: PAUSED`, `advertising_channel_type: SEARCH`, the budget, the political advertising declaration, bidding, network, location option, dates |
| 3 | `campaign_criterion_operation`, one per item | each targeted location, each excluded location with `negative: true`, the language, each negative keyword with `negative: true` |
| 4 | `ad_group_operation`, one per ad group | `type: SEARCH_STANDARD`, `status: ENABLED`, `cpc_bid_micros` under Manual CPC |
| 5 | `ad_group_ad_operation`, one per ad group | `status: ENABLED`, `final_urls`, `responsive_search_ad` with headlines, descriptions, `path1` and `path2` |
| 6 | `ad_group_criterion_operation`, one per keyword | text, match type, `status: ENABLED`, `cpc_bid_micros` where the keyword has a bid |
| 7 | `asset_operation`, one per asset | a sitelink asset carries `final_urls` on the asset and `sitelink_asset` with the link text and descriptions. A callout asset carries `callout_asset` with `callout_text` |
| 8 | `campaign_asset_operation`, one per asset | the campaign, the asset, `field_type` of `SITELINK` or `CALLOUT` |
| 9 | `shared_set_operation` | new list only: name with the key suffix, `type: NEGATIVE_KEYWORDS` |
| 10 | `shared_criterion_operation`, one per keyword | new list only: the list and the keyword |
| 11 | `campaign_shared_set_operation` | links the new or existing list to the campaign |

## Field notes

- **Budget.** Never join a shared budget. A shared budget lets this campaign move spend that
  belongs to campaigns nobody approved here.
- **Network.** Google Search only: `target_google_search` is true. `target_search_network`,
  `target_content_network` and `target_partner_search_network` are false. Search partners and
  Display stay off.
- **Bidding.** Maximize clicks is `target_spend`, with `cpc_bid_ceiling_micros` only for a
  ceiling. It is the default because it needs no conversion history, and a new campaign has none.
  Manual CPC is `manual_cpc` with `enhanced_cpc_enabled` set to false.
- **Location option.** Send `geo_target_type_setting` only for a draft that sets a location option.
  `positive_geo_target_type` takes the draft value, and `negative_geo_target_type` is `PRESENCE`.
  Without the field, Google's default applies.
- **Dates.** `start_date_time` is the start date at `00:00:00`, and `end_date_time` is the end date
  at `23:59:59`, in the account's time zone. Google accepts only these two times.
- **Language.** The language criterion stays in the request while Google removes language
  targeting from Search campaigns.
- **Ad groups and ads are ENABLED inside the PAUSED campaign.** Nothing serves until a person
  enables the campaign.
- **Pins.** A pinned headline or description carries `pinned_field` with the draft's pin value.
- **Sitelink descriptions.** Send both descriptions or neither.
- **Unique names.** Budget names and shared list names are unique per account. Add the first 8
  characters of the draft key to each, for example `[campaign name] (1a2b3c4d)`. A retried create
  then fails on Google's own uniqueness check instead of making a second budget.
- **Political advertising declaration.** Google rejects a campaign create without
  `contains_eu_political_advertising`. This skill does not draft political advertising, so every
  create sends `DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING`.
- **Read back.** The response lists one result per operation. Record the resource names of the
  budget, campaign, ad groups, ads, keywords and shared list in the log entry.

## Draft limits

Check these before the request is built.

- Daily budget: at least 1,000,000 micros (one unit of account currency, noted as Google's
  practical minimum), at most the owner's `<MAX_DAILY_BUDGET>`.
- Any bid: at least 10,000 micros (noted as Google's smallest bid in US dollars), at most the
  daily budget ceiling.
- Campaign and ad group names: at most 120 characters. Ad group names are unique within the draft,
  ignoring case.
- Summary: one line, at most 300 characters.
- Keyword and negative keyword text: at most 80 characters.
- Targeted locations: 1 to 20 geo target IDs. Excluded locations: up to 100.
- RSA, sitelink, callout, keyword, ad group and shared list counts: as in "The draft" in `SKILL.md`.

## Google Ads Editor route

Use this route without API access, or where the operator prefers Editor.

1. Build the campaign from `draft.json`: ad groups, ads, keywords, negatives, sitelinks, callouts
   and the shared list. Set the campaign status to Paused first.
2. Give the campaign the same values as the API route: Search network only, a budget that is not
   shared, the bidding, the location option and the dates.
3. Run Check changes. Treat any error as a failed check, and report its exact text.
4. Do not post before the approver approves. After approval, the approver posts the changes. Then look in the
   Google Ads web interface and check that the campaign status is Paused.
5. Record the result in the log entry, as for an API create.

The Google Ads web interface is where a person reads reports and enables the campaign. This skill
does not create campaigns through it.

File: google-ads-create/references/create-request.md · Version 1.0 · November 2026
