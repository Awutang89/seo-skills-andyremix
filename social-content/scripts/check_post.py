#!/usr/bin/env python
"""social-content checker: character counts, copy lint, prompt seed and index validation.

Subcommands
  post   Count characters the way each platform does and lint a draft.
  seed   Validate a JSON image prompt seed before it goes to the image engine.
  index  Check that every file listed in a social workspace index.md exists.

Exit codes: 0 no hard failures, 1 usage or input error, 2 one or more hard failures.
Offline only. Reads no keys, writes nothing.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---------------------------------------------------------------- limits
LIMITS = {
    # platform: (hard limit per post, soft target per post or None)
    "x": (280, 260),
    "x-premium": (25000, None),  # dated figure; the saved profile is the truth
    "threads": (500, None),
    "linkedin": (3000, None),
}
LINKEDIN_TARGET = (500, 1200)

VISUAL_ROLES = {
    "raw-screenshot", "annotated-screenshot", "receipt-strip", "chart", "diagram",
    "checklist", "teardown-crop", "stat-card", "meme", "lo-fi-photo", "generated-scene",
}
ARTIFACT_ROLES = {"raw-screenshot", "annotated-screenshot", "receipt-strip", "teardown-crop"}
ASPECTS = {"1:1", "4:5", "9:16", "16:9", "3:2", "platform native crop"}

# ---------------------------------------------------------------- phrase lists (data)
LAZY_CTA = [
    "agree?", "thoughts?", "comment below", "drop a comment", "follow for more",
    "hope this helps", "let me know in the comments", "repost if", "rt if",
]
DISTRIBUTION_CTA = [
    "link in comments", "link in the comments", "link in first comment", "link in the first comment",
    "dm me", "free download", "grab a copy", "grab your copy",
]
AI_PHRASES = [
    "in today's fast-paced world", "in today's world", "in an ever-evolving landscape",
    "game-changer", "game changer", "game-changing", "unlock", "leverage", "delve", "harness",
    "empower", "supercharge", "seamless", "robust", "elevate", "cutting-edge", "revolutionary",
    "transformative", "unprecedented", "the truth is", "here's the thing", "let's dive in",
    "it is important to note", "it's important to note", "it is worth mentioning", "needless to say",
    "in conclusion", "serves as a testament to", "at the end of the day", "the lesson is",
    "the key takeaway", "but that's only half the story", "what happened next surprised me",
    "this changed everything", "unpopular opinion", "nobody talks about", "no one talks about",
]
AI_TEMPLATES = [
    (re.compile(r"\bnot (?:just|only|merely)\b[^.!?\n]{1,60}\bbut\b", re.I), "not just/only X, but Y"),
    (re.compile(r"\bisn['’]t just\b[^.!?\n]{1,60}\bit['’]s\b", re.I), "X isn't just Y, it's Z"),
    (re.compile(r"\bis not merely\b", re.I), "X is not merely Y"),
    (re.compile(r"\bwhether you['’]re\b[^.!?\n]{1,60}\bor\b", re.I), "whether you're X or Y"),
]
WEAK_OPENERS = [
    "i wanted to share", "in today's world", "here are my thoughts on", "ai is changing everything",
    "let's dive in", "here's the thing",
]
SOCIAL_PROOF = [
    "users tell us", "clients say", "customers say", "patients report", "people using it report",
    "people using it", "we're seeing", "we are seeing", "it helped them",
]

DASH_RE = re.compile(r"[—–]| - | -- |(?<=\w)--(?=\w)")
HASHTAG_RE = re.compile(r"(?<![\w&])#[A-Za-z_][\w]*")
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
BOLD_RE = re.compile(r"\*\*[^*\n]+\*\*")
EMOJI_BULLET_RE = re.compile(r"^\s*[☀-➿\U0001F300-\U0001FAFF✅❌✔➡]")
PLACEHOLDER_RE = re.compile(r"\{[A-Z][^{}]*\}")


# ---------------------------------------------------------------- counting
def _x_weight(cp: int) -> int:
    if 0 <= cp <= 4351 or 8192 <= cp <= 8205 or 8208 <= cp <= 8223 or 8242 <= cp <= 8247:
        return 1
    return 2


def x_weighted_length(text: str) -> int:
    """Approximate X's weighted count: URLs count 23, each emoji cluster counts 2,
    Latin and common punctuation count 1, other scripts (CJK etc.) count 2."""
    text = unicodedata.normalize("NFC", text)
    total = 0
    pos = 0
    for m in URL_RE.finditer(text):
        total += _x_count_plain(text[pos:m.start()])
        total += 23
        pos = m.end()
    total += _x_count_plain(text[pos:])
    return total


def _x_count_plain(s: str) -> int:
    total = 0
    joiner = False
    for ch in s:
        cp = ord(ch)
        if cp == 0xFE0F or 0x1F3FB <= cp <= 0x1F3FF:  # variation selector, skin tone
            continue
        if cp == 0x200D:  # zero width joiner: next code point belongs to the same emoji
            joiner = True
            continue
        if joiner:
            joiner = False
            continue
        total += _x_weight(cp)
    return total


def plain_length(text: str) -> int:
    return len(unicodedata.normalize("NFC", text))


def x_prefix_280(text: str) -> str:
    """Return the longest prefix whose weighted length is <= 280."""
    lo, hi = 0, len(text)
    while lo < hi:  # weighted length never shrinks as the prefix grows, so binary search works
        mid = (lo + hi + 1) // 2
        if x_weighted_length(text[:mid]) <= 280:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo]


# ---------------------------------------------------------------- helpers
def split_posts(text: str) -> list[str]:
    parts = re.split(r"(?m)^\s*---\s*$", text)
    return [p.strip() for p in parts if p.strip()]


def read_text(args) -> str:
    if args.text is not None:
        return args.text
    if args.file:
        p = Path(args.file)
        if not p.is_file():
            raise SystemExit(_usage_error(f"file not found: {p}"))
        return p.read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit(_usage_error("give --file, --text, or pipe text on stdin"))


def _usage_error(msg: str) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return 1


def load_voice(paths) -> str:
    chunks = []
    for p in paths or []:
        fp = Path(p)
        if fp.is_file():
            chunks.append(fp.read_text(encoding="utf-8", errors="replace"))
        else:
            print(f"WARN: voice file not found, ignored: {fp}", file=sys.stderr)
    return "\n".join(chunks)


def find_phrases(text_lower: str, phrases):
    hits = []
    for ph in phrases:
        pat = r"(?<![\w])" + re.escape(ph) + (r"(?![\w])" if ph[-1].isalnum() else "")
        if re.search(pat, text_lower):
            hits.append(ph)
    return hits


class Report:
    def __init__(self):
        self.items = []  # (level, code, message)

    def add(self, level, code, msg):
        self.items.append({"level": level, "code": code, "message": msg})

    @property
    def fails(self):
        return [i for i in self.items if i["level"] == "FAIL"]


# ---------------------------------------------------------------- post
def cmd_post(args) -> int:
    text = read_text(args).replace("\r\n", "\n")
    voice = load_voice(args.voice_file)
    voice_lower = voice.lower()
    rep = Report()
    platform = args.platform
    posts = split_posts(text)
    if not posts:
        return _usage_error("draft is empty")

    hard, soft = LIMITS[platform]
    counter = x_weighted_length if platform in ("x", "x-premium") else plain_length
    counts = [counter(p) for p in posts]

    if len(posts) > 1:
        if platform == "linkedin":
            rep.add("FAIL", "multi-post", "LinkedIn draft contains --- separators; a LinkedIn post is one post")
        elif platform == "x-premium":
            rep.add("WARN", "multi-post", "X Premium long post split into several posts; is an X thread what was requested?")
        else:
            rep.add("INFO", "thread", f"{len(posts)} posts detected; only valid when a thread or sequence was requested")

    for i, (p, n) in enumerate(zip(posts, counts), 1):
        label = f"post {i}" if len(posts) > 1 else "post"
        if n > hard:
            rep.add("FAIL", "over-limit", f"{label}: {n} characters, limit {hard}")
        elif soft and n > soft:
            rep.add("WARN", "near-limit", f"{label}: {n} characters, target {soft} or fewer")
        if platform == "linkedin" and not (LINKEDIN_TARGET[0] <= n <= LINKEDIN_TARGET[1]):
            rep.add("INFO", "linkedin-target", f"{label}: {n} characters; usual target {LINKEDIN_TARGET[0]} to {LINKEDIN_TARGET[1]} when proof supports it")

    if platform == "x-premium" and counts[0] > 280:
        head = x_prefix_280(posts[0])
        if not re.search(r"[.!?:]\s*$|[.!?:]\s", head[-40:] if head else ""):
            rep.add("WARN", "first-280", "the first 280 weighted characters end mid thought; move the hook and main point up")
        rep.add("INFO", "first-280-text", f"first 280: {head!r}")

    body = "\n".join(posts)
    lower = body.lower()

    # dashes
    dashes = DASH_RE.findall(body)
    if dashes:
        voice_dashes = bool(re.search(r"[—–]| - ", voice))
        if args.allow_dashes or voice_dashes:
            rep.add("INFO", "dashes", f"{len(dashes)} dash(es); allowed because the voice evidence uses them. Match its rate.")
        else:
            rep.add("FAIL", "dashes", f"{len(dashes)} dash(es) (em, en, spaced hyphen or double hyphen); house default is zero")

    # hashtags
    tags = HASHTAG_RE.findall(body)
    if tags:
        voice_tags = bool(HASHTAG_RE.search(voice))
        if platform == "threads" and len(set(t.lower() for t in tags)) > 1:
            rep.add("FAIL", "threads-topics", f"{len(tags)} tags; Threads gets one Topic at most")
        elif args.allow_hashtags or voice_tags:
            rep.add("INFO", "hashtags", f"hashtags {tags} allowed by voice evidence or brief")
        else:
            rep.add("WARN", "hashtags", f"hashtags {tags} with no voice evidence; remove unless the brief asks for them")

    def voice_ok(ph):
        return ph in voice_lower

    for ph in find_phrases(lower, LAZY_CTA):
        rep.add("INFO" if voice_ok(ph) else "FAIL", "lazy-cta", f'engagement bait: "{ph}"')
    for ph in find_phrases(lower, DISTRIBUTION_CTA):
        level = "INFO" if (voice_ok(ph) or args.offer_supplied) else "FAIL"
        rep.add(level, "distribution-cta", f'distribution CTA without a supplied offer: "{ph}"')
    for ph in find_phrases(lower, AI_PHRASES):
        rep.add("INFO" if voice_ok(ph) else "WARN", "ai-phrase", f'default AI phrase: "{ph}"')
    for rx, name in AI_TEMPLATES:
        if rx.search(body) and not rx.search(voice):
            rep.add("WARN", "ai-template", f"template sentence: {name}")
    first_line = posts[0].strip().splitlines()[0].lower() if posts[0].strip() else ""
    for ph in WEAK_OPENERS:
        if first_line.startswith(ph):
            rep.add("WARN", "weak-opener", f'weak first line: "{ph}..."')
    for ph in find_phrases(lower, SOCIAL_PROOF):
        rep.add("FAIL" if args.high_risk else "WARN", "social-proof",
                f'social proof phrase "{ph}": needs a source' + (" (high-risk topic)" if args.high_risk else ""))

    emoji_bullets = sum(1 for ln in body.splitlines() if EMOJI_BULLET_RE.match(ln))
    if emoji_bullets >= 2 and not EMOJI_BULLET_RE.search(voice):
        rep.add("WARN", "emoji-bullets", f"{emoji_bullets} lines start with an emoji bullet")
    bolds = BOLD_RE.findall(body)
    if len(bolds) >= 2:
        rep.add("WARN", "bold", f"{len(bolds)} bold spans; most platforms do not render markdown bold")
    lines = [ln for ln in body.splitlines() if ln.strip()]
    if len(lines) >= 6:
        short = sum(1 for ln in lines if len(ln.split()) <= 8)
        if short / len(lines) > 0.8:
            rep.add("WARN", "broetry", "most lines are one short sentence; vary paragraph rhythm")

    result = {
        "platform": platform,
        "counting": "X weighted (URLs 23, emoji 2, CJK 2)" if counter is x_weighted_length else "Unicode characters (NFC)",
        "posts": [{"index": i, "characters": n, "limit": hard} for i, n in enumerate(counts, 1)],
        "findings": rep.items,
        "pass": not rep.fails,
    }
    _emit(result, args.json, header=f"{platform}: " + ", ".join(f"{n}/{hard}" for n in counts))
    return 2 if rep.fails else 0


# ---------------------------------------------------------------- seed
def cmd_seed(args) -> int:
    p = Path(args.path)
    if not p.is_file():
        return _usage_error(f"seed not found: {p}")
    try:
        seed = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL: invalid JSON: {e}")
        return 2
    rep = Report()
    if not isinstance(seed, dict):
        rep.add("FAIL", "shape", "seed must be a JSON object")
        _emit({"findings": rep.items, "pass": False}, args.json, header=str(p))
        return 2

    for key in ("output", "main_visual", "composition", "text_elements", "constraints"):
        if key not in seed:
            rep.add("FAIL", "missing-key", f"missing top-level key: {key}")
    out = seed.get("output") or {}
    role = str(out.get("role", "")).strip()
    if role == "none":
        rep.add("FAIL", "role", "role none means no image; do not write a seed")
    elif role not in VISUAL_ROLES:
        rep.add("FAIL", "role", f"role must be one of the 12 roles, got {role!r}")
    aspect = str(out.get("aspect_ratio", "")).strip()
    if aspect not in ASPECTS:
        rep.add("FAIL", "aspect", f"aspect_ratio {aspect!r} not in {sorted(ASPECTS)}")
    plat = str(out.get("platform", ""))
    if not re.search(r"\b(x|threads|linkedin)\b", plat, re.I):
        rep.add("WARN", "platform", f"platform {plat!r} should name X, Threads or LinkedIn")
    if not out.get("mobile_read"):
        rep.add("WARN", "mobile", "output.mobile_read is empty; say what must read at feed size")

    refs = seed.get("reference_images") or []
    if role in ARTIFACT_ROLES and not refs:
        rep.add("FAIL", "no-artifact", f"role {role} needs the person's real image in reference_images; otherwise send a capture brief")
    for r in refs:
        if isinstance(r, dict) and r.get("role", "").startswith("base") and not r.get("preserve"):
            rep.add("WARN", "preserve", f"reference image {r.get('image_id')} has no preserve rule")

    rd = seed.get("render_data") or {}
    if not rd.get("do_not_invent"):
        rep.add("WARN", "do-not-invent", "render_data.do_not_invent is empty")

    texts = seed.get("text_elements") or []
    words = 0
    for t in texts:
        content = str(t.get("content", "")) if isinstance(t, dict) else ""
        words += len(content.split())
        if DASH_RE.search(content):
            rep.add("FAIL", "dashes", f"on-image text has a dash: {content!r}")
    if words > 8:
        rep.add("WARN", "text-heavy", f"{words} words of on-image text; most feed images want 0 to 8")

    constraints = " ".join(str(c) for c in (seed.get("constraints") or [])).lower()
    if "watermark" not in constraints:
        rep.add("WARN", "constraints", "constraints do not rule out a watermark")
    if "mobile" not in constraints and not out.get("mobile_read"):
        rep.add("WARN", "constraints", "nothing about mobile readability")

    notes = [k for k in seed if k.startswith("_")]
    if notes:
        rep.add("FAIL" if args.final else "WARN", "note-keys",
                f"template note keys {notes}; delete them so they do not reach the image prompt")
    body = {k: v for k, v in seed.items() if not k.startswith("_")}
    placeholders = sorted(set(PLACEHOLDER_RE.findall(json.dumps(body, ensure_ascii=False))))
    if placeholders:
        rep.add("FAIL" if args.final else "WARN", "placeholders",
                f"unfilled placeholders {placeholders}; fill from the person's source before generating")

    _emit({"seed": str(p), "role": role, "findings": rep.items, "pass": not rep.fails}, args.json, header=f"seed {p.name}: role {role}")
    return 2 if rep.fails else 0


# ---------------------------------------------------------------- index
def cmd_index(args) -> int:
    p = Path(args.path)
    if not p.is_file():
        return _usage_error(f"index not found: {p}")
    rep = Report()
    rows = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("|")]
    if not rows:
        rep.add("FAIL", "no-table", "no table found")
    else:
        header = [c.strip().lower() for c in rows[0].strip().strip("|").split("|")]
        expected = ["date", "slug", "topic", "platforms", "status", "file"]
        if header != expected:
            rep.add("FAIL", "header", f"header {header} should be {expected}")
        else:
            fi = header.index("file")
            for ln in rows[2:]:
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                if len(cells) != len(header):
                    rep.add("FAIL", "row", f"malformed row: {ln.strip()}")
                    continue
                target = Path(cells[fi])
                full = target if target.is_absolute() else (p.parent / target)
                if not full.is_file():
                    rep.add("FAIL", "missing-file", f"{cells[1]}: {cells[fi]} does not exist; mark it missing, do not rebuild it")
                else:
                    rep.add("INFO", "ok", f"{cells[1]}: {cells[fi]}")
    _emit({"index": str(p), "findings": rep.items, "pass": not rep.fails}, args.json, header=f"index {p}")
    return 2 if rep.fails else 0


# ---------------------------------------------------------------- output
def _emit(result: dict, as_json: bool, header: str):
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(header)
    for f in result.get("findings", []):
        print(f"  {f['level']:<4} {f['code']}: {f['message']}")
    print("PASS" if result.get("pass") else "FAIL")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="social-content checker (offline)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("post", help="count characters and lint a draft; separate thread posts with a line of ---")
    sp.add_argument("--platform", required=True, choices=sorted(LIMITS))
    src = sp.add_mutually_exclusive_group()
    src.add_argument("--file")
    src.add_argument("--text")
    sp.add_argument("--voice-file", action="append", help="voice examples or profile; phrases, dashes and hashtags found there are allowed")
    sp.add_argument("--allow-dashes", action="store_true", help="the brief or voice explicitly allows dashes")
    sp.add_argument("--allow-hashtags", action="store_true", help="the brief explicitly asks for hashtags")
    sp.add_argument("--offer-supplied", action="store_true", help="the person supplied the offer or link behind a CTA")
    sp.add_argument("--high-risk", action="store_true", help="health, legal, money, safety or guaranteed results topic")
    sp.add_argument("--json", action="store_true")

    ss = sub.add_parser("seed", help="validate a JSON image prompt seed")
    ss.add_argument("path")
    ss.add_argument("--final", action="store_true", help="treat unfilled {PLACEHOLDERS} as failures")
    ss.add_argument("--json", action="store_true")

    si = sub.add_parser("index", help="check a social workspace index.md")
    si.add_argument("path")
    si.add_argument("--json", action="store_true")

    args = ap.parse_args(argv)
    try:
        return {"post": cmd_post, "seed": cmd_seed, "index": cmd_index}[args.cmd](args)
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 1


if __name__ == "__main__":
    sys.exit(main())
