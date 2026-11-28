---
name: explanatory-diagrams
version: 1.0
description: "Hand-code SVG figures for a published explainer, sized for the site's blog template. Ranks candidates by where a reader is lost, applies six fences so a drawing never asserts more than its prose, and re-fetches every quantity from its primary source. The final check is looking at the rendered picture, which no agent can do today, so the skill hands that half to a human by name and never reports a figure as verified from its markup. Use after an article is written and before it is illustrated. Triggers on: diagram this article, add figures, illustrate the explainer, visualise the mechanism, make a diagram for section N. Outputs SVG source plus alt text, and a written hold for any figure that cannot be drawn honestly."
---

# Explanatory Diagrams

Adding hand-authored SVG diagrams to a finished technical article: which diagrams an article needs, which it must not have, and how to verify the result.

**Scope.** Explanatory diagrams only: mechanisms, spatial arrangements, stage sequences, things that sit inside or beside other things. Not charts from a dataset, not decorative or generated imagery, not screenshots.

**Status.** Rules resting on a single observation are marked HYPOTHESIS, so a reader can tell a proven rule from an inferred one.

⛔ **Read this before relying on the method: passing every check below does not mean the diagram is good.** Sections 7 to 10 exist to close that gap, and they are still the weakest part of this method. **Treat it as necessary and not sufficient.**

---

## The governing idea

**An image may carry only what the article already states.**

A picture asserts things prose does not: a quantity, a proportion, a location, a completeness. It asserts them whether or not it labels them, and a reader takes them as claims. The article is the claim authority. A diagram that teaches beyond its article is not a better diagram, it is an unsourced claim in a medium that makes claims hard to notice.

Two consequences run through everything below.

**A diagram cannot hedge.** Prose can say "roughly", "in most cases", "this is disputed". A line through five points asserts a continuous function. A region inside a boundary asserts containment. If the source cannot support the confidence the rendering implies, the rendering is wrong even when every label is correct.

**Verify by looking.** Every geometry defect found was invisible in the markup and invisible in the spec. The file was valid and the picture was wrong. A coordinate-level pre-check catches a subset mechanically; it narrows the looking pass and never replaces it.

---

## Step 1: Check the article is a valid input

⛔ **Stop, and say why, if any of these hold:**

- The article is on hold, withdrawn, or carries a claim known to be refuted.
- It is an internal document rather than something written for a reader.
- It is mid-revision. A diagram built against a moving draft goes stale silently, because nothing diffs a picture against prose.

**Then find its constraints.** If the article carries a list of things it must not assert, that list governs the diagrams too and is the single most useful input to Step 4. If it records what was cut during editing, read that as well: **a diagram is where cut material comes back.**

---

## Step 2: Resolve styling and destination before ranking anything

**Styling.** Inherit it from the surface the diagram will appear on. Section 7 carries the measured values for the site's blog template. On any other surface, measure the container and re-derive; none of those numbers transfer.

Declare a font stack and load nothing. A diagram that fetches a web font breaks on any surface without network access and quietly ties the artifact to a licence.

**Destination.** If where the article will publish is unresolved, build for the surface that has a reader today and record that bypass explicitly.

---

## Step 3: Generate candidates from where a reader is lost

Walk the article section by section. For each, ask: is there something here a reader must hold in their head that a picture would hold for them? Mechanisms with stages, spatial arrangements, sequences where order matters. Prose that is already concrete usually needs no picture.

**Rank by reader value, not by how drawable something is.**

### HYPOTHESIS: then walk every section again and name the ones with no candidate

For each uncovered section, say whether that absence is **a judgement**, **a miss**, or **required by a constraint**.

*Why this exists.* On separate articles the first-pass ranking missed the single most concrete section, and each time that was where a cold reader was most likely to be lost. The ranking optimises for conceptual material and skips the procedural. The second walk is the only thing that caught it. On one run it caught nothing missing and instead forced a candidate that would have been quietly dropped into an explicit hold with unblocking conditions. Both outcomes are the pass working.

