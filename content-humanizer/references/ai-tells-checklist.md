# AI tells checklist

The full detection list for Mode 1 (Detect). The patterns sit in six families, A to F, in the order of SKILL.md "Why AI text sounds like AI". Family A is the strongest. Families B, C and D are weak alone. Family E acts on one sighting, but it comes after them, in upstream's order. Family F acts on one sighting, in a reply only. Second-order tells follow the six families.

Rate each finding: 🔴 critical (edit on one sighting) / 🟡 medium (edit when it clusters) / 🟢 minor (polish).

**Strength.** A tell needs one clear sighting before any action, unless its pattern is marked *weak alone*. A weak-alone tell needs a second tell in the same passage. Families A and E act on one sighting, except the weak-alone lines in E4 and E5. In families B, C and D every pattern is weak alone, with two counting rules: a dash beyond the voice profile's rate is fixed on one hit (B1), and the C1 words count only in clusters. Family F acts on one sighting, but only in a clear reply. **Informal text** (chat messages, comments, reviews) is the exception to all of this. One tell is not enough there, except chatbot residue (E1). Two tells of different kinds turn the whole text into a rewrite target (SKILL.md Mode 1, "Informal text").

**Scanner coverage.** Each section is tagged `[scan + manual]` when `scripts/humanizer_scorer.py` lists candidates for it (its "ref" column uses these section ids) or `[manual]` when only a read of the prose finds it. Scanner hits are candidates, not commands: record a verdict for each meaningful one as `C5 "stunning" -> REWRITE (sales word replacing the fact)`. When the manual walk finds nothing, write `manual checklist clean (A-F)` once instead of a "none" line per section.

**Maintenance.** When a section here gains or loses a watched phrase that has a fixed surface form, update the matching list in `humanizer_scorer.py` in the same change, and the other way round.

**Fixing any pattern:** never add a fact, number, name, source, or anecdote the draft or user did not supply (SKILL.md Ground rule 1). Where a fix would need a missing detail, ask for it, narrow the claim, or cut it.

---

## A. Staging instead of stating 🔴

The strongest and most common tells in current model prose. Act on one sighting.

### A1. Not X but Y `[scan + manual]`
**Watch for:** "it's not X, it's Y"; "not just / not only / not merely X, but Y"; "X rather than Y"; the split form ("This doesn't mean X. It means Y."); a negative tail clipped onto the end ("..., no guesswork", "..., no wasted trips"). Cross-sentence shapes the scanner also catches: "isn't X. It's Y", "You don't need X. You need Y", the verb echo ("The dough doesn't need more flour. It needs more time."), the clipped pivot ("Not a gadget, just a better breakfast."), "not about X, it's about Y", and "less about X, more about Y".
**Across a set:** one earned contrast in a piece can stay. The same contrast in every product description of a collection, or in each channel variant of one campaign, is a reflex: keep at most one (scorer sibling set mode).
**Why it reads as AI:** the negative half rejects a view that nobody put forward, and that makes the other half feel larger. The sentence gains weight but no new claim.
**Fix:** say the point plainly. Keep a contrast only where its negative half corrects a belief the reader really holds, or where each half carries information of its own.
- Before: "It's not just a knife. It's a statement."
- After: "The blade is 8 inches long and runs the full length of the handle, so the knife balances in your grip." (only if the draft gives the length)

### A2. One-line closers and fragment rows `[scan + manual]`
**Watch for:** a paragraph of one sentence that repeats the paragraph above it; "Let that sink in."; "That's the real win."; "Read that again."; "That distinction matters."; one closer reused after several sections; a sentence whose only job is to explain the example just before it; a last sentence that starts with "Overall" or "Ultimately" and repeats the verdict its paragraph already gave; a row of fragments ("No tools. No hassle. No regrets."); ALL CAPS or. periods. between. words.
**Why:** the line asks the reader to pause instead of giving them anything new.
**Fix:** cut a closer that repeats. Also cut a sentence whose only job is to explain the example before it. Merge a fragment row into one sentence with a specific claim. A short sentence can stay when it carries a new fact. In informal text, a fragment row or an emphatic stop is the writer's register, so leave it (SKILL.md Mode 1, "Informal text").
- Before: "Setup takes five minutes. No tools. No manual. Just you."
- After: "You can set it up in five minutes without tools." (if the draft says so)

