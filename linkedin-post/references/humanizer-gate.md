# Writing checks and the score

The checks every LinkedIn draft passes before it is saved: posts from `linkedin-post`, and comment
and reply drafts from `linkedin-engage`. They keep the account's own voice and show the writer which
shapes a reader takes for machine-written text. They are craft checks. The Page records govern what a
post may say and how it is laid out.

Based on the li-human scripts (`humanize.py`, `detect.py`, `slop.json`) and skill text of
`linkedin-agent-skill` by Jake Schincariol (https://github.com/Jakeschincariol/linkedin-agent-skill),
MIT licence, Copyright (c) 2026 Jake Schincariol. The written checks below are merged with the
stock-phrase list in `social-content` (`references/drafting-guide.md` and `references/editing-guide.md`) and the checklist in
`content-humanizer` (`references/ai-tells-checklist.md`).

## What the score run does

The draft file keeps the text **exactly as written**. Nothing cleans, replaces or removes anything. Where the author's
`detect.py` is installed (`<detect.py path>`), run it unchanged on that text and scan it for what a clean step would have
replaced:

1. `detect.py` scores the text: five checks (BURSTINESS, SPECIFICITY, SLOP DENSITY, FINGERPRINT,
   VOICE), each 0 to 100, an overall `human_score` and a `verdict` (`PASS`, `REVIEW` or `FLAGGED`).
   It adds the structural tells it found (`structures`), which nothing rewrites.
2. The scan counts invisible characters (zero-width and joiner characters, no-break and unusual
   spaces, the soft hyphen, direction marks) and typographic marks (em and en dashes, curly quotes,
   the ellipsis character), and leaves every one in the text. A joiner inside an emoji sequence is
   part of the emoji and is not counted.

The score run gives one `humaniser` entry per LinkedIn draft, in order:

- the report: `human_score`, `verdict`, `checks`, `structures` and `found` (`invisible` and
  `typographic`, each a list of name and count);
- `{error: "..."}` when the scoring service could not run: the draft was saved exactly as sent, with
  no score;
- `null` for a channel other than LinkedIn.

The score, the structures and the found items are written in the draft file's receipt.

## What the writer does with the report

1. Read the `humaniser` entry. Never skip it and never report a score that is not in it.
2. Report every `found` item and every `structures` entry in the receipt, with its count.
3. Fix a found typographic item or a flagged structure by editing the text, and save once more with
   `replaces_draft_id`. One such rewrite is the limit for a score. An invisible character is never
   removed by the writer or by any tool without a person's decision: report it, with the count, and leave
   it. The approver decides (an emoji joiner is legitimate).
4. Do not loop to reach `PASS`. The verdict is evidence for the approver, not a gate, and no rewrite
   exists to raise it.
5. On `{error}`: run the written checks below by hand, say in the receipt that the draft was not
   scored and why, and invent no score.

**Known effect on the score (VOICE):** `detect.py`'s VOICE check rewards contractions and personal
pronouns. The Page voice bars contractions and the second person, so a Page draft scores lower on
VOICE by design. Say so in the receipt. Never add contractions or "you" to lift the score.

Comments and replies from `linkedin-engage` are not saved, so the scripts do not run on them: apply
the checks below by hand.

## What this check is, and what it is not

- `detect.py` is local heuristics, as its author says. It calls no detector service and cannot
  predict one's verdict.
- Evading a detector is not a goal. Never describe a draft as undetectable, as passing a detector,
  or as safe from being flagged. The checks exist for quality, clarity and voice.
- The score warns; it never blocks a save. A named person decides.

## Order of work

1. Write the draft, then apply the shape and word checks below by hand, so the saved text is the one
   the writer chose.
2. Run the written checks.
3. For a post, save, read the report, and act on it as above. A comment or reply is not saved:
   stop after the written checks and give the draft in chat.
4. Show the saved text with the receipt. Never the receipt alone.

## 1. Typography and invisible characters (writer's checks)

The text carries no em dash, en dash or spaced hyphen used as a dash, no curly quote where a plain
one is meant, no ellipsis character and no invisible character the writer did not intend. A dash
becomes a full stop, comma, colon or brackets (rewrite the sentence if needed); an en dash in a
range becomes "to". Hyphens inside words are fine.

### The lexicon

When a stock word appears in the draft, the writer swaps it for the plain word by hand, keeps
capitalisation, and leaves URLs and names untouched. Check the sentence still reads; rewrite it if
the swap is clumsy. No tool replaces anything in the saved text: the score reports slop density and the
writer fixes it.

**Verbs:** delve into (look at), delve (look), dive deep into (get into), leverage (use),
leveraging (using), utilize or utilise (use), utilizing or utilising (using), harness (use), embark
on (start), foster (build), facilitate (help), showcase (show), unlock (get), elevate (improve),
streamline (simplify), spearhead (lead), underscore (show), underscores (shows), cultivate (build),
amplify (boost), curate (pick), curated (picked), empower (let), revolutionize or revolutionise
(change). From `social-content`: supercharge, transform (use the exact verb).

**Adjectives:** transformative (big), robust (solid), seamless (clean), seamlessly (cleanly),
pivotal (key), crucial (important), vital (important), comprehensive (complete), cutting-edge
(new), game-changing (big), groundbreaking (new), unparalleled (unmatched), invaluable (useful),
meticulous (careful), meticulously (carefully), myriad of (many), myriad (many), multifaceted
(complicated), holistic (whole), bespoke (custom), innovative (new), profound (big), remarkable
(notable), compelling (convincing). From `social-content`: revolutionary, unprecedented (cut unless
literally true or quoted).

**Nouns:** deep dive (breakdown), game-changer (big deal), tapestry (mix), realm (world), landscape
(market), journey (process), testament to (proof of), cornerstone (base), beacon (signal), paradigm
(model), synergy (overlap), ecosystem (system), treasure trove (pile), plethora of (lots of),
plethora (lots), arsenal (set), north star (goal).

**Connectives:** moreover (also), furthermore (also), additionally (also), nevertheless (still),
consequently (so), thus (so), hence (so), notably (delete), importantly (delete), ultimately (in
the end), in essence (basically), in conclusion (so), when it comes to (with), in order to (to), a
wide range of (many), it is worth noting that (note that). From `social-content`: it is important
to note, needless to say, serves as a testament to.

**Openers (delete or replace):** in today's fast-paced world (right now), in today's digital age
(right now), in the ever-evolving landscape of (in), in the ever-changing world of (in), let's face
it, here's the thing, picture this, imagine a world where (imagine if), it's no secret that, we've
all been there, I am excited to announce, I'm thrilled to share, I am humbled to, without further
ado, buckle up, the harsh truth is, spoiler alert. From `social-content`: let's dive in, the truth
is, in an ever-evolving landscape.

**Closers (delete):** let that sink in, the choice is yours, food for thought, the future is here,
what are your thoughts?, drop a comment below, at the end of the day, read that again, you're
welcome, save this for later, who's with me. Also: needle-moving (useful), move the needle (make a
difference), a testament to (proof of), had the opportunity to (got to). From `social-content`:
the lesson is, the key takeaway, hope this helps, follow for more, comment below.