*Marked a hypothesis because a handful of instances is a pattern, not a law.*

---

## Step 4: Apply the fences, after ranking and never before

**A fence filters candidates. It never ranks them.** Rank on value first, then remove. Applying fences during ranking produces a list optimised for what is permissible rather than for what a reader needs.

| # | Fence | The test |
|---|---|---|
| 1 | **Claim authority** | Does the image carry anything the article does not state? A picture asserts a quantity whether or not it labels one |
| 2 | **Source confidence** | Can the source bear the confidence the *rendering* implies? A rendering can over-claim where the prose does not |
| 3 | **Prior decision** | Does this reassert something an editorial decision removed? |
| 4 | **The article's own fence** | Does the article's must-not-assert list forbid depicting this? |
| 5 | **Licensing** | Does it need third-party material? Prefer a drawn schematic. Photography is a procurement question, not a rendering one |
| 6 | **Spatial assertion** | Does the layout assert a containment, adjacency or position the source does not state? **A region has to sit somewhere, and geometry cannot hedge** |

Fences 1 to 5 test what an image claims. **Fence 6 is the only one testing where an image puts a thing**, and it was added after the first five cleared a candidate that turned out to be undrawable: a three-region diagram had to place one region either inside or outside a boundary, and no source stated which.

### Worked cases (illustrative)

**Fence 2 holding an image.** A curve drawn from five separately reported figures in a study whose abstract and body disagreed. Prose could attribute the figures and carry the disagreement. A smooth line could not: it asserts a continuous measured function and silently picks one side. The source's quality never changed; what changed was the medium's capacity to carry a hedge.

**Fence 4 rejecting an image.** A timeline contrasting a short duration with a long one, where the article's constraint list forbade any duration or implied bound. In prose the number is framed by its sentence. A drawn axis strips that framing and leaves a number beside an event, and a reader cannot tell a "how long until you notice" axis from a "how long you have" axis.

**Fence 1 rejecting an image.** A diagram of a formula's components required drawing a specific count for each of two repeated parts. The article gives the formula symbolically and states neither count. Any grid a reader can count asserts an architecture the article does not carry.

### A hold is not a refusal

**Specify a held image in full**, then state what would unblock it and what binds if it is built later. A hold with named unblocking conditions is a decision; a hold without them is an unexplained gap the next person re-derives.

---

## Step 5: Re-fetch every quantity from its primary source

⛔ **Never trust a figure as it appears in the article**, even when the article is correct and cites properly. Open the cited source and read the number off it. For a third-party source, read the page. For a source on the site itself, read the site's own page.

**The reason is not catching errors. It is catching constraints.** For example, both figures can confirm verbatim while the fetch still changes the diagram: a specification table may not state the exact type for the part being drawn, mentioning it only in copy about a different variant. So the label names the general type and never the exact one. **The label a diagram most wants is often the one no source states**, and only going to the source reveals that.

⚠️ **A fetch that returns nothing is a failed fetch, not a completed one.** A JavaScript-rendered page returns a shell with no body: the request succeeds, the content is absent, nothing errors. If a parse comes back empty, **the fetch failed, and every quantity depending on it is undrawable.** Falling back to a local copy is not verification: an internal cross-check is not independent of an internal error, and the danger is that it feels like verification.

⚠️ **A sourceable quantity is not automatically a drawable one.** Traceability and permission are separate tests.

**If a quantity cannot be fetched, it cannot be drawn.** Drop it, or drop the candidate.

⚠️ Budget the fetches before starting: one parse per distinct source, never one per figure.

---

## Step 6: Decide what the geometry encodes, before drawing

**Every diagram must encode at least one thing in its geometry that its labels do not say. Name it before drawing.**

| Encodable, safe without a source | Needs a grounded quantity |
|---|---|
| **Sequence.** What comes before what | Relative size |
| **Containment.** What is inside what | Bar or column length |
| **Dependency.** What fails without what | Area, angle, position on a measured axis |
| **Grouping.** What belongs with what | Anything a reader could take a ratio off |
| **Branching.** What causes several things | |
| **Symmetry.** That two things are alike | |

