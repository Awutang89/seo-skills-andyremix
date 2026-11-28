---
name: domain-acquisition-audit
description: "Audit a list of domains offered for purchase as link equity, before payment. Counts TRUE referring domains — strips Wikipedia scrapers, mirror networks, free-blog platforms, syndicated article farms, directory farms, forums, caches and link-spam from the raw referring-domain count — then prices the list at cost per true referring domain, which is routinely 10-50x the headline cost per referring domain a vendor quotes. Also checks each domain against the buyer's OWN acquisition criteria (TLDs, language, market, spam ceiling — always ask, never assume), confirms it still ranks for anything, and scans for adult/gambling/pharma anchors and PBN footprints. Use this whenever someone mentions buying domains, an expired-domain list, a backlink package, a domain broker or vendor shortlist, link acquisition, domain flipping, aged domains, PBN inventory, or asks whether a domain is worth its asking price — even if they only say 'is this domain any good' or paste a list of domains with prices. Outputs a verdict per domain plus a CSV block."
---

# Domain Acquisition Audit

Due diligence on domains offered for sale as link assets. Built from a worked audit
of a vendor list where only a small share of the
quoted referring domains survived classification as genuine editorial links —
turning the quoted cost per referring domain into a far higher one.

The machinery here is objective. The **pass/fail bar belongs to the buyer** and is
never assumed: a buyer acquiring German properties wants the opposite of a buyer
acquiring English ones.

## Inputs

A list of candidate domains, optionally with asking prices. Any format the operator
pastes — bare domains, `domain — $price`, a numbered shortlist, a CSV.

## Step 0 — Establish the criteria. Ask. Do not assume.

Before spending a single billed call, confirm the buyer's criteria. Ask only for
what was not already stated, in one message:

1. **TLDs** — allowed, excluded, or no constraint?
2. **Language / market** — which language should the link history be in? Which
   country? Or no constraint?
3. **Topical fit** — what is the buyer's subject area, so relevance can be judged?
4. **Spam ceiling** — max acceptable backlink spam score (0-100). Default 25 if
   the operator has no view.
5. **Minimum true referring domains** — the floor below which a domain is not
   worth buying at any price. Default 25 if no view.
6. **Disqualifiers** — adult, gambling, pharma, piracy, legal exposure. Default:
   all disqualifying.

Never substitute the criteria from the source audit. `.com/.org/.net` and
"English-language history" were **one buyer's brief**, not a standard.

If the operator declines to set criteria, run the objective passes only (2, 3, 4,
6) and report cost per true referring domain without pass/fail verdicts. Say so.

## Required tools (fail closed if absent)

- A backlinks overview read — target-grain summary: rank, backlinks, referring
  domains, spam score, nofollow share, broken share, TLD and country distribution.
- A backlinks profile read — individual backlink rows. **The most expensive read in
  the audit**: a full backlinks pull,
  billed per call. Call it **once per candidate domain**, `mode=one_per_domain`,
  ordered by referring-domain rank descending, limit 200. Derive every downstream
  view from those rows. Never re-pull to answer a follow-up question.
- A ranked-keywords read — does the domain still rank for anything, and in what
  language.
- A `<SERP API>` read — indexation checks on suspected doorway networks
  (`site:host/path`, quoted anchor phrases).

Optional, only if the operator asks for it:
- A domain overview read — traffic estimate for a single market.

**Budget.** Two billed calls per candidate domain (`overview` + `profile`) is the
floor. A twenty-domain list is ~40 calls. Announce the expected call count before
starting and get a go-ahead. Never retry a failed billed call — report it.

## Step 1 — Criteria compliance

For each domain, record pass/fail against the Step 0 criteria. Then compute the
figure that actually lands with a buyer:

> **the share of total quoted cost sitting on domains that fail a stated criterion**

A count ("13 of 20 fail") is arguable. "$<amount> — <share>% of the quote — is on domains
that fail a criterion you stated up front" is not.

## Step 2 — Link profile

From the backlinks overview read: rank, backlinks, referring domains, spam score,
nofollow share, broken-backlink share, referring TLD and country distribution.

Report the DataForSEO rank honestly. It is a **0-1000** scale, not Ahrefs DR or
Moz DA, which are 0-100. Present it as `DR≈` after dividing by ten so it reads on
the familiar scale, and state that it is a rescaling, not a conversion — it runs
lower than Ahrefs for mid-tier sites. Never quote it as a Domain Rating.

## Step 3 — True referring domains (the core pass)

Run the backlinks profile read once per domain, then classify every referring domain
with the script:

```
node domain-acquisition-audit/scripts/classify-referring-domains.mjs \
  --in <backlinks.json> --min-rank 300 --out <classified.json>
```

The script reads `{ "<domain>": [ { from, rank, url, title, anchor, dofollow } ] }`
and returns per-domain counts by class plus the true-referring-domain total. This script is not included in this repository.

