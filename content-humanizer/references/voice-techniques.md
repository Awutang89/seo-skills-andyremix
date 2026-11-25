# Voice techniques reference

The Mode 3 playbook. After Mode 2 removes the AI patterns, these techniques bring in the brand's own personality.

**Two limits apply to everything here:**
1. Voice never adds facts. Every number, anecdote, admission, and customer story must come from the draft, the user, or the brand files (SKILL.md Ground rule 1). In the examples below, numbers stand for figures the brand supplied.
2. Voice never brings back the family A (staging) tells in `ai-tells-checklist.md`. A strong voice states the point. It doesn't stage it with "Here's the thing," a not-X-but-Y contrast, or a dramatic one-line closer.

---

## Brand profiles

Use the brand's profile (`./brand/voice-profile.md`, written by brand-voice) before any generic voice type below. The examples in this skill use these sample brands:

| Brand | Voice type |
|---|---|
| Example Outdoor Store | Warm Lifestyle Expert: close to the Thoughtful Peer, numbers-first, picks a winner |
| Example Industrial Supplier | Direct Expert: consequence-first, uses dashes and in-text bold signposts by design |

Where a profile allows a style the checklist flags (Example Industrial Supplier's dashes and bold signposts), follow the profile's rate. SEO articles follow the dash rule in seo-content.

**Precedence inside a brand's voice files:** explicit rules in `voice-profile.md` win over the approved passage in `calibration.md`, and calibration wins over patterns read from `samples/`. Samples fill gaps only. One habit seen in one sample is not a rule, and a sample never authorizes a claim, a number, or a copied passage. If the brand has no `calibration.md`, say the voice is uncalibrated and suggest adding an approved calibration passage; don't block on it.

**No voice source at all:** use the strongest natural voice already present in the draft; if there is none, use plain neutral prose (specific, varied, no hype). Reference, spec, policy, and legal text stay plain regardless.

---

## Step 1: Extract the voice profile

When no profile exists, ask for one piece of content the brand considers representative, then answer:

| Question | What to look for |
|---|---|
| Average sentence length? | Count words across 10 sentences. 15 or fewer = punchy. 25 or more = flowing. |
| Formality? | Contractions ("it's" vs "it is"), first person, slang, jargon. |
| Humor? | Dry wit, self-deprecating, provocateur, or none. |
| Relationship to the reader? | Peer (figuring it out together), expert (teaching), challenger (tells the reader they are probably wrong). |
| Signature phrases? | Constructions that appear more than once. |
| Punctuation habits? | Dashes, bold, parentheses, exclamation marks, and how often. This sets the dash rate. |
| What do they avoid? | What's conspicuously absent. |

Write this down as a profile before editing, and refer to it throughout.

---

## The core voice types

### Voice type 1: The Direct Expert

**Profile:** Short sentences. Confident claims. Qualifies only when the qualification is the point.

**Natural fit:** B2B, technical buyers, capital equipment, developer tools. Example Industrial Supplier.

**Techniques:**
- Lead each section with the conclusion, not the setup
- Make claims without softening them: "Most shops undersize the compressor" rather than "Many shops may find their compressor sizing could be improved"
- Address the reader in the second person throughout
- Short paragraphs, often 1 to 2 sentences, each carrying a fact
- Lists with the fewest words that still say it
- No rhetorical questions unless the next sentence answers them

**Before:** "It's important to consider that selecting an appropriately sized compressor can have significant positive impacts on operational efficiency."
**After:** "Size the compressor to your peak CFM demand. An undersized unit runs hot and wears out early."

---

### Voice type 2: The Thoughtful Peer

**Profile:** Longer sentences when the thought needs them. Shares the reasoning, not only the conclusion. Treats the reader as roughly an equal.

**Natural fit:** community brands, founder blogs, homeowner guides. The base of Example Outdoor Store's warm expert.

**Techniques:**
- Show the reasoning: say why the brand lands where it does
- Name real uncertainty specifically: "The manufacturer doesn't publish a snow load, so in heavy-snow areas, ask before you buy."
- Share a real mistake before the lesson, if the brand supplied one
- Connect ideas with real transitions instead of jumping
- Use "we" only if there is a real "we"

**Before:** "Homeowners should consider their climate when selecting a greenhouse."
**After:** "Where you live decides most of this. A polycarbonate greenhouse holds heat better through a cold night, and glass lets in more light but loses heat faster. If your winters are long, the polycarbonate kit is usually the better buy."

---

### Voice type 3: The Provocateur

**Profile:** Challenges received wisdom with actual conviction and evidence behind it.

**Natural fit:** opinionated brands, contrarian analysts, challenger startups.

**Techniques:**
- Open with the unpopular claim as a claim: "Most compressor sizing guides overestimate your CFM."
- Challenge a belief the reader actually holds, and say whose belief it is. A contrast against a belief nobody holds is the not-X-but-Y tell.
- Answer the strongest real objection in full, then make the case
- Let an uncomfortable number sit without fanfare, if the brand has the number

**Before:** "There are various approaches to content marketing that teams may find valuable."
**After (the brand supplied its own traffic data):** "Most of our blog posts bring in almost nothing. In our analytics, the top 10% of posts drive nearly all the leads, so we now spend most of our budget updating those."

---

### Voice type 4: The Enthusiastic Practitioner

**Profile:** Real enthusiasm for the craft, shown through detail.

**Natural fit:** hobby and maker products, creative tools, practitioner communities.

**Techniques:**
- Let enthusiasm come through the detail, not adjectives: say what the writer likes and why
- Share the detail only a practitioner would notice
- Use the trade's terms without over-explaining them to practitioners
- Parenthetical asides that show depth: "(Pressure-treated posts are fine here. The hardware is the part that rusts.)"

**Before:** "Proper lumber selection allows for a longer-lasting shed."
**After (illustrative; use only if the product data says this):** "Pick the siding first. Cedar shrugs off rot for years with just a coat of stain, while pine needs sealing every season or it goes gray and soft."

---

## Techniques for any voice type

### The real anecdote

Strong when it's real and specific; invented if the editor writes it. Ask the user for a real story about this, such as a customer, a mistake, or a surprise. Use the format only with their answer:

**Setup:** "When we [did X]..." / **What happened:** "[the specific thing]." / **The lesson:** "[the principle]."

### The honest admission

Readers trust brands that admit what they got wrong, don't know, or tried and failed. Only use an admission the brand actually made. A general limitation from the draft also works: "This kit doesn't include a floor; you'll need to build or buy one."

### The contrarian setup

State a belief the reader really holds, then show what the evidence says. Name the source of the evidence from the draft or brand files. If the conventional wisdom is only partly wrong, say which part: "Bigger tanks help, but only when your demand comes in bursts."

### Sentence rhythm signature

Once the brand's cadence is known, apply it consistently:
- **Punchy brand:** mostly short sentences, each carrying a fact
- **Flowing brand:** longer sentences that build on each other
- **Mixed cadence (most natural):** a longer sentence for context, a short one for the key fact, another longer one that moves on

Short sentences must carry information. Fragment rows for drama are a tell in every voice.

### The earned ending

The last line should add something or send the reader somewhere. It should not repeat.

- **Last concrete fact:** end on the most useful specific and stop
- **The action:** name the one thing to do next ("Measure your space before you order.")
- **An honest limit:** what this doesn't cover, and where to find it

Avoid a closing line that restates the piece ("That's the real difference."), send-offs ("the future looks bright"), and "By following these steps, you'll be well on your way to..."

---

## Editorial presence

Clean prose can still read as written by nobody. Presence means a reader can tell someone chose the evidence, noticed what matters, and made a judgment within what the evidence allows. It comes from:
- **A supported judgment, stated first, then the reason:** "For a windy lot, the steel gazebo is the safer buy: it is rated for 30 mph anchored, and the vinyl model lists no rating." (both facts from the draft)
- **Real tension left visible:** cheap but costly to run, strong but heavy to assemble. Say both. Don't force a tidy verdict the evidence doesn't support, and don't hide a downside.
- **A useful distinction or consequence:** why a spec changes the buyer's decision.
- **Sharp curation:** leaving out what doesn't matter.

**By format.** A comparison or review earns presence with a supported recommendation. A how-to earns it by naming the step most likely to go wrong and why ("Most leaning sheds were leveled by eye."; only if the source says so). A data or spec page earns it through curation, definitions, and calling one limitation important. Don't paste the same devices into every format, and don't spread personality evenly: some passages should just deliver the fact.

**Limits:**
- First person only for work the writer actually supplied, or an author stance the brand stated. Otherwise make the judgment directly, without an invented narrator.
- Examples, analogies, and short stories only when they teach, and no longer than the point needs. Cut sentences that only announce importance or repeat the heading.
- No quirk quotas. An aside, a fragment, dry humor, or a first-person line is welcome when it fits; never add them by quota, and never fake typos or slang.
- **Commercial voice.** Example Outdoor Store and Example Industrial Supplier sell what they write about. Help the reader decide before asking for the sale, judge the store's own products by the same criteria as others, disclose that the store sells them where it matters, and put the call to action after the independent verdict.

## Voice injection quality check

After applying voice:
- [ ] Read it aloud. Does it sound like a person a reader would actually follow?
- [ ] Does every paragraph read differently from the others?
- [ ] Is there at least one moment where this brand's personality is unmistakable?
- [ ] Would someone who knows the brand's other content recognize it?
- [ ] **Was nothing added?** No new number, source, anecdote, admission, or customer claim that wasn't supplied.
- [ ] **Did voice bring back a tell?** Search for "Here's," a not-X-but-Y contrast, a one-line closer, and dashes beyond the profile's rate.
- [ ] **Skeptical-reader read.** Read it as a doubtful member of the audience. Rewrite any passage that could sit in a thousand other articles, claims experience the brand didn't have, hides a downside, or uses polish to outrun the evidence.

File: content-humanizer/references/voice-techniques.md · Version 3.0.0 · November 2026