All six safe encodings are structural rather than quantitative, so fence 1 blocks none of them. The tension between honesty and encoding is not real; it looks real when only the prohibition is stated.

⛔ **Two failure tests, both cheap:**

1. **The deletion test.** Remove every rectangle, line and colour, keep the words in place. If nothing is lost, the graphic encodes nothing. **Rebuild it or ship the text.**
2. **The disclaimer count.** If an image needs a note saying what its geometry does *not* mean, ask what it *does* mean. One such note across a set is honest. **Three out of four is the tell**, and it is what a cold reader described as *"I could delete the graphic and keep the words and lose almost nothing."*

⚠️ **Honest limits still stay.** This does not license removing a caveat, it requires earning one. "Not to scale" beside a graphic that genuinely encodes sequence is fine. The same note beside a graphic that encodes nothing is a disclaimer standing in for a design.

### Arrows assert causation, so spend them deliberately

An arrow measurably flips a reader into a causal reading (Heiser and Tversky 2006: functional-unit descriptions M=2.24 vs 1.26, F(1,61)=10.9). Consequences, each of which reversed a real build:

- **Alternatives must not be joined by arrows.** If the article presents two approaches as choices, an arrow between them asserts a progression the prose denies.
- **An arrow into one element scopes its claim to that element.** To scope a driver to a whole group, draw an enclosing region instead.
- **Do not draw a transformation the article never claims.** Substitution arrows assert a before-and-after that a comparison does not.

---

## Step 7: The measured surface (the site's blog template)


⛔ **On any other surface, none of these numbers transfer. Measure the container and re-derive.**

**A content image renders at `<desktop-image-width>` on desktop and `<phone-image-width>` on a 390px phone. The prose beside it renders at `<body-font-size>` at every breakpoint.** So the image scales and the text does not: `<phone-image-width>` ÷ `<desktop-image-width>` = **`<phone-scale>`**, fixed by the page.

Re-derivation formula: **`image width = min(clientWidth − <page-padding>, columnCap) − <column-padding>`**, where `columnCap` is `<narrow-column-width>` at ≤`<breakpoint>` and `<wide-column-width>` above.

⚠️ **Use `clientWidth`, not `innerWidth`.** A desktop browser emulating a phone renders a 15px scrollbar the real layout does not have, so `innerWidth` 390 gives `clientWidth` 375 and every downstream number shrinks. Check `innerWidth - clientWidth` before trusting any width measured that way.

**Canvas: `<desktop-image-width>` viewBox units wide.** Scale is then 1.0 on desktop, so an authored px is a rendered px and the type scale relates directly to the prose. At 560 the scale is `<scale-at-560>`, an 18px label renders at `<label-size-at-560>` beside `<body-font-size>` prose, and the diagram reads as a poster dropped into an article.

⛔ **The SVG must declare `width` and `height`, not only a `viewBox`.** A viewBox-only SVG was silently cropped on the live page while seven checks passed.

**Height is derived from content, never chosen.** Four images built without this rule came out at four slightly different heights, close enough to read as a mistake rather than a choice.

### The element budget, which is the real design constraint

Count the elements that must sit across the widest row before choosing anything else.

| Elements across | Width each (`<desktop-image-width>` canvas, 24px outer margins, 16px gutters) | Characters at `<type-floor>` | Verdict |
|---|---|---|---|
| 2 | `<width-2>` | `<chars-2>` | ✅ comfortable |
| 3 | `<width-3>` | `<chars-3>` | ✅ the working default |
| 4 | `<width-4>` | `<chars-4>` | ⚠️ tight, short labels only |
| 5+ | `<width-5>` | `<chars-5>` | ⛔ stack it, split it, or cut it |

Content width is `<desktop-image-width>` − 48 = `<content-width>`. Three across is (`<content-width>` − 32) / 3 = `<width-3>`.

