#!/usr/bin/env python3
"""humanizer_scorer.py: scores content 0-100 on 'humanity' and lists every AI-writing candidate.

Two outputs from one pass:

1. The score (unchanged since v2.0): 0-100 over seven dimensions (AI vocabulary 20,
   sentence variance 20, passive voice 15, hedging 15, staging and sales 10,
   dashes 10, paragraph variety 10). Code, markup, Liquid, links and YAML front
   matter are stripped before scoring (prose_only).
2. The flag list (v2.1): every candidate hit with its line number, the checklist
   section it belongs to (references/ai-tells-checklist.md), and a PROPOSED
   verdict, KEEP or REWRITE, with the reason. Verdicts are proposals. The editor
   confirms or overturns each one in Mode 1 of SKILL.md. A hit is a candidate,
   never a command.

What the flag pass adds over the score:
- Cross-sentence templates. Paragraphs are joined before matching, so a contrast
  split over two sentences or wrapped over two lines is caught: "isn't X. It's Y",
  "you don't X. You Y", "doesn't need X. It needs Y", "Not X, just Y",
  "not about X, it's about Y", "less about X, more about Y", fragment rows.
- Sibling set mode. Pass two or more files (product descriptions for one
  collection, the email/social variants of one campaign). Any template or staging
  beat used in two or more files is reported, and its flags turn to REWRITE: a
  beat used once is a choice; the same beat in every variant is a reflex.
- Gating. --fail-under N and --fail-on-rewrite return exit code 1 so a pipeline
  can stop on a bad draft. Exit 2 means a usage or file error. Without a gate
  option the exit code is 0, so existing callers are unaffected.

Maintenance contract: every word list and regex here maps to a section of
references/ai-tells-checklist.md (the "ref" field). A change that adds, removes
or edits a rule here also updates the matching checklist section,
then rerun the demo and a real article to check for false positives.

Usage (PowerShell or any shell; quote paths with spaces):
    python "<skill dir>/scripts/humanizer_scorer.py" draft.md
    python "<skill dir>/scripts/humanizer_scorer.py" a.md b.md c.md      # sibling set
    python "<skill dir>/scripts/humanizer_scorer.py" draft.md --protect-headings --fail-on-rewrite
    Get-Content draft.md | python "<skill dir>/scripts/humanizer_scorer.py" -   # stdin
    python "<skill dir>/scripts/humanizer_scorer.py"                      # demo mode

For pasted or untrusted text, save it to a temp file and pass the path. Never
paste source text into the command line itself.
"""

import argparse
import bisect
import json
import math
import re
import sys

# Windows consoles default to cp1252, which cannot print the report's box and emoji characters.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")

# ── Sample content for zero-config demo ──────────────────────────────────────
SAMPLE_HUMAN = """
We tried to fix our churn problem the wrong way for about a year.

We threw money at marketing, assumed acquisition would outpace loss, and avoided looking at the actual numbers. It didn't work. Churn stayed flat at 8% monthly, which sounds manageable until you realize that's 65% annual churn. We were filling a leaky bucket with a garden hose.

What finally worked was embarrassingly simple: we called the customers who left.

We skipped the ones who had complained and went after the ones who stopped logging in without a word. We called 30 churned accounts over two weeks. Most of them didn't hate the product. They forgot about it, because it solved a problem they cared about once and then stopped caring about.

So we rebuilt onboarding around one question: what would make this impossible to ignore?

Three months later, 30-day activation was up 40% and churn had dropped to 4.5%. We still argue about how much of that was onboarding and how much was the pricing change we shipped the same month, which is a question I can't fully answer.
"""

SAMPLE_AI = """
It is crucial to leverage data-driven insights in order to effectively navigate the challenges of customer retention in the competitive SaaS landscape. Furthermore, by implementing robust onboarding strategies, organizations can ensure that users achieve maximum value from the product, thereby significantly reducing churn rates.

To facilitate this process, it's important to note that companies should delve into their customer behavior data to identify patterns and trends. Moreover, by fostering meaningful connections with customers and ensuring comprehensive support throughout their journey, businesses can cultivate lasting relationships that drive long-term success.

In conclusion, the implementation of these holistic strategies will empower organizations to streamline their customer success operations and achieve sustainable growth in an increasingly competitive marketplace.
"""


# ── AI vocabulary signals (whole-word matches) ── checklist C1 ───────────────
AI_VOCABULARY = [
    "delve", "delves", "delving", "deep dive",
    "crucial", "vital", "pivotal",
    "leverage", "leverages", "leveraging", "leveraged",
    "robust",
    "comprehensive",
    "holistic",
    "foster", "fosters", "fostering",
    "facilitate", "facilitates", "facilitating",
    "navigate", "navigating",
    "ensure", "ensures", "ensuring",
    "utilize", "utilizes", "utilizing",
    "furthermore", "moreover", "additionally",
    "innovative", "cutting-edge", "groundbreaking",
    "seamless", "seamlessly",
    "empower", "empowers", "empowering",
    "streamline", "streamlines", "streamlining",
    "cultivate", "cultivating",
    "enhance", "enhances", "enhancing",
    "showcase", "showcases", "showcasing",
    "underscore", "underscores", "underscoring",
    "testament", "tapestry", "interplay",
    "meticulous", "meticulously", "intricate", "intricacies",
    "garner", "garnered", "bolstered",
    "paradigm", "ecosystem", "synergy",
    "in conclusion", "in summary", "to summarize",
    # v2.1 additions (checklist C1 and C5)
    "vibrant", "renowned", "exemplifies", "exemplify", "realm", "enduring",
    "align with", "aligns with", "emphasizing", "encompassing",
]

# "landscape" only counts in its abstract sense; literal landscaping is normal product copy.
ABSTRACT_LANDSCAPE = re.compile(
    r"\b(?:competitive|evolving|ever-changing|changing|digital|business|market|marketing|"
    r"regulatory|industry|tech|technology|current|media|retail|ecommerce|e-commerce|saas)\s+landscape\b"
    r"|\blandscape\s+of\b",
    re.IGNORECASE,
)

# checklist B4. Opening hedges come first; they are cut on sight.
OPENING_HEDGES = [
    "it is important to note",
    "it's important to note",
    "it should be noted",
    "it is worth mentioning",
    "it's worth mentioning",
    "it goes without saying",
    "needless to say",
    "it is crucial to",
    "it's crucial to",
]
STACKED_HEDGES = [
    "one might argue",
    "it can be argued",
    "it could be argued",
    "could potentially",
    "might potentially",
    "might possibly",
    "may potentially",
    "potentially possibly",
]
MID_HEDGES = [
    "in many cases",
    "in most cases",
    "in certain cases",
    "in most instances",
    "in many instances",
    "generally speaking",
    "for the most part",
    "this may vary",
    "results may differ",
    "there are various",
]
HEDGING_PHRASES = OPENING_HEDGES + STACKED_HEDGES + MID_HEDGES

PASSIVE_PATTERNS = [
    r'\b(is|are|was|were|be|been|being)\s+(being\s+)?\w+ed\b',
    r'\b(can|could|should|would|may|might|must)\s+be\s+\w+ed\b',
]

