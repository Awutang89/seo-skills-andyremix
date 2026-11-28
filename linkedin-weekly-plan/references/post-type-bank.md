# Post-type bank

Every post type from the five idea banks in the `linkedin-strategy` playbook reference, section 5,
de-duplicated. In the Page system this vocabulary is the **angle**: the bank type name a plan slot
carries, and the `angle` field a saved post records. A content type (for example `product-proof`) is
a different thing: it is the route a post takes, and a type record (a file in `./campaigns/linkedin/`) defines it.
The bank is background for naming an angle; the accepted ideas and the Page records decide the slots.

| Bank | Source |
|---|---|
| 070 | 15 formats that never stop working (Di Bratto) |
| 072 | 40 post ideas (Di Bratto) |
| 080 | 10 posts every founder needs (Stovold) |
| 098 | Six post types: three get seen, three get paid (Kremins) |
| 053 | Five jacking types (Escobar) |

## How to read a row

- **id:** the name recorded as the slot's angle, in the `angle` field, in the `source_ref` fragment
  (`#angle=<id>;bank=<bank>`) and in the post receipt.
- **Stage:** reach, trust or convert. 098 labels its first three types "get seen" (reach here) and
  its last three "get paid" (trust or convert here). 076's weekday options give the rest. All other
  stage tags are this pack's mapping. The creators give none.
- **Input:** `no team input` means the post needs only the strategy page, the person's supplied
  links and public sources, and its angle is a position the strategy page holds. `needs team input`
  means it needs a real company event, number, objection, decision or customer outcome that the
  person gave in reply to this week's question. Brand files and published articles are background,
  never team input. A needs-input type is never filled by research or invention.
- **Research-led:** a `no team input` type whose substance is gathered from public sources rather
  than from the strategy page's positions: `authority-curation`, `emerging-trend`, `checklist`,
  `big-brand-teardown`, `comparison` and `industry-commentary`. At most one research-led type a
  week. With no team input, prefer the types built from the strategy page's positions and offer:
  `contrarian-belief`, `mythbuster`, `industry-prediction`, `framework`, `if-i-were`,
  `offer-breakdown` and `best-suited-for`.
- **Type and Notes:** the plan passes both cells of the chosen row to `linkedin-post` exactly as
  written; the post follows them.
- **Banks:** every bank that lists the type, with its item number. Record the bank the slot used.
  When the angle follows another bank's wording, record that bank. Otherwise record the first one.
  `ai-opinion`, `hiring-opinion` and `pro-tips` come from the 076 template, not one of the five
  banks: record `076` for them.

## Reach

| id | Type | Input | Banks | Notes |
|---|---|---|---|---|
| contrarian-belief | Contrarian belief or industry belief the poster disagrees with | no team input | 070 #10, 072 #25 and #26, 080 #9, 053 hot takes | A position that risks followers (076 Monday). |
| mythbuster | Mythbuster or strategic reframe: what everyone believes, why it is wrong, what to do instead | no team input | 098 #1, 080 #2 | |
| industry-prediction | Bold industry prediction, tied to the account's expertise | no team input | 070 #8, 072 #29 | |
| emerging-trend | A trend the ICP does not know yet and needs to know | no team input | 070 #7, 053 trend riding | Research-led. Public sources only, cited. |
| news-take | News take (newsjacking): what a news story means and how it changes the space | no team input | 098 #2, 053 newsjacking | Only for a slot within 48 hours of a news link the person supplied this week (098); otherwise the slot is `needs input: news link on the day`. This pack fetches no news itself. |
| viral-take-reaction | Reaction to a viral industry take or a negative post | no team input | 072 #28, 070 #4 | Only for a slot within 48 hours of a link to the take that the person supplied; otherwise the slot is `needs input: news link on the day`. React to the idea, quote it accurately, never mock the author. |
| namejacking | A named public figure's public statement, used as the hook | no team input | 053 namejacking | Public statements only, quoted accurately and attributed. Never implies endorsement. |
| authority-curation | A dense, researched list tied to a bigger-name authority | no team input | 070 #6 | Research-led. Every item cited. |
| bad-tactic-callout | A bad tactic the ICP still uses, called out | no team input | 070 #12 | |
| hidden-cost | The hidden cost of the buyer's current process | no team input | 072 #4 | 047 Tuesday ("[problem] is costing [role]s [thing]"). |
| ai-opinion | A distinct opinion on AI in the ICP's work | no team input | 076 Wednesday (kept for the template, not one of the five banks; record `076`) | |
| hiring-opinion | An opinion on team building or hiring | no team input | 076 Monday (not one of the five banks; record `076`) | A view, not a story about a real hire. |
| infographic | A process explained often, as one step-by-step image | no team input | 098 #3 | Media: infographic (linkedin-post media table). |
| origin-story | Origin story, why the product was built, the moment the founder decided | needs team input | 070 #15, 072 #31 and #32, 080 #3 | 047 Thursday ("X years ago, I started [business]"). A measurable transformation only from the ledger. |
| mistake-story | Biggest mistake, failed experiment, and what was learned | needs team input | 072 #33 and #34, 080 #6 | Only a mistake that has a resolution (080). |
| difficult-decision | A difficult decision as a founder | needs team input | 072 #35 | |
| changed-my-mind | Something the poster changed their mind about | needs team input | 072 #30 | |
| room-you-werent-in | What was learned in a room the reader was not in | needs team input | 070 #1 | Nothing confidential from the room. |
| day-in-the-life | A relatable day in the life | needs team input | 080 #7 | Personal accounts mainly. |
| starting-again | Advice wished for before starting, and the plan for a fresh start | needs team input | 072 #36 and #37 | |
| tech-stack-roundup | Breakdown or roundup of the tech stack | needs team input | 072 #16 | 076 Wednesday: companies tagged by the person. |

