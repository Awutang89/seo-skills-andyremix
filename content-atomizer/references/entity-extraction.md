# Entity Extraction: Method Reference

Deep reference for **Step 2.5** of the article-splitting flow — extracting the entities a piece of
content actually covers, determining which of them it ranks for, and using entity distribution to
decide where a long article should split.

Loaded by `SKILL.md` and `article-splitting.md`. Reusable independently: the inventory and gap
analysis are useful for any on-page audit, not just splitting.

---

## Why entities, not just keywords

A keyword is a phrase someone typed. An **entity** is a thing that exists — a product, a standard, a
material, a method, an organisation — which search and AI systems resolve, disambiguate, and connect
to other things.

This distinction does real work in a split decision:

- **Keywords tell you what a page is targeting. Entities tell you what it's about.** Two candidate
  articles can target cleanly distinct keywords and still cover identical subject matter. Keyword
  separation is a surface property; entity separation is structural.
- **Entities survive where search data doesn't.** Entity extraction reads your text. It works on
  original research, proprietary methodology, and in-house test data — content with no SERP to
  measure and no presence in any model's training data. For novel material, entity overlap isn't a
  supporting check, it's the primary evidence.
- **Entity density is a credibility floor.** An article carrying three entities on a technical topic
  reads as thin to a reader and as low-coverage to a retrieval system, regardless of word count.

---

## The taxonomy

Classify every extracted entity. Types are deliberately generic — adapt the set to your domain, but
keep the central/incidental distinction.

| Type | What counts | Why it matters |
|---|---|---|
| **Product / model** | Named products, model numbers, SKUs, versions | Highest commercial intent; strong disambiguation signal |
| **Brand / manufacturer** | Companies whose products you discuss | Comparison and roundup relevance |
| **Standard / certification** | Formal specs, ratings, regulatory codes, compliance marks | Strong authority signal; rarely ambiguous |
| **Technical concept** | Named methods, processes, phenomena, principles | The conceptual backbone; drives topical coverage |
| **Unit / measure** | Units, metrics, formulas, thresholds | Signals depth; often the citable part |
| **Organisation** | Standards bodies, regulators, institutions, associations | Authority and citation weight |
| **Person** | Named experts, researchers, cited authors | E-E-A-T signal; usually sparse |
| **Place** | Regions, jurisdictions, facilities | Only when the topic is geo-dependent |
| **Tool / software** | Named tools, platforms, instruments | Practical/how-to relevance |

### Central vs. incidental

**This classification determines everything downstream. Get it right.**

An entity is **central** when the content would be materially incomplete without it — it's explained,
compared, measured, or used to reach a conclusion.

An entity is **incidental** when it's mentioned in passing, appears once as an example, or shows up
only in a list.

| Test | Central | Incidental |
|---|---|---|
| Mention count | ≥ 3, or ≥ 2 across different sections | 1–2 in one section |
| Role | Explained, compared, measured, argued about | Named in passing or listed |
| Removal test | Removing it leaves a gap | Removing it changes nothing |
| Heading presence | Appears in an H2/H3 | Body only |

**All overlap maths uses central entities only.** Incidental entities inflate overlap without meaning
anything — two articles both mentioning the same three brands once each are not the same article.

---

## Extraction procedure

### Step 1 — Sweep the text

Read the full source. For each entity found, record:

| Entity | Type | Mentions | Sections | Central? | Resolvable? |
|---|---|---|---|---|---|
| [name] | Standard | 7 | H2 3, H2 8, FAQ | Central | Yes — Wikidata |
| [name] | Product | 2 | H2 5 | Incidental | Yes |
| [name] | Concept | 11 | H2 1, 2, 4, 9 | Central | No — internal term |

**Sweep systematically, not impressionistically:** headings first (heading presence is a centrality
signal), then body, then tables, then FAQ, then image captions and alt text. Tables are the most
commonly missed source — spec tables are dense with entities.

### Step 2 — Resolvability check

For each entity, determine whether it resolves as a **real-world entity** or is only a phrase.

Practical test: does it have a Wikipedia/Wikidata entry, an official standards-body page, a
manufacturer product page, or an equivalent canonical reference?

