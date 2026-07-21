# Deduplication Rules Reference

## The fundamental law

**One keyword. One article. No exceptions.**

If two articles both target the same primary keyword, they cannibalize each other. Google can't decide which to rank, so it ranks neither well. One of them wins a little, both of them lose a lot.

This document defines the exact rules for resolving every type of keyword conflict.

---

## Rule 1: Exact Duplicate Primary Keywords

**Situation:** The exact same keyword string appears as a primary keyword in two different articles.

**Resolution:** Always pick one home. Use this decision tree:

```
1. Which article covers this topic MORE comprehensively?
   → That article keeps the primary keyword

2. If both are equally comprehensive, which pillar is this keyword most logically part of?
   → Assign to that pillar's article

3. If still unclear, which article has more search intent alignment?
   → Informational intent → assign to the guide/hub
   → Commercial intent → assign to the buying/comparison article
   → Problem-solving intent → assign to the troubleshooting article

4. After assigning, the other article must:
   → Get a new unique primary keyword (different angle or scope)
   → OR be deleted if it's truly redundant
   → Add an internal link pointing to the home article
```

**Example resolution:**
- `best [product] for [use case]` appeared in Cluster 1D ([use case] products) AND Cluster 3A (buying guides)
- Decision: Cluster 1D owns it — it's the dedicated [use case] product article
- Cluster 3A gets updated to link to Cluster 1D instead of targeting the same keyword
- Cluster 3A's spoke changes to "best [product] for [use case B]" — a distinct but related keyword

---

## Rule 2: Semantic Duplicate Primary Keywords

**Situation:** Two keywords have different wording but the same search intent. If Google would rank both articles for both keywords, they compete.

**Test:** Would the same user searching both phrases want the same article?
- YES → Same article should own both. Pick the higher-volume phrasing as primary, other becomes secondary.
- NO → Different articles can target each phrase.

**Common semantic duplicate patterns:**

| Phrase A | Phrase B | Same or Different? |
|---|---|---|
| [product type A] vs [product type B] | [product type B] vs [product type A] | SAME — word order flip |
| [product] for [use case] | [use case] [product] | SAME — word rearrangement |
| [use case] [key spec] requirements | [use case] [product] requirements | SAME — searcher wants [key spec] data for [use case] |
| [product] sizing | [product] [component] sizing | SAME — same task, different vocabulary |
| [attribute] [product] maintenance | [attribute synonym] [product] maintenance | SAME — [attribute] = [attribute synonym] |
| [key spec] requirements for [use case] | [use case] [key spec] requirements | SAME — word order flip |

When two are the SAME:
- Primary keyword = higher search volume version
- The other becomes a secondary keyword in the same article

When two are DIFFERENT (appear similar but different intent):
- "[product] for [use case]" (sizing focus — what size to buy) vs "[attribute] [product] for [use case]" (type focus — why [attribute] matters for [use case]) → Different enough for separate articles with documented angle notes

---

## Rule 3: Cluster-Level Duplication

**Situation:** An entire cluster of articles is semantically redundant with another cluster. All the primary keywords in Cluster B are already covered in Cluster A.

**Most common cause:** Type comparison clusters. A site creates a separate "Type Comparisons" cluster with articles like "[product type A] vs [product type B]" — but those articles already exist as spokes in the individual type clusters.

**Resolution options:**

**Option A — Remove the redundant cluster entirely**
- Delete or redirect the duplicate articles
- Add internal linking notes so the surviving articles reference each other
- Use case: Cluster is pure duplication with no unique angle

**Option B — Reframe with angle differentiation**
- Every article in the redundant cluster gets a new, unique primary keyword that covers the same topic from a different angle
- Use case: The topic needs two approaches (e.g., "sizing for [use case]" vs "tools used in [use case]")
- Requires documenting the angle clearly so writers don't overlap

**Option C — Merge clusters**
- Fold the articles from the redundant cluster into the primary cluster as additional spokes
- Use case: The redundant cluster has 2-3 unique articles mixed with duplicate ones

**Worked example (Cluster 3C removal):**

Cluster 3C was a "Type Comparisons" cluster with articles:
- "[product type A] vs [product type B]" → already in Cluster 1A spoke #1
- "[spec A] vs [spec B]" → already in Cluster 1B spoke #1
- "[attribute A] vs [attribute B] [product]" → already in Cluster 2D spoke #3
- "[attribute C] vs [attribute D]" → already in Cluster 1C hub
- "[power source A] vs [power source B] [product]" → already in Cluster 1E hub
- "[attribute] [product]" → already in Cluster 1A spoke #3

Decision: Remove Cluster 3C entirely (Option A). All these articles have homes. Cluster 3C was just duplicating existing articles with the same primary keywords.

Result: No duplicate primary keywords. Cross-reference table shows where each lives.

---

## Rule 4: Overlapping Application Clusters (Sizing vs Use Case)