## Trust

| id | Type | Input | Banks | Notes |
|---|---|---|---|---|
| framework | A stealable decision framework | no team input | 072 #15 | 076 Tuesday. |
| pain-plus-framework | A pain point straight into a practical framework | no team input | 070 #13 | |
| wrong-vs-right | Wrong way versus right way to an outcome, image-based | no team input | 070 #11 | |
| if-i-were | "If I were [the ICP] trying to get [outcome]" | no team input | 070 #5 | 076 Thursday. Third person on the Page. |
| checklist | A checklist for the ICP | no team input | 072 #7 | Research-led. |
| template | A template for the ICP to copy | no team input | 072 #13 | |
| step-by-step | A step-by-step guide or workflow to solve a buyer problem | no team input | 072 #12 | 076 Thursday ("a workflow to steal"). |
| pro-tips | A list of pro tips | no team input | 076 Thursday (not one of the five banks; record `076`) | |
| industry-commentary | Industry commentary | no team input | 072 #27 | Research-led. 076 Tuesday. |
| big-brand-teardown | How a recognisable company solves a buyer problem, or its strategy | no team input | 070 #9, 072 #23, 053 brandjacking | Research-led. 076 Tuesday. Public information only. |
| icp-mistake | A common mistake the ICP makes, and the fix | no team input | 072 #1 | |
| workaround | A common workaround worth a look | no team input | 072 #5 | |
| comparison | A comparison of ways to solve a buyer problem | no team input | 072 #8 | Research-led. Fair to the alternatives. No competitor claim without a source. |
| simulated-conversation | A simulated conversation that teaches prospects something | no team input | 070 #2 | Playbook section 6 has the format. Clearly a constructed exchange, not a real customer. |
| behind-the-scenes | Behind the scenes: how the work or the results are delivered | needs team input | 080 #5, 072 #39 | 068 day 2. |
| behind-the-numbers | Real numbers, the mistakes behind them, what was learned, or a surprising fact from own data | needs team input | 098 #4, 072 #24 | Numbers only from the person or the ledger. |
| process-highlight | A highlight of the company's own process | needs team input | 072 #14 | |
| build-trade-off | A trade-off made while building the product or service | needs team input | 072 #9 | |
| unusual-tactic-result | An unusual tactic and its result | needs team input | 070 #3 | The result from the ledger only. |
| resource-giveaway | A proven internal resource, given away | needs team input | 070 #14 | The person supplies the resource. |
| milestone | A company milestone and the work behind it | needs team input | 072 #40 | |
| hiring-approach | The company's approach to hiring | needs team input | 072 #38 | For a live role, a job post instead. |
| use-case-walkthrough | A walkthrough of one use case | needs team input | 072 #11 | |
| recurring-series | The account's recurring series (newsletter, video or post series) | needs team input | 080 #8 | Only the series the strategy page names. |
| customer-story | Customer lesson, a customer's first win, landing the first customer | needs team input | 072 #20, #21 and #22 | Carries the review mark that `[screening-rules]` names for customer data in public posts. Approved facts ledger entries only. |

## Convert

| id | Type | Input | Banks | Notes |
|---|---|---|---|---|
| case-study | Case study: one customer, where they were stuck, what changed, what happened next, before and after, or a testimonial with its story | needs team input | 098 #6, 080 #1, 072 #17, #18 and #19 | 076 Friday ("a recent customer result"), 068 day 3, 047 Wednesday. Carries the review mark that `[screening-rules]` names for customer data in public posts. Approved facts ledger entries only. A missing number is `{{your number}}`. |
| objection-crusher | An objection heard on sales calls, and how it is handled | needs team input | 098 #5, 072 #3 | 076 Friday. Only objections the person supplied. |
| sales-call-faq | The answer to a question asked on sales calls | needs team input | 072 #2 | 076 Friday. Only questions the person supplied. |
| offer-breakdown | Who the company works with, how, the outcome, what working together looks like | no team input | 080 #4 | From the strategy page's offer. Outcome claims only from the ledger. |
| best-suited-for | Who the product or service is best suited for, and who it is not | no team input | 072 #10 | From the strategy page. |
| buyer-criteria | Buyer criteria worth considering | no team input | 072 #6 | |

## Customer data rule

`case-study` and `customer-story`, and any slot that names a customer or a result, carry
the review mark that `[screening-rules]` names for customer data in public posts, in
the plan table and the receipt. A customer name, result or metric comes only from an approved facts
ledger entry: the planner reads the ledger (`./campaigns/linkedin/facts-ledger.md`) before using any
customer outcome, and the plan table's FLAGS column carries the mark. The person's answer to the
week's question is not a ledger entry: a customer outcome the person gives goes into a post only
after it is in the ledger. Until then the slot is `needs input`.

## Not types

- **Relatable story** (068 days 1, 4, 5) and **unique methodology** (068 day 2) are template slots.
  Choose a reach or trust type from this bank for them.
- **Recurring content** (080 #8) is `recurring-series` above, not a new series.
- **080 #10** was not captured in the source. It is not a type.

File: linkedin-weekly-plan/references/post-type-bank.md · Version 1.0 · November 2026