# checklist C6. Counted in the hedging dimension since v2.1.
VAGUE_AUTHORITY = [
    "studies show",
    "research suggests",
    "research shows",
    "experts agree",
    "experts say",
    "experts believe",
    "experts argue",
    "observers have cited",
    "some critics argue",
    "many companies",
    "leading brands",
    "industry reports",
    "it has been shown",
    "according to research",
    "data suggests",
    "evidence suggests",
]

# Staging, chatbot residue, and sales language: the tells that justify an edit on one sighting.
# Each entry: (regex, label, checklist ref). Scored in the staging dimension.
STAGING_PATTERNS = [
    # not X but Y (single sentence)
    (r"\bit'?s not (?:just |only |merely |about )?[^.;!?]{1,60}[,;] it'?s\b", "it's not X, it's Y", "A1"),
    (r"\bnot (?:just|only|merely) [^.;!?]{1,60}\bbut\b", "not just X but Y", "A1"),
    (r"\bisn'?t (?:just|only|merely) (?:a |an |about )?", "isn't just", "A1"),
    (r"\bthis (?:doesn'?t|does not) mean\b", "this doesn't mean X. It means Y", "A1"),
    # closers
    (r"\blet that sink in\b", "let that sink in", "A2"),
    (r"\bread that again\b", "read that again", "A2"),
    # sayings that sound deep
    (r"\bthe real (?:question|skill|problem|issue|reason|story|work|fix|answer|point|difference|win|secret)\b",
     "the real <noun>", "A3"),
    (r"\bat its core\b", "at its core", "A3"),
    (r"\bwhat really matters\b", "what really matters", "A3"),
    (r"\bthe heart of the matter\b", "the heart of the matter", "A3"),
    (r"\bthe deeper issue\b", "the deeper issue", "A3"),
    (r"\bin reality,", "in reality,", "A3"),
    (r"(?:^|[.!?]\s+)fundamentally,", "fundamentally,", "A3"),
    # staged run-ups
    (r"\blet'?s (?:dive|delve|explore|break (?:this|it) down|take a (?:closer )?look)\b", "let's dive in", "A4"),
    (r"\bnow let'?s (?:look|turn|move)\b", "now let's look at", "A4"),
    (r"\bhere'?s (?:the thing|what you need to know|the deal|why this matters)\b", "here's the thing", "A4"),
    (r"\bthe thing is\b", "the thing is", "A4"),
    (r"\bwithout further ado\b", "without further ado", "A4"),
    (r"\bbuckle up\b", "buckle up", "A4"),
    (r"\bhonestly\?", "honestly?", "A4"),
    (r"\breal talk\b", "real talk", "A4"),
    (r"\blet'?s be honest\b", "let's be honest", "A4"),
    # arguing with no one
    (r"\bto be clear\b", "to be clear", "A5"),
    (r"\bdon'?t get me wrong\b", "don't get me wrong", "A5"),
    (r"\ba tempting approach would be\b", "a tempting approach would be", "A5"),
    (r"\bnow that we'?ve covered\b", "now that we've covered", "E4"),
    # chatbot residue, sycophancy, gap-filling
    (r"\bgreat question\b", "great question", "E1"),
    (r"\bi hope this helps\b", "I hope this helps", "E1"),
    (r"\blet me know if you'?d like\b", "let me know if you'd like", "E1"),
    (r"\bwould you like me to\b", "would you like me to", "E1"),
    (r"(?<!\w)you(?:'re| are) absolutely right\b", "you're absolutely right", "E1"),
    (r"\bexcellent point\b", "excellent point", "E1"),
    (r"(?:^|[.!?]\s+)(?:certainly|of course)!", "Certainly! / Of course!", "E1"),
    (r"\bas of my (?:last|latest) (?:update|training)\b", "knowledge-cutoff disclaimer", "E2"),
    (r"\bup to my last training\b", "knowledge-cutoff disclaimer", "E2"),
    (r"\bwhile specific details are (?:limited|scarce)\b", "gap-filling disclaimer", "E2"),
    (r"\bbased on (?:the )?available information\b", "gap-filling disclaimer", "E2"),
    (r"\bmaintains a low profile\b|\bprefers to stay out of the spotlight\b"
     r"|\bkeeps (?:personal details|(?:his|her|their) personal life) private\b",
     "privacy guess", "E2"),
    # inflation and sales language
    (r"\bstands? as a testament\b", "stands as a testament", "C2"),
    (r"\bthe future looks bright\b", "the future looks bright", "C2"),
    (r"\bexciting times\b", "exciting times ahead", "C2"),
    (r"\bthe possibilities are endless\b", "the possibilities are endless", "C2"),
    (r"\bjourney toward excellence\b", "journey toward excellence", "C2"),
    (r"\bserves as\b", "serves as", "C7"),
    (r"\bstands as\b", "stands as", "C7"),
    (r"\bnestled\b", "nestled", "C5"),
    (r"\bin the heart of\b", "in the heart of", "C5"),
    (r"\bboasts?\b", "boasts", "C5"),
    (r"\bbreathtaking\b", "breathtaking", "C5"),
    (r"\bstunning\b", "stunning", "C5"),
    (r"\bmust-(?:have|visit)\b", "must-have", "C5"),
    (r"\belevate your\b", "elevate your", "C5"),
    (r"\bunparalleled\b", "unparalleled", "C5"),
]

# Cross-sentence template shapes (checklist A1 / A2). Matched on joined paragraphs, so a
# contrast split over two sentences or wrapped over two lines is still caught. The second
# beat must point back at the same subject (it / that / they / you), which keeps
# "...because it isn't exciting. You could walk 50 feet to the store" from matching.
TEMPLATE_PATTERNS = [
    (r"\b(?:it|that|this|the\s+\w+)?\s*"
     r"(?:is\s?n'?t|are\s?n'?t|was\s?n'?t|were\s?n'?t|'s\s+not|is\s+not|are\s+not|was\s+not|were\s+not)\b"
     r"[^.!?]{1,80}?[.,;:]\s*"
     r"(?:it'?s|they'?re|that'?s|this'?s|he'?s|she'?s|it\s+is|that\s+is|this\s+is|they\s+are)\b",
     "isn't X. It's Y", "A1"),
    (r"(?<!\w)you\s+(?:do\s?n'?t|do\s+not|are\s?n'?t|are\s+not|can'?t|cannot|won'?t)\b[^.!?]{1,80}?[.,;:]\s*you\b",
     "you don't X. You Y", "A1"),
    (r"\b(?:does\s?n'?t|does\s+not|do\s?n'?t|do\s+not|did\s?n'?t|did\s+not)\s+([a-z]+)\b[^.!?]{0,80}?[.,;:]\s*"
     r"(?:it|they|he|she|we|you|that|this)\s+\1(?:s|es|ed)?\b",
     "doesn't X. It Xs (verb echo)", "A1"),
    (r"(?:^|[.!?]\s+)not\s+[^.!?]{1,60}?[,.]\s*(?:just|merely|simply|only)\b",
     "Not X, just Y", "A1"),
    (r"\bnot\s+(?:just\s+)?about\b[^.!?]{1,80}?[,.;]\s*(?:it'?s|its|it\s+is)\s+about\b",
     "not about X, it's about Y", "A1"),
    (r"\bless\s+about\b[^.!?]{1,80}?\bmore\s+about\b",
     "less about X, more about Y", "A1"),
    (r",\s*no\s+(?:guess\w*|wasted\s+\w+|fluff|filler|hassle|headaches?|surprises|compromises?|nonsense)\s*[.!]",
     "clipped negative tail", "A1"),
    (r"\bno\s+\w+(?:\s+\w+)?[.!]\s+no\s+\w+(?:\s+\w+)?[.!]",
     "fragment row (No X. No Y.)", "A2"),
]