**Situation:** The site has both a Sizing cluster and an Applications cluster covering the same industries/uses. Example: "[Product] for [use case]" appears in both the Sizing pillar and the Applications pillar.

**This is the trickiest duplication type** because both articles are legitimate — but they can't share the same primary keyword.

**Resolution: Angle differentiation mandate**

Sizing cluster angle: **"What size/type do I need?"**
- Primary keyword focuses on selection criteria
- Content answers: [key spec] requirements, [spec B] requirements, [attribute], type selection
- Example primary: "[product] for [use case]"

Applications cluster angle: **"How do I use it / what tools do I need?"**
- Primary keyword focuses on the tools and workflow
- Content answers: which tools to use, how to set up the system, workflow tips
- Example primary: "[use case] [product] setup" or "[use case] [product] tools"

Both articles exist. Neither competes. Both link to each other.

**Angle differentiation matrix for common overlapping pairs:**

| Shared Topic | Sizing Article Primary | Application Article Primary |
|---|---|---|
| [Use case A] | [product] for [use case A] | [use case A] [product] setup |
| [Use case B] | [product] for [use case B] | [use case B] [product] tools |
| [Use case C] | [product] for [use case C] | [use case C] [product] system |
| [Use case D] | [product] for [use case D] | [product] for [use case D] workflow |
| [Use case E] | [product] for [use case E] | [use case E] [product] tools |
| [Use case F] | [product] for [use case F] | [use case F] [product] system |
| [Use case G] | [product] for [use case G] | [use case G] requirements |
| [Use case H] | [product] for [use case H] | [use case H] requirements |

---

## Rule 5: [Key Spec]/Technical Keyword Conflicts

**Situation:** [key spec]-related keywords appear across multiple clusters — the [key spec] hub, the tool-specific requirements articles, and the application guides all want [key spec] keywords.

**Resolution hierarchy:**

```
Level 1 ([Key Spec] Hub) — Owns the broadest [key spec] keywords
  → "[product] [key spec] requirements"
  → "how to calculate [key spec]"
  → "[key spec] requirements chart"
  → "[key spec] requirements by tool" (hub-level overview)

Level 2 ([Key Spec] Spokes) — Owns specific [key spec] by tool
  → "[use case A] [key spec] requirements" ([key spec] number focus)
  → "[key spec] requirements for [use case B]" ([key spec] number + [attribute] breakdown)
  → "[key spec] requirements for [use case C]" ([key spec] number + [component] sizing)

Level 3 (Tool Requirements Articles) — Owns full requirements ([key spec] + [spec B] + use cases)
  → "[use case A] [product] requirements" ([key spec] + [spec B] + [attribute] + use cases)
  → "[use case B] [product] requirements" ([key spec] + [spec B] + setup + [product type])
  → "[use case C] [product] requirements" ([key spec] + [spec B] + [component] + [material])

Level 4 (Application Sizing Guides) — Owns selection-level keywords
  → "[product] for [use case C]" (what to buy, sizing guide)
  → "[product] for [use case B]" (what to buy, full setup guide)
```

**Key rule:** A keyword about a SPECIFIC [key spec] number belongs at Level 2. A keyword about the FULL REQUIREMENTS (including [spec B], use cases, setup) belongs at Level 3. A keyword about WHAT [PRODUCT] TO BUY belongs at Level 4.

Never put a Level 2 keyword in a Level 4 article, or vice versa.

---

## Rule 6: Specifications Keyword Conflicts

**Situation:** Specification keywords ([spec A], [key spec], [spec B], efficiency, [attribute]) appear in both the sizing pillar and the technical specifications pillar.

**Resolution: Conversion vs Concept**

If the keyword is about CONVERTING between units or CALCULATING a number:
→ Belongs in the Sizing pillar (people searching this want a number for a decision)
→ Example: "[spec A] to [key spec] conversion chart", "[spec B] to [key spec] conversion", "how many [key spec] per [spec A]"

If the keyword is about UNDERSTANDING a concept or comparing efficiency:
→ Belongs in the Specifications pillar (people searching this want to understand)
→ Example: "what is [efficiency metric]", "[spec A] to [key spec] efficiency ratio", "what is [technical concept]"

