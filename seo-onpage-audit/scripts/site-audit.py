#!/usr/bin/env python3
"""
site-audit.py — optional site-level pass for the seo-onpage-audit skill.

Generic and site-agnostic: crawls ANY target site and derives the four cross-page
checks a single-URL fetch cannot prove:
  - title / meta-description uniqueness (exact + near-duplicate)
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
    """Batch-scrape URLs, returning [{url, title, meta_description, links[]}]."""
    start = _post("/batch/scrape", {"urls": urls, "formats": ["links"], "onlyMainContent": False})
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
        pages.append({
            "url": meta.get("sourceURL") or meta.get("url") or d.get("url") or "",
            "title": (meta.get("title") or "").strip(),
            "meta_description": (meta.get("description") or "").strip(),
            "links": d.get("links") or [],
        })
    return [p for p in pages if p["url"]]


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