A **true referring domain** is one that is:
1. not in any junk class (see `references/link-classes.md`),
2. **dofollow** — a nofollow link passes no equity, and
3. at or above the authority floor (`--min-rank`, default 300 ≈ DR≈30).

Two behavioural detectors run alongside the host patterns, and catch the most:
- **Syndicated farm** — one page title reused across 3+ distinct referring hosts.
- **Cross-target farm** — one host linking to 4+ of the candidate domains. A site
  linking to four unrelated domains on the same shortlist is a directory, not an
  editor. This caught the single largest junk class in the source audit.

**Why this matters more than any other number.** A Wikipedia scraper reads as
DR≈62 because it inherited Wikipedia's content wholesale — nobody chose to link to
anything.
Vendors price on raw referring domains; this pass prices
on real ones.

**Sampling honesty.** The pull is the top 200 referring domains by authority. For a
domain with fewer than 200, the count is complete. For a larger profile, the count
is a **floor** — more real links may sit deeper, but all of them rank below every
link counted, and junk density rises as authority falls. The script prints which
case applies per domain.

**Mind the denominator.** The script's `survivalRate` is true RD as a share of
*what was sampled*. The figure the buyer needs is true RD as a share of the
**total claimed referring domains** from the backlinks overview read — the number the
vendor is pricing on. In the source audit those were <sampled-share>% and **<claimed-share>%**
respectively, from the same run. Always report the second, and label it.

Tune the classifier to be **generous to the vendor**: keep borderline cases as
editorial, so the reported survival rate is the optimistic reading and cannot be
argued down.

## Step 4 — Cost per true referring domain

The deliverable number:

```
cost per true RD = asking price / true referring domains
inflation factor = (cost per true RD) / (asking price / claimed referring domains)
```

Report both, per domain and for the portfolio, ranked worst first. Flag every
domain with fewer than the operator's minimum true referring domains.

This figure is **criteria-independent** — it holds whatever the buyer is looking
for, which makes it the strongest thing in the report.

## Step 5 — Is it alive

A ranked-keywords read per domain. A domain that ranks for nothing is being sold on
backlink history alone. Report the ranking-keyword count, and what the keywords
actually are — a domain that ranks for a subject far from its stated one
has already been
repurposed by someone else.

Check the live homepage where it matters. Parked pages, monetization redirects and
placeholder templates are all signals the domain is inventory, not a site.

## Step 6 — Risk scan

Sweep anchors for adult, gambling, pharma, cracked-software and link-selling
vocabulary — in the target's own languages, not just English. Then:

- **Establish whether it is live.** A spam network's pages may not be indexed. Use
  `<SERP API>` with `site:` and quoted-phrase queries. Links on unindexed
  pages pass nothing and are not a penalty risk. Say so plainly rather than
  inflating the finding.
- **Separate dofollow from nofollow.** A domain can carry
  adult anchors (all nofollow, inert) and gambling anchors (all dofollow, the
  actual problem). Reporting them as one number would be wrong.
- **Do not blame the vendor for a spray.** Scraped-list spam lands on every parked
  expired domain. It says what the domain *is*, not what the vendor did.

Flag legal exposure separately from SEO quality — a piracy-brand domain is a
refusal at any price, not a pricing input.

## Output

Follow `_system/output-format.md`. Three blocks:

**1. Verdict table** — one row per domain: domain, price, criteria pass/fail,
DR≈, claimed RD, **true RD**, **$/true RD**, spam score, ranking keywords,
verdict. Sort by `$/true RD` descending so the worst value is first.

Verdicts: `Reject` (fails a stated criterion or carries a disqualifier),
`Weak` (passes criteria, but thin or dead), `Consider` (passes, with real links).

**2. Portfolio roll-up** — total quoted, total claimed RD, total true RD, survival
rate, blended $/true RD, inflation factor, and the share of cost sitting on
criteria failures.

**3. CSV block** — the verdict table as comma-separated rows in a fenced code
block, so the operator can paste it into a sheet. This skill stores nothing; the
CSV is the export.

Then a short recommendation: which to buy, at what price, which to strike on
principle, and what to put back to the vendor.

## What this skill cannot do

State these as gaps rather than working around them. None of the reads above exposes:

- `backlinks/history` — so **no 18-month decay curve**. Referring-domain trend is
  the strongest pricing lever there is (a domain shedding 42% of its referring
  domains is a wasting asset) and it is not reachable through the reads above.
- `domain_whois_overview` — so **no drop-catch detection**. Re-registration date
  and registrar reveal whether "aged authority" survived a drop.
- `historical_bulk_traffic_estimation` / `bulk_traffic_estimation` — so **no
  multi-country traffic history**. The ranked-keywords read covers one market at a
  time.

If the operator needs these, say they require new data tools, and do not
substitute a weaker signal while implying it is the same thing.

## Reference

`references/link-classes.md` — every junk class, why it is junk, and its host
patterns. Read it when a classification looks wrong or a new farm shape appears.

File: domain-acquisition-audit/SKILL.md · Version 1.0 · November 2026