### A3. Sayings that sound deep `[scan + manual]`
**Watch for:** "the real question is," "the real problem / fix / reason / difference," "at its core," "what really matters," "fundamentally," "in reality," "the heart of the matter," "the deeper issue," "X becomes a trap," "X is the Y of Z," "the currency of," "the language of," "the architecture of."
**Fix:** replace the saying with the specific claim underneath it.
- Before: "At its core, a sourdough starter is the language of patience."
- After: "A sourdough starter needs about a week of daily feeding before it can raise a loaf." (if sourced)

### A4. Staged run-up before the point `[scan + manual]`
**Watch for:** "Let's dive in," "Here's what you need to know," "Let's break this down," "Let's explore," "Without further ado," "Buckle up," "Here's the thing," "The thing is," "Honestly?," "Look," "Real talk," "Let's be honest," "Now let's look at," "Next, let's...," "Heads up," "Quick note," and chatty warnings that announce a point before they make it.
**Why:** the writer announces the point or stages candor instead of making the point.
**Fix:** delete the run-up and start with the point. "Honestly" inside an ordinary casual sentence is fine. The tell is a lone "Honestly?" or "Look," set in front of a routine claim.
- Before: "Do you need the 12-cup carafe? Honestly? Only if you brew for more than four people."
- After: "You need the 12-cup carafe only to brew for more than four people."

**"The part" as a stand-in** is the same move: "the hard part is," "the part that matters is." When "the part" stands in for a thing, name the thing or make the claim. Keep a real part of something ("the replacement part ships separately").

**The dramatic colon** is the same move inside a sentence: the first clause builds suspense for an ordinary second clause. Keep a colon that introduces a real list, definition, quote, or example.
- Before: "The fix is simple: grind finer for espresso."
- After: "Grind finer for espresso."

### A5. Arguing with no one `[scan + manual]`
**Watch for:** "To be clear," "I'm not saying," "This isn't about," "This is not to say," "Don't get me wrong," "You might think... but," "Some might say... but," "It would be easy to just," "A tempting approach would be," "An obvious approach would be," "One might be tempted to."
**Why:** the text rebuts an objection, or turns down an option, that no one in the text raised. It is usually left over from an earlier draft.
**Fix:** remove the defense. If it hides a real claim, state the claim. Keep an objection a reader would genuinely raise, answered in full, and keep a rejected option that readers are likely to consider. Two or more rejections of options nobody raised, in one passage, are a strong sign.

---

## B. Shapes by rule 🟡 (🔴 in clusters)

The same shapes, hedges, and punctuation in every passage, needed or not. Every pattern here is *weak alone*, except dashes (B1).

### B1. Dashes `[scan + manual]`
**Rule:** zero em dashes (—), en dashes (–), spaced hyphens ( - ), or double hyphens ( -- ) in final copy, unless the brand voice profile or sample uses them; then match its rate (scorer `--dash-allowance N`). SEO articles follow the dash rule in seo-content. Numeric ranges count: write "7 to 10 days," not "7–10 days." Hyphens in compound words, code, paths, and URLs are fine.
**Strength:** not weak alone. A dash beyond the voice profile's rate is fixed on one hit (SKILL.md Ground rule 5). Informal text that Mode 1 leaves alone keeps its dashes.
**Why:** a dash spares the writer from choosing how two clauses connect, so models put one almost anywhere. Many readers now take the dash as an AI signature.
**Fix:** put a period, comma, colon, or parentheses in its place, or recast the sentence. Don't just delete.

### B2. Forced triads `[manual]`
Ideas arrive in threes to sound complete, whether or not the meaning has three parts: "quality, durability, and style." It also shows at paragraph scale as three parallel examples followed by a lesson. **Fix:** check that each item is distinct. Keep three when there are really three.

### B3. Repeated sentence openings `[manual]`
Several sentences in a row start "This..." or "It..." or "The...". **Fix:** merge, change the subject, or start with the action. The fix removes the repetition, not the word. One sentence in the group keeps its opening. Deliberate repetition for rhythm is fine.

### B4. Hedging, qualification, and filler `[scan + manual]`

Humans hedge. AI hedges in every sentence.

