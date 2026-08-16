# AI Writing Patterns — Sentence-Shape Tells

Companion to `llm-words-to-avoid.md` (vocabulary) and `content-humanizer/references/ai-tells-checklist.md`
(structure and rhythm). This file covers the third layer: **sentence shapes**.

The distinction matters. A word list catches *which* words a draft uses. The metrics helper catches *how
the paragraphs are built*. Neither catches a sentence that is constructed the way a model constructs
sentences — "serves as," the tacked-on "-ing" clause, the false range, the aphorism. Those survive a
find-and-replace pass and a burstiness check untouched, which is exactly why they read as AI after
everything else has been cleaned.

Patterns adapted from `blader/humanizer` v2.9.1 (MIT), which derives from
[Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
Patterns that duplicate the existing lists, or that fight the SEO conventions in this library, were
deliberately left out (see "What we deliberately do not adopt" at the end).

**When to run this:** Phase 5, after the word-level sweep. Also the second pass of the Phase 7 Editorial
Line-Edit Audit, where it is flag-only.

Examples throughout use an invented product (the "TX-200") so the before/after pairs stay concrete
without tying the rule to any one vertical.

---

## Part 1: The fourteen patterns

### 1. Copula avoidance

Models substitute elaborate constructions for plain *is* and *has*.

**Watch:** serves as, stands as, marks, represents, acts as, functions as, boasts, features, offers,
provides, comes equipped with

**Before:**
> The TX-200 series serves as a workhorse for demanding users and boasts an impressive runtime.

**After:**
> The TX-200 is a 1,200Wh portable power station rated for 12 hours at a 100W draw.

**The test:** could this sentence use *is*, *are*, or *has* without losing meaning? If yes, use it. Plain
copulas read as a spec sheet, which is exactly the primary-source register the Phase 5 comparison rules
already ask for.

**Not a violation:** "delivers 900W of continuous output" — *delivers* is doing real work there. Flag it
only when it stands in for *has*.

---

### 2. Superficial "-ing" analyses

A present-participle clause tacked onto the end of a sentence to simulate depth. It adds no fact.

**Watch:** highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to,
showcasing, allowing for, making it, further cementing

**Before:**
> The unit switches to battery in under 20 milliseconds, ensuring uninterrupted operation and
> highlighting the importance of choosing the right backup solution.

**After:**
> The unit switches to battery in under 20 milliseconds. Desktop computers typically tolerate a gap of
> about 16 milliseconds before they reboot, so the margin is thinner than it sounds.

**The test:** delete the "-ing" clause. If no fact is lost, it was decoration — and the space it occupied
should carry a number instead.

---

### 3. Negative parallelisms and tailing negations

Two shapes, same origin. The first inflates an ordinary claim by denying a smaller version of it. The
second bolts a clipped negative fragment onto a finished sentence.

**Watch:** "Not only… but also," "It's not just X, it's Y," "This isn't about X. It's about Y,"
and trailing fragments: *no guessing, no wasted motion, no surprises, no compromises*

**Before:**
> It's not just a battery, it's a complete backup system.
> Sizing comes from your actual device list, no guesswork.

**After:**
> The kit includes the battery, the inverter, and a 200W solar panel.
> Sizing comes from your actual device list rather than a wattage rule of thumb.

The tailing negation is the sneakier one — it reads as punchy rather than padded, so it survives editing
passes that catch "not only… but also."

---

### 4. Hyphenated pair overuse

Models hyphenate compound modifiers uniformly, including in predicate position. Human writers hyphenate
attributively and usually drop it after the noun.

| Position | Form | Example |
|---|---|---|
| Attributive (before noun) | **Keep** the hyphen | a high-quality build, a long-term warranty |
| Predicate (after noun) | **Drop** the hyphen | the build is high quality, the warranty is long term |

**Watch:** high-quality, real-time, long-term, heavy-duty, data-driven, end-to-end, well-known,
decision-making, cross-functional, entry-level

**Before:**
> The casing is heavy-duty, the controls are user-friendly, and the warranty is long-term.

**After:**
> The casing is heavy duty, the controls are user friendly, and the warranty is long term.

**SEO guardrail — read this before applying:** never alter the hyphenation of a primary or secondary
keyword, or any term in `KEYWORD-REGISTER.csv`. If the hyphenated form *is* the search term
("solar-powered generator," "wall-mounted heater"), it keeps its hyphen in every position, predicate
included. This rule applies to incidental prose compounds only. When in doubt, check the register first
and leave it alone.

Also exempt: manufacturer product names, spec-table cells, and anything inside a quotation.

---

### 5. False ranges

"From X to Y" where X and Y do not sit on a shared measurable scale. It performs comprehensiveness
without stating anything.

**Before:**
> From weekend camping trips to whole-home backup, from phone charging to running power tools, the right
> unit changes everything.

**After:**
> Charging a phone draws about 20W. Running a circular saw draws 1,400W. Size for the highest-draw device
> you plan to run, not the average.

**The test:** are the two endpoints on one axis with a middle? *"$500 to $3,000"* and *"20W to 1,400W"*
are real ranges — keep them. *"From hobbyists to professionals"* is not; it is two nouns wearing a range
costume.

This one concentrates in listicle and buying-guide intros, which is where comparison and roundup articles
start.

---

### 6. Persuasive authority tropes

Phrases that promise to cut through noise to a deeper truth, followed by an ordinary point.

**Watch:** the real question is, at its core, in reality, what really matters, fundamentally, the deeper
issue, the heart of the matter, here's the truth, make no mistake

**Before:**
> The real question isn't capacity. At its core, what really matters is understanding your power needs.

**After:**
> Capacity is the wrong spec to shop on. Continuous output in watts decides whether your devices run at
> all.

The brand voice is allowed to be blunt and to pick a winner. The tell is the *ceremony before* the claim,
not the claim. Cut the runway, keep the take.

---

### 7. Aphorism formulas

An ordinary claim reshaped into a portable maxim. Sounds quotable, says less than the plain version.

**Watch:** "X is the Y of Z," "X becomes a trap," "X is not a tool but a Y," the language of, the currency
of, the architecture of, the backbone of, the lifeblood of

**Before:**
> Watt-hours are the currency of portable power. Peak output is the vanity metric of the industry.

**After:**
> Watt-hours measure how long the unit runs. Peak output only tells you what it can start, not what it can
> sustain.

Note the interaction with the GEO rules: aphorisms *feel* like citation capsules because they are
self-contained and quotable. They are not. A capsule carries a claim, a number, and a source. An aphorism
carries a metaphor. AI answer engines score the first and discard the second.

---

### 8. Fragmented headers

An H2 followed by a one-line paragraph that restates the heading before the real content starts.

**Before:**
> ## Cycle Life
>
> Cycle life matters.
>
> Charging past the rated cycle count degrades capacity and shortens service life…

**After:**
> ## Cycle Life
>
> Charging past the rated cycle count degrades capacity and shortens service life…

**Do not confuse this with the Answer-First H2 Rule.** The required 40-60 word opener — stat, source,
direct answer — is the section's first paragraph and stays. A fragmented header is a contentless
restatement sitting *in front of* that opener. If the first line after the H2 carries no fact, cut it; the
answer-first block moves up to take its place.

---

### 9. Speculative gap-filling

When a model cannot find a source, it writes a sentence about not finding one, then fills the hole with
plausible-sounding filler.

**Watch:** while specific details are limited, based on available information, not publicly available,
it is believed that, likely, generally accepted, as of [date], industry consensus suggests

**Before:**
> While specific cycle-life test data for this model is limited, it likely performs comparably to other
> lithium units in its class.

**After:**
> The manufacturer does not publish cycle-life test data for this model.

Or cut the sentence. Both are fine; the invented comparison is not.

This is the same rule as the Phase 7 fact pass, arriving one phase earlier. An unverified number gets
flagged **unverified**, not softened with "likely" until it reads as sourced. Hedging is not a substitute
for a citation.

---

### 10. Elegant variation (synonym cycling)

Referring to one thing by a rotating cast of synonyms across consecutive sentences, because the model is
penalised for repetition.

**Before:**
> The unit draws 22 amps. The device requires a dedicated circuit. The machine will trip a shared breaker.
> The system needs 10-gauge wire.

**After:**
> The unit draws 22 amps, so it needs a dedicated 30-amp circuit wired in 10-gauge. On a shared breaker it
> will trip.

**SEO guardrail — this does not cancel the NeuronWriter guidance.** Phase 1 tells you to mix terms with
synonyms for variety, and that still stands: vary vocabulary **across the article**, so the piece covers
the full term set rather than hammering one phrase. The tell is narrower — cycling names for the **same
referent in consecutive sentences**. Inside a paragraph, one thing keeps one name.

---

### 11. Chatbot artifacts, emojis, and quote marks

Three cheap mechanical scans. Run them last.

**Chatbot artifacts** — conversational scaffolding pasted in with the content: *I hope this helps,
Certainly!, Of course!, Would you like me to, Let me know if, Here is an overview of, Should I continue?*
These should never reach a draft. Scan anyway; they survive copy-paste more often than you would expect.

**Emojis** in headings and body prose: cut. 🚀 ✅ 💡 in an H2 or a bullet is a chatbot formatting habit,
not a brand choice. A ✓ or ✗ inside a comparison-table cell is a legitimate formatting decision and stays.

**Quote marks** — a weak signal, handled honestly. Curly quotes on their own prove nothing: Word, Google
Docs, and most CMSes auto-curl, and pandoc curls straight quotes on the way to HTML regardless of what the
`.md` contains. Do **not** chase them. What *is* worth a look: **mixed** straight and curly quotes inside
one document, which usually means a block was pasted in from somewhere else and deserves a fact check.

---

### 12. Significance and legacy inflation

Asserting that something matters instead of showing why. The model reaches for importance it has not
earned, usually in brand, vendor, or "about the manufacturer" blocks where it has the fewest facts.

**Watch:** cemented its position as, marked a turning point, stands as a testament to, has revolutionised
the industry, left an indelible mark, cornerstone of, paved the way for, enduring legacy, a defining
moment in

**Before:**
> Founded in 1935, the company has cemented its position as a cornerstone of the American manufacturing
> industry, leaving an indelible mark on generations of workshops.

**After:**
> The company has built its units in the same Ohio plant since 1935, and ships them with a 10-year
> warranty where most competitors stop at five.

Several of these words (*testament, enduring, indelible*) are already on the Ctrl+F list. This pattern is
the sentence *shape* that survives swapping them out — "has established itself as a leading provider"
contains no flagged word and commits the same offence.

**SEO guardrail — this does not weaken E-E-A-T.** Phase 3 asks you to establish authority, and that still
stands. The difference is direction: authority is **demonstrated** with dated specifics, warranty terms,
certifications, and production facts, then the reader concludes it matters. Inflation **declares** the
conclusion and supplies nothing. Cut the declaration, keep the facts — the section usually gets shorter
and stronger.

---

### 13. Formulaic outlook sections

A closing section that exists because the template expects one, not because there was anything left to
say. Generic tensions, hedged predictions, no dated specifics, no position.

**Watch (H2s):** Challenges and Future Prospects, Challenges and Opportunities, The Future of X, Looking
Ahead, What's Next for X, Final Thoughts

**Before:**
> ## Challenges and Future Outlook
>
> While these units offer many advantages, challenges remain. Cost and maintenance requirements continue
> to be considerations for many businesses. Looking ahead, the industry is expected to evolve as
> technology advances and efficiency demands increase.

**After:**
> Cut the section. If nothing dated and specific belongs here, its absence is an improvement.

Or replace it with a real one:

> ## What Changes in 2027
>
> The current cell chemistry is being phased out across the 2027 model year, and the replacement carries a
> different charge profile. If you are buying this year, confirm which chemistry ships in your unit — the
> outgoing stock is discounted now, and the two are not cross-compatible for warranty purposes.

The test is whether the section survives being read by someone who already knows the topic. Dated
specifics, a named source, and a stated position pass. Hedged futurology does not.

**This is the "Challenges" section named in the cluster test in Part 2.** It rarely appears alone — it
usually arrives with a rule-of-three and an *evolving landscape*.

**SEO guardrail — do not confuse this with information gain.** Phase 2 rewards a forward-looking angle
competitors lack, and a genuine trends section is exactly that. Keep the one that carries a date, a
source, and a consequence. Cut the one that hedges.

---

### 14. Subjectless fragments

A noun phrase punctuated as a sentence, continuing the previous subject instead of stating one. Endemic
in product roundups, where the model runs a spec sentence and then trails verdict fragments after it.

**Before:**
> The unit sustains 40 amps continuous. Ideal for workshops running multiple tools at once. A solid choice
> for anyone needing steady output.

**After:**
> The unit sustains 40 amps continuous — enough for a workshop to run two tools off the same circuit
> without the supply sagging.

The fragments carried no fact the first sentence did not already imply. Fixing them usually merges the
pile into one sentence that says more.

**SEO guardrail — this is not a ban on short sentences, and the distinction is narrow.** Phase 5 requires
one sentence under eight words per paragraph, Part 2 protects the single emphatic fragment, and both
still stand. A deliberate fragment lands a point the reader feels: *Really. Not even close.* A subjectless
fragment makes the reader reconstruct a subject the model dropped. Ask what work it does — emphasis, or
a dropped subject. Emphasis stays.

Upstream pairs this with passive voice, which is already handled: `humanizer_scorer.py` scores passive as
one of its six dimensions and the Phase 7 QA gate caps it at 10% of sentences. Only the fragment half was
missing.

---

## Part 1B: Statistical and journalism tells

Patterns 1-14 describe sentence *shapes*. This group is different in kind and comes from a different
source: a 2026 corpus study of 55,940 sentences and 1.2m words comparing ChatGPT, Claude, Gemini and Grok
against professional journalism and bestselling fiction, plus a 2025 detection study. These are
**distributional** tells. Each one is a measurable difference in how often a model reaches for something,
not a phrase you can Ctrl+F once and be done with.

That makes them the layer under everything above. A draft can pass all fourteen patterns and still read as
machine-written because its words are a little too long, its punctuation a little too sparse, and its
sentences chained with "and" instead of cut.

Adapted from `ama-zingco/anti-ai-writing-skill` (MIT). Its own warning applies and is worth repeating: **the
tells decay.** Two of its rules reversed between 2025 and 2026 because models train on the feedback that
flags them. Date-stamp anything you adopt here.

---

### 15. Long Latinate words

Word length is one of the cleanest human/machine separators measured. Every major model writes far more
eight-letter-plus words than journalists do. The fix is Anglo-Saxon over Latinate, not "simpler writing."

**Watch:** utilize, facilitate, commence, demonstrate, approximately, additional, sufficient, requirement,
implement, individual, purchase, obtain, assistance, initiate

**Before:**
> Operators should utilize the controller to facilitate additional capacity when requirements exceed
> approximately 40 amps.

**After:**
> Use the controller to add capacity when the load goes past 40 amps.

Twenty-two words become thirteen and nothing is lost. **Do not flatten a precise technical term**, though.
Words like *reciprocating* or *displacement* are long because they are exact. The rule targets long words
chosen over short synonyms, not long words that carry meaning.

---

### 16. Nominalizations

Models turn verbs into nouns and then need a weak verb to carry the sentence. The buried verb is almost
always the better one.

**Watch:** conducted an evaluation of, performed an inspection of, provides protection for, offers
improvement in, made the decision to, gives consideration to, is a requirement of

**Before:**
> We conducted an evaluation of the unit and made a determination that replacement was necessary.

**After:**
> We inspected the unit and decided to replace it.

Fastest scan: search `-tion `, `-ment `, `-ance ` and `-ity `. Where one sits next to a colourless verb
(*conducted, performed, provides, offers, made*), the verb is hiding in the noun.

---

### 17. Overuse of "and"

"And" is the single most overused word in model prose, and it is the mechanism behind their long
sentences: clauses get chained rather than cut. This pattern is the cause; pattern 23's burstiness
failure is the symptom.

**The check:** find any sentence with two or more "and"s. Try replacing one with a period.

**Before:**
> The unit sustains 40 amps and needs a dedicated circuit and most buyers undersize the wiring, and then
> they wonder why the breaker trips.

**After:**
> The unit sustains 40 amps, so it needs a dedicated circuit. Most buyers undersize the wiring, then
> wonder why the breaker trips.

Most of the time the sentence improves and the paragraph picks up rhythm. Not every "and" is a fault:
a genuine list needs them. Two or more in one sentence is the trigger to look, not an automatic cut.

---

### 18. Adverb density

Models lean on adverbs, especially `-ly` forms, where a stronger verb would do. *Increasingly* is the
worst offender measured across all major models.

**Watch:** increasingly, significantly, dramatically, effectively, essentially, particularly, notably,
consistently, ultimately, simply, truly, incredibly

**Before:**
> These units are increasingly popular because they significantly reduce heat and dramatically extend
> service life.

**After:**
> These units run cooler, and they last roughly twice as long.

Note what the rewrite did: it replaced the adverbs with a number. That is usually the move. An adverb is
often a placeholder where a specific quantity belongs.

---

### 19. Punctuation scarcity

The counterintuitive one, and the reason the dash rule has a corollary. Models use **fewer** commas,
semicolons and parentheses than human writers, and hardly any parentheses at all. Two causes: they write
longer sentences, and they rarely quote anyone.

So a naive de-AI pass makes things worse. Strip the em dashes, delete the punctuation, let the sentence
run long, and the draft now trips a stronger signal than the one it was cleaning.

**The rule:** every dash you remove becomes a comma, semicolon, colon, or parentheses. Never nothing.

**Before (dash removed badly):**
> The larger capacity handles intermittent work fine it is sustained load that kills entry-level units and
> most buyers do not find that out until the warranty has expired.

**After:**
> The larger capacity handles intermittent work fine; sustained load is what kills entry-level units. Most
> buyers do not find out until the warranty has expired.

**The scan:** read a paragraph and count commas, semicolons and parentheses. If a 100-word paragraph has
three or fewer marks total, it is almost certainly too sparse. Long sentences with no internal punctuation
are the signature.

---

### 20. Contrast framing

Manufacturing tension between two things that are not actually in tension, using *while* or *although* as
the hinge. Distinct from pattern 3, which covers *"not just X but Y."*

**Watch:** While X, Y. Although X, Y. Though X, Y. Despite X, Y.

**Before:**
> While the premium tier costs more upfront, it offers better performance under continuous use.

**After:**
> The premium tier costs more and runs continuously. The entry tier is cheaper and needs to rest.

The rewrite states both facts flatly and lets the reader weigh them. The original implies a paradox that
was never there: higher price and higher duty rating are the same fact seen twice.

Ordinary contrast is fine. The tell is **frequency** and the reflex to open with it.

---

### 21. Hypophora

Posing a question and answering it immediately, in body prose, as a way to manufacture momentum.

**SEO guardrail - this does NOT apply to headings, and the distinction is the whole point.** The
Answer-First H2 Rule stays. The 20-25 word answer capsule after a question-based H2 stays. Those are
document *structure*, they are what gets a page cited, and roughly three-quarters of ChatGPT-cited pages
use them. Nothing in this pattern touches Phase 3 or Phase 6.

The tell is narrower: a rhetorical question **inside a paragraph**, answered in the next breath, doing
decorative rather than structural work.

**Before:**
> So what does that mean for your setup? It means you need at least 40 amps of continuous headroom.

**After:**
> A setup running two tools at once needs at least 40 amps of continuous headroom.

Watch for *So what does that mean? Why does this matter? The answer? What is the catch?* If cutting the
question loses nothing, it was decoration.

---

### 22. Attribution verbs

Humans writing about sources repeat "says" and do not care. Models rotate through descriptive synonyms to
avoid repetition, which reads as a thesaurus at work.

**Watch:** notes, explains, emphasizes, highlights, observes, points out, stresses, underscores, remarks,
adds, cautions

**Before:**
> The manufacturer notes that the unit is rated for continuous duty. A competitor emphasizes ease of
> service, while a third highlights its warranty.

**After:**
> The manufacturer says the unit is rated for continuous duty. A competitor says its unit is easy to
> service. A third says its warranty runs ten years.

Default to *says* or *said* and let it repeat. Repetition here is invisible to readers and its absence is
not. This connects to pattern 10: elegant variation applied to verbs instead of nouns.

---

### 23. Quote homogeneity and invented experts

Two related failures around sourcing.

**Models barely quote anyone.** That absence is itself a tell, and it is partly what drives pattern 19,
since quoted speech brings commas and parentheses with it.

**When they do quote, every speaker sounds identical** - to each other and to the surrounding article.
Model-written quotes are complete sentences that state a position perfectly and match the article's
register exactly. Real quotes are short, uneven, and sound like a specific person. If you could swap two
speakers' quotes without anyone noticing, they are not real.

**Invented experts** are the extreme case. Models reuse the same fictional names and hand out *Dr.*
regardless of field. A quick scan is enough here, because Phase 1.5 already requires verified sources:
**every named person in a draft must trace to a real, checkable source.** No exceptions, and a name you
cannot verify gets cut rather than softened.

---

### Vocabulary additions

Words from the upstream high-frequency list not currently in `llm-words-to-avoid.md`. Add them to the
Ctrl+F sweep; full entries are not needed.

```
garner, interplay, showcase, testament, enduring, valuable,
align with, key (as an adjective: "a key factor")
```

---

## Part 2: What NOT to flag

Every rule above deletes text. Without a counterweight, a humanization pass run by a scorer plus a QA gate
that long will sand a good article down to a flat one. Real writers hit these patterns constantly.

None of the following is evidence of AI writing on its own:

- **Perfect grammar and consistent style.** Professionals get edited. Polish is not a tell.
- **Formal or academic vocabulary.** Models overuse *specific* fancy words (see `llm-words-to-avoid.md`),
  not all of them. Do not flatten a precise technical term because it sounds elevated.
- **One transition word.** *Additionally* becomes AI-coded when stacked across consecutive sections. A
  single *however* is a sentence doing its job.
- **A single em dash.** Editors use them. Evidence only alongside other tells.
- **Curly quotes alone.** See pattern 11 — the toolchain produces these.
- **One short emphatic sentence.** Humans land points that way. See the staccato bound in Phase 5.
- **"Honestly" or "look" mid-sentence.** Ordinary in candid writing. The tell is the standalone theatrical
  pause, not the word.
- **Bland prose.** AI has *specific* tells. Dry writing without them is just dry.
- **Mixed casual and formal register.** Common in trade and practitioner writing.
- **Correct, complex formatting.** Tables and clean structure come from templates.
- **Unsourced claims.** A sourcing problem, not an AI problem. Route it to the fact pass, not here.
- **Secondhand text.** Never rewrite a watched phrase inside a quotation, a product name, a manufacturer's
  spec language, or an example where the phrase is being discussed rather than used.

**Look for clusters, not instances.** One em dash means nothing. An em dash plus a rule-of-three plus
*"the evolving landscape"* plus a "Challenges" section is a confession.

---

## Part 3: Signs of human writing — preserve these

When a passage shows these, leave it alone. Over-editing here is how a humanization pass makes an article
*less* human, and it is the failure mode worth guarding against most.

- **Specific, hard-to-fabricate detail.** A real part number. An odd figure. "The site that ran three
  space heaters off one 15-amp circuit until the breaker gave out." Models round specifics off; people
  hoard them.
- **Mixed feelings and unresolved tension.** "This is the better buy for most people, but the service
  network bothers me and I can't fully justify why." Models default to clean verdicts.
- **Variety in sentence length.** Real writing alternates. Do not regularise it.
- **Genuine asides and self-corrections.** Parentheticals, interruptions, a walked-back claim.
- **First-person editorial choices the writer can defend.** If there is a reason behind the word, it is a
  human signal.
- **Dated, era-bound references.** Specific years, model generations, a rule change that landed in a
  particular quarter.
- **Admitted limitations.** Already required by the Phase 5 checklist — this is the same signal viewed
  from the detection side.

---

## Part 4: Quick scan

Phase 7 Editorial Line-Edit Audit — flag, do not rewrite. One row per hit.

| # | Pattern | Fastest check |
|---|---|---|
| 1 | Copula avoidance | Ctrl+F: serves as, stands as, boasts, features, offers |
| 2 | "-ing" decoration | Ctrl+F: ensuring, highlighting, showcasing, reflecting, allowing for |
| 3 | Negative parallelism | Ctrl+F: "not just", "not only", ", no " |
| 4 | Predicate hyphenation | Ctrl+F each compound; check register before changing |
| 5 | False ranges | Ctrl+F: "from " — check both endpoints share a scale |
| 6 | Authority tropes | Ctrl+F: at its core, the real question, fundamentally |
| 7 | Aphorism formulas | Ctrl+F: the currency of, the backbone of, " is the " |
| 8 | Fragmented headers | Read the first line under each H2 — does it carry a fact? |
| 9 | Speculative gap-fill | Ctrl+F: likely, it is believed, details are limited |
| 10 | Synonym cycling | Read consecutive sentences — one referent, one name |
| 11 | Artifacts / emoji / quotes | Ctrl+F: "I hope", emoji in headings, mixed quote styles |
| 12 | Significance inflation | Ctrl+F: cemented, testament, cornerstone, paved the way, turning point |
| 13 | Formulaic outlook section | Read the last H2 — any date, source, or position in it? |
| 14 | Subjectless fragments | Scan for sentences opening with an adjective: Ideal for, Perfect for |
| 15 | Long Latinate words | Ctrl+F: utilize, facilitate, commence, demonstrate, approximately |
| 16 | Nominalizations | Ctrl+F: `-tion `, `-ment ` next to conducted/performed/provides/made |
| 17 | Overuse of "and" | Any sentence with 2+ "and" - try one as a period |
| 18 | Adverb density | Ctrl+F: increasingly, significantly, dramatically, effectively |
| 19 | Punctuation scarcity | Count marks per 100 words - 3 or fewer is too sparse |
| 20 | Contrast framing | Ctrl+F: "While ", "Although ", "Despite " at sentence start |
| 21 | Hypophora (body prose only) | Ctrl+F: "So what does", "Why does this matter", "The answer?" |
| 22 | Attribution verbs | Ctrl+F: notes, explains, emphasizes, highlights, observes |
| 23 | Quote homogeneity / invented experts | Could two speakers swap quotes unnoticed? Every name checkable? |

---

## What we deliberately do not adopt

Recorded so the next sync does not re-litigate these.

- **Title case in headings.** Upstream flags it. The H2 conventions in this library are title-cased and
  the Phase 6 header examples depend on it. Skipped on purpose.
- **Zero em dashes.** Upstream cuts them entirely as a hard constraint. We cap at **one per article**
  (tightened 2026-08 from one per paragraph, per the Economist 2026 finding) and extend detection to en
  dashes, spaced em dashes, and double hyphens. Allowing exactly one is a house style decision: a single
  dash is not evidence of anything, and a hard zero would flag real editors. What is *not* optional is the
  replacement rule in pattern 19 - extras become punctuation, never nothing.
- **Inline-header vertical lists** (`- **Thing:** description`). Upstream flags the shape. This library
  uses it throughout for scannability and featured-snippet list formatting.
- **Diff-anchored writing.** Documentation-specific. No article application.
- **Notability and media-coverage inflation.** Wikipedia-specific.
- **Voice calibration from a writing sample.** Superseded by the brand voice profiles, which are stronger
  for this use — a maintained profile beats a pasted sample.
- **Scientific register in non-technical copy** (`anti-ai-writing-skill` rule 21: parameter, methodology,
  mechanism, variable, metric). Rejected on 2026-08-16 for technical verticals, where words like *duty
  cycle* and *displacement* are load-bearing, so the rule would fire constantly on correct writing. The
  real target, borrowed authority in non-technical prose, is already covered by pattern 6 (authority
  tropes). Reconsider if this library is applied to a non-technical niche.
- **Odd-numbered paragraph counts** (rule 4: avoid 5, 7 or 9 paragraph structures). No mechanism offered
  and no evidence given that paragraph *count* parity is detectable. Symmetric section length is the real
  tell and the checklist already covers it.

---

## Covered elsewhere — deliberately not duplicated here

The remaining upstream patterns are handled by other files in the stack. Listed so a future sync can
confirm coverage without re-reading all three.

| Upstream pattern | Where we handle it |
|---|---|
| Overused AI vocabulary | `llm-words-to-avoid.md` — 100+ words, phrase lists, the Core 40 sweep |
| Filler phrases | `llm-words-to-avoid.md` Section 2 (transition/connector phrases) |
| Signposting ("let's dive in") | `llm-words-to-avoid.md` Section 2 |
| Rule of three overuse | `llm-words-to-avoid.md` Section 5 (Triple Pattern); checklist Category 3 |
| Generic positive conclusions | `llm-words-to-avoid.md` Section 5 (Summary Sandwich); checklist Category 3 |
| Promotional language | `llm-words-to-avoid.md` Section 4 (buzzwords) |
| Excessive hedging | `content-humanizer/references/ai-tells-checklist.md` Category 2 |
| Vague attributions / weasel words | checklist Category 2 (Vague authority claims) |
| Overuse of boldface | checklist Category 4 |
| Sycophantic / servile tone | checklist Category 5 (False warmth) |
| Passive voice | `humanizer_scorer.py` dimension + Phase 7 QA gate (≤10% of sentences) |

---

## Upstream sources

Two, tracked separately because they disagree about what an AI tell even is.

**1. https://github.com/blader/humanizer** — patterns 1-14. Derived from Wikipedia's "Signs of AI writing."
Compared at v2.9.1 (2026-08). Re-audited 2026-08-13 against the same version: no upstream changes, but a
full 33-pattern coverage pass found three gaps, added as patterns 12-14. Check the version before the next
sync.

**2. https://github.com/ama-zingco/anti-ai-writing-skill** — patterns 15-23. Derived from a 2026 corpus
study (55,940 sentences, 1.2m words, four models against professional journalism and fiction) and a 2025
detection study. Audited 2026-08-16 against all 25 of its rules: 13 already covered, 2 rejected above, and
the em-dash cap tightened from one per paragraph to one per article on its evidence.

The second source is the stronger evidence base, since it measures corpora rather than cataloguing
impressions. It is also the more perishable: it states that its own tells decay and that two of its rules
reversed inside twelve months. **Anything adopted from it needs re-checking, not just re-reading.**
