# Claim labels

Every load-bearing claim in a brief, script or recommendation carries one of these labels, inline or in a labelled block before the recommendation.

| Label | Meaning |
|---|---|
| Fact | Verifiable now from the artefact, file, command output, or cited prior. Must be checkable in the same response or via a follow-up tool call. A fact stops being a fact the moment it's restated without the verification chain. |
| Derived | A line that follows from named, sourced premises and that no source states in so many words: a ratio, a total, a comparison, a plain-words rendering of a figure. It is labelled Derived and names its premises, each of which carries its own label and source; it is no stronger than its weakest premise. A Derived line is not an Assumption (the premises are checked) and not a Fact about the source (the source does not print it); say which premises, and recompute where the premises are numbers. In a claims table behind a spoken line, an Assumption row is framing only and is never a spoken line; a spoken line is a primary quote, a Derived row or a Taught line. |
| Assumption | Claims that follow from reasoning but are not directly verified. Must be named explicitly, with the reasoning the assumption rests on. The "Assumption:" prefix is the discipline anchor: if removed, the claim drifts to fact. |
| Taught | A plain gloss, a small worked case or an analogy, spoken without a source row, labelled Taught in the claims table, never Fact. It may simplify as far as every conclusion the viewer would draw from it stays true. Where a viewer would draw a wrong conclusion about their own work, the sentence carries one "but unlike..." clause, or it is cut. |
| Unknown | Things genuinely not knowable from current information. Must be named, not silently bypassed. |

## What Taught allows

- A term the point needs is defined in plain words before it is leaned on. A term the point does not need is cut, not defined.
- An invented number or worked case is allowed when the same or the next sentence says what it means for the viewer. A number with no "so what" fails, however correct.
- An analogy states where it stops holding.
- No figure the viewer would carry home. A vendor ratio or a measured figure is not spoken or shown where a viewer would carry it to their own setup, unless its scope makes that carry impossible (the setup it was measured on is stated and plainly not the viewer's). Where the scope cannot rule the carry out, the script says the direction only, scoped, or nothing.

What Taught does not license: a real-world figure, a vendor's statement, a ranking or a performance claim. Those stay claims with source rows, and a named vendor [product] stays subject to `[screening-rules]`.

## Stress test

Before finalising a recommendation that decides what to do or stop doing, answer in the response: would the recommendation change if any assumption were wrong?

- If yes: either raise the assumption to validate-before-deciding, or proceed and explicitly accept the assumption risk with the recommendation. Do not hide the dependency.
- If no: name the facts that alone carry the recommendation; the assumptions are decorative, not load-bearing.

## Limits

The Taught class is a design choice with partial support and has not been validated. A claim whose status cannot be established is labelled Unknown, not left out.

### Spoken lines

A spoken line is a primary quote, a Derived row or a Taught line. Taught is a third permitted spoken class and is allowed only within the limits above. Every other spoken line is a primary quote or a Derived row.

---

Reference: claim-labels | Version: 1 | November 2026

File: humanise-draft/references/claim-labels.md · Version 1.0 · November 2026