#### Opening hedges (usually safe to cut)
"It's important to note that...", "It's worth mentioning that...", "It should be noted that...", "Needless to say...", "It goes without saying..."

#### Stacked qualifiers
**Watch for:** "could potentially," "might arguably," "it's also possible that," "in some cases it may," "to be fair," "this is an inference."
**Fix:** where qualifiers pile up on one claim, keep one, and only when the source supports the doubt. Leave scope limits, legal and safety notices, and genuine corrections in place. Everyday hedges such as "perhaps" or "tends to" are normal human habits, not tells.
- Before: "It could potentially be argued that preheating might help in some cases."
- After: "Preheating helps."

#### Mid-sentence hedges (examine each)
"In many cases," "Generally speaking," "For the most part," "This may vary depending on..."

#### Filler and inflated wording
| Filler | Plain form |
|---|---|
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| in the event that | if |
| has the ability to | can |
| utilize / facilitate / numerous | use / help / many |

A weak verb propped up by an adverb ("really improves," "significantly enhances") usually wants a stronger verb or a number from the draft. Keep adverbs that carry scope, certainty, timing, frequency, or measurement ("usually," "twice a year").

**Diagnostic:** if the hedge protects a claim that should just be a claim, cut it. If it reflects real uncertainty, make the uncertainty specific: "The manual doesn't give a maximum oven temperature, so check with the manufacturer."

