#!/usr/bin/env python3
"""fact_diff.py: proves a humanize or edit pass changed prose only.

Compares the text BEFORE a pass with the text AFTER it and reports every change to
material the pass is not allowed to touch (SKILL.md Ground rules 1, 2 and 4):

  numbers        values with currency and units ($1,299.99, 30 mph, 135 PSI, 5-year,
                 99%), number words (two to ninety), dimensions (10x12, 10 x 12 ft)
  dates          2026-09-27, September 27, 2026, Sept. 5, September 2026, Q3 2026, 9/27/2026
  urls           markdown link and image targets (parentheses inside URLs are handled),
                 autolinks, bare URLs, HTML href and src
  link anchors   the anchor text paired with each URL
  headings       markdown and HTML headings, in order, with their level
  entities       brand, product, model and place names (Brand A, Example Sub-brand, XT-54, Example Retailer).
                 Harvested from mid-sentence capitals, ALL CAPS and alphanumeric tokens,
                 so ordinary sentence-initial words do not count
  protected      code blocks, inline code, Liquid tags, HTML tags and comments, YAML front
                 matter, placeholders ({{...}}, [[...]], [TODO ...], <INSERT ...>), Shopify
                 metafield references, footnote markers, table rows (in order), and any
                 phrase passed with --protect

This is a mechanical regression gate. It does not judge evidence, voice, or prose
quality, and a pass here does not mean the text is true. It only proves the pass
did not move the facts.

Exit codes: 0 = no unapproved change; 1 = unapproved change (or an --article-checks
failure); 2 = usage or file error.

A change can be approved when a pattern fix really called for it (for example, a
cut sentence that only repeated a number stated elsewhere). Approve by value or by
category:value, on the command line or one per line in a file:
    --approve "$1,299.99"   --approve "entities:Example Retailer"   --approve "headings:*"
Thousands separators are ignored on both sides, so "$1,299.99" and "$1299.99" match.

Usage (PowerShell or any shell; quote paths with spaces):
    python "<skill dir>/scripts/fact_diff.py" before.md after.md
    python "<skill dir>/scripts/fact_diff.py" before.md after.md --protect "Example Outdoor Store" --json
    python "<skill dir>/scripts/fact_diff.py" --self-test
    python "<skill dir>/scripts/fact_diff.py" edited.md article.md --article-checks \\
        --site-url https://example.com/blogs/resources/<slug>
"""

import argparse
import bisect
import difflib
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlsplit

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MONTHS = {
    "january": "jan", "february": "feb", "march": "mar", "april": "apr", "may": "may", "june": "jun",
    "july": "jul", "august": "aug", "september": "sep", "october": "oct", "november": "nov",
    "december": "dec", "jan": "jan", "feb": "feb", "mar": "mar", "apr": "apr", "jun": "jun",
    "jul": "jul", "aug": "aug", "sep": "sep", "sept": "sep", "oct": "oct", "nov": "nov", "dec": "dec",
}
MONTH_RX = (r"(?:January|February|March|April|May|June|July|August|September|October|November|December"
            r"|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\.?")

