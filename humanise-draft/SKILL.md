---
name: humanise-draft
description: "Gate a script or message that may be machine-made: test its frame, scan for tells, send two blind readers, rebuild from the claim, then give one verdict. Triggers on: humanise this, is this AI-made. Outputs the rebuilt copy and its verdict."
---

# Humanise draft

Gates a draft for machine tells and repairs it from the claim, in one pass. It returns PASS or HOLD. A draft that still reads HOLD after the pass is shown to the operator with the HOLD reason stated, and there is no further round unless the operator asks.
Not for: claim truth or source fidelity (a repair is compared against its source in Step 4, and that comparison is not a claim audit); brand voice (the surface's own rules); inventing a human anecdote or detail (never); beating AI detectors or hiding AI use where a platform or policy requires disclosure (not a goal, and not done); a company-page LinkedIn post, which has its own voice profile that this skill does not carry. The only success measure is the operator's read. A PASS means the checks and the blind readers named no tell. It is never a certificate that the text is human.

The rules this skill rests on. Voice is fixed when a text is generated and never repaired at edit by adding texture. A reviewer names the defect and never prescribes a texture change. A model may judge checkable facts about prose and never its quality. Vocabulary is read as a cluster, because a word list gives false positives. The frame is checked before a word is touched, and repair starts from the claim and a specific.

## Tools this skill calls

| Tool | Used for | Cost and limit |
|---|---|---|
| `content-humanizer/scripts/humanizer_scorer.py` | Scan the draft for AI tells and dashes | Pure text checks: no model call, no network. Empty input is NOT RUN |
| A blind reader: a person, or a fresh model session that has not seen the brief | Two blind readers per pass, four if the repair changes the text | Read each result directly. Cost per run not measured (Unknown). The task is at most 3,500 characters, charter included |
| Read the Short's folder, `shorts/<piece-id>/` | Only when the operator names a piece: read its steps and whether the humanise step may start, from `log.md` | Read only, free |
| Read a stored file and its hash in `log.md` | Only when the operator names a piece: read its script and brief, and list what is stored | Read only, free |
| A new file in the Short's folder | Only when the operator names a piece: store the humanise record | One file per version. Not written for a closed step |
| `log.md`, mark a step done | Only when the operator names a piece: close its humanise step with the verdict | Refused with every failed rule if the step may not close. Evidence is up to 20 items of 500 characters |
| `log.md`, reopen a step | Only if the operator asks: send a piece back to its script step | Returns that step and every later one to pending and clears the lock. A note is required |

Not used: any web tool, the refresh and forced-choice procedures (cut, see Honest limits), and `decisions.md`, which is human only.

## References

A reference is read from this skill's folder, at the path in the table below.

| Reference | Fetch it when | Stamp |
|---|---|---|
| `references/reader-charter.md` | When starting the two blind readers: the text to paste at the start of each task | Part of this skill |
| `references/ai-tells.md` | Step 0 (its footer date) and Step 2b: the tells a scan can flag, the tells read by judgement, the vocabulary clusters | Part of this skill |
| `references/narration-ear-rules.md` | For a narration draft, and when a line has a register mismatch | Part of this skill |
| `references/house-spelling-and-punctuation.md` | When the spelling gate or an em dash is in doubt | Part of this skill |
| `references/fence-list.md` | For the topics, names and claims that the brand never covers | Template: the owner fills `[fence-list]` |
| `references/claim-labels.md` | When a repair touches a claim line and its label must be kept | Part of this skill |

## What the operator must supply

- The draft text, pasted; or, for a piece's script, the piece number: the script is read from the piece.
- Its surface: company video narration, a company article, the operator's own message, or another named surface.
- Where a brief exists, its reader, job and stance lines (for a piece, read the latest `brief` artifact).

The artifact steps apply only when a piece number is given and its humanise step is in play. A standalone draft is pasted, checked and handed back, and nothing is stored.

### Artifacts: how this skill keeps its text
The Short's folder of local files, `shorts/<piece-id>/`, stores the text each stage produces. Write the whole text to a new file in that folder, named by its kind and version, for example `humanise-v1.md`. Record the file and its SHA-256 hash in the Short's `log.md`. `log.md` also holds each step's status, `script_version`, `script_locked` and the evidence lines. Only a person writes `decisions.md`, which records each decision with its kind, gate, decider, recorded text and the file and hash it approves. A step is marked done only when its gate is met. Each failed rule is a refusal, and this skill reports it. Read a stored text; never rebuild it from memory. A closed step takes no new text of its kind, only claims, handoff, label and run-record. Say a text is stored only when its file and hash are recorded, and quote that hash.

## Procedure

### Step 0: Pre-flight

1. Read the draft in full. Name its surface. This skill carries the narration rules and the house spelling and punctuation rules. For a surface whose own voice rules are not carried here, say so in the hand-over, apply the shared references only, and do not present the result as a check against that surface's voice. Stop if the surface is a company-page LinkedIn post.
2. Fetch the AI tells reference and read its footer date. If that date is more than 90 days before today, or the model that wrote the draft is newer than the sources the list was read from, say the list may be stale and that gating continues on it. The vocabulary part of the list ages fastest.
3. The scanner's own self-test cannot be run from here. A scan answer is as reliable as its status, and never certifies a text.
4. Build the text to be checked once. For a piece, read the script from the Short's folder, kind `script`, latest, and state the file, version and hash read. For a script, strip it by hand to the narration only, which is what a listener meets: the narration up to its claims heading. If a heading the cut needs, such as `## Straight-through narration`, is missing, that is a layout defect upstream, so report it, make the verdict HOLD, and do not patch the script by hand. For any other draft, strip the notes, frontmatter and source columns by hand and say so. Use this one narration-only text for every check and both readers.
5. State what was loaded and that this is pass 1.

### Step 1: The frame gate

A draft with no audience, no mode or no point of view has a frame defect, not a wording defect. No amount of humanising fixes it, and the repair belongs upstream, with whoever wrote the brief. Write four one-line answers from the brief and the draft together:

1. Who is it talking to? A named reader in their situation.
2. What is it doing for them? Talking with, teaching, arguing or reporting, and which. A text that only states an event, status or number is answered reporting.
3. What is at stake for them if they skip it?
4. Whose voice is it, and what does it think? The narrator's stance.

If any answer cannot be written from the brief and the draft, stop: HOLD, reason "frame", and send the unanswered question back to the brief. Do not humanise a draft that cannot answer these.

### Step 2: Detect, with three instruments

a. The checks. Run `content-humanizer/scripts/humanizer_scorer.py` on the narration-only text, saved as a file:

- The AI tells scan: the scorer lists each hit with its line, its checklist section and an excerpt. Read each hit's tier, the weight of its pattern, from the AI tells reference: 1 the strongest and 3 the weakest. Tier 1 and 2 hits must be resolved. Tier 3 hits are read and noted, not changed, because two of those patterns also fire on ordinary human writing. The scorer flags only some of the tells in the reference. Step 2b reads the whole table. The status is INFO or NOT RUN. A hit is a candidate to read, never a defect.
- The text gates: the em dash (EM) gate reads PASS when the scorer flags no em dash. Read the house spelling (SPELL) gate by hand against the house spelling and punctuation reference. Both must read PASS. The claims (CLAIMS) and brief fence (BRIEF) gates read NOT RUN here because no register or term list is supplied; say so, and do not count them as passes. Check each line against `[screening-rules]` and carry the marker that each rule names.

The NOT RUN rule: a check that cannot run is not a pass. A status of NOT RUN, an unreadable answer, a refusal or an empty input is reported as NOT RUN with its reason and is never reported clean. Any check the verdict depends on that did not run makes the verdict HOLD with that reason.

b. The list read, by reading. Read the draft against the AI tells reference, especially the tells a scan cannot see: no narrator, a defused question, over-explanation, a verdict attached to a fact. Quote each line.

c. Two blind readers, run once. Fetch `references/reader-charter.md`. Each reader's task is the charter, then the narration-only text, and nothing else: no brief, no observation from this pass, no earlier round, no AI tells list, no other reader's output. The charter is 1,331 characters, and the whole task must stay within 3,500 characters, so the text can be at most 2,168 characters. Count it. If it fits, give the same task to two blind readers: two people, or two fresh model sessions that have not seen the brief. The readers are not told the surface. Two readers, because one reader's miss is not independent evidence; they share a model family, so their agreement is not proof either.

Read each reader's answer in full. If a run has not finished, wait and read again before calling it stuck. Never end the turn promising that a result will post: read both before going on. Read each answer only from the report of its own run, never one run's answer from another's. The readers' list of flagged mechanisms is diagnostic and never a gate: a count of tells cannot separate human from machine text, so use the list to find lines to diagnose in Step 3, not to pass or fail.

If the text is over the budget, do not shorten it and do not split it silently. Judge it in context instead: answer the charter's three questions directly, quoting lines. That answer is not blind, because it is written with the brief and the list in hand. Label every such answer "not blind" in the report, and say that no independent reader ran.

### Step 3: Diagnose each flag to its cause

For every flagged line (a tier 1 or 2 hit, the list read, or any reader's named tell), write in a few words what the line is for, then classify it:

| Cause | Meaning | Remedy (all upstream of the prose) |
|---|---|---|
| Scaffold | The line only points at the next, restates, or announces | Cut it |
| Missing specific | The line asserts a connection or a feeling with no fact under it | Get the fact from the sources or ask the operator. Never invent one; otherwise cut |
| Structural pattern | A contrast pair, a refrain, a defused question, a list of three, a trailing verdict | Rebuild from the claim: say the one fact plainly, in the order a person would say it |
| No narrator | Sources reported in order, with no stake, turn or view | A frame defect: HOLD and return to the brief or the concept, do not patch |
| Vocabulary cluster | Several era-tagged words in one paragraph | Use the plain word the speaker would use |
| Register mismatch | The wrong voice for the surface | Rewrite the line from the surface's rules (the narration rules reference for narration) |

### Step 4: Repair, as a new text

Write the repaired text whole and never overwrite the one gated. Rules:

- Keep the script's layout headings, `## Straight-through narration` included, so the checks run on the repaired text without hand-patching.
- Rewrite from the claim and the source, not from the sentence. Prefer cutting to rewriting.
- Never add texture: no fragment for rhythm, no manufactured aside, no invented quirk, no deliberate roughness, no synonym swap. It reads as manufactured, and the original can be reconstructed from it.
- Never invent a specific to fill a missing-fact flag.
- Keep every licensed claim intact. After the rewrite, set each changed claim line beside its source sentence (subject, verb, strength, scope, link) and show the comparison. A repair that shifts a claim is worse than the tell. This is a comparison, not a claim audit: where the piece has a review step, a changed claim line owes that review.
- British spelling, no em dash, and the rules of the surface (fetch the house spelling and punctuation reference if in doubt).

### Step 5: The verdict, one pass

Fix what can be fixed once (Steps 3 and 4), then set the verdict from the repaired text. If the text changed, run the checks again and start two fresh readers on the repaired narration-only text, the same way as in Step 2c. PASS only if all of these hold:

- No tier 1 or 2 hit is unresolved, and EM and SPELL read PASS.
- Question 3 of both readers finds a person: a narrator with a view, a stake, or something only someone who did the work would know.
- Both readers' answer to what kind of text this is and who it is for matches Step 1's.
- Step 1's four answers still hold.

Anything else is HOLD, and the pass ends there. Never self-assert "clean": cite the checks' statuses and quote the readers' answers. The scan, the list read and the repair share the list; the readers do not, which is the independent check. If the readers disagree, the stricter one decides. A verdict set from in-context answers is written "PASS (not blind)" or "HOLD (not blind)".

### Step 6: Hand over, and record

- PASS: show the repaired text. Open the hand-over with four lines: who it is for, what it is doing for them, what is at stake, and the narrator's stance (Step 1's answers). Then say which checks ran and what they cannot show: no instrument certifies "human", and the operator's read decides. Ask for that read as: "reads AI-written, yes or no, and which lines".
- HOLD: show the repaired text with the HOLD reason in one line: the frame question, or the lines the pass could not clear and why, with the checks' statuses and the readers' findings beside it. Say nothing is certified. Do not run a second round; the operator decides whether to ask for one, repair upstream, or take the text as it stands. A frame HOLD is shown too, with the question that goes back to the brief.
- Quote the readers' answers verbatim in the hand-over, with their run numbers.
- Record on a piece, only when the operator names one: read the Short's `log.md` and `decisions.md`. Store the humanise record whole first, as a new file in the Short's folder, kind `humanise`, step `humanise`. It holds the verdict (PASS or HOLD) and its reason, the checks' statuses, the readers' run numbers and answers, the repairs made, the lines left because the fix is upstream, and, when a repair changed the text, the repaired script in full. A repaired script cannot be a new script version while the script step is closed, so it travels inside this record. Then, if the `humanise` step is pending and may start, write the close line in `log.md`: `{step: "humanise", status: "done", verdict: "PASS" or "HOLD", evidence: [...], note}`. Evidence is references of up to 500 characters each, never the text: the humanise file name and hash, the checks' statuses, the readers' run numbers, the verdict and its reason. A HOLD is NOT closed: the step stays pending, and the hand-over says so. Close it only after the operator has cleared it: they repair upstream and a new pass reads PASS, or they say in words to take the text as it stands, and then close it as done with verdict HOLD and a note that quotes their words and says the operator took it as it stands. If the record refuses the close, report each refusal exactly as returned; never say the step is closed when it was refused, and do not retry with changed values.
- If the repaired text differs from the script as the piece has it, say that the script has changed: the lock refuses until a review has run on the version being locked. Humanise runs before the final review round, so a review has not yet read the old text and none is lost. Ask the operator first. If they agree, reopen the script step in `log.md` (step `script`, with a note saying why): review, humanise and lock return to pending and the lock clears. Store the repaired script (kind `script`, step `script`), close the script step in `log.md` (status done, `script_version` one higher than the piece's current value, evidence naming the new file's name and hash), then hand to the review skill for a round on that version. The repair was the humanise pass, so humanise does not run again on that version unless the operator asks.

### Step 7: The operator's read

A line the operator calls AI-sounding that no round flagged is a miss. Report it as a miss with its mechanism, so whoever maintains the list can add it. This skill keeps no store of misses. A flag the operator disagrees with is re-tiered where the list is maintained, not hidden. Do not tune the gate to pass more drafts.

## Run as a batch stage

A stage runner can start this skill as one unit of a batch, with nobody at the keyboard. These rules replace the operator questions and the interactive stops and change nothing else: every refusal and rule above still binds, and nothing here lets the stage decide what a person decides.

1. **No questions.** Step 1's frame answers come from the brief, the concept and the script stored on the piece. An answer the piece does not hold is written beside it as "assumed, not confirmed" and the pass goes on. A missing specific (the table row of that name) is cut, never asked for.
2. **The piece is named in the first line.** Step 6's "record on a piece" applies without waiting for a name. Store the humanise record whole, then close the humanise step with its verdict as Step 6 says. A HOLD closes the step as HOLD: it is a flag at the next checkpoint, never a stop and never a reason to run a second round.
3. **A repair that changes the text stays in the record.** Store the repaired script in full inside the humanise record and say in the reply that it differs from the script as stored. Do not reopen the script step and do not ask to: a reopen is a person's, and the next review round reads the script as stored.
4. **Skip Step 7.** The operator's read is asked of nobody here. The hand-over's "ask for that read" line is left out.
5. **Readers run inside the turn.** Start each blind reader, wait for it in this turn and read its result directly. Never end the turn with a run pending.
6. **What stays a person's:** a decision, an approval, an `n/a` mark, a reopen of the script, and the choice to repair upstream a line the pass could not clear.

## Honest limits

- The scan is a set of patterns. It misses what it does not name, and two of its patterns fire on ordinary human writing. The list is not validated on readers of the company's own content.
- Two readers share a model family and judge only what fits in their task, so a clean read proves nothing about a longer text. Over the budget the check is not blind.
- The person condition in Step 5 assumes a surface that has an author. A surface written in the company's name with no person has its own profile, which this skill does not carry.
- Cost: the checks are free text checks with no model call. Each reader is a person or a fresh model session: two per pass, four when the repair changes the text. Cost per run is unmeasured (Unknown).
- The AI tells list carries its own read date in its stamp: 6 November 2026.

File: humanise-draft/SKILL.md · Version 1.0 · November 2026