| Resolvable | Consequence |
|---|---|
| **Yes** | Search and AI systems can connect it to a knowledge graph. Full weight in overlap maths. Worth marking up in schema. |
| **No — proprietary/novel** | Your own term, method, or model. Zero external corroboration. **Still counts fully for overlap** (it's still subject matter) but carries no authority signal — and is a candidate for you to *define* canonically. |
| **No — ambiguous** | Collides with a more common meaning. Flag it: it needs disambiguating context nearby or it will be misread. |

**Novel entities are an opportunity, not a defect.** An entity you coined that resolves nowhere is a
term you can own — the definitional page for it has no competition. Flag these explicitly in the
output; they're often the strongest independent-article candidates in a novel-content source.

### Step 3 — Section→entity map

Attribute every central entity to the sections it appears in. This is the raw material for split
grouping — the map, not the list, is what drives the decision.

```
H2 1  ── E1, E4, E7
H2 2  ── E1, E4
H2 3  ── E2, E9, E11
H2 4  ── E2, E9
H2 5  ── E3, E12, E14
```

Clusters emerge visually. Sections sharing an entity core belong together; sections whose entity sets
barely intersect are split candidates. **Group by this map before assigning keywords** — entity
distribution should drive the grouping, not be checked against it afterwards.

---

## "What are we ranking for" — three evidence sources

The extraction above says what the content *covers*. This says what it's actually *associated with*.
Use all three; they fail in different places.

### Source 1 — Existing query data

The queries already sending impressions or clicks to the URL are direct evidence of associated
entities. Pull from whatever you have: search console data, your keyword register, rank tracking.

| Strength | Limit |
|---|---|
| Direct behavioural evidence, no inference | Only exists for live URLs with accumulated history. Useless for unpublished or brand-new content. |

Map each query back to the entity it implies, then mark each entity **ranked / not ranked**.

### Source 2 — Entity + modifier SERP check

For each central entity, search `[entity] + [common modifier]` (e.g. `vs`, `sizing`, `cost`,
`requirements`, `how to`) and check whether the URL surfaces at all.

| Strength | Limit |
|---|---|
| Works for entities with no register history | Requires the entity to have a populated SERP. Fails on novel/proprietary entities — same blind spot as the Tier-1 SERP test in `article-splitting.md`. |

Record position or absence. Absence across all modifiers for a central entity is a real finding: you
cover it but aren't associated with it.

### Source 3 — Competitor entity diff

Pull the top 10 for the source's primary keyword. Extract central entities from each. Union them.
Subtract yours.

| Strength | Limit |
|---|---|
| The only source that finds what you *don't* know you're missing | Reflects the current SERP consensus — it won't reveal genuinely novel angles, and it can propagate whatever the incumbents collectively get wrong |

What remains is the **entity gap**: entities the winning pages treat as central that your content
doesn't cover. This feeds directly into information-gain work — gaps become section material in the
children.

> Run all three where possible. Where a source is unavailable, **say so in the output** rather than
> quietly omitting it. An entity marked "unknown" is honest; one silently dropped is misleading.

---

## The four outputs

### Output 1 — Entity inventory

| Entity | Type | Mentions | Central? | Resolvable? | Ranked for? | Evidence |
|---|---|---|---|---|---|---|
| [name] | Standard | 7 | Central | Yes | Yes — p4 | Query data |
| [name] | Concept | 11 | Central | No — novel | Unknown | No SERP to test |
| [name] | Product | 2 | Incidental | Yes | No | Absent all modifiers |

### Output 2 — Entity→child assignment

Every proposed child needs an **entity core** — the central entities it owns outright — not just a
keyword.

| Child | Primary keyword | Central entities owned | Count | Clears R7? |
|---|---|---|---|---|
| Child 1 | [kw] | E1, E4, E7, E9, E12 | 5 | Yes |
| Child 2 | [kw] | E2, E5, E11 | 3 | **No — fold back** |

A child that can't clear R7 (minimum central entities) is not a viable article regardless of its word
count. Fold it into its nearest neighbour by entity overlap.

Entities that legitimately belong to more than one child are **shared context** — permitted, but they
count toward the overlap maths below, and the child that explains an entity most fully owns it.

### Output 3 — Entity overlap matrix

The Tier-2 test from the decision cascade. For every child pair, compute shared central entities as a
percentage of the smaller set:

```
shared_pct = |A ∩ B| / min(|A|, |B|)
```

|  | Child 1 | Child 2 | Child 3 |
|---|---|---|---|
| **Child 1** | — | 22% | 18% |
| **Child 2** | 22% | — | **64%** |
| **Child 3** | 18% | 64% | — |

Apply R4 / R5 from the ruleset:

| Overlap | Reading | Action |
|---|---|---|
| ≥ 60% (R4) | Same subject matter regardless of keyword difference | **Block the split.** Merge the pair. |
| 36–59% | Ambiguous | Route to Tier 3 Q&A |
| ≤ 35% (R5) | Genuinely distinct subject matter | Split is safe on entity grounds |

Using the *smaller* set as the denominator is deliberate: it catches the case where a small child is
wholly contained within a larger one, which raw Jaccard would mask.

**In the example above, Children 2 and 3 must merge** — 64% is over the R4 block threshold even if
their primary keywords look distinct.

### Output 4 — Entity gap list

| Missing entity | Type | Competitors covering it | Assign to |
|---|---|---|---|
| [name] | Standard | 6 of 10 | Child 1 |
| [name] | Concept | 4 of 10 | Child 3 |

Sort by competitor frequency. An entity that 6+ of the top 10 treat as central and you don't cover at
all is a structural coverage hole, not a nice-to-have.

---

## Use in Mode B (social atomisation)

Lighter application, but real:

- **Central entities are the specifics that make a hook land.** Named standards, model numbers, and
  measured values are what stop a scroll; generic claims don't.
- **Entity list drives topic-authority consistency** — posting repeatedly around the same entity core
  is what builds a recognisable niche on every platform.
- **Novel/proprietary entities are your differentiated content.** If it resolves nowhere, nobody else
  is posting about it — lead with those.

---

## Quality rules

1. **Central vs. incidental is the load-bearing judgement.** Sloppy classification corrupts every
   downstream number. When genuinely unsure, apply the removal test.
2. **Never fabricate a resolvability check.** If you haven't verified an entity has a canonical
   reference, mark it unknown. A fabricated Wikidata claim is worse than no claim.
3. **Novel entities count fully for overlap, and zero for authority.** Both halves matter.
4. **Report which evidence sources were unavailable.** Especially for novel content, where two of the
   three usually are.
5. **Extract before grouping.** Entity distribution drives split grouping. Running it afterwards to
   validate a grouping you already chose defeats the point.
6. **Don't inflate the inventory.** Every common noun is not an entity. If it wouldn't appear in a
   knowledge graph or a spec sheet, it's vocabulary, not an entity.
