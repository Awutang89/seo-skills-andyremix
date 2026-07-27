#!/usr/bin/env python3
"""
site-audit.py — optional site-level pass for the seo-onpage-audit skill.

Generic and site-agnostic: crawls ANY target site and derives the cross-page
checks a single-URL fetch cannot prove:
  - title / meta-description uniqueness (exact + near-duplicate)
  - canonical uniqueness — every indexable URL must declare its OWN canonical;
    duplicate canonical targets, missing/relative/cross-host canonicals, and
    canonicals outside <head> are all flagged
  - URL-structure consistency (separators, case, depth, trailing slash outliers)
  - orphan pages (0 inbound internal links in the crawled graph)
  - inbound-link distribution (important/shallow pages with few inbound links)

Everything is computed from the crawl — no local files, no hardcoded keys, no
assumptions about the site's platform.

Crawler: Firecrawl v2 (map + batch/scrape), stdlib urllib only.
The API key is read from the FIRECRAWL_API_KEY environment variable — never hardcode it.
(A running Firecrawl MCP server, or Scrapling, can replace the fetch layer; the
analysis functions below are independent of how the pages were fetched.)

Usage:
  set FIRECRAWL_API_KEY=fc-...            (PowerShell: $env:FIRECRAWL_API_KEY="fc-...")
  python site-audit.py https://example.com [--limit 200] [--json out.json]
  python site-audit.py --urls-file urls.txt   # skip mapping; scrape a given URL list
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

API = "https://api.firecrawl.dev/v2"


# --------------------------------------------------------------------------- #
# Fetch layer (Firecrawl). Swap this out for an MCP server or Scrapling if you
# prefer — the analysis layer below only needs the `pages` list it returns.
# --------------------------------------------------------------------------- #
def _headers():
    key = os.environ.get("FIRECRAWL_API_KEY")
    if not key:
        sys.exit("ERROR: set the FIRECRAWL_API_KEY environment variable (or use the "
                 "Firecrawl MCP server / Scrapling instead).")
    return {"Authorization": "Bearer " + key, "Content-Type": "application/json"}


def _post(path, payload):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode("utf-8"),
                                 headers=_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(url):
    req = urllib.request.Request(url, headers=_headers(), method="GET")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def map_site(root, limit):
    """Discover URLs on the site (Firecrawl v2 /map)."""
    try:
        res = _post("/map", {"url": root, "limit": limit})
    except urllib.error.HTTPError as e:
        sys.exit("Firecrawl /map failed: HTTP %s %s" % (e.code, e.read().decode("utf-8", "replace")))
    links = res.get("links") or res.get("data") or []
    urls = []
    for item in links:
        u = item.get("url") if isinstance(item, dict) else item
        if u:
            urls.append(u)
    return urls[:limit]


def scrape_pages(urls):
    """Batch-scrape URLs.

    Returns [{url, title, meta_description, links[], canonicals[], canonical_parsed,
              canonical_outside_head}].

    `rawHtml` is requested because the canonical link element is NOT reliably exposed
    in Firecrawl's metadata — it has to be parsed out of the served HTML. Raw (not
    rendered) HTML is also the correct source: Google honors the canonical in the
    server response even if JS later rewrites it.
    """
    start = _post("/batch/scrape",
                  {"urls": urls, "formats": ["links", "rawHtml"], "onlyMainContent": False})
    status_url = start.get("url")
    if not status_url:
        sys.exit("Firecrawl /batch/scrape did not return a status URL: %s" % json.dumps(start)[:400])

    data = []
    while True:
        res = _get(status_url)
        data.extend(res.get("data") or [])
        if res.get("status") == "completed" and not res.get("next"):
            break
        if res.get("next"):
            status_url = res["next"]
            continue
        if res.get("status") in ("failed", "cancelled"):
            sys.exit("Firecrawl batch job %s." % res.get("status"))
        time.sleep(4)

    pages = []
    for d in data:
        meta = d.get("metadata") or {}
        html = d.get("rawHtml") or d.get("html") or ""
        page = {
            "url": meta.get("sourceURL") or meta.get("url") or d.get("url") or "",
            "title": (meta.get("title") or "").strip(),
            "meta_description": (meta.get("description") or "").strip(),
            "links": d.get("links") or [],
        }
        page.update(parse_canonicals(html, meta))
        pages.append(page)
    return [p for p in pages if p["url"]]


# --------------------------------------------------------------------------- #
# Canonical extraction (fetcher-independent: hand it HTML from any source)
# --------------------------------------------------------------------------- #
_LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
_ATTR = re.compile(r"""([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""")


def _canonicals_in(html_fragment):
    hrefs = []
    for tag in _LINK_TAG.findall(html_fragment or ""):
        attrs = {}
        for m in _ATTR.finditer(tag):
            attrs[m.group(1).lower()] = (m.group(2) or m.group(3) or m.group(4) or "")
        if "canonical" in attrs.get("rel", "").lower().split():
            href = attrs.get("href", "").strip()
            if href:
                hrefs.append(href)
    return hrefs


def parse_canonicals(html, meta=None):
    """Extract every rel=canonical href from served HTML.

    `canonical_parsed` is False when no HTML was available — that is 'unknown',
    NOT 'missing canonical'. Never report a missing canonical without HTML to prove it.
    """
    meta = meta or {}
    if not html:
        fallback = (meta.get("canonical") or meta.get("canonicalUrl")
                    or meta.get("canonical_url") or "").strip()
        if fallback:
            return {"canonicals": [fallback], "canonical_parsed": True,
                    "canonical_outside_head": False}
        return {"canonicals": [], "canonical_parsed": False, "canonical_outside_head": False}

    m = re.search(r"</head\s*>", html, re.I)
    head, rest = (html[:m.start()], html[m.start():]) if m else (html, "")
    in_head = _canonicals_in(head)
    outside = _canonicals_in(rest)
    return {
        # A canonical after </head> is ignored by Google — record it, but keep it out
        # of the authoritative list so downstream checks judge what Google judges.
        "canonicals": in_head,
        "canonical_parsed": True,
        "canonical_outside_head": bool(outside) and not in_head,
    }


# --------------------------------------------------------------------------- #
# Analysis layer (pure functions over the `pages` list — fetch-agnostic)
# --------------------------------------------------------------------------- #
def _norm(s):
    return " ".join((s or "").lower().split())


def _same_host(a, b):
    try:
        return urllib.parse.urlparse(a).netloc.lower() == urllib.parse.urlparse(b).netloc.lower()
    except Exception:
        return False


def _canon(u):
    """Canonicalize a URL for graph matching: drop query/fragment, strip trailing slash."""
    try:
        p = urllib.parse.urlparse(u)
        path = p.path.rstrip("/") or "/"
        return (p.scheme + "://" + p.netloc.lower() + path)
    except Exception:
        return u


def find_duplicates(pages, field):
    groups = defaultdict(list)
    for p in pages:
        val = _norm(p[field])
        if val:
            groups[val].append(p["url"])
    exact = {v: urls for v, urls in groups.items() if len(urls) > 1}

    # near-duplicate: same first 60 normalized chars but not already an exact dup
    near = defaultdict(list)
    for p in pages:
        val = _norm(p[field])
        if val and val not in exact:
            near[val[:60]].append(p["url"])
    near = {k: urls for k, urls in near.items() if len(urls) > 1}
    return exact, near


def missing_field(pages, field):
    return [p["url"] for p in pages if not _norm(p[field])]


def build_link_graph(pages):
    known = {_canon(p["url"]) for p in pages}
    inbound = Counter({_canon(p["url"]): 0 for p in pages})
    for p in pages:
        src = _canon(p["url"])
        seen = set()
        for link in p["links"]:
            if not _same_host(p["url"], link):
                continue
            tgt = _canon(link)
            if tgt in known and tgt != src and tgt not in seen:
                inbound[tgt] += 1
                seen.add(tgt)
    return inbound


def url_structure_outliers(pages):
    def depth(u):
        return len([seg for seg in urllib.parse.urlparse(u).path.split("/") if seg])

    seps_underscore, has_upper, trailing = [], [], []
    for p in pages:
        path = urllib.parse.urlparse(p["url"]).path
        if "_" in path:
            seps_underscore.append(p["url"])
        if any(c.isupper() for c in path):
            has_upper.append(p["url"])
        if path.endswith("/") and path != "/":
            trailing.append(p["url"])
    depths = Counter(depth(p["url"]) for p in pages)
    return {
        "underscore_in_path": seps_underscore,
        "uppercase_in_path": has_upper,
        "trailing_slash": trailing,
        "depth_distribution": dict(sorted(depths.items())),
    }


def _dewww(host):
    return host[4:] if host.startswith("www.") else host


def _norm_canon(u):
    """Normalize for canonical identity: lowercase scheme+host, drop fragment,
    strip one trailing slash. Query is KEPT — ?page=2 is a different canonical."""
    try:
        p = urllib.parse.urlparse(u)
        path = p.path.rstrip("/") or "/"
        base = p.scheme.lower() + "://" + p.netloc.lower() + path
        return base + ("?" + p.query if p.query else "")
    except Exception:
        return u


def _url_delta(page_url, canon_url):
    """How does the canonical differ from the page's own URL? Returns labels."""
    a, b = urllib.parse.urlparse(page_url), urllib.parse.urlparse(canon_url)
    labels = []
    if a.scheme.lower() != b.scheme.lower():
        labels.append("protocol")
    ha, hb = a.netloc.lower(), b.netloc.lower()
    if ha != hb:
        labels.append("www" if _dewww(ha) == _dewww(hb) else "cross-host")
    pa, pb = a.path or "/", b.path or "/"
    if pa != pb:
        if pa.rstrip("/") == pb.rstrip("/"):
            labels.append("trailing-slash")
        elif pa.lower().rstrip("/") == pb.lower().rstrip("/"):
            labels.append("case")
        else:
            labels.append("different-page")
    if (a.query or "") != (b.query or ""):
        labels.append("query")
    return labels


# Deltas that still resolve to the same document — sloppy, worth fixing, not fatal.
_NEAR_MISS = {"protocol", "www", "trailing-slash", "case"}


def canonical_audit(pages):
    """Every indexable URL must declare its OWN canonical.

    Flags, in rough severity order:
      - duplicate canonicals: 2+ crawled URLs claiming the same canonical target
        (split into intentional-looking consolidation vs. a cluster whose target
        is not even one of them — the classic 'everything points at the homepage')
      - missing canonical
      - multiple conflicting canonical tags on one page (Google ignores all of them)
      - canonical placed outside <head> (ignored)
      - relative canonical (should be absolute)
      - cross-host canonical (hands ranking signals to another domain)
      - non-self-referencing canonical (this URL is asking to be dropped)
      - near-miss self-reference (protocol / www / trailing-slash / case drift)
      - canonical target never seen in the crawl (verify it 200s and is indexable)
    """
    known = {_norm_canon(p["url"]) for p in pages}
    unknown_data, missing, multiple, outside_head = [], [], [], []
    relative, cross_host, non_self, near_miss, self_ref, param_only = [], [], [], [], [], []
    groups = defaultdict(list)     # normalized canonical target -> [page urls]
    resolved = {}                  # page url -> absolute canonical

    for p in pages:
        url = p["url"]
        if not p.get("canonical_parsed"):
            unknown_data.append(url)
            continue
        hrefs = p.get("canonicals") or []
        if not hrefs:
            # A canonical sitting after </head> is ignored by Google, so the page is
            # effectively uncanonicalized — but the fix is "move it", not "add one".
            (outside_head if p.get("canonical_outside_head") else missing).append(url)
            continue
        if len({_norm_canon(urllib.parse.urljoin(url, h)) for h in hrefs}) > 1:
            multiple.append((url, hrefs))
            continue                      # conflicting -> Google ignores all; no target
        raw = hrefs[0]
        if not urllib.parse.urlparse(raw).scheme:
            relative.append((url, raw))
        target = urllib.parse.urljoin(url, raw)
        resolved[url] = target
        groups[_norm_canon(target)].append(url)

        delta = _url_delta(url, target)
        if not delta:
            self_ref.append(url)
        elif "cross-host" in delta:
            cross_host.append((url, target))
        elif "different-page" in delta:
            non_self.append((url, target))
        elif delta == ["query"]:
            # ?variant=/?sort= collapsing to the clean URL — the normal, intended use.
            param_only.append((url, target))
        else:
            near_miss.append((url, target, "+".join(delta)))

    dup_consolidation, dup_orphaned = [], []
    for target, urls in groups.items():
        if len(urls) < 2:
            continue
        entry = {"canonical": target, "urls": sorted(urls), "count": len(urls),
                 "target_in_group": target in {_norm_canon(u) for u in urls},
                 "target_crawled": target in known}
        (dup_consolidation if entry["target_in_group"] else dup_orphaned).append(entry)
    dup_consolidation.sort(key=lambda e: -e["count"])
    dup_orphaned.sort(key=lambda e: -e["count"])

    dangling = sorted({t for u, t in resolved.items()
                       if _norm_canon(t) not in known
                       and _same_host(u, t)})

    return {
        "duplicate_orphaned": dup_orphaned,
        "duplicate_consolidation": dup_consolidation,
        "missing": missing,
        "multiple_tags": multiple,
        "outside_head": outside_head,
        "relative": relative,
        "cross_host": cross_host,
        "non_self_referencing": non_self,
        "param_consolidation": param_only,
        "near_miss": near_miss,
        "self_referencing": self_ref,
        "dangling_targets": dangling,
        "no_html": unknown_data,
        "checked": len(pages) - len(unknown_data),
    }


# --------------------------------------------------------------------------- #
def report(pages, thin=3):
    inbound = build_link_graph(pages)
    orphans = [u for u, n in inbound.items() if n == 0]
    # importance proxy: shallow pages (depth <= 1) that receive few inbound links
    def depth(u):
        return len([s for s in urllib.parse.urlparse(u).path.split("/") if s])
    thin_important = sorted(
        [(u, n) for u, n in inbound.items() if depth(u) <= 1 and n < thin and u not in orphans],
        key=lambda x: x[1])

    dup_titles, near_titles = find_duplicates(pages, "title")
    dup_metas, near_metas = find_duplicates(pages, "meta_description")
    struct = url_structure_outliers(pages)
    canon = canonical_audit(pages)

    out = []
    w = out.append
    w("SITE-LEVEL SEO AUDIT  —  %d pages crawled\n" % len(pages))

    w("## Title / meta uniqueness")
    w("  Missing title:            %d" % len(missing_field(pages, "title")))
    w("  Missing meta description: %d" % len(missing_field(pages, "meta_description")))
    w("  Duplicate titles:         %d group(s)" % len(dup_titles))
    for val, urls in list(dup_titles.items())[:15]:
        w("    - \"%s\" x%d" % (val[:70], len(urls)))
    w("  Near-duplicate titles:    %d group(s)" % len(near_titles))
    w("  Duplicate metas:          %d group(s)" % len(dup_metas))
    for val, urls in list(dup_metas.items())[:15]:
        w("    - \"%s\" x%d" % (val[:70], len(urls)))
    w("  Near-duplicate metas:     %d group(s)\n" % len(near_metas))

    w("## Canonical uniqueness (one own canonical per URL)")
    if canon["no_html"] and not canon["checked"]:
        w("  SKIPPED — no served HTML available, so canonicals could not be read.")
        w("  (Re-run with a fetcher that returns rawHtml; absence of HTML is not")
        w("   evidence of a missing canonical.)\n")
    else:
        w("  URLs checked: %d   self-referencing & exact: %d"
          % (canon["checked"], len(canon["self_referencing"])))
        if canon["no_html"]:
            w("  No HTML (canonical unknown, NOT assumed missing): %d" % len(canon["no_html"]))

        w("  CRITICAL — duplicate canonicals, target outside the group: %d group(s)"
          % len(canon["duplicate_orphaned"]))
        for g in canon["duplicate_orphaned"][:10]:
            w("    - %d URLs -> %s%s" % (g["count"], g["canonical"],
                                         "" if g["target_crawled"] else "  [target not crawled]"))
            for u in g["urls"][:5]:
                w("        %s" % u)
            if g["count"] > 5:
                w("        ... +%d more" % (g["count"] - 5))
        w("  Duplicate canonicals, one member is the target (verify intentional): %d group(s)"
          % len(canon["duplicate_consolidation"]))
        for g in canon["duplicate_consolidation"][:10]:
            w("    - %d URLs -> %s" % (g["count"], g["canonical"]))

        w("  Missing canonical:                 %d" % len(canon["missing"]))
        for u in canon["missing"][:15]:
            w("        %s" % u)
        w("  Multiple conflicting canonical tags: %d  (Google ignores all of them)"
          % len(canon["multiple_tags"]))
        for u, hrefs in canon["multiple_tags"][:10]:
            w("        %s  -> %s" % (u, ", ".join(hrefs[:3])))
        w("  Canonical outside <head> (ignored — move it into <head>): %d"
          % len(canon["outside_head"]))
        for u in canon["outside_head"][:10]:
            w("        %s" % u)
        w("  Relative canonical (use absolute):  %d" % len(canon["relative"]))
        for u, raw in canon["relative"][:10]:
            w("        %s  -> \"%s\"" % (u, raw))
        w("  Cross-host canonical:               %d" % len(canon["cross_host"]))
        for u, t in canon["cross_host"][:10]:
            w("        %s  -> %s" % (u, t))
        w("  Non-self-referencing (points at a different page): %d"
          % len(canon["non_self_referencing"]))
        for u, t in canon["non_self_referencing"][:15]:
            w("        %s  -> %s" % (u, t))
        w("  Param URLs consolidated to a clean URL (normal, verify intent): %d"
          % len(canon["param_consolidation"]))
        w("  Near-miss self-reference (protocol/www/slash/case drift): %d"
          % len(canon["near_miss"]))
        for u, t, kind in canon["near_miss"][:10]:
            w("        [%s] %s  -> %s" % (kind, u, t))
        w("  Canonical target never seen in crawl: %d  (verify 200 + indexable)"
          % len(canon["dangling_targets"]))
        for t in canon["dangling_targets"][:10]:
            w("        %s" % t)
        w("")

    w("## Orphan pages (0 inbound internal links): %d" % len(orphans))
    for u in orphans[:30]:
        w("    - %s" % u)
    if len(orphans) > 30:
        w("    ... +%d more" % (len(orphans) - 30))
    w("")

    w("## Inbound-link distribution")
    w("  Important (depth<=1) pages with < %d inbound: %d" % (thin, len(thin_important)))
    for u, n in thin_important[:20]:
        w("    - %s  (%d inbound)" % (u, n))
    w("")

    w("## URL-structure consistency")
    w("  Depth distribution: %s" % struct["depth_distribution"])
    w("  Underscores in path: %d  (prefer hyphens)" % len(struct["underscore_in_path"]))
    w("  Uppercase in path:   %d  (prefer lowercase)" % len(struct["uppercase_in_path"]))
    w("  Trailing slash:      %d  (keep consistent site-wide)" % len(struct["trailing_slash"]))

    return "\n".join(out), {
        "pages": len(pages),
        "orphans": orphans,
        "thin_important": thin_important,
        "duplicate_titles": dup_titles,
        "duplicate_metas": dup_metas,
        "near_duplicate_titles": list(near_titles.keys()),
        "near_duplicate_metas": list(near_metas.keys()),
        "url_structure": struct,
        "missing_title": missing_field(pages, "title"),
        "missing_meta": missing_field(pages, "meta_description"),
        "canonicals": canon,
    }


def main():
    ap = argparse.ArgumentParser(description="Site-level SEO cross-page audit (Firecrawl).")
    ap.add_argument("root", nargs="?", help="Root URL to map + crawl, e.g. https://example.com")
    ap.add_argument("--urls-file", help="Text file of URLs (one per line); skips mapping.")
    ap.add_argument("--limit", type=int, default=200, help="Max URLs to crawl (default 200).")
    ap.add_argument("--thin", type=int, default=3, help="Inbound-link threshold for 'thin' (default 3).")
    ap.add_argument("--json", help="Write the structured findings to this JSON path.")
    args = ap.parse_args()

    if args.urls_file:
        with open(args.urls_file, encoding="utf-8") as f:
            urls = [ln.strip() for ln in f if ln.strip()][: args.limit]
    elif args.root:
        print("Mapping %s ..." % args.root, file=sys.stderr)
        urls = map_site(args.root, args.limit)
        print("  found %d URLs" % len(urls), file=sys.stderr)
    else:
        ap.error("provide a root URL or --urls-file")

    if not urls:
        sys.exit("No URLs to crawl.")

    print("Scraping %d pages ..." % len(urls), file=sys.stderr)
    pages = scrape_pages(urls)
    text, data = report(pages, thin=args.thin)
    print(text)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("\n(structured findings written to %s)" % args.json, file=sys.stderr)


if __name__ == "__main__":
    main()