**Worked example ([spec A] to [key spec] conflict):**
- "[spec A] to [key spec] [product]" (conversion chart, give me the numbers) → Sizing pillar (2A spoke #6)
- "[spec A] to [key spec] ratio" (what does this ratio mean, what's a good ratio) → Specs pillar (6A spoke #3)

Both articles exist. Different primaries. Writers are briefed on the angle.

---

## Rule 7: Standards Keyword Conflicts

**Situation:** Standards like [standard A] or [regulatory standard] appear in both a [Treatment] cluster and a Standards & Compliance cluster.

**Resolution: Assign to the most actionable context**

Ask: "When someone searches this standard, what are they trying to DO?"
- Understand how to achieve the standard (treatment/equipment context) → Assign to treatment/equipment cluster
- Understand the legal/compliance requirements → Assign to standards cluster
- Both? Pick the higher search volume context, link to the other

**Example:**
- "[standard A]" → Most searchers want to know about [attribute] classes to specify treatment equipment → Assign to [Treatment] cluster (5B spoke #10)
- Standards cluster links to that article instead of duplicating it

---

## Rule 8: Secondary/Longtail Keyword Assignment

**Situation:** A keyword is specific enough to be a secondary or longtail (not a primary), but appears as a secondary in multiple articles.

**Resolution:** Secondary and longtail keywords also get ONE home.

The rule applies at all levels, not just primaries.

**Assignment test for secondaries/longtails:**
1. Which article's primary keyword is most semantically related to this secondary?
2. Which article would benefit most from ranking for this secondary?
3. If a user searching this phrase lands on the article, do they get the answer they wanted?

The article that scores highest on all 3 gets the keyword. Remove it from all others.

**Example:**
- "[product] [component] type" appeared as a secondary in BOTH the [component] change article (4A#3) AND the [component] guide article (4A#4)
- Decision: 4A#4 (the [component] guide) is the definitive [component] reference — it owns "[product] [component] type"
- 4A#3 (the [component] change how-to) removes "[product] [component] type" and instead adds "[product] [component] change step by step"

---

## Rule 9: SERP-Overlap Test (empirical tiebreaker)

**Situation:** Rules 2 and 4 hinge on a judgment call — "is this the same intent?" / "are these
really separate applications?" When two experienced editors could disagree, stop guessing and let
Google's rankings decide.

**Method:** Search both keywords (incognito, or pull the SERPs via DataForSEO) and list the top 10
organic URLs for each. Count how many URLs appear in **both** top-10s.

| Shared top-10 URLs | Interpretation | Action |
|---|---|---|
| 7–10 | Google treats them as the same query | **Merge into one article.** Higher-volume phrasing is primary; the other becomes a secondary (Rule 2) |
| 4–6 | Same topic cluster | Keep in the same cluster; separate articles only with a documented angle (Rule 4) |
| 2–3 | Adjacent topics | Separate articles in adjacent clusters; cross-link them |
| 0–1 | Distinct topics | Separate articles, separate clusters |

**Why it works:** SERP overlap is empirical evidence of how Google interprets intent. Two phrasings
that return the same 8 URLs will cannibalize if you build two articles — Google has already decided
they answer the same query. Two phrasings that share 1 URL will not.

**Efficiency:** Pre-group candidate keywords by intent before testing, so you only compare pairs
that are plausibly duplicates. You don't SERP-test every pair — only the ambiguous ones surfaced by
Steps 1.2–1.4.

**Worked example:**
- `[product] for [use case]` vs `[use case] [product] requirements` — semantically they *feel*
  close. SERP test: only 2 shared URLs in the top 10. → **Separate articles** (2–3 band), cross-linked.
  One is a buying/sizing guide, the other a requirements spec. The data confirms the angle split.
- `[product type A] vs [product type B]` vs `[product type B] vs [product type A]` — 9 shared URLs. → **Merge**,
  as Rule 2 already predicted; the SERP test just makes it auditable.

**Documentation:** Record the shared-URL count in the article NOTE, e.g.
`*NOTE: SERP-overlap with "[use case] [product] requirements" = 2/10 → separate, cross-link.*`

> Method adapted from the SERP-clustering approach in the open-source `claude-seo` project (MIT).
> Article-level companion check (is a finished draft a near-duplicate of its sibling?) lives in
> `skills/seo-content/references/thin-content.md`.

---

## Conflict resolution summary

| Conflict Type | Rule | Resolution |
|---|---|---|
| Exact duplicate primaries | Rule 1 | One home, other gets new keyword or is removed |
| Semantic duplicate primaries | Rule 2 | One home, other becomes secondary |
| Redundant cluster | Rule 3 | Remove, merge, or angle-differentiate |
| Sizing vs application overlap | Rule 4 | Angle differentiation (what to buy vs how to use) |
| [Key spec] across multiple clusters | Rule 5 | Level hierarchy (hub → specific [key spec] → full requirements → selection) |
| Specs vs sizing | Rule 6 | Conversion/calculation → sizing; Concept/understanding → specs |
| Standards in two clusters | Rule 7 | Most actionable context wins |
| Duplicate secondaries/longtails | Rule 8 | One home — same test as primaries |
| Ambiguous same-or-different call | Rule 9 | SERP-overlap test — shared top-10 URLs decide merge vs. separate |

---

## Documentation requirement

Every resolved conflict must be documented with a NOTE in the article's keyword entry in the database:

```
*NOTE: "[use case] [key spec] requirements" belongs to Cluster 2A spoke #4.
This article (7B spoke) covers the full [use case] setup including
[spec B], setup tips, and [product type] comparison — not the [key spec] number specifically.*
```

This note:
1. Tells the writer exactly what angle to take
2. Prevents future editors from accidentally re-adding the keyword
3. Creates the internal linking instruction ("link to 2A spoke #4 for [key spec] specifics")
