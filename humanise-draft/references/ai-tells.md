# AI tells

Structural and phrase-level signs that a text reads as machine-written. Used to find lines worth a second look. A hit is a candidate to read, not a defect. A hit does not show a text is machine-written, an empty list does not show it is human, and a scan never certifies a text as human.

## Tells a scan can flag

Each tell carries the checker's weight: 1 is the strongest signal and 3 the weakest. The run of near-equal sentences fires on human text too.

| Tell | Example | Weight |
|---|---|---|
| Negative parallelism (not just/only X but Y) | This is not only a [product] but also a market. | 1 |
| Negative parallelism (it is not X, it is Y) | It's not a [product], it's a platform. | 1 |
| Contrast pair (X is a N. But Y is a M.) | [figure] is a count. But the headline figure is a comparison. | 1 |
| No X, no Y, just Z | No hype, no fluff, just results. | 1 |
| Announced count / scaffold | Three things a [product] waits for | 1 |
| Tidy closing. Flags: what to take from this; the takeaway; in the end, it comes down; in summary; in short,; in conclusion; ultimately,; at the end of the day | What to take from this: the [product] matters. | 1 |
| Narration about the piece (scaffold opener). Flags: Now,; So,; Then there's; Next,; Let's; Here's; Back to; Another meaning, question, way or thing | Fine. Now, how much does it reach? Other text. | 3 |
| Significance inflation. Flags: stands as; serves as a testament; a testament to; pivotal moment; underscores, underscoring; plays a vital, crucial, key or important role; broader trend, landscape or context; evolving landscape; indelible mark; setting the stage | The [product] stands as a testament to the era and plays a vital role. | 2 |
| Vague attribution. Flags: experts argue, say or believe; observers have or note; industry reports or observers; some critics; many believe or argue; it is widely believed or held | Experts argue that the number is high. | 2 |
| Trailing participle verdict. Flags: after a comma: highlighting, underscoring, emphasising, reflecting, showcasing, contributing to, fostering, ensuring, enhancing, symbolising | The firm built a plant, highlighting its commitment. | 2 |
| Copula avoidance. Flags: serves as; stands as; functions as; boasts; marks the; represents a | The [product] serves as a [topic] tool. | 3 |
| Formal connective / hedge opener. Flags: moreover; furthermore; additionally; it's worth noting; it is important to note; when it comes to | Moreover, the [product] is dense. | 3 |
| Claude-flavoured stock phrase. Flags: the one thing you need; honest caveat; smoking gun; load-bearing; that's precisely; here's the thing; to be clear, | Honest caveat: it is slow. | 3 |
| Refrain: the same first four words open three or more sentences (sentences of five words or more) |  | 1 |
| Run of four or more consecutive sentences whose lengths are within three words of each other |  | 3 |

## Tells read by judgement

No scan flags these. Each is read in context.

- Promotional register ("vibrant", "rich", "nestled", "groundbreaking"), travel-guide or advertisement tone
- Vague connection: "in connection with", "associated with"
- Em dash frequency (measured, not presence): human baseline about 3.2 per 1,000 words; the house rule bans them outright
- Perfect grammar and punctuation throughout, no minor irregularity
- Overformal or over-mirrored quotes: quotations that sound like the surrounding prose
- Rule of three and equal-weight lists: three parallel items, adjectives or clauses by default
- A question posed and defused at once, or a rhetorical question answered in the next breath
- Even, safe, surprise-free content: nothing a reader would not have guessed; no named specific, no friction, no point of view
- Over-explanation: restating what was just shown, or explaining a term the audience knows
- No narrator: sources summarised in order with no stake, opinion or turn (the regurgitation tell)
- The planted hook with a closing callback: a question posed with "hold on to the answer", paid off by "whatever you guessed at the start"
- Enumerate then tally: a list of parallel meanings, then "that makes five things", then a rule
- The aphoristic paragraph closer: a short quotable line that ends each paragraph ("A [product] count can't tell you which ...")
- An even gloss after every term: a definition in an appositive for each term of art, in uniform packets
- No person: no named employer, project, place or aside, no hedge, no digression, nothing only someone who did the work would know
- The abstract placeholder noun: a generic noun standing for what a person would name ("a figure about X", "a count of [product]s", "tells you scale", "the count with repeats")

## Vocabulary: read as a cluster

A cluster of several of these in one text is a signal; one or two are coincidence. A word list is a depreciating asset: read a flagged paragraph, never scan for single words.

- 2023 to mid-2024: delve, tapestry, testament, intricate, meticulous, garner, landscape, pivotal, underscore
- Mid-2024 to mid-2025: align with, bolstered, fostering, highlighting, showcasing, enduring
- Mid-2025 onward: emphasising, enhance, highlighting, showcasing

## Formatting and leftovers

Overuse of boldface, inline-header bullet lists, title case, emoji as formatting, unusual tables; chatbot residue ("I hope this helps", knowledge-cutoff disclaimers, placeholder text); citation markup residue by model family. A script or caption should have none.

## Repair

Name the defect and fix it at its source. Do not repair by adding a fragment or varying the rhythm: that manufactures a detectable tell. What reads as human is a specific only the writer could know, an opinion with a cost, a minor mess that is not even, and a change of mind inside the piece. These are absences to supply from the work, never textures to apply.

## Limits

Nothing here has been validated on readers of the company's own content. The vocabulary tier ages fastest, and newer models avoid some older tells and invent others, so the list needs refreshing. The final judgement is a human reader's.

---

Reference: ai-tells | Version: 1 | November 2026 | Source wording read 6 November 2026

File: humanise-draft/references/ai-tells.md · Version 1.0 · November 2026