# Flag-only rules: listed with line numbers and verdicts but NOT scored, so v2.0 scores
# stay comparable. Each entry: (regex, label, checklist ref, rule kind).
FLAG_ONLY_PATTERNS = [
    (r"\bfeatures an?\b", "features a (copula avoidance)", "C7", "cluster"),
    (r"\bin order to\b|\bdue to the fact that\b|\bat this point in time\b|\bin the event that\b"
     r"|\b(?:has|have) the ability to\b", "filler phrase", "B4", "cluster"),
    (r"\bdeeply rooted\b|\bfocal point\b|\bindelible mark\b|\bkey turning point\b|\bmarks? a shift\b"
     r"|\bsetting the stage for\b|\breflects a broader\b|\bplays? a (?:key|vital|crucial|pivotal) role\b"
     r"|\blasting legacy\b", "inflated significance", "C2", "rewrite"),
    (r"\bshaping the\b|\bdespite these challenges\b|\bcontinues to thrive\b",
     "inflated significance", "C2", "cluster"),
    (r",\s+(?:highlighting|underscoring|showcasing|emphasizing|reflecting|symbolizing|ensuring|fostering"
     r"|contributing to|encompassing)\b", "-ing rider", "C4", "rewrite"),
    (r"\bnot publicly available\b|\b(?:does|do)\s+not\s+publish\b|\bdoesn'?t\s+publish\b",
     "absence claim", "C6", "rewrite"),
    (r"\b(?:is|are|was|were)\s+(?:simple|clear|obvious|straightforward|twofold)\s*:"
     r"|(?:^|[.!?]\s+)(?:the\s+)?(?:catch|kicker|twist|truth|lesson|takeaway|bottom line|short answer)\s*(?:is\s*)?:",
     "dramatic colon", "A4", "rewrite"),
    (r"\bfeel free to\b|\bhappy to help\b|(?:^|[.!?]\s+)here(?:'s| is) (?:a|an|your)\b",
     "chatbot phrase (soft)", "E1", "edge"),
    (r"\b(?:is|are|was|were|stays?|remains?)\s+(?:very\s+|fully\s+)?[a-z]+-(?:resistant|proof|free|friendly|ready"
     r"|based|driven|focused|made|built|treated|coated|rated|tested)(?=\s*[.,;!?])",
     "hyphenated pair after the noun", "B5", "hyphen_pred"),
    # v3.0 watch phrases (blader/humanizer 4.0.0 structure). Flag-only, so scores stay comparable.
    (r"\bthat distinction matters\b", "that distinction matters", "A2", "rewrite"),
    (r"(?:^|[.!?]\s+)(?:heads up|quick note)\b", "heads up / quick note", "A4", "rewrite"),
    (r"\bone might be tempted to\b|\ban obvious approach would be\b", "rejects an option nobody raised", "A5", "rewrite"),
    (r"\bto be fair\b|\bthis is an inference\b", "qualifier (to be fair / this is an inference)", "B4", "cluster"),
    (r"(?:^|[.!?]\s+)actually,|\bquietly\b", "Actually / quietly", "C1", "cluster"),
    (r"\bcommitment to\b", "commitment to", "C5", "cluster"),
    (r"\bsome critics\b(?!\s+argue)", "some critics", "C6", "rewrite"),
    (r"\boperates as\b|\bmaintains an?\b(?! low profile)|\brefers to\b", "copula avoidance (operates as / maintains a / refers to)", "C7", "cluster"),
    (r"\bnot disclosed\b|\bin the (?:provided|available) sources\b", "gap wording", "E2", "rewrite"),
    (r"\bcompiled from\b|\bgenerated from\b|\bthe table below compares\b|\bthis section is organized by\b",
     "method or layout narration", "E4", "cluster"),
]

HYPHEN_PAIRS = [
    "data-driven", "client-facing", "decision-making", "real-time", "well-documented",
    "end-to-end", "high-quality", "long-term", "well-known", "state-of-the-art",
    "user-friendly", "top-notch", "game-changing", "best-in-class",
]

# Dashes used as punctuation: em dash, en dash, spaced hyphen, double hyphen.
# The lookarounds skip nested list bullets and markdown table rules (|---|).
DASH_PATTERN = re.compile(r"—|–|(?<=\S) - (?=\S)|(?<![-|:])--(?![-|:>])")

# Emoji: pictographic blocks, minus the check marks and stars used in comparison tables.
EMOJI_PATTERN = re.compile(
    "[\U0001F300-\U0001FAFF\U0001F000-\U0001F0FF\U0001F1E6-\U0001F1FF☀-➿⬀-⯿]"
)
EMOJI_EXEMPT = set("✓✔✗✘★☆")   # check marks, crosses, stars
CURLY_PATTERN = re.compile("[‘’“”]")
BOLD_PATTERN = re.compile(r"\*\*[^*\n]+\*\*|__[^_\n]+__")
BOLD_EXEMPT_LINE = re.compile(r"^\s*(?:[-*]\s+)?\*\*(?:warning|caution|note|important|safety)\b", re.IGNORECASE)
INLINE_HEADER = re.compile(
    r"^\s*(?:[-*+]|\d+[.)])\s+(?:\*\*[^*\n]+:\*\*|\*\*[^*\n]+\*\*\s*:|__[^_\n]+:__|__[^_\n]+__\s*:)"
)
HEADING_LINE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
SMALL_WORDS = {"a", "an", "the", "and", "or", "but", "nor", "for", "so", "yet", "of", "to", "in",
               "on", "at", "by", "as", "is", "via", "with", "from", "into", "than"}


# ── Preprocessing ────────────────────────────────────────────────────────────

