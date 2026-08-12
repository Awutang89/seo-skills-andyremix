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

## Part 1: The eleven patterns

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

### Vocabulary additions

Words from the upstream high-frequency list not currently in `llm-words-to-avoid.md`. Add them to the
Ctrl+F sweep; full entries are not needed.

```
garner, interplay, showcase, testament, enduring, valuable,
align with, key (as an adjective: "a key factor")
```

---

## Part 2: What NOT to flag

Every rule above deletes text. Without a counterweight, a humanization pass run by a scorer plus a 60-row
QA gate will sand a good article down to a flat one. Real writers hit these patterns constantly.

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

---

## What we deliberately do not adopt

Recorded so the next sync does not re-litigate these.

- **Title case in headings.** Upstream flags it. The H2 conventions in this library are title-cased and
  the Phase 6 header examples depend on it. Skipped on purpose.
- **Zero em dashes.** Upstream cuts them entirely as a hard constraint. We cap at one per paragraph
  (Phase 5 rhythm targets) and extend detection to en dashes, spaced em dashes, and double hyphens. The
  cap is a house style decision, not an oversight.
- **Inline-header vertical lists** (`- **Thing:** description`). Upstream flags the shape. This library
  uses it throughout for scannability and featured-snippet list formatting.
- **Diff-anchored writing.** Documentation-specific. No article application.
- **Notability and media-coverage inflation.** Wikipedia-specific.
- **Voice calibration from a writing sample.** Superseded by the brand voice profiles, which are stronger
  for this use — a maintained profile beats a pasted sample.

Upstream source: https://github.com/blader/humanizer — check the version there before the next sync.
Compared at v2.9.1 (2026-08).
