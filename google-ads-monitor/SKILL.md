---
name: google-ads-monitor
version: 1.0
description: >
  Read-only anomaly watch over Google Ads: spend pacing, CTR shifts, conversion dropouts,
  efficiency drift, creative fatigue and delivery stops. Each candidate is triaged against expected
  patterns before anything is flagged. Outputs triaged observations, and material ones go to the
  recommendation log for a human approver. Triggers on: check the ads, anything wrong with paid,
  monitor campaigns, spend spike, why did conversions stop. Not for: a full account audit
  (google-ads-audit), copy or budget proposals (google-ads-optimize), new campaigns
  (google-ads-create).
---

# Google Ads Monitor

Monitoring exists to separate three things. **Expected patterns** are learning phases, weekends,
seasonality and changes someone made on purpose. **Unexplained anomalies** need investigation.
**Noise** gets no comment. Most monitoring failures are noise promoted to alarm. The main job of
this skill is to not cry wolf.

**Operating contract:**

- **Read-only.** It never changes an account and never drafts a change. A material finding becomes
  a recommendation entry, and stops there.
- **Check data freshness first.** Ad platforms finalize data late. A comparison of an unfinished
  day against a finished one manufactures anomalies. Exclude the trailing finalization window
  (typically 1 to 3 days) from comparisons.
- **No alerts on trivial denominators.** 3 clicks → 9 clicks is not "+200%". It is nothing. The
  volume floors in `google-ads-optimize/references/google-ads-standards.md` apply here too.
- **Say what is unknown.** Some evidence cannot separate noise from a real change. Then the output
  says exactly that, and names the data that settles the question.

**Keys:** Google Ads API access needs a developer token (`GOOGLE_ADS_DEVELOPER_TOKEN`) and OAuth
credentials in the form the client library expects. An account reached through a manager account
also needs `GOOGLE_ADS_LOGIN_CUSTOMER_ID`. Keep them in the environment or in `.env` (see `.env.example`).
Never ask for a key in chat. Without API access, work from report downloads out of the Google Ads
web interface.

## Data

Pull daily rows at campaign and ad group level. Use the Google Ads API (the GAQL report queries in
`google-ads-audit/SKILL.md`) or the same reports from the Google Ads web interface. API cost
arrives in micros: divide by 1,000,000 before showing currency. Web interface downloads show
currency already.

Compare like with like: the same day-of-week mix, complete days only, and one platform at a time
before any cross-platform statement.

## Signals watched

| Signal | Test | Floor before flagging |
|---|---|---|
| Spend pacing | daily spend against the trailing 14-day median | ±40% on a complete day |
| CTR shift | campaign CTR against its trailing window | ≥ 500 impressions per side |
| Conversion dropout | conversions at 0 while clicks flow | ≥ 30 clicks since the last conversion, past the conversion lag |
| Efficiency drift | CPA or ROAS against the trailing median | CPA: ≥ 30 clicks, and past the conversion lag. ROAS: ≥ 15 conversions in the window |
| Creative fatigue | CTR decaying for 3 or more weeks in a row | ≥ 2,000 impressions a week |
| Delivery stop | impressions drop to about 0 on an active campaign | any (this signal is binary) |

A conversion dropout with healthy clicks is a **tracking** question first and a performance
question second. Say which hypothesis leads.

## Process

1. Pull the window. The default is the last 14 complete days against the prior 14.
2. Classify every candidate signal as expected, unexplained or noise. List the expected and noise
   signals in one line each, then drop them.
3. For each unexplained anomaly, state the observation, the confidence, the most likely causes in
   rank order, and the check that tells them apart.
4. Add each material anomaly to the recommendation log, `./campaigns/google-ads/recommendations.md`.
   Material means money is actively misbehaving, delivery stopped, or tracking is suspect. Use
   `kind: pause` only for delivery or burn emergencies. Otherwise use `kind: other` with the
   investigation ask. Each entry carries an entry number, the date and `source: google-ads-monitor`. It
   also carries explicit IDs (customer ID, campaign ID, ad group ID where it applies), a one-line
   summary, the evidence and `status: proposed`.
5. Report one section per anomaly. Then list what was "watched and fine", so the operator knows
   what was covered. End with the data coverage caveats.

A recommendation changes nothing. A named human approver accepts or rejects each entry. An
accepted change goes live only by a separate act: a person makes it in the Google Ads web interface
or Google Ads Editor. This skill sends no change to the Google Ads API. Its API use is read-only.

## The test

A monitor that flags something on every run is broken. The correct output on a healthy account is
short: "checked 6 signals across N campaigns, all within expected ranges, freshest complete day
<date>."

File: google-ads-monitor/SKILL.md · Version 1.0 · November 2026