NUMBER_WORDS = {
    "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
    "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}

UNIT_RX = (r"%|percent|psi|scfm|cfm|gallons?|gal|horsepower|hp|volts?|vac|v|amps?|dba|db|feet|foot|ft"
           r"|inch(?:es)?|in\.|mm|cm|lbs?|pounds?|kg|mph|sq\.?\s?ft|square\s+feet|years?|yrs?|months?"
           r"|weeks?|days?|hours?|hrs?|minutes?|mins?|seconds?|°\s?[fc]|btu|kw|watts?|w|rpm|"
           r"people|persons?|pieces?|pcs|swings?|seats?|kids|children|bays?|stages?|cylinders?")
UNIT_NORMAL = [
    (r"^(?:percent)$", "%"), (r"^gallons?$|^gal$", "gal"), (r"^horsepower$", "hp"), (r"^volts?$", "v"),
    (r"^amps?$", "a"), (r"^dba$", "db"), (r"^(?:feet|foot)$", "ft"), (r"^inch(?:es)?$|^in\.$", "in"),
    (r"^(?:lbs?|pounds?)$", "lb"), (r"^sq\.?\s?ft$|^square\s+feet$", "sqft"), (r"^(?:years?|yrs?)$", "yr"),
    (r"^months?$", "mo"), (r"^weeks?$", "wk"), (r"^days?$", "day"), (r"^(?:hours?|hrs?)$", "hr"),
    (r"^(?:minutes?|mins?)$", "min"), (r"^seconds?$", "s"), (r"^watts?$", "w"), (r"^°\s?f$", "°f"),
    (r"^°\s?c$", "°c"), (r"^persons?$", "people"), (r"^(?:pieces?|pcs)$", "pc"),
]

ENTITY_STOP = {
    "I", "I'm", "I've", "I'll", "I'd", "OK", "A", "An", "The", "This", "That", "These", "Those", "It", "Its",
    "It's", "If", "When", "Where", "While", "For", "And", "But", "Or", "So", "Yet", "You", "Your", "You're",
    "We", "Our", "We're", "They", "Their", "They're", "He", "She", "His", "Her", "In", "On", "At", "To",
    "With", "By", "From", "As", "Is", "Are", "Was", "Not", "No", "Yes", "Here", "There", "What", "How",
    "Why", "Which", "Who", "Each", "Every", "Most", "Many", "Some", "All", "Any", "Both", "One", "Then",
    "Also", "Just", "Only", "Even", "After", "Before", "Because", "Since", "Unless", "Until", "Once",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "TL", "DR", "FAQ",
    "Q", "Note", "Tip", "Step", "Warning", "Caution", "Important",
} | {m.capitalize() for m in MONTHS} | {w.capitalize() for w in NUMBER_WORDS}


# ── helpers ──────────────────────────────────────────────────────────────────

def blank(s: str) -> str:
    return "".join(ch if ch == "\n" else " " for ch in s)


class Doc:
    """One text, with every protected category extracted and positions mapped to lines."""

    def __init__(self, text: str):
        self.raw = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("﻿")
        self.nl = [i for i, ch in enumerate(self.raw) if ch == "\n"]
        self.tokens = defaultdict(list)      # category -> [(token, line)]
        self.ordered = {}                    # category -> [(token, line)] compared in order
        self.links = []                      # (anchor, url, line)
        self._extract()

    def line(self, pos: int) -> int:
        return bisect.bisect_right(self.nl, pos - 1) + 1 if pos > 0 else 1

    def add(self, cat, token, pos):
        self.tokens[cat].append((token, self.line(pos)))

    def _sub(self, text, pattern, cat, flags=0, keep=None, token_fn=None):
        """Record every match as a token of `cat`, then blank it so later passes skip it."""
        def repl(m):
            tok = token_fn(m) if token_fn else m.group(0)
            if tok is not None:
                self.add(cat, tok, m.start())
            if keep is not None:
                return keep(m)
            return blank(m.group(0))
        return re.sub(pattern, repl, text, flags=flags)

    def _extract(self):
        t = self.raw
        # protected blocks
        fm = re.match(r"\A---\n(?:.*\n){0,60}?(?:---|\.\.\.)\n", t)
        if fm:
            self.add("protected", "front matter:\n" + fm.group(0).strip(), 0)
            t = blank(fm.group(0)) + t[fm.end():]
        t = self._sub(t, r"^[ \t]*(```|~~~)[^\n]*\n.*?^[ \t]*\1[^\n]*$", "protected",
                      re.DOTALL | re.MULTILINE, token_fn=lambda m: "code block: " + m.group(0).strip())
        t = self._sub(t, r"<!--.*?-->", "protected", re.DOTALL, token_fn=lambda m: "html comment: " + m.group(0))
        t = self._sub(t, r"`[^`\n]+`", "protected", token_fn=lambda m: "inline code: " + m.group(0))
        t = self._sub(t, r"\{%.*?%\}|\{\{.*?\}\}", "protected", re.DOTALL,
                      token_fn=lambda m: "liquid: " + re.sub(r"\s+", " ", m.group(0)))
        # links, before HTML tags are blanked
        for m in re.finditer(r"<a\b[^>]*\bhref\s*=\s*[\"']([^\"']*)[\"'][^>]*>(.*?)</a>", t, re.I | re.S):
            self.links.append((re.sub(r"<[^>]+>|\s+", " ", m.group(2)).strip(), m.group(1), self.line(m.start())))
            self.add("urls", m.group(1), m.start())
        for m in re.finditer(r"<(?:img|source|iframe|script|link)\b[^>]*\b(?:src|href)\s*=\s*[\"']([^\"']*)[\"']",
                             t, re.I):
            self.add("urls", m.group(1), m.start())
        t = self._sub(t, r"<[A-Za-z/!][^>\n]*>", "protected", token_fn=lambda m: "html: " + m.group(0))
        # placeholders, metafields, footnotes
        t = self._sub(t, r"\[\[[^\]\n]+\]\]|\[(?:TODO|INSERT|PLACEHOLDER|CTA|IMAGE|LINK|TK)\b[^\]\n]*\]"
                         r"|\{[A-Z][A-Z0-9_]{2,}\}", "protected", token_fn=lambda m: "placeholder: " + m.group(0))
        t = self._sub(t, r"\b(?:product|article|shop|collection|page|blog|variant|customer)\.metafields\.[\w.]+",
                      "protected", token_fn=lambda m: "metafield: " + m.group(0))
        t = self._sub(t, r"\[\^[^\]\n]+\]", "protected", token_fn=lambda m: "footnote: " + m.group(0))
        # markdown links and images: [anchor](url "title"); URLs may contain balanced parentheses
        md_link = r"(!?)\[((?:[^\[\]\n]|\[[^\[\]\n]*\])*)\]\(\s*<?((?:[^()\s<>]|\([^()\s]*\))+)>?(?:\s+\"[^\"]*\")?\s*\)"

        def link_keep(m):
            if not m.group(1):
                self.links.append((m.group(2).strip(), m.group(3), self.line(m.start())))
            self.add("urls", m.group(3), m.start())
            return " " * (len(m.group(1)) + 1) + m.group(2) + " " * (len(m.group(0)) - len(m.group(2)) - len(m.group(1)) - 1)
        t = re.sub(md_link, link_keep, t)
        t = self._sub(t, r"<(https?://[^>\s]+)>", "urls", token_fn=lambda m: m.group(1))
        t = self._sub(t, r"(?<![\w(\"'=])https?://[^\s<>\"')\]]+(?:\([^\s()]*\)[^\s<>\"')\]]*)*",
                      "urls", token_fn=lambda m: m.group(0).rstrip(".,;:!?"))
        # headings (ordered) and table rows (ordered)
        self.ordered["headings"] = []
        self.ordered["table rows"] = []
        lines = t.split("\n")
        offset = 0
        for i, line in enumerate(lines, 1):
            hm = re.match(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$", line)
            if hm:
                self.ordered["headings"].append((f"H{len(hm.group(1))} {hm.group(2).strip()}", i))
            elif line.strip().startswith("|"):
                row = re.sub(r"\s+", " ", self.raw.split("\n")[i - 1].strip())
                if not re.fullmatch(r"\|?[\s:|-]+\|?", row):
                    self.ordered["table rows"].append((row, i))
            offset += len(line) + 1
        for m in re.finditer(r"<h([1-6])[^>]*>(.*?)</h\1>", self.raw, re.I | re.S):
            self.ordered["headings"].append((f"H{m.group(1)} " + re.sub(r"<[^>]+>|\s+", " ", m.group(2)).strip(),
                                             self.line(m.start())))
        body = "\n".join("" if re.match(r"^\s{0,3}#{1,6}\s", ln) else ln for ln in lines)
        # dates
        body = self._sub(body, r"\b\d{4}-\d{2}-\d{2}\b", "dates")
        body = self._sub(body, r"\b" + MONTH_RX + r"\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?\b", "dates",
                         token_fn=lambda m: norm_date(m.group(0)))
        body = self._sub(body, r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?" + MONTH_RX + r"(?:,?\s+\d{4})?\b", "dates",
                         token_fn=lambda m: norm_date(m.group(0)))
        body = self._sub(body, r"\b" + MONTH_RX + r",?\s+\d{4}\b", "dates", token_fn=lambda m: norm_date(m.group(0)))
        body = self._sub(body, r"\bQ[1-4]\s+\d{4}\b", "dates")
        body = self._sub(body, r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "dates")
        # dimensions (10x12, 10' x 12', 10 x 12 ft)
        body = self._sub(body, r"(?<![\w.])(\d+(?:\.\d+)?)\s*(?:'|ft|\")?\s*[x×]\s*(\d+(?:\.\d+)?)"
                               r"(?:\s*(?:'|ft|\")?\s*[x×]\s*(\d+(?:\.\d+)?))?(?:\s*(?:'|\"|ft|feet|in\.|inches|cm|mm)\b)?",
                         "numbers", re.I, token_fn=lambda m: "x".join(g for g in m.groups() if g) + " (dimensions)")
        # entities are harvested before numbers are blanked so model numbers stay whole
        self._entities(body)
        # numbers with currency and units
        num = (r"(?<![\w.])([$€£])?\s?(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(/\d+)?"
               r"(?:(?:\s?|-)(" + UNIT_RX + r")(?![A-Za-z]))?")
        body = self._sub(body, num, "numbers", re.I, token_fn=norm_number)
        words = r"\b(" + "|".join(NUMBER_WORDS) + r")\b(?:(?:\s|-)(" + UNIT_RX + r")(?![A-Za-z]))?"
        self._sub(body, words, "numbers", re.I,
                  token_fn=lambda m: str(NUMBER_WORDS[m.group(1).lower()]) + (" " + norm_unit(m.group(2)) if m.group(2) else ""))
        for anchor, url, ln in self.links:
            self.tokens["link anchors"].append((f"[{anchor}] -> {url}", ln))

    def _entities(self, body):
        vocab = set()
        tok_rx = re.compile(r"(?<![\w'’-])([A-Z][A-Za-z0-9&'’-]*[A-Za-z0-9]|[A-Z]{2,}|[A-Z0-9]+-?[A-Z0-9]*\d[A-Z0-9-]*)(?![\w'’-])")
        for line in body.split("\n"):
            content = re.sub(r"^\s*(?:[-*+]|\d+[.)]|>)\s+", lambda m: " " * len(m.group(0)), line)
            for m in tok_rx.finditer(content):
                tok = m.group(1)
                if tok in ENTITY_STOP or tok.isdigit():
                    continue
                prev = content[:m.start()].rstrip()
                sentence_start = prev == "" or prev[-1] in ".!?:\"“(|*" or prev.endswith("**")
                alnum = bool(re.search(r"\d", tok)) or (tok.isupper() and len(tok) >= 2)
                if alnum or not sentence_start:
                    vocab.add(tok)
        self._entity_vocab = vocab
        self._entity_body = body

    def entity_counts(self, vocab):
        out = []
        for tok in vocab:
            for m in re.finditer(r"(?<![\w'’-])" + re.escape(tok) + r"(?![\w'’-])", self._entity_body):
                out.append((tok, self.line(m.start())))
        return out


def norm_unit(u):
    if not u:
        return ""
    u = u.lower().strip()
    for pat, rep in UNIT_NORMAL:
        if re.match(pat, u):
            return rep
    return u


def norm_number(m):
    cur, num, frac, unit = m.group(1) or "", m.group(2).replace(",", ""), m.group(3) or "", m.group(4)
    return f"{cur}{num}{frac}" + (f" {norm_unit(unit)}" if unit else "")


def norm_date(s):
    s = s.replace(",", " ").replace(".", " ")
    parts = [p for p in s.split() if p.lower() != "of"]
    out = []
    for p in parts:
        pl = re.sub(r"(st|nd|rd|th)$", "", p.lower()) if re.match(r"^\d", p) else p.lower()
        out.append(MONTHS.get(pl, pl))
    return " ".join(out)


# ── comparison ───────────────────────────────────────────────────────────────

def multiset_diff(before, after):
    cb, ca = Counter(t for t, _ in before), Counter(t for t, _ in after)
    lines_b, lines_a = defaultdict(list), defaultdict(list)
    for t, ln in before:
        lines_b[t].append(ln)
    for t, ln in after:
        lines_a[t].append(ln)
    changes = []
    for tok in sorted(set(cb) | set(ca)):
        if cb[tok] > ca[tok]:
            changes.append(("MISSING", tok, cb[tok] - ca[tok], "before", lines_b[tok]))
        elif ca[tok] > cb[tok]:
            changes.append(("ADDED", tok, ca[tok] - cb[tok], "after", lines_a[tok]))
    return changes


def ordered_diff(before, after):
    sb, sa = [t for t, _ in before], [t for t, _ in after]
    changes = []
    sm = difflib.SequenceMatcher(a=sb, b=sa, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        for k in range(i1, i2):
            changes.append(("MISSING" if op == "delete" else "CHANGED", before[k][0], 1, "before", [before[k][1]]))
        for k in range(j1, j2):
            changes.append(("ADDED" if op == "insert" else "CHANGED TO", after[k][0], 1, "after", [after[k][1]]))
    if not changes and sb != sa:
        changes.append(("REORDERED", "order differs", 1, "after", []))
    return changes


_DIGIT_GROUP = re.compile(r"(?<=\d),(?=\d{3}(?!\d))")


def norm_approval(s):
    """Lowercase, trim, collapse spaces, and drop thousands separators, so an approval
    written as "$1,299.99" matches the stored number token "$1299.99"."""
    return re.sub(r"\s+", " ", _DIGIT_GROUP.sub("", s.lower().strip()))


def is_approved(cat, tok, approvals):
    tl = norm_approval(tok)
    for a in approvals:
        al = norm_approval(a)
        if ":" in al and al.split(":", 1)[0].strip() in CATEGORIES:
            c, v = [x.strip() for x in al.split(":", 1)]
            if c == cat and (v == "*" or v == tl or v in tl):
                return True
        elif al == tl or (len(al) >= 3 and al in tl and cat in ("protected", "link anchors")):
            return True
    return False


CATEGORIES = ["numbers", "dates", "urls", "link anchors", "headings", "table rows", "entities", "protected",
              "user-protected"]


def compare(pre: Doc, post: Doc, protect, approvals, allow_anchor_edits):
    report = {}
    for cat in ("numbers", "dates", "urls", "protected"):
        report[cat] = multiset_diff(pre.tokens[cat], post.tokens[cat])
    for cat in ("headings", "table rows"):
        report[cat] = ordered_diff(pre.ordered[cat], post.ordered[cat])
    # anchors: only report pairs whose URL survived (a lost URL is already reported under urls)
    anchors = multiset_diff(pre.tokens["link anchors"], post.tokens["link anchors"])
    report["link anchors"] = anchors
    vocab = pre._entity_vocab | post._entity_vocab
    report["entities"] = multiset_diff(pre.entity_counts(vocab), post.entity_counts(vocab))
    user = []
    for phrase in protect:
        rx = re.compile(re.escape(phrase))
        b = [(phrase, pre.line(m.start())) for m in rx.finditer(pre.raw)]
        a = [(phrase, post.line(m.start())) for m in rx.finditer(post.raw)]
        user += multiset_diff(b, a)
    report["user-protected"] = user

    results = {}
    for cat in CATEGORIES:
        rows = []
        for status, tok, n, side, lines in report.get(cat, []):
            approved = is_approved(cat, tok, approvals)
            soft = cat == "link anchors" and allow_anchor_edits
            rows.append({"status": status, "token": tok, "count": n, "side": side, "lines": lines[:8],
                         "approved": approved or soft})
        results[cat] = rows
    return results


# ── article checks (mechanical output hygiene) ───────────────────────────────

def canonical(url, site_host=None):
    try:
        p = urlsplit(url)
    except ValueError:
        return url
    host = (p.hostname or site_host or "").lower()
    port = f":{p.port}" if p.port and p.port not in (80, 443) else ""
    path = p.path.rstrip("/") or "/"
    return f"{host}{port}{path}" + (f"?{p.query}" if p.query else "")


def article_checks(doc: Doc, site_url=None, require_h1=False):
    errors, warnings = [], []
    raw = doc.raw
    lines = [ln for ln in raw.split("\n")]
    nonempty = [(i + 1, ln.strip()) for i, ln in enumerate(lines) if ln.strip()]
    if not nonempty:
        return [("EMPTY_OUTPUT", 1, "the file is empty")], []
    if raw.strip().startswith("```") and raw.strip().endswith("```"):
        errors.append(("WHOLE_ARTICLE_CODE_FENCE", 1, "the whole article is wrapped in a code fence"))
    if len(re.findall(r"^[ \t]*```", raw, re.M)) % 2:
        errors.append(("UNBALANCED_CODE_FENCE", 1, "odd number of ``` fences"))
    first_ln, first = nonempty[0]
    if re.match(r"^(?:here'?s|here is)\s+(?:the|your)\b|^(?:certainly|sure|of course)\b[,!.]|^(?:draft|article)\s*:",
                first, re.I):
        errors.append(("RESPONSE_WRAPPER", first_ln, first[:80]))
    edge = nonempty[:3] + nonempty[-3:]
    for ln, text in edge:
        if text.startswith(">"):
            continue
        if re.search(r"\bI\s+(?:have\s+)?(?:ensured|followed|verified|complied|double-checked)\b"
                     r"|\bquality checks? (?:pass|passed)\b|\bthis (?:draft|article|rewrite) (?:meets|follows|complies)\b"
                     r"|\bthe (?:article|rewrite) (?:above|below)\b|\bhumanizer report\b", text, re.I):
            errors.append(("SELF_CERTIFICATION", ln, text[:80]))
    for ln, text in nonempty:
        if re.search(r"^\s*(?:\(|\[)?(?:note to (?:editor|reviewer)|editor'?s? note|reviewer:|editor:)"
                     r"|\bkeep the (?:cta|placeholder|link|heading)s?\b[^.]*\bintact\b|^word count\s*:|^TODO\b",
                     text, re.I):
            errors.append(("INSTRUCTION_LEAK", ln, text[:80]))
    if require_h1 and not any(h.startswith("H1 ") for h, _ in doc.ordered["headings"]):
        errors.append(("MISSING_H1", 1, "no H1 heading"))
    seen_nums = defaultdict(set)
    for h, ln in doc.ordered["headings"]:
        m = re.match(r"^(H\d) (\d+)[.)]\s", h)
        if m:
            if m.group(2) in seen_nums[m.group(1)]:
                errors.append(("DUPLICATE_NUMBERED_HEADING", ln, h[:80]))
            seen_nums[m.group(1)].add(m.group(2))
    # links
    starts = len(re.findall(r"(?<!!)\]\(", re.sub(r"`[^`\n]*`", "", raw)))
    if starts != len([1 for a, u, _ in doc.links if True]) and starts > len(doc.links):
        warnings.append(("MALFORMED_MARKDOWN_LINK", 1, f"{starts} link openings, {len(doc.links)} parsed links"))
    site_host = urlsplit(site_url).hostname.lower() if site_url and urlsplit(site_url).hostname else None
    internal_seen = Counter()
    for anchor, url, ln in doc.links:
        u = url.strip()
        if not u:
            errors.append(("EMPTY_LINK", ln, f"[{anchor}]()"))
            continue
        scheme = urlsplit(u).scheme.lower()
        if scheme and scheme not in ("http", "https", "mailto", "tel"):
            errors.append(("UNSUPPORTED_LINK_SCHEME", ln, u[:80]))
            continue
        if scheme in ("http", "https") and not urlsplit(u).hostname:
            errors.append(("INVALID_ABSOLUTE_URL", ln, u[:80]))
            continue
        if not anchor.strip():
            warnings.append(("EMPTY_ANCHOR", ln, u[:80]))
        if site_host and (not scheme or (urlsplit(u).hostname or "").lower() in (site_host, "www." + site_host)):
            if u.startswith("#"):
                continue
            c = canonical(u, site_host)
            if c == canonical(site_url):
                errors.append(("SELF_LINK", ln, u[:80]))
            internal_seen[c] += 1
            if internal_seen[c] == 2:
                warnings.append(("DUPLICATE_INTERNAL_LINK", ln, u[:80] + " (one link per internal target)"))
    return errors, warnings


# ── main ─────────────────────────────────────────────────────────────────────

def read(path):
    with open(path, "r", encoding="utf-8-sig") as fh:
        return fh.read()


def self_test():
    """Quick checks for the approval matcher, including the help example."""
    before = "The kit costs $1,299.99 and ships in 5 days. Max 135 PSI."
    after = "The kit ships in 5 days. Max 135 PSI."
    cases = [
        (["$1,299.99"], True),            # the documented help example
        (["$1299.99"], True),             # same value without the separator
        (["numbers:$1,299.99"], True),    # category form
        (["numbers:*"], True),
        (["$1,299"], False),              # a different value must not approve it
        ([], False),
    ]
    pre, post = Doc(before), Doc(after)
    failures = 0
    for approvals, want in cases:
        rows = compare(pre, post, [], approvals, False)["numbers"]
        got = bool(rows) and all(r["approved"] for r in rows)
        ok = got == want
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} approve={approvals!r} -> approved={got} (want {want})")
    extra = [("numbers", "$1299", "$1,299", True), ("numbers", "12000 btu", "12,000 BTU", True),
             ("entities", "QT-54", "entities:qt-54", True)]
    for cat, tok, appr, want in extra:
        got = is_approved(cat, tok, [appr])
        ok = got == want
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} is_approved({cat!r}, {tok!r}, [{appr!r}]) = {got}")
    print("SELF-TEST: " + ("PASS" if not failures else f"FAIL ({failures})"))
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description="Compare text before and after a humanize/edit pass and fail on any "
                                             "unapproved change to numbers, prices, units, dates, URLs, link anchors, "
                                             "headings, named entities, or protected tokens.")
    ap.add_argument("before", help="text before the pass (edited draft)")
    ap.add_argument("after", help="text after the pass (humanized candidate)")
    ap.add_argument("--protect", action="append", default=[], metavar="PHRASE",
                    help="exact phrase that must appear the same number of times (repeatable)")
    ap.add_argument("--protect-file", metavar="FILE", help="file with one protected phrase per line")
    ap.add_argument("--approve", action="append", default=[], metavar="VALUE",
                    help="approved change: 'value' or 'category:value' or 'category:*' (repeatable)")
    ap.add_argument("--approve-file", metavar="FILE", help="file with one approval per line ('#' comments)")
    ap.add_argument("--allow-anchor-edits", action="store_true",
                    help="report link-anchor text changes without failing (URLs stay strict)")
    ap.add_argument("--article-checks", action="store_true",
                    help="also check the AFTER text for response wrappers, self-certification, leaked "
                         "reviewer instructions, broken fences, and bad links")
    ap.add_argument("--site-url", help="the page's own URL, for self-link and duplicate internal link checks")
    ap.add_argument("--require-h1", action="store_true", help="with --article-checks, require one H1")
    ap.add_argument("--json", action="store_true", help="print the result as JSON instead of text")
    ap.add_argument("--self-test", action="store_true", help="run the built-in approval checks and exit")
    if "--self-test" in sys.argv[1:]:
        return self_test()
    args = ap.parse_args()

    try:
        pre_text, post_text = read(args.before), read(args.after)
        protect = list(args.protect)
        if args.protect_file:
            protect += [ln.strip() for ln in read(args.protect_file).splitlines() if ln.strip()
                        and not ln.startswith("#")]
        approvals = list(args.approve)
        if args.approve_file:
            approvals += [ln.strip() for ln in read(args.approve_file).splitlines() if ln.strip()
                          and not ln.startswith("#")]
    except (OSError, UnicodeDecodeError) as exc:
        print(f"fact_diff.py: cannot read input: {exc}", file=sys.stderr)
        return 2

    pre, post = Doc(pre_text), Doc(post_text)
    results = compare(pre, post, protect, approvals, args.allow_anchor_edits)
    errors, warnings = (article_checks(post, args.site_url, args.require_h1) if args.article_checks else ([], []))
    unapproved = sum(1 for rows in results.values() for r in rows if not r["approved"])
    approved = sum(1 for rows in results.values() for r in rows if r["approved"])
    failed = unapproved > 0 or bool(errors)
    sha = {"before": hashlib.sha256(pre_text.encode("utf-8")).hexdigest(),
           "after": hashlib.sha256(post_text.encode("utf-8")).hexdigest()}

    if args.json:
        print(json.dumps({"before": args.before, "after": args.after, "sha256": sha, "result": "FAIL" if failed else "PASS",
                          "unapproved_changes": unapproved, "approved_changes": approved, "changes": results,
                          "article_errors": errors, "article_warnings": warnings,
                          "counts": {c: [len(pre.tokens.get(c, pre.ordered.get(c, []))),
                                         len(post.tokens.get(c, post.ordered.get(c, [])))]
                                     for c in ("numbers", "dates", "urls", "link anchors", "headings",
                                               "table rows", "protected")}},
                         indent=2, ensure_ascii=False))
        return 1 if failed else 0

    print(f"FACT DIFF  {args.before}  ->  {args.after}")
    print(f"  sha256 before {sha['before'][:16]}  after {sha['after'][:16]}")
    print("  Mechanical gate only: it proves the facts did not move, not that they are true.")
    print()
    for cat in CATEGORIES:
        rows = results[cat]
        if cat in ("headings", "table rows"):
            n_b, n_a = len(pre.ordered[cat]), len(post.ordered[cat])
        elif cat == "entities" or cat == "user-protected":
            n_b = n_a = None
        else:
            n_b, n_a = len(pre.tokens[cat]), len(post.tokens[cat])
        counts = f" ({n_b} before, {n_a} after)" if n_b is not None else ""
        if not rows:
            if cat != "user-protected" or protect:
                print(f"  OK    {cat}{counts}")
            continue
        bad = sum(1 for r in rows if not r["approved"])
        print(f"  {'FAIL' if bad else 'OK*':<5} {cat}{counts}: {len(rows)} difference(s), {bad} unapproved")
        for r in rows:
            where = f"{r['side']} L{','.join(str(x) for x in r['lines'])}" if r["lines"] else ""
            mark = "approved" if r["approved"] else ""
            n = f" x{r['count']}" if r["count"] > 1 else ""
            tok = r["token"] if len(r["token"]) <= 110 else r["token"][:107] + "..."
            print(f"        {r['status']:<10} \"{tok}\"{n}  {where}  {mark}".rstrip())
    if args.article_checks:
        print()
        if not errors and not warnings:
            print("  OK    article checks")
        for code, ln, detail in errors:
            print(f"  FAIL  {code} L{ln}: {detail}")
        for code, ln, detail in warnings:
            print(f"  WARN  {code} L{ln}: {detail}")
    print()
    if failed:
        print(f"RESULT: FAIL  {unapproved} unapproved change(s)"
              + (f", {len(errors)} article error(s)" if errors else "")
              + ". Restore the original value, or approve it with --approve if a pattern fix required it.")
    else:
        print(f"RESULT: PASS  ({approved} approved change(s))" if approved else "RESULT: PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