**Empty drama (rewrite unless the source earns it):** but that's only half the story, what
happened next surprised me, this changed everything.

The account's strategy may remove a word from this list when the poster genuinely uses it.

## 2. Flagged structures (rewrite by hand)

| Flag | Pattern | Fix |
|---|---|---|
| not-just | "It's not just X, it's Y" | Say the one thing meant. Delete the setup half. |
| not-only | "Not only X but also Y" | Split into two sentences, or drop the weaker half. |
| isnt-about | "It isn't about X. It's about Y." | Lead with Y. The reversal is the tell. |
| from-x-to-y, whether-you | "from X to Y", "whether you're X or Y" | Name the actual range or the actual reader. |
| the-result | a one-word or two-word rhetorical question line ("The result?", "The catch?") | Answer it inline. |
| heres-what | "Here's what I learned" | State the lesson. |
| triad | a neat list of three ("fast, simple, and cheap.") | Two items or four, unless there are really three. |
| emoji | any emoji, especially rocket, fire, bulb, sparkles, dart | None in a company post; a personal account follows its own record. Never an emoji bullet or opener. |
| hashtags | any hashtag | None. |
| bait | "Agree?", "Thoughts?", "Who else?", "Am I wrong?", "Comment below", "Repost if", "Follow for more", "comment X and I'll send it" | Ask a question only this post could ask, or end on a grounded line. |
| two CTAs | more than one ask | Keep one, matched to the funnel stage. |
| long first line | line 1 over the layout record's first-line limit | Cut to the hook. |
| as-an-ai | model self-reference | Delete the sentence. |
| essay closer | "In summary", "To summarise", "In conclusion" at the start of a line | A post needs no conclusion paragraph. |
| broetry | a run of one-sentence paragraphs; a line break after every line | Break between ideas, not lines (017, 079). |
| skeleton | "hook, three bullets, lesson, CTA" with nothing at stake | Put back one real friction point, caveat or sharper opinion. |
| uniform rhythm | every sentence or bullet the same length | Vary length: one short line, one longer. |
| moral ending | a motivational closer | End on the specific consequence from this post. |
| second person | "you", "your", "yours" | Name the reader by noun and rewrite in the third person. |

## 3. Written checks (report each)

The numeric limits (length, first line, paragraph and sentence size) are in the layout record and the
content type record. Count; never guess.

- **Length:** count characters and compare with the type record's length band. Report the count made.
- **Dashes:** zero em dashes, en dashes or spaced hyphens.
- **Hashtags:** zero.
- **Emoji:** none for the Page.
- **Bait:** none.
- **Asks:** as the layout record allows.
- **Link:** only as the layout and type records allow, with the tags the link record names.
- **First line:** within the layout record's limit.
- **Spelling:** British (organise, behaviour, colour, centre, programme for a scheme, licence as a
  noun). Proper nouns, product names, URLs and quotes keep their own spelling.
- **Banned phrases:** none from the voice record's lists.
- **Specificity:** at least one concrete number, name, date or detail from a real source, or a
  bracketed placeholder flagged in the receipt. Never an invented one.
- **Voice:** reads like the account: formal, plain, no contractions, no second person.
- **Swap test:** would the post work for any company by swapping one noun? If yes, rewrite.
- **Read aloud:** read the post through once as a cold reader and fix anything that sounds off (079
  tip 18).

## Comments and replies

The same fixes and flags apply. A comment is short and people read it closely, so a dash, a stock
phrase or a generic opener is more obvious in a comment than in a post. A comment that reads as
generated has failed: "generated comments are obvious and they undo the whole thing" (101).

File: linkedin-post/references/humanizer-gate.md · Version 1.0 · November 2026