### B5. Hyphenated pairs everywhere `[scan + manual]`
**Watch for:** client-facing, high-quality, long-term, real-time, well-documented, well-known, and similar pairs placed after their noun.
"The coating is scratch-resistant." Keep the hyphen before a noun ("a scratch-resistant coating"), drop it after ("the coating is scratch resistant"). A compound that the dictionary always hyphenates keeps the hyphen after the noun too, for example "third-party" and "cross-functional." On SEO articles, never change the hyphens of a keyword term (seo-content's SEO guardrail). 🟢 alone.

### B6. Passive voice and missing subjects `[scan + manual]`
"Batteries not included. The blades are sharpened at the factory." **Fix:** name who does what, when that makes it clearer. 🟢 alone.

### B7. The SEEB paragraph `[manual]`
Every paragraph runs Statement, Explanation, Example, Bridge. **Fix:** vary the shapes: a short paragraph that carries one strong fact, a question the next line answers, a real list, an aside.

### B8. Parallelism overload `[manual]`
Every section is a list of three items of the same length. **Fix:** break the pattern. Most sections don't need bullets.

### B9. The summary conclusion `[manual]`
The conclusion restates the introduction. **Fix:** end on the last concrete fact, or a clear next step.

### B10. Symmetric section lengths `[manual]`
Every H2 runs about the same length. Real writers give more space to what deserves it.

### B11. Clause stacks that force backtracking `[manual]`
Active grammar can still bury the actor: "With the lid, which ships separately unless ordered with the pot, fitted before the pot goes into the oven, the stew keeps its moisture." **Fix:** split it and put the actor and action first. Don't answer by making every sentence short.

### B12. Synonym cycling `[manual]`
One thing renamed on every mention for variety: "the blender... the unit... the machine... this workhorse." Readers wonder whether these are different things. **Fix:** pick one name and keep it; use a pronoun where it's clear. On SEO articles, keep the keyword variants seo-content placed on purpose.

---

## C. Inflation and borrowed authority 🟡 (🔴 in clusters)

Under the inflation there is often a sound fact. Keep that fact and strip what is piled on it. Every pattern here is *weak alone*, and the C1 words count only in clusters.

### C1. Overused vocabulary 🟡 (🔴 at >5 per 1,000 words) `[scan + manual]`

These words show up in AI output at many times their rate in human writing, especially in groups. One instance is fine. Several in one piece is a tell. A formal word not on this list is not a tell by itself.

#### Verbs
| Word | Say instead |
|---|---|
| delve / delve into | look at, cover, or just start |
| leverage / utilize | use |
| foster / cultivate | build, grow, encourage |
| facilitate | help, make easier |
| navigate (figurative) | handle, deal with |
| ensure | make sure, check |
| streamline | say what gets faster |
| empower | let, help |
| enhance / elevate | improve, or say how |
| showcase / highlight / underscore | show, or cut |
| garner / bolster | get, strengthen |
| gate / gated / gating (figurative) | say what blocks or controls what. Keep technical senses: feature gating, a CI quality gate. The scanner does not list these. |

#### Adjectives
| Word | Say instead |
|---|---|
| crucial / vital / pivotal / key | show why it matters |
| robust (figurative) | the specific property |
| comprehensive / holistic | say what it covers |
| seamless | describe the actual experience |
| innovative / cutting-edge / groundbreaking | say what's different |
| meticulous / intricate | say what the care or detail is |
| vibrant / valuable / enduring / renowned | usually delete |
| exemplifies / aligns with | is, shows, fits, or say how |
| dynamic | usually delete |

#### Nouns, connectors and adverbs
| Word | Say instead |
|---|---|
| landscape (abstract) | the market, how X works today. Literal landscaping is fine. |
| tapestry / testament / interplay | cut or name the actual thing |
| ecosystem / paradigm / synergy | be specific |
| realm | area, field, or cut |
| vector / substrate / flywheel / locus / surface (as business metaphors) | the actor, mechanism, or result they hide |
| furthermore / moreover / additionally | nothing, "and," "also" |
| deep dive | look |
| Actually (opening a sentence) | cut, or state the correction plainly |
| quietly | cut, or say what happened |

**Abstract business metaphors.** "The quote tool becomes a growth flywheel" hides what happens. Say the mechanism: "The pricing calculator emails a quote, so buyers don't leave to call." (only what the draft states). Keep technical senses: a vector in geometry, an API surface.

Companion list for SEO articles: `seo-content/references/llm-words-to-avoid.md`.

### C2. Inflated significance `[scan + manual]`
**Watch for:** "stands as a testament," "a pivotal moment," "plays a key role," "marks a shift," "shaping the," "reflects a broader," "lasting legacy," "setting the stage for," "evolving landscape," "deeply rooted," "focal point," "indelible mark," "key turning point"; stock "Challenges and outlook" sections and the stock line "Despite these challenges, ... continues to thrive"; send-offs like "the future looks bright," "exciting times ahead."
**Fix:** keep the fact and cut the claim of importance. Close on the final concrete fact, or on a plan the source states.

### C3. Vague association `[manual]`
**Watch for:** "associated with," "in connection with," "linked to," "tied to."
**Fix:** name the relationship the source gives. If the source doesn't say, keep the vague wording rather than inventing a role.

### C4. Shallow -ing riders `[scan + manual]`
**Watch for:** a participle bolted onto a fact: "highlighting," "underscoring," "emphasizing," "showcasing," "reflecting," "symbolizing," "ensuring," "fostering," "encompassing," "contributing to."
**Fix:** keep the fact, drop the rider unless the source supports what it claims. A named source attached to the rider is no proof: keep the rider only where that source says it.
- Before: "The pan has stainless rivets, ensuring years of worry-free use."
- After: "The pan has stainless rivets, which won't rust."

### C5. Sales language `[scan + manual]`
**Watch for:** "nestled," "in the heart of," "boasts," "stunning," "breathtaking," "vibrant," "rich" (figurative), "must-have," "elevate your," "unparalleled," "world-class," "diverse array," "renowned," "groundbreaking," "commitment to."
**Why it matters here:** this is the most common failure in product and category copy.
**Fix:** say what the thing is and what it does.
- Before: "Nestled in any kitchen, this stunning walnut cutting board boasts endless charm."
- After: "This walnut cutting board is 18 by 12 inches, with a juice groove on one side." (from the product data)

### C6. Borrowed and vague authority `[scan + manual]`
**Watch for:** "studies show," "research suggests," "experts agree," "experts argue," "observers have cited," "some critics," "industry reports," "many companies," "leading brands," "it has been shown"; lists of prestige outlets, press mentions, or follower counts used as proof when they have nothing to do with the reader's decision (notability puffery: cut them; never add an outlet, date, or quote to make them specific).
**Fix:** if the draft or user names the source and what it said, use that. If not, cut the claim, narrow it to what is known, or flag it: "Need a source for this." **Never write a source in.** An unsourced sentence is not a tell by itself, since most writing cites nothing.

**Absence claims.** "Example Kitchen does not publish a battery life" and "not publicly available" claim that something does not exist. Gap wording with no claim behind it ("not disclosed," "in the available sources") belongs to E2. Remove it there. A failed search only shows it was not found. Unless the draft establishes the absence, write what was checked: "The Example Kitchen spec sheet doesn't list a battery life." Add the check date only if the draft gives one. The scorer skips conditional guidance ("if the maker doesn't publish a battery life, assume 8 hours").

**Soft quantifiers.** "Many," "often," and "a lot of" are fine as plain speech. When one carries a decision ("Many buyers regret the 8-quart model"), it is a claim: source it from the draft or narrow it.

### C7. Avoiding "is," "are," and "has" `[scan + manual]`
**Watch for:** "stands as," "serves as," "functions as," "operates as," "represents," "boasts," "features," "offers," "maintains a," "refers to."
**Fix:** use "is," "are," "has."

### C8. False ranges `[manual]`
**Watch for:** "from X to Y" joining things that are not on one scale: "from first-time bakers to commercial bakeries," "from home cooks to restaurant kitchens."
**Fix:** name who it is actually for, from the draft: "The 5-quart mixer fits a home baker making one or two loaves a week." (only if the draft says so)

### C9. Tone `[manual]`

#### False warmth
"We hope this guide has been helpful in your journey to...", "It's our sincere hope that these strategies will empower you." **Fix:** cut.

#### Generic positive conclusion `[scan + manual]`
"The possibilities are endless," "a step in the right direction," "a journey toward excellence," "the future looks bright." **Fix:** cut, and end on the last concrete fact or the next action. If the piece has no real ending to fall back on, report it upstream; don't write one from nothing.

#### Emotional escalation without basis
Clinical all the way through, then inspirational at the end: "Now you can finally cook the meals you have always dreamed of." **Fix:** end on substance. Warmth has to be earned by what came before.

#### Artificial enthusiasm
"Exciting," "fascinating," "incredible opportunity" attached to nothing that earns it. **Fix:** cut, or let the fact carry it.

---

## D. Formatting by rule 🟡

Clean formatting alone proves nothing, since templates produce it too. What reads as AI is decoration repeated on every heading or list item. Every pattern here is *weak alone*.

### D1. Bold as decoration `[scan + manual]`
Bold scattered on several phrases per paragraph, or every list item given a **Bold label:** and a colon.
**Fix:** take the bold off. Where the labels add nothing of their own, rewrite the labeled list as prose. (Example Software Co's voice profile uses in-text bold signposts on purpose; keep those at the profile's rate, scorer `--allow-bold`.) The scanner counts bold only once there are three or more spans, and ignores table cells and safety labels (**Warning:**, **Caution:**).

### D2. Decorative headings `[scan + manual]`
Headings In Title Case, emoji or arrows (→) on headings and list items, a horizontal rule between every section. **Fix:** sentence case, no decoration.
- **Title repeated as a heading:** the body opens with a top-level heading that copies the title. The title already shows elsewhere, such as in the front matter or a page title field. Show the title once and remove the copy.
- **Heading written for effect:** a heading that teases instead of naming its section ("Where it all comes together"). Rename it for what the section holds, using only the section's own content ("Delivery times by region").
- **Headings are protected** in SEO articles and embedded mode (SKILL.md Ground rule 4). The same holds for a repeated title and a heading written for effect. A title-case heading there gets KEEP with a note to the caller; it is never rewritten inside the humanize pass (scorer `--protect-headings`). Check brand and model names before calling a heading title case.
- **Emoji:** ✓, ✗, and ★ in comparison-table cells are fine; the scanner ignores them.

### D3. Colon-then-list `[manual]`
Every section opens with "Here's what you need to know:" and a list. **Fix:** vary it. 🟢

### D4. Curly quotes `[scan + manual]`
“Curly” quotes where the target format uses "straight" ones. Most editors auto-curl, so 🟢 alone.

---

## E. Leftovers from the chat and the draft 🔴

Remove outright. Act on one sighting, except where a pattern says *weak alone*.

### E1. Chatbot residue and flattery `[scan + manual]`
**Watch for:** "Great question!", "Certainly!", "Of course!", "You're absolutely right", "Excellent point", "Happy to help", "Let me know if you'd like...", "I hope this helps", "Would you like me to...", "Feel free to...", "Here is a...", "Should I continue?" In customer email, "feel free to call us" and "happy to help" can be the brand's own voice; the tell is the wrapper at the start or end of a generated piece.
**Fix:** remove the wrapper, keep the content. Easiest to miss when it wraps real content. If nothing remains once the wrapper is gone, there is no content to humanize: report an upstream voice gap (SKILL.md Mode 4) instead of writing new material.

### E2. Knowledge-limit disclaimers and gap-filling guesses `[scan + manual]`
**Watch for:** "as of my last update," "up to my last training," "based on available information," "while specific details are limited," "not widely documented," "not disclosed," "in the provided sources," "in the available sources," "it is believed that," "likely [grew up / began / was founded]"; privacy guesses about a founder or brand owner ("maintains a low profile," "keeps personal details private," "prefers to stay out of the spotlight").
**Fix:** remove the gap wording and keep every supported fact in the sentence. If nothing supported is left, say plainly that the source does not cover the point, or cut the sentence. Never present a guess as a fact.

### E3. Heading repeated in the first sentence `[scan + manual]`
**Watch for:** "## Care" followed by "Care matters." before the real content.
**Fix:** delete the repeat.

### E4. Empty connectives and writing about the document `[scan + manual]`
**Watch for:** "Now that we've covered X, let's move to Y," "In this section, we'll look at..."; an account of how the text was assembled or sourced ("compiled from," "generated from"); a description of a layout that is already visible ("the table below compares," "this section is organized by").
**Fix:** cut. Let the headings do the navigation. (Same as seo-content's Sentence Contribution Rule.) A credit that names a source the reader can check stays. If a caveat changes what the reader does next, it stays. Cut a stated convention that the reader can work out alone. Where the reader cannot, keep one statement and cut the repeats. Never add a new one. A single line of method or layout narration ("compiled from," "the table below compares") is *weak alone*. The empty connectives in this section stay one-sighting tells.

### E5. Writing about the previous version `[manual]`
Docs and product copy that describe what changed instead of what is: "The new handle replaces the old plastic design, which had issues." **Fix:** describe the current product. Mention the old version only in changelogs and "what's new" copy. *Weak alone.*

### E6. Bare answer-first opening `[manual]`
**Watch for:** an opening that restates the title as an answer ("The best skillet for searing is cast iron.") and could introduce any article in the category after swapping the product name.
**Fix:** this needs an editorial decision (which situation, tension, or consequence matters to this reader), so it is not a humanizer rewrite. Keep the opening and report it as an upstream voice gap. Never invent a hook, scene, or anecdote to replace it.

---

## F. Writing for the wrong reader 🔴 (replies only)

A model writes for a reader with no context, since that suits the most cases. A reply goes to someone who already has the background. Act on this family only in a clear reply, or where the thread around the text is visible. Otherwise leave it alone.

### F1. Re-explaining what the reader knows `[manual]`
**Watch for:** a short reply that retells the problem, walks back through the diagnosis, and stacks up proof before the decision appears. Other signs are proof that nobody asked for, such as a query, a command, or a table of figures. Background that the reader wrote or agreed to is a sign too, and so is an answer held back until the last line.
**Why:** retelling the background gives the reader nothing new and moves the point to the end. Every sentence can be clean on its own, so sentence-level edits do not catch it.
**Fix:** open with the decision. Keep only reasoning that bears on whether the reader agrees. Often that is one fact the reader lacks, plus any link needed to act. Put the diagnosis and the proof in the follow-up ticket or document, and list what moved in the report (SKILL.md Ground rule 2). Never cut a fact the reader does not already have.
- Before: "Thanks for flagging the late orders. To recap, the warehouse feed went down on Monday, so stock counts froze, and the site kept selling the 8-quart pressure cooker after it sold out. I checked the logs, and 14 orders came in during that window. So I think the fix is to email those 14 customers today with a new ship date."
- After: "I suggest we email the 14 customers today with a new ship date. Their orders came in while the warehouse feed was down, so the site oversold the 8-quart pressure cooker."

---

## Second-order and quantitative tells (survive word swaps)

Families A to F are mostly words, sentence shapes, and the order of a reply. Second-order tells describe how the text is built, so they survive find-and-replace. Measure them with an optional content-metrics helper, which tallies burstiness, windowed TTR, and structural tics. Otherwise estimate on the densest section. (Adapted from the `claude-blog` ai-slop-detection model, MIT.)

### Quantitative thresholds
| Metric | What it measures | Flag when | Fix |
|---|---|---|---|
| **Sentence-length burstiness** (stdev ÷ mean of sentence word counts) | Rhythm variation | **< 0.30** 🔴 | Human prose sits around 0.5 to 0.7. Mix in short sentences that carry a fact and a longer one that needs the room. |
| **Type-token ratio** (windowed, 500-word segments) | Vocabulary variety | **< 0.40** 🟡 | Use the windowed figure. Raw TTR falls naturally on long articles. |
| **AI-trigger density** | C1 words per 1,000 words | **> 5 / 1k** 🔴 | Same threshold as the seo-content Phase 7 gate. |

### The 10 structural tics (present or not)
Each one present is 🟡; three or more is 🔴:
1. **Question-heavy headings:** over 70% of H2/H3 are questions.
2. **"Here" openers:** 3+ sentences or paragraphs starting "Here's..." or "Here are...".
3. **Metronomic three-clause sentences:** over 50% of sentences share the same comma-comma-clause shape.
4. **False balance:** "Some say X, others say Y" with no position taken, where the data supports one.
5. **Hedge clustering:** several hedges stacked in one passage (B4).
6. **Uniform list lengths:** every list has the same number of items of the same length.
7. **Predictable transitions:** "Moreover," "Furthermore," "Additionally" opening consecutive sections.
8. **Symmetric section lengths:** every H2 about the same word count.
9. **Repetitive paragraph openers:** consecutive paragraphs starting the same way.
10. **Empty connective sentences:** E4.

A draft that passes families A to F but has burstiness under 0.30 plus 3+ structural tics still reads as AI. Fix the rhythm and structure, not just the words.

---

## Quick audit scoring

For a 1,000-word piece, count:

| Signal | Severity threshold |
|---|---|
| Family A and E tells (staging, leftovers), except the weak-alone lines in E4 and E5 | any = 🔴 |
| C1 vocabulary words | >5 = 🔴 |
| Sales language (C5) | >2 = 🔴 |
| Opening hedges | >2 = 🔴 |
| Vague authority claims | >2 = 🔴 |
| Dashes | any beyond the voice profile's rate = 🔴 (B1: fix each one) |
| SEEB paragraphs | >60% of paragraphs = 🔴 |
| False warmth | >1 = 🟡 |

**Verdict:**
- 0 to 5 total flags: light edit (quick Mode 2 pass)
- 6 to 12 flags: full humanize pass (complete Mode 2)
- 12+ flags: full rewrite (Mode 1 audit, complete Mode 2, then Mode 3)

**Second-order overlay:** burstiness under 0.30, windowed TTR under 0.40, or 3+ structural tics each push the verdict one tier toward a fuller rewrite, even when the flag count is low.

---

## What not to flag

- A watched phrase inside a quotation, title, product or brand name, or a passage that discusses the phrase
- Salutations and sign-offs on emails and letters
- The register of informal text: lowercase, short forms, fragments, and emphatic stops in chat messages, comments, and reviews (SKILL.md Mode 1, "Informal text")
- Text written before 2022-11-30
- A single weak tell (🟢, or 🟡 alone) with no others nearby
- Perfect grammar and a consistent style. Careful writers have both.
- A mix of casual and formal registers. Technical buyers, young writers, and neurodivergent writers mix them naturally.
- Bland prose with no specific tell. Bland is an editing problem, not proof of a model.
- Formal or academic words that are not on the C1 list
- Common transitions used once ("however," "also"). They count only when piled up.
- Curly quotes alone (most editors and Shopify auto-curl them)
- Unsourced claims alone. Most of the web is unsourced; flag missing proof under C6, not as an AI tell.
- Correct complex formatting (a real spec table, a numbered procedure)
- Human signals, which should be preserved: an odd, specific detail; mixed feelings; a dated reference; a genuine aside or self-correction; a first-person choice the writer can explain

File: content-humanizer/references/ai-tells-checklist.md · Version 3.0.0 · November 2026