**Type floor: `<type-floor>` authored**, which renders at `<phone-label-size>` on a phone. A label authored at `<body-font-size>` to match desktop prose renders at `<phone-prose-size>` on a phone and is unreadable. **The phone is the binding constraint, not the desktop.**

**Font stack:** a system stack, declared and never fetched. `<font stack>`.

---

## Step 8: Alt text is not optional and is authored last

The alt string is the one image-attached text the CMS reliably asks for, and it is frequently filled with a filename by default.

⚠️ **Nothing diffs an alt string against its image.** On three separate builds an alt string described elements that had been removed from the picture. **Author it against the final SVG, not against the spec**, and re-read it after any rebuild.

---

## Step 9: Verify by looking

⛔ **READ THIS FIRST: an agent running this skill today cannot complete this step, and that is a known hole in the runtime rather than a shortcut an agent may take.**

No tool renders markup a run has just authored and hands it back for inspection. Saving the image file in the project stores it, but does not render an SVG written this turn. So checks 1, 2 and 5 below are **not executable by an agent**, and they are the checks that catch the defects this method exists to prevent: every geometry defect across the prior builds was invisible in the markup and invisible in the spec.

**What this means in practice, and it is not optional:**

- **The agent does checks 3 and 4.** They are string reads and they work.
- **Hand checks 1, 2 and 5 to a human, explicitly, by name.** Say which figures need looking at and what to look for. Do not imply the figures are verified.
- ⛔ **Never report a diagram as checked when only the markup was read.** A syntactically valid SVG with a spec-compliant trace can still ship a broken label, a wrong proportion or a containment error. Saying "verified" here is worse than saying nothing, because it stops anyone else looking.

When a render-and-inspect tool exists (freshly authored markup returned as a raster at a desktop width and ~390px), this step becomes executable and the caveat above should be struck.

In order, and the last one is not skippable:

1. **Render it.** A valid file is not a correct picture. *(Human, today.)*
2. **Check the geometry asserts what was meant.** *(Human, today.)* A checker passed an image whose enclosure wrapped five items instead of two, asserting the inverse of the article.
3. **Read every string against its source sentence.** A standfirst that appears nowhere in the article passed both a geometry check and a naive substring trace, because every individual word was present somewhere.
4. **Check for an unresolvable pronoun.** A standfirst that opened with "It" bound to the nearest heading, which was the wrong column, and the image asserted the inverse of its claim.
5. **Look at it at phone width.** `<phone-scale>` scale. If a label is unreadable, the element budget was wrong, not the canvas. *(Human, today.)*

⚠️ **A layout checker returns CLEAN on an image whose label visibly clips its box**, and a character-width estimate said `<estimated-width>` where the real measurement was `<measured-width>`. **An estimate is untrustworthy even when it reports room.** Measure or look.

---

## Step 10: What to hand back

- The SVG source for each figure, with `width`, `height` and `viewBox` all declared.
- The alt text for each, authored against the final file.
- For every held figure: the full specification, what would unblock it, and what binds if it is built later.
- For every section with no figure: whether that is a judgement, a miss, or a constraint.

**Nothing here publishes.** Placing an image on a page is a separate, human-approved step.

---

## Known limits

Stated because an undeclared absence reads as an absence of the problem.

- **No craft check exists.** This method can pass a set of diagrams that are correct and ugly.
- **The measured values in Step 7 are for one blog template.** They are a measurement of a live surface, so re-derive rather than quoting them onward.
- ⛔ **Step 9's looking pass cannot be run by an agent**, because nothing renders freshly authored markup back for inspection. This is the single largest hole in the method as it runs here: the steps that catch geometry defects are exactly the ones that are unavailable. Until a render-and-inspect tool exists, a human does that half or it does not happen.
- **The catalogue of which visual technique carries which encoding is not here.** Step 6 says a graphic must encode something and names the six safe encodings. It does not say how "exceeds a limit" is conventionally drawn, or what each device misreads as.

File: explanatory-diagrams/SKILL.md · Version 1.0 · November 2026