def prose_only(text: str) -> str:
    """Strip content that is not prose, so code, markup, and links don't count as tells."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)   # YAML front matter
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)           # fenced code
    text = re.sub(r"`[^`\n]*`", "", text)                             # inline code
    text = re.sub(r"\{%.*?%\}|\{\{.*?\}\}", "", text, flags=re.DOTALL)  # Liquid
    text = re.sub(r"<[^>]+>", " ", text)                              # HTML tags
    text = re.sub(r"\]\([^)]*\)", "]", text)                          # markdown link targets
    text = re.sub(r"https?://\S+", "", text)                          # bare URLs
    text = re.sub(r"^\s*(?:[-*_]\s*){3,}$", "", text, flags=re.MULTILINE)  # horizontal rules
    return text


def _blank(match) -> str:
    return "".join(ch if ch == "\n" else " " for ch in match.group(0))


def mask_nonprose(text: str) -> str:
    """Same exclusions as prose_only, but blanked with spaces so line numbers stay true."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # YAML front matter only when a closing delimiter appears near the top
    m = re.match(r"\A---\n(?:.*\n){0,40}?(?:---|\.\.\.)\n", text)
    if m:
        text = _blank(m) + text[m.end():]
    text = re.sub(r"^[ \t]*(```|~~~).*?^[ \t]*\1[^\n]*$", _blank, text, flags=re.DOTALL | re.MULTILINE)
    text = re.sub(r"<!--.*?-->", _blank, text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", _blank, text)
    text = re.sub(r"\{%.*?%\}|\{\{.*?\}\}", _blank, text, flags=re.DOTALL)
    text = re.sub(r"<[^>\n]+>", _blank, text)
    text = re.sub(r"\]\((?:[^()\s]|\([^()\s]*\))*(?:\s+\"[^\"]*\")?\)",
                  lambda mm: "]" + " " * (len(mm.group(0)) - 1), text)
    text = re.sub(r"https?://\S+", _blank, text)
    text = re.sub(r"^\s*(?:[-*_]\s*){3,}$", _blank, text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?\s*$", _blank, text, flags=re.MULTILINE)
    return text


def split_units(text: str):
    """Split text into units for matching: paragraphs (wrapped lines joined), headings,
    list items, and table rows. Returns dicts with joined text and per-line offsets."""
    units = []
    cur = None

    def close():
        nonlocal cur
        if cur:
            units.append(cur)
        cur = None

    for lineno, raw in enumerate(text.split("\n"), 1):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            close()
            continue
        is_heading = bool(HEADING_LINE.match(stripped))
        is_table = stripped.startswith("|")
        is_item = bool(re.match(r"^(?:[-*+]|\d+[.)])\s+", stripped))
        if is_heading or is_table or is_item or cur is None or cur["kind"] in ("heading", "table"):
            close()
            kind = "heading" if is_heading else "table" if is_table else "item" if is_item else "para"
            cur = {"kind": kind, "text": stripped, "starts": [0], "lines": [lineno]}
        else:
            cur["starts"].append(len(cur["text"]) + 1)
            cur["lines"].append(lineno)
            cur["text"] += " " + stripped
    close()
    for u in units:
        u["norm"] = u["text"].replace("’", "'").replace("‘", "'")
    return units


def unit_line(unit, pos: int) -> int:
    i = bisect.bisect_right(unit["starts"], pos) - 1
    return unit["lines"][max(0, i)]


def count_phrase(text_lower: str, phrase: str) -> int:
    return len(re.findall(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", text_lower))


def _phrase_rx(phrase: str):
    return re.compile(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", re.IGNORECASE)


def _nonoverlapping(spans):
    """Keep the first of any overlapping (start, end, ...) spans."""
    kept = []
    last_end = -1
    for sp in sorted(spans, key=lambda s: (s[0], -s[1])):
        if sp[0] >= last_end:
            kept.append(sp)
            last_end = sp[1]
    return kept


def staging_spans(unit_text: str):
    """All staging + template hits in one unit, overlaps removed. (start, end, label, ref, kind)"""
    spans = []
    for pattern, label, ref in TEMPLATE_PATTERNS:
        for m in re.finditer(pattern, unit_text, re.IGNORECASE):
            spans.append((m.start(), m.end(), label, ref, "template"))
    for pattern, label, ref in STAGING_PATTERNS:
        for m in re.finditer(pattern, unit_text, re.IGNORECASE):
            spans.append((m.start(), m.end(), label, ref, "staging"))
    return _nonoverlapping(spans)


# ── Scoring functions ─────────────────────────────────────────────────────────

def score_ai_vocabulary(text: str) -> dict:
    """Score 0-20: fewer AI words = higher score."""
    text_lower = text.lower()
    words_total = max(1, len(re.findall(r'\b\w+\b', text)))

    hits = []
    for phrase in AI_VOCABULARY:
        count = count_phrase(text_lower, phrase)
        if count > 0:
            hits.append((phrase, count))
    landscape = len(ABSTRACT_LANDSCAPE.findall(text))
    if landscape:
        hits.append(("landscape (abstract)", landscape))

    total_hits = sum(c for _, c in hits)
    density = total_hits / (words_total / 100)  # per 100 words

    if total_hits == 0:
        score = 20
    elif total_hits <= 2:
        score = 16
    elif total_hits <= 5:
        score = 11
    elif total_hits <= 10:
        score = 6
    elif total_hits <= 15:
        score = 2
    else:
        score = 0

    return {
        "score": score,
        "max": 20,
        "ai_word_hits": total_hits,
        "density_per_100_words": round(density, 2),
        "flagged_terms": [f for f, _ in sorted(hits, key=lambda h: -h[1])[:10]],
    }


def score_sentence_variance(text: str) -> dict:
    """Score 0-20: high variance = more human (robots use uniform length)."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.split()) >= 3]

    if len(sentences) < 3:
        return {"score": 10, "max": 20, "std_dev": 0, "avg_length": 0, "note": "too few sentences to score"}

    lengths = [len(s.split()) for s in sentences]
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)

    # Good human writing has std_dev of 8-15 for mixed content
    if std_dev >= 12:
        score = 20
    elif std_dev >= 8:
        score = 16
    elif std_dev >= 5:
        score = 10
    elif std_dev >= 3:
        score = 5
    else:
        score = 0  # very robotic: all sentences same length

    return {
        "score": score,
        "max": 20,
        "std_dev": round(std_dev, 1),
        "avg_length": round(avg, 1),
        "min_length": min(lengths),
        "max_length": max(lengths),
    }


def score_passive_voice(text: str) -> dict:
    """Score 0-15: less passive = more human."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    n_sentences = max(1, len(sentences))

    passive_count = 0
    for pattern in PASSIVE_PATTERNS:
        passive_count += len(re.findall(pattern, text, re.IGNORECASE))

    passive_ratio = passive_count / n_sentences

    if passive_ratio < 0.1:
        score = 15
    elif passive_ratio < 0.2:
        score = 12
    elif passive_ratio < 0.3:
        score = 8
    elif passive_ratio < 0.4:
        score = 4
    else:
        score = 0

    return {
        "score": score,
        "max": 15,
        "passive_count": passive_count,
        "passive_ratio": round(passive_ratio, 2),
        "passive_pct": f"{round(passive_ratio * 100)}%",
    }


def score_hedging(text: str) -> dict:
    """Score 0-15: fewer hedges and vague authority claims = more direct = more human.
    Since v2.1, vague authority ("studies show") counts toward this score too."""
    text_lower = text.lower()
    hits = []
    for phrase in HEDGING_PHRASES:
        count = count_phrase(text_lower, phrase)
        if count > 0:
            hits.append((phrase, count))

    total_hedges = sum(c for _, c in hits)
    vague_hits = sum(count_phrase(text_lower, p) for p in VAGUE_AUTHORITY)
    scored = total_hedges + vague_hits

    if scored == 0:
        score = 15
    elif scored == 1:
        score = 12
    elif scored == 2:
        score = 8
    elif scored == 3:
        score = 4
    else:
        score = 0

    return {
        "score": score,
        "max": 15,
        "hedge_count": total_hedges,
        "vague_authority_count": vague_hits,
        "scored_count": scored,
        "flagged_phrases": [f for f, _ in hits],
    }


def score_staging(text: str) -> dict:
    """Score 0-10: staged contrasts (including cross-sentence templates), closers, run-ups,
    chatbot residue, and sales language. These justify an edit on one sighting, so the
    score drops fast."""
    counts = {}
    for unit in split_units(text):
        for _s, _e, label, _ref, _kind in staging_spans(unit["norm"]):
            counts[label] = counts.get(label, 0) + 1

    total = sum(counts.values())

    if total == 0:
        score = 10
    elif total == 1:
        score = 6
    elif total <= 3:
        score = 3
    else:
        score = 0

    return {
        "score": score,
        "max": 10,
        "staging_count": total,
        "flagged_patterns": [f for f, _ in sorted(counts.items(), key=lambda h: -h[1])[:10]],
    }


def score_dashes(text: str) -> dict:
    """Score 0-10: final copy should have no dashes unless the brand voice uses them."""
    dash_count = len(DASH_PATTERN.findall(text))
    word_count = max(1, len(re.findall(r'\b\w+\b', text)))
    per_1000 = dash_count / (word_count / 1000)

    if dash_count == 0:
        score = 10
    elif per_1000 <= 1:
        score = 7   # about one in an article
    elif per_1000 <= 3:
        score = 4
    elif per_1000 <= 6:
        score = 2
    else:
        score = 0   # compulsive: AI fingerprint

    return {
        "score": score,
        "max": 10,
        "dash_count": dash_count,
        "per_1000_words": round(per_1000, 2),
    }


def score_paragraph_variety(text: str) -> dict:
    """Score 0-10: varied paragraph lengths = more human."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and not p.strip().startswith('#')]
    if len(paragraphs) < 3:
        return {"score": 5, "max": 10, "note": "too few paragraphs to score"}

    lengths = [len(p.split()) for p in paragraphs]
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)

    has_short = any(l <= 15 for l in lengths)
    has_long = any(l >= 80 for l in lengths)

    score = 0
    if std_dev >= 30:
        score += 5
    elif std_dev >= 15:
        score += 3
    elif std_dev >= 5:
        score += 1

    if has_short:
        score += 3
    if has_long and std_dev >= 15:
        score += 2

    score = min(10, score)
    return {
        "score": score,
        "max": 10,
        "paragraph_count": len(paragraphs),
        "paragraph_std_dev": round(std_dev, 1),
        "has_short_paragraphs": has_short,
        "avg_paragraph_words": round(avg, 1),
    }


# ── Main scoring ──────────────────────────────────────────────────────────────

def score_humanity(text: str) -> dict:
    text = prose_only(text.replace("\r\n", "\n"))
    vocab = score_ai_vocabulary(text)
    variance = score_sentence_variance(text)
    passive = score_passive_voice(text)
    hedging = score_hedging(text)
    staging = score_staging(text)
    dashes = score_dashes(text)
    paragraphs = score_paragraph_variety(text)

    total = (vocab["score"] + variance["score"] + passive["score"] + hedging["score"]
             + staging["score"] + dashes["score"] + paragraphs["score"])

    if total >= 85:
        label = "Sounds human ✅"
    elif total >= 70:
        label = "Mostly human, light edits needed"
    elif total >= 50:
        label = "Mixed, AI patterns detectable"
    elif total >= 30:
        label = "Robotic, significant rewrite needed"
    else:
        label = "AI fingerprint, full rewrite required 🔴"

    return {
        "humanity_score": total,
        "label": label,
        "sections": {
            "ai_vocabulary": vocab,
            "sentence_variance": variance,
            "passive_voice": passive,
            "hedging": hedging,
            "staging": staging,
            "dashes": dashes,
            "paragraph_variety": paragraphs,
        }
    }


# ── Flag pass: line numbers + proposed KEEP / REWRITE verdicts ────────────────

def _inside_quotes(unit_text: str, pos: int) -> bool:
    before = unit_text[:pos]
    straight = before.count('"')
    opened = before.count("“") - before.count("”")
    return straight % 2 == 1 or opened > 0


def _quote(unit, line):
    """Text of the original line for display, max 100 chars."""
    idx = unit["lines"].index(line)
    start = unit["starts"][idx]
    end = unit["starts"][idx + 1] - 1 if idx + 1 < len(unit["starts"]) else len(unit["text"])
    q = unit["text"][start:end].strip()
    return q if len(q) <= 100 else q[:97] + "..."


def collect_raw_flags(text: str):
    """Find every candidate with its line number. Verdicts are assigned later."""
    masked = mask_nonprose(text)
    units = split_units(masked)
    flags = []

    def add(unit, pos, rule, label, ref, kind, match_text):
        line = unit_line(unit, pos)
        flags.append({
            "line": line, "ref": ref, "rule": rule, "label": label, "kind": kind,
            "match": match_text.strip()[:60], "quote": _quote(unit, line),
            "unit": id(unit), "unit_kind": unit["kind"],
            "in_quotes": _inside_quotes(unit["norm"], pos),
        })

    word_total = 0
    bold_candidates = []
    for ui, unit in enumerate(units):
        t = unit["norm"]
        word_total += len(re.findall(r"\b\w+\b", t))
        # staging + templates (scored)
        for s, _e, label, ref, kind in staging_spans(t):
            add(unit, s, kind, label, ref, "red", t[s:_e])
        # vocabulary (scored)
        for phrase in AI_VOCABULARY:
            for m in _phrase_rx(phrase).finditer(t):
                add(unit, m.start(), "vocab", phrase, "C1", "vocab", m.group(0))
        for m in ABSTRACT_LANDSCAPE.finditer(t):
            add(unit, m.start(), "vocab", "landscape (abstract)", "C1", "vocab", m.group(0))
        # hedging and vague authority (scored)
        for group, rule in ((OPENING_HEDGES, "hedge_open"), (STACKED_HEDGES, "hedge_stack"),
                            (MID_HEDGES, "hedge_mid")):
            for phrase in group:
                for m in _phrase_rx(phrase).finditer(t):
                    add(unit, m.start(), rule, phrase, "B4", rule, m.group(0))
        for phrase in VAGUE_AUTHORITY:
            for m in _phrase_rx(phrase).finditer(t):
                add(unit, m.start(), "vague", phrase, "C6", "vague", m.group(0))
        # passive (scored)
        for pattern in PASSIVE_PATTERNS:
            for m in re.finditer(pattern, t, re.IGNORECASE):
                add(unit, m.start(), "passive", "passive voice", "B6", "passive", m.group(0))
        # dashes (scored)
        for m in DASH_PATTERN.finditer(t):
            label = "dash"
            if m.group(0) == "–" and re.search(r"\d\s*$", t[:m.start()]) and re.match(r"\s*[\d$]", t[m.end():]):
                label = "en dash in a numeric range"
            add(unit, m.start(), "dash", label, "B1", "dash", m.group(0))
        # flag-only rules
        for pattern, label, ref, kind in FLAG_ONLY_PATTERNS:
            for m in re.finditer(pattern, t, re.IGNORECASE):
                if label == "absence claim" and re.search(r"\b(?:if|when|unless|where)\b[^.!?]{0,40}$",
                                                          t[:m.start()], re.IGNORECASE):
                    continue   # conditional guidance ("if the maker doesn't publish X"), not a claim
                add(unit, m.start(), "flag", label, ref, kind, m.group(0))
        for phrase in HYPHEN_PAIRS:
            for m in _phrase_rx(phrase).finditer(t):
                predicate = bool(re.match(r"\s*(?:[.,;:!?)]|$)", t[m.end():]))
                add(unit, m.start(), "hyphen", phrase, "B5", "hyphen_pred" if predicate else "hyphen", m.group(0))
        for m in CURLY_PATTERN.finditer(unit["text"]):
            add(unit, m.start(), "curly", "curly quote", "D4", "curly", m.group(0))
        for m in EMOJI_PATTERN.finditer(t):
            if m.group(0) in EMOJI_EXEMPT:
                continue
            add(unit, m.start(), "emoji", "emoji", "D2", "emoji", m.group(0))
        # formatting, line by line
        for idx, line in enumerate(unit["lines"]):
            start = unit["starts"][idx]
            end = unit["starts"][idx + 1] - 1 if idx + 1 < len(unit["starts"]) else len(t)
            seg = t[start:end]
            if INLINE_HEADER.match(seg):
                add(unit, start, "inline_header", "**Label:** list item", "D1", "inline_header", seg[:40])
            elif unit["kind"] != "table" and not BOLD_EXEMPT_LINE.match(seg):
                for m in BOLD_PATTERN.finditer(seg):
                    bold_candidates.append((unit, start + m.start(), m.group(0)))
        if unit["kind"] == "heading":
            hm = HEADING_LINE.match(t)
            words = re.findall(r"[A-Za-z][\w'-]*", hm.group(2)) if hm else []
            after_colon = set()
            for mm in re.finditer(r":\s*([A-Za-z][\w'-]*)", hm.group(2) if hm else ""):
                after_colon.add(mm.group(1))
            cap_small = [w for w in words[1:] if w.lower() in SMALL_WORDS and w[0].isupper()
                         and w not in after_colon]
            big = [w for w in words if w.lower() not in SMALL_WORDS]
            all_big_capped = len(words) >= 4 and big and all(w[0].isupper() for w in big) \
                and any(w.lower() in SMALL_WORDS and w[0].islower() for w in words[1:])
            if cap_small or all_big_capped:
                add(unit, 0, "title_case", "Title Case heading", "D2", "title_case", hm.group(2)[:40])
            # heading echoed by a short first sentence (E3)
            if ui + 1 < len(units) and units[ui + 1]["kind"] == "para" and hm:
                nxt = units[ui + 1]
                first = re.split(r"(?<=[.!?])\s+", nxt["norm"])[0]
                hwords = {w.lower() for w in words if len(w) > 3}
                fwords = {w.lower() for w in re.findall(r"[A-Za-z][\w'-]*", first)}
                new_words = {w for w in fwords if len(w) > 3 and w not in hwords}
                if hwords and len(first.split()) <= 12 and len(new_words) <= 3 \
                        and len(hwords & fwords) / len(hwords) >= 0.6:
                    add(nxt, 0, "heading_echo", "heading repeated in first sentence", "E3", "rewrite", first[:60])

    if len(bold_candidates) >= 3:
        for unit, pos, mt in bold_candidates:
            add(unit, pos, "bold", "bold emphasis", "D1", "bold", mt)

    flags.sort(key=lambda f: (f["line"], f["ref"]))
    return flags, word_total, units


REASONS = {
    "A1": "staged contrast: say the point plainly; KEEP only if its negative half corrects a belief the reader really holds",
    "A2": "closer or fragment row: cut, or merge into one sentence that carries a fact",
    "A3": "saying that sounds deep: replace with the specific claim underneath",
    "A4": "run-up before the point: delete it and start with the point",
    "A5": "arguing with no one: remove the defense or state the real claim",
    "E1": "chatbot residue: remove the wrapper, keep the content",
    "E2": "knowledge-limit or guess: remove the gap wording and keep every supported fact; never guess",
    "E3": "heading repeated in the first sentence: delete the repeat",
    "E4": "empty connective: cut; let the headings navigate",
    "C2": "inflated significance: keep the fact, drop the significance",
    "C5": "sales language: say what the thing is and does",
    "C6": "vague authority: name the source the draft gives, narrow, or cut; never write a source in",
    "C7": "copula avoidance: use is / are / has",
}


def assign_verdicts(flags, word_total, opts, sibling_labels=None):
    """Propose KEEP or REWRITE with a reason for every flag."""
    sibling_labels = sibling_labels or {}
    per_unit = {}
    for f in flags:
        if f["rule"] not in ("curly", "passive"):
            per_unit[f["unit"]] = per_unit.get(f["unit"], 0) + 1
    count = {}
    for f in flags:
        count[(f["rule"], f["label"])] = count.get((f["rule"], f["label"]), 0) + 1
    rule_total = {}
    for f in flags:
        rule_total[f["kind"]] = rule_total.get(f["kind"], 0) + 1
    vocab_per_1k = rule_total.get("vocab", 0) / max(1, word_total) * 1000
    hedge_total = sum(rule_total.get(k, 0) for k in ("hedge_open", "hedge_stack", "hedge_mid"))
    passive_n = rule_total.get("passive", 0)
    sentences = max(1, word_total / 18)
    dash_seen = 0

    for f in flags:
        kind, clustered = f["kind"], per_unit.get(f["unit"], 0) >= 2
        verdict, reason = "REWRITE", ""
        if f["in_quotes"] and kind not in ("dash", "curly", "emoji", "bold", "inline_header", "title_case"):
            verdict, reason = "KEEP", "inside a quotation: the text quotes or discusses the phrase"
        elif f["unit_kind"] == "heading" and opts.protect_headings:
            verdict, reason = "KEEP", "heading is protected in this run; raise it upstream if it needs changing"
        elif kind == "red":
            n = count[(f["rule"], f["label"])]
            if f["label"] in sibling_labels:
                reason = f"same beat in {sibling_labels[f['label']]} sibling files: a reflex; keep at most one"
            elif n >= 2 and f["rule"] == "template":
                reason = f"same template {n} times in this piece: a reflex"
            else:
                reason = REASONS.get(f["ref"], "acts on one sighting")
        elif kind == "vocab":
            if vocab_per_1k > 5 or clustered:
                reason = f"stock AI word in a cluster ({vocab_per_1k:.1f} per 1,000 words)"
            else:
                verdict, reason = "KEEP", "isolated instance; one is fine"
        elif kind == "hedge_open":
            reason = "opening hedge with nothing behind it: cut and start with the note"
        elif kind == "hedge_stack":
            reason = "stacked qualifiers: keep one only if the source supports the doubt"
        elif kind == "hedge_mid":
            if hedge_total > 2 or clustered:
                reason = "hedge in a cluster: make the uncertainty specific or state the claim"
            else:
                verdict, reason = "KEEP", "isolated hedge; human writers hedge too"
        elif kind == "vague":
            reason = REASONS["C6"]
        elif kind == "passive":
            if passive_n / sentences >= 0.2:
                reason = "passive voice is frequent: name the actor where that is clearer"
            else:
                verdict, reason = "KEEP", "passive rate in range"
        elif kind == "dash":
            dash_seen += 1
            if dash_seen <= opts.dash_allowance:
                verdict, reason = "KEEP", f"within the voice profile's dash allowance ({opts.dash_allowance})"
            elif f["label"].startswith("en dash in a numeric range"):
                reason = "numeric range: write 'X to Y' (Ground rule 5)"
            else:
                reason = "dash as punctuation: use a period, comma, colon, or parentheses (Ground rule 5)"
        elif kind == "curly":
            if clustered:
                reason = "curly quotes inside a cluster of other tells: normalize"
            else:
                verdict, reason = "KEEP", "CMS typography alone is not a tell"
        elif kind == "emoji":
            if f["unit_kind"] == "table" or opts.allow_emoji:
                verdict, reason = "KEEP", "table marker or voice profile allows emoji"
            else:
                reason = "decorative emoji: remove unless the brand voice uses them"
        elif kind == "bold":
            if opts.allow_bold:
                verdict, reason = "KEEP", "voice profile uses bold signposts (Example Software Co); keep at the profile's rate"
            elif rule_total.get("bold", 0) >= 6 or clustered:
                reason = f"bold used {rule_total.get('bold', 0)} times: keep only emphasis a skimmer needs"
            else:
                verdict, reason = "KEEP", "occasional emphasis"
        elif kind == "inline_header":
            if rule_total.get("inline_header", 0) >= 3:
                reason = "templated **Label:** list: use prose or a plain list unless the labels carry information"
            else:
                verdict, reason = "KEEP", "one or two labeled items are fine"
        elif kind == "title_case":
            reason = "Title Case: use sentence case unless house style says otherwise (SEO H2s follow seo-content); check proper nouns"
        elif kind == "hyphen_pred":
            reason = "hyphen after the noun: drop it ('the coating is scratch resistant')"
        elif kind == "hyphen":
            if rule_total.get("hyphen", 0) + rule_total.get("hyphen_pred", 0) >= 4:
                reason = "hyphenated pairs are piling up: rephrase some"
            else:
                verdict, reason = "KEEP", "attributive hyphen before a noun is correct"
        elif kind == "cluster":
            if count[(f["rule"], f["label"])] >= 2 or clustered:
                reason = f"{f['label']}: repeated or clustered, use the plain form"
            else:
                verdict, reason = "KEEP", "isolated instance"
        elif kind == "rewrite":
            if f["label"] == "absence claim":
                reason = "absence claim: write what was checked ('not listed on [source]'), and add a date only if the draft gives one"
            elif f["label"] == "dramatic colon":
                reason = "colon builds suspense instead of introducing a list, definition, or example"
            elif f["label"] == "-ing rider":
                reason = "-ing rider adds fake analysis: keep the fact, drop the rider"
            else:
                reason = REASONS.get(f["ref"], f["label"])
        elif kind == "edge":
            if f["unit"] in (opts._first_unit, opts._last_unit):
                reason = "chatbot wrapper at the start or end of the piece: remove"
            else:
                verdict, reason = "KEEP", "ordinary phrase mid-text; adjudicate by context"
        f["verdict"], f["reason"] = verdict, reason
    return flags


def analyze(text: str, opts, sibling_labels=None) -> dict:
    result = score_humanity(text)
    flags, word_total, units = collect_raw_flags(text)
    opts._first_unit = id(units[0]) if units else None
    opts._last_unit = id(units[-1]) if units else None
    result["_raw_flags"] = flags
    result["_word_total"] = word_total
    assign_verdicts(flags, word_total, opts, sibling_labels)
    result["flags"] = [{k: v for k, v in f.items() if k not in ("unit", "in_quotes")} for f in flags]
    return result


def cross_file_labels(results: dict) -> dict:
    """Template and staging labels that appear in two or more files."""
    files_by_label = {}
    for name, res in results.items():
        seen = {f["label"] for f in res["_raw_flags"] if f["kind"] == "red"}
        for label in seen:
            files_by_label.setdefault(label, []).append(name)
    return {label: files for label, files in files_by_label.items() if len(files) >= 2}


# ── Reports ───────────────────────────────────────────────────────────────────

def print_report(result: dict, label: str = "") -> None:
    total = result["humanity_score"]
    verdict = result["label"]
    s = result["sections"]

    bar_filled = int(total / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)

    print()
    print("╔══════════════════════════════════════════╗")
    print("║       HUMANIZER SCORER: REPORT           ║")
    print("╚══════════════════════════════════════════╝")
    if label:
        print(f"  Input: {label}")
    print()
    print(f"  HUMANITY SCORE:  {total}/100")
    print(f"  [{bar}]")
    print(f"  Verdict: {verdict}")
    print()
    print("  ── Section Breakdown ──────────────────────")

    sections = [
        ("AI Vocabulary",      s["ai_vocabulary"]),
        ("Sentence Variance",  s["sentence_variance"]),
        ("Passive Voice",      s["passive_voice"]),
        ("Hedging Phrases",    s["hedging"]),
        ("Staging & Sales",    s["staging"]),
        ("Dashes",             s["dashes"]),
        ("Paragraph Variety",  s["paragraph_variety"]),
    ]
    for name, sec in sections:
        sc, mx = sec["score"], sec["max"]
        bar2 = "█" * int(sc / mx * 10) + "░" * (10 - int(sc / mx * 10))
        print(f"  {name:<20} {sc:>2}/{mx}  [{bar2}]")

    print()
    print("  ── Detected Issues ────────────────────────")

    st = s["staging"]
    if st["staging_count"] > 0:
        pats = ", ".join(st["flagged_patterns"][:5])
        print(f"  🔴 Staging / sales tells: {st['staging_count']} [{pats}]")
    else:
        print("  ✅ No staging or sales tells detected")

    v = s["ai_vocabulary"]
    if v["ai_word_hits"] > 0:
        terms = ", ".join(v["flagged_terms"][:5])
        print(f"  🔴 AI vocabulary: {v['ai_word_hits']} hits [{terms}]")
    else:
        print("  ✅ No AI vocabulary detected")

    sv = s["sentence_variance"]
    if sv["std_dev"] < 5:
        print(f"  🔴 Sentence rhythm robotic: std dev only {sv['std_dev']} (target: 8+)")
    elif sv["std_dev"] < 8:
        print(f"  🟡 Sentence variance low: {sv['std_dev']} (target: 8+)")
    else:
        print(f"  ✅ Sentence variance good: {sv['std_dev']}")

    pv = s["passive_voice"]
    if pv["passive_ratio"] > 0.3:
        print(f"  🔴 Passive voice overuse: {pv['passive_pct']} of sentences")
    elif pv["passive_ratio"] > 0.2:
        print(f"  🟡 Passive voice elevated: {pv['passive_pct']}")
    else:
        print(f"  ✅ Passive voice in range: {pv['passive_pct']}")

    hg = s["hedging"]
    if hg["hedge_count"] > 2:
        terms = ", ".join(hg["flagged_phrases"][:3])
        print(f"  🔴 Hedging overload: {hg['hedge_count']} phrases [{terms}]")
    elif hg["hedge_count"] > 0:
        print(f"  🟡 Hedging present: {hg['hedge_count']} phrase(s) {hg['flagged_phrases']}")
    else:
        print("  ✅ No hedging detected")

    if hg["vague_authority_count"] > 0:
        print(f"  🟡 Vague authority claims: {hg['vague_authority_count']} (e.g. 'studies show'). "
              "Name the real source if the draft has one; never invent one")

    dh = s["dashes"]
    if dh["dash_count"] > 0:
        print(f"  🟡 Dashes: {dh['dash_count']} ({dh['per_1000_words']}/1,000 words). "
              "Target 0 unless the brand voice profile uses them")

    pg = s["paragraph_variety"]
    if pg.get("has_short_paragraphs") is False:
        print("  🟡 No short paragraphs: vary paragraph length")

    print()
    print("  ── Priority Fixes ─────────────────────────")

    if st["staging_count"] > 0:
        print("  1. Remove staging and sales tells (state the point directly)")
    if v["ai_word_hits"] > 5:
        print("  2. Replace AI vocabulary")
    if sv["std_dev"] < 8:
        print("  3. Vary sentence length; short sentences must carry a fact")
    if pv["passive_ratio"] > 0.25:
        print("  4. Flip passive sentences to active voice")
    if hg["hedge_count"] > 2:
        print("  5. Cut hedging phrases and state claims directly")
    if dh["dash_count"] > 0:
        print("  6. Replace dashes with periods, commas, colons, or parentheses")
    if pg.get("has_short_paragraphs") is False:
        print("  7. Vary paragraph length with a short paragraph that carries one strong fact")

    if total >= 85:
        print("  ✅ No priority fixes: content reads as human")
    print()


def print_flags(result: dict) -> None:
    flags = result["flags"]
    rewrites = sum(1 for f in flags if f["verdict"] == "REWRITE")
    print("  ── Flags (line, checklist ref, proposed verdict) ──")
    if not flags:
        print("  No candidates found. Semantic patterns (forced triads, synonym cycling, false ranges,")
        print("  uniform section shapes, soul check) still need the manual walk in Mode 1.")
        print()
        return
    print(f"  {len(flags)} candidate(s): {rewrites} proposed REWRITE, {len(flags) - rewrites} proposed KEEP.")
    print("  Proposals, not verdicts: confirm or overturn each with a stated reason (SKILL.md Mode 1).")
    print()
    for f in flags:
        print(f"  L{f['line']:<4} {f['ref']:<3} {f['verdict']:<7} {f['label']}: \"{f['match']}\"")
        print(f"         | {f['quote']}")
        print(f"         -> {f['reason']}")
    print()


def print_cross_file(repeated: dict) -> None:
    print("═" * 60)
    print("SIBLING SET: beats repeated across files")
    print("═" * 60)
    if not repeated:
        print("  No template or staging beat repeats across the set.")
        print()
        return
    print("  A beat used once is a choice. The same beat in several variants is a reflex:")
    print("  vary it or cut all but one.")
    print()
    for label, files in sorted(repeated.items(), key=lambda kv: -len(kv[1])):
        print(f"  {label}: in {len(files)} files")
        for fname in files:
            print(f"      {fname}")
    print()


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8-sig") as fh:
        return fh.read()


def main():
    parser = argparse.ArgumentParser(
        description="Scores content 0-100 on 'humanity' and lists every AI-writing candidate with its line "
                    "number and a proposed KEEP or REWRITE verdict. Checks AI vocabulary, sentence variance, "
                    "passive voice, hedging, staging and sales tells (including cross-sentence templates), "
                    "dashes, and paragraph variety. Code, HTML, Liquid, links, and YAML front matter are ignored. "
                    "Pass two or more files for sibling set mode."
    )
    parser.add_argument("files", nargs="*", default=None,
                        help="Text or markdown file(s) to analyze; '-' reads stdin. Two or more files run "
                             "sibling set mode. With no file, runs a demo comparing human vs AI samples.")
    parser.add_argument("--json", action="store_true", help="Also output results as JSON.")
    parser.add_argument("--no-flags", action="store_true", help="Print only the score report, not the flag list.")
    parser.add_argument("--protect-headings", action="store_true",
                        help="Headings are protected (SEO pipeline, embedded mode): flags in headings become KEEP.")
    parser.add_argument("--dash-allowance", type=int, default=0, metavar="N",
                        help="Dashes the voice profile or house rule allows (default 0). The first N become KEEP.")
    parser.add_argument("--allow-bold", action="store_true",
                        help="The voice profile uses in-text bold signposts (Example Software Co). Bold flags become KEEP.")
    parser.add_argument("--allow-emoji", action="store_true", help="The voice profile uses emoji.")
    parser.add_argument("--fail-under", type=int, default=None, metavar="SCORE",
                        help="Exit 1 if any file scores below SCORE (gate).")
    parser.add_argument("--fail-on-rewrite", action="store_true",
                        help="Exit 1 if any flag has a proposed REWRITE verdict (gate).")
    args = parser.parse_args()

    if not args.files:
        print("[Demo mode: comparing human vs AI sample content]")
        print()
        print("═" * 50)
        print("SAMPLE 1: Human-written content")
        print("═" * 50)
        r1 = analyze(SAMPLE_HUMAN, args)
        print_report(r1, "Human sample")
        if not args.no_flags:
            print_flags(r1)

        print("═" * 50)
        print("SAMPLE 2: AI-generated content")
        print("═" * 50)
        r2 = analyze(SAMPLE_AI, args)
        print_report(r2, "AI sample")
        if not args.no_flags:
            print_flags(r2)

        print(f"  Delta: Human scored {r1['humanity_score']}, AI scored {r2['humanity_score']}")
        print(f"  Difference: {r1['humanity_score'] - r2['humanity_score']} points")
        print()
        return 0

    texts = {}
    for path in args.files:
        try:
            texts[path] = read_input(path)
        except (OSError, UnicodeDecodeError) as exc:
            print(f"Error: cannot read {path}: {exc}", file=sys.stderr)
            return 2

    # First pass without sibling info, to find beats repeated across the set.
    results = {name: analyze(text, args) for name, text in texts.items()}
    repeated = cross_file_labels(results) if len(texts) > 1 else {}
    if repeated:
        counts = {label: len(files) for label, files in repeated.items()}
        results = {name: analyze(text, args, counts) for name, text in texts.items()}

    for name, result in results.items():
        if len(texts) > 1:
            print("═" * 60)
            print(f"FILE: {name}")
            print("═" * 60)
        print_report(result, name)
        if not args.no_flags:
            print_flags(result)
    if len(texts) > 1:
        print_cross_file(repeated)

    if args.json:
        out = []
        for name, result in results.items():
            clean = {k: v for k, v in result.items() if not k.startswith("_")}
            clean["file"] = name
            out.append(clean)
        payload = out[0] if len(out) == 1 else {"files": out, "sibling_repeats": repeated}
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    failed = False
    if args.fail_under is not None and any(r["humanity_score"] < args.fail_under for r in results.values()):
        print(f"GATE: FAIL (a file scored below {args.fail_under})")
        failed = True
    if args.fail_on_rewrite and any(f["verdict"] == "REWRITE" for r in results.values() for f in r["flags"]):
        print("GATE: FAIL (proposed REWRITE verdicts remain; adjudicate or fix them)")
        failed = True
    if (args.fail_under is not None or args.fail_on_rewrite) and not failed:
        print("GATE: PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
