#!/usr/bin/env python
"""Search Console audit engine for the gsc-audit skill.

Stdlib only. Windows friendly (run with `python`, paths with spaces are fine).

Sub-commands
------------
  analyze   Read a run folder (config.json + raw/*.json pulls), run every
            analysis, write gsc-lane.json, url-briefs.md, inspection-queue.json
            and handoff files. Archives every raw pull first (unless --no-archive).
  archive   Copy a run folder's raw pulls into the dated history archive.
  history   Merge every archived `daily` pull into one daily series
            (latest pull wins per date) so trends can reach past 16 months.
  periods   Print the recommended date windows for a given "today".
  not-run   Write the lane result for "GSC not connected" (setup gate).

Run `python gsc_analyzer.py <command> -h` for options.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

try:  # UTF-8 console output on Windows
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

LANE = "gsc"
CONTRACT_VERSION = "1.0"
API_ROW_CAP = 25000
DATA_LAG_DAYS = 3

# ---------------------------------------------------------------------------
# Thresholds. Names are ours; the numbers are the audit rules in
# references/analyses.md. Change them there and here together. Values shared with other
# SEO skills (CTR curve, calibration minimums, striking distance, target position, brand
# hints) are fixed in skills/_system/references/seo-shared-numbers.md.
# ---------------------------------------------------------------------------
T = {
    "ctr_min_impressions": 50,
    "ctr_max_position": 20.0,          # position must be below this
    "ctr_underperformance_ratio": 0.70,  # flag when actual < expected * 0.70
    "decay_min_previous_clicks": 10,
    "decay_min_loss_ratio": 0.25,
    "decay_position_drop": 2.0,         # position worse by >= 2
    "decay_ctr_ratio": 0.75,            # CTR below 75% of previous
    "decay_impressions_drop": 0.25,     # impressions down >= 25% (demand/visibility)
    "decay_seasonal_yoy_ratio": 0.90,   # current >= 90% of same window last year
    "quick_win_min_position": 11.0,
    "quick_win_max_position": 20.0,
    "quick_win_min_impressions": 100,
    "quick_win_target_position": 5,     # sizing target for 11-20 (directional)
    "cannibal_min_pages": 2,
    "cannibal_min_total_impressions": 50,
    "device_min_impressions": 50,       # on EACH device
    "device_ctr_ratio": 2.0,
    "device_position_gap": 5.0,
    "dead_min_previous_clicks": 10,
    "dead_auto_inspect": 5,
    "brand_excellent": 0.70,            # > 70%
    "brand_healthy": 0.50,              # 50-70%
    "brand_needs_growth": 0.30,         # 30-50%, below = critical
    "stable_min_impressions": 100,      # reliable metrics
    "noisy_max_impressions": 50,        # volatile below this
    "zero_click_min_impressions": 200,  # high-impression, zero-click inspection suspects
    "geo_min_share": 0.05,
    "geo_ctr_ratio": 0.70,
    "trend_change": 0.10,               # +-10% = growth / decline
    "month_anomaly": 0.40,              # +-40% month over month
    "seasonal_index_ratio": 1.5,
    "calib_min_rows": 30,               # per rounded position
    "calib_min_impressions": 500,       # per rounded position
    "calib_min_positions": 5,           # positions needed before own curve is used
    "sitemap_stale_days": 30,
    "inspection_budget": 10,
}

# One default CTR curve (positions 1-20); 21-30 -> 0.003, >30 -> 0.001.
# Same curve the seo-site-audit sizing layer uses, so numbers agree.
DEFAULT_CTR_CURVE = {
    1: 0.28, 2: 0.15, 3: 0.10, 4: 0.075, 5: 0.055, 6: 0.040, 7: 0.032,
    8: 0.026, 9: 0.022, 10: 0.018, 11: 0.015, 12: 0.013, 13: 0.012,
    14: 0.011, 15: 0.010, 16: 0.009, 17: 0.008, 18: 0.007, 19: 0.006, 20: 0.005,
}

DEFAULT_HIGH_VALUE = ["/products/", "/collections/", "/cart"]
DEFAULT_NAV_HINTS = [".com", "store", "shop", "reviews", "review", "coupon", "promo",
                     "discount code", "phone", "contact", "login", "order", "shipping",
                     "return", "returns", "warranty", "legit", "scam", "location"]

# Raw pull kinds the analyzer understands (file stem before "__").
KNOWN_KINDS = {
    "current_page", "previous_page", "yoy_page",
    "current_query_page", "previous_query_page",
    "current_query", "previous_query",
    "daily", "page_date",
    "page_device", "device", "page_country", "country",
    "search_type_totals", "search_appearance", "previous_search_appearance",
    "inspections", "sitemaps", "sitemap_urls",
}


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def num(value, default=0.0):
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def ratio_ctr(value, clicks=0.0, impressions=0.0):
    """CTR as a 0-1 fraction; accepts percent input or derives it."""
    if value is None or value == "":
        return clicks / impressions if impressions else 0.0
    ctr = num(value)
    if ctr > 1:
        ctr /= 100.0
    return ctr


def parse_date(text):
    return dt.date.fromisoformat(str(text)[:10])


def rnd(x, n=4):
    return round(x, n) if isinstance(x, float) else x


def normalize_url(url):
    """Return (key, path). Key drops scheme, fragment, query and trailing slash."""
    url = str(url or "").strip()
    if not url:
        return "", ""
    parts = urlsplit(url if "://" in url else "https://placeholder" + (url if url.startswith("/") else "/" + url))
    path = parts.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    key = (host + path) if host != "placeholder" else path
    return key, path


def page_type(path):
    p = path.lower()
    if p in ("", "/"):
        return "home"
    if re.search(r"^/collections/[^/]+/products/", p):
        return "product_in_collection"
    if p.startswith("/products/"):
        return "product"
    if p.startswith("/collections"):
        return "collection"
    if re.match(r"^/blogs/[^/]+/[^/]+", p):
        return "blog_article"
    if p.startswith("/blogs/"):
        return "blog_index"
    if p.startswith("/pages/"):
        return "page"
    if p.startswith("/cart") or p.startswith("/checkout"):
        return "cart"
    if p.startswith("/search"):
        return "search"
    return "other"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")[:60] or "site"


def pct_change(new, old):
    return (new - old) / old if old else None


# ---------------------------------------------------------------------------
# brand classification
# ---------------------------------------------------------------------------
class BrandMatcher:
    """Whole-word brand matching with an ambiguous-term rule.

    Ambiguous terms (e.g. "example outdoor", which is also a generic phrase)
    count as brand only when the query IS the term, or the query also carries
    a navigational hint ("example outdoor reviews", "example outdoor .com").
    """

    def __init__(self, brand_terms, ambiguous_terms=None, nav_hints=None):
        self.brand = [t.lower().strip() for t in (brand_terms or []) if str(t).strip()]
        self.ambiguous = {t.lower().strip() for t in (ambiguous_terms or []) if str(t).strip()}
        self.nav = [h.lower() for h in (nav_hints or DEFAULT_NAV_HINTS)]
        self._re = {t: re.compile(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])") for t in self.brand}

    def classify(self, query):
        q = str(query or "").lower().strip()
        hit_ambiguous = False
        for term, rx in self._re.items():
            if not rx.search(q):
                continue
            if term not in self.ambiguous:
                return "brand"
            if q == term or any(h in q for h in self.nav):
                return "brand"
            hit_ambiguous = True
        return "ambiguous_non_brand" if hit_ambiguous else "non_brand"

    def is_brand(self, query):
        return self.classify(query) == "brand"


# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------
def rows_from_payload(payload):
    """Accept API shape ({keys:[...]} + meta.dimensions) or flat dict rows."""
    meta = payload.get("meta", {}) if isinstance(payload, dict) else {}
    rows = payload.get("rows", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        return meta, []
    dims = [d.strip() for d in (meta.get("dimensions") or [])]
    out = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        flat = dict(row)
        if "keys" in row and dims:
            for name, value in zip(dims, row["keys"]):
                flat[name] = value
            flat.pop("keys", None)
        if "searchAppearance" in flat and "search_appearance" not in flat:
            flat["search_appearance"] = flat["searchAppearance"]
        if "url" in flat and "page" not in flat:
            flat["page"] = flat["url"]
        out.append(flat)
    return meta, out


def metric_row(row):
    clicks = num(row.get("clicks"))
    impressions = num(row.get("impressions"))
    return {
        "clicks": clicks,
        "impressions": impressions,
        "ctr": ratio_ctr(row.get("ctr"), clicks, impressions),
        "position": num(row.get("position"), 0.0),
    }


def load_run(run_dir):
    run_dir = Path(run_dir)
    cfg_path = run_dir / "config.json"
    if not cfg_path.exists():
        raise SystemExit(f"config.json not found in {run_dir}")
    config = json.loads(cfg_path.read_text(encoding="utf-8"))
    raw = {}
    metas = defaultdict(list)
    raw_dir = run_dir / "raw"
    unknown = []
    if raw_dir.exists():
        for f in sorted(raw_dir.glob("*.json")):
            kind = f.stem.split("__")[0]
            if kind not in KNOWN_KINDS:
                unknown.append(f.name)
                continue
            payload = json.loads(f.read_text(encoding="utf-8"))
            meta, rows = rows_from_payload(payload)
            meta = dict(meta)
            meta["file"] = f.name
            meta["rows_in_file"] = len(rows)
            metas[kind].append(meta)
            raw.setdefault(kind, []).extend(rows)
    return config, raw, metas, unknown


# ---------------------------------------------------------------------------
# CTR curve (default, or calibrated from the property's own rows)
# ---------------------------------------------------------------------------
def build_ctr_curve(rows, brand, mode="auto"):
    curve = dict(DEFAULT_CTR_CURVE)
    source = {p: "default" for p in curve}
    stats = {}
    if mode in ("auto", "own") and rows:
        buckets = defaultdict(lambda: [0.0, 0.0, 0])
        for r in rows:
            q = r.get("query")
            if q and brand.is_brand(q):
                continue  # brand queries inflate CTR
            m = metric_row(r)
            pos = int(round(m["position"]))
            if 1 <= pos <= 20 and m["impressions"] > 0:
                b = buckets[pos]
                b[0] += m["clicks"]
                b[1] += m["impressions"]
                b[2] += 1
        usable = {p: b for p, b in buckets.items()
                  if b[2] >= T["calib_min_rows"] and b[1] >= T["calib_min_impressions"]}
        stats = {p: {"rows": b[2], "impressions": b[1], "ctr": rnd(b[0] / b[1])} for p, b in sorted(buckets.items())}
        if len(usable) >= T["calib_min_positions"] or (mode == "own" and usable):
            for p, b in usable.items():
                curve[p] = b[0] / b[1]
                source[p] = "own_gsc"
            # keep the curve non-increasing with position
            for p in range(2, 21):
                if curve[p] > curve[p - 1]:
                    curve[p] = curve[p - 1]
                    source[p] = source[p] + "+smoothed"
    used_own = any(s.startswith("own") for s in source.values())
    return {
        "mode_requested": mode,
        "mode_used": "calibrated_own_gsc" if used_own else "default",
        "curve": {p: rnd(v, 5) for p, v in curve.items()},
        "source_by_position": source,
        "calibration_stats": stats,
        "note": ("Own-data curve measures pages against this store's own average CTR at each "
                 "position; positions without enough rows fall back to the default curve.")
        if used_own else "Not enough non-brand rows per position to calibrate; default curve used.",
    }


def expected_ctr(position, curve):
    pos = num(position, 100.0)
    if pos <= 0:
        pos = 100.0
    if pos > 30:
        return 0.001
    if pos > 20:
        return 0.003
    pos = max(1.0, pos)
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    lo_v, hi_v = curve[lo], curve[min(hi, 20)]
    return lo_v + (hi_v - lo_v) * (pos - lo)


# ---------------------------------------------------------------------------
# the seven analyses
# ---------------------------------------------------------------------------
def analyze_ctr(page_rows, curve, high_value):
    out = []
    for r in page_rows:
        m = metric_row(r)
        if m["impressions"] < T["ctr_min_impressions"] or m["position"] <= 0 or m["position"] >= T["ctr_max_position"]:
            continue
        exp = expected_ctr(m["position"], curve)
        if m["ctr"] >= exp * T["ctr_underperformance_ratio"]:
            continue
        key, path = normalize_url(r.get("page"))
        caveats = []
        ptype = page_type(path)
        if ptype == "home":
            caveats.append("Homepage: navigational queries depress CTR; act only if the gap is severe.")
        if ptype == "collection":
            caveats.append("Collection page: broad head terms often carry lower CTR; check the query mix.")
        if m["position"] <= 1.5:
            caveats.append("Near position 1 with low CTR usually means a SERP feature (AI Overview, shopping pack, snippet) takes the clicks; check the live SERP before rewriting.")
        out.append({
            "page": r.get("page"), "url_key": key, "path": path, "page_type": ptype,
            "high_value": is_high_value(path, high_value),
            "position": rnd(m["position"], 2), "impressions": m["impressions"], "clicks": m["clicks"],
            "actual_ctr": rnd(m["ctr"]), "expected_ctr": rnd(exp), "ctr_gap": rnd(exp - m["ctr"]),
            "potential_clicks": int(round(max(exp - m["ctr"], 0) * m["impressions"])),
            "cause": "unverified: weak title/meta, SERP feature, or intent mismatch (check SERP)",
            "caveats": caveats, "issue": "ctr_underperformance",
        })
    out.sort(key=lambda x: (-x["potential_clicks"], -x["impressions"]))
    return out


def analyze_decay(cur_pages, prev_pages, yoy_pages):
    prev = {normalize_url(r.get("page"))[0]: metric_row(r) for r in prev_pages}
    yoy = {normalize_url(r.get("page"))[0]: metric_row(r) for r in yoy_pages}
    cur = {normalize_url(r.get("page"))[0]: (r, metric_row(r)) for r in cur_pages}
    out, dead = [], []
    urls = {normalize_url(r.get("page"))[0]: r.get("page") for r in prev_pages}
    for key, page in urls.items():
        p = prev[key]
        c = cur.get(key, (None, {"clicks": 0.0, "impressions": 0.0, "ctr": 0.0, "position": 0.0}))[1]
        _, path = normalize_url(page)
        if p["clicks"] >= T["dead_min_previous_clicks"] and c["clicks"] == 0:
            dead.append({
                "page": page, "url_key": key, "path": path, "page_type": page_type(path),
                "previous_clicks": p["clicks"], "previous_impressions": p["impressions"],
                "current_impressions": c["impressions"], "click_loss": p["clicks"],
                "still_has_impressions": c["impressions"] > 0, "issue": "dead_page",
            })
        if p["clicks"] < T["decay_min_previous_clicks"] or c["clicks"] == 0:
            continue  # zero-click pages are reported once, as dead pages
        loss = p["clicks"] - c["clicks"]
        if loss <= 0 or loss / p["clicks"] < T["decay_min_loss_ratio"]:
            continue
        rank_drop = bool(c["position"] and p["position"] and c["position"] - p["position"] >= T["decay_position_drop"])
        ctr_drop = bool(p["ctr"] and c["impressions"] and c["ctr"] < p["ctr"] * T["decay_ctr_ratio"])
        imp_drop = bool(p["impressions"] and (p["impressions"] - c["impressions"]) / p["impressions"] >= T["decay_impressions_drop"])
        if rank_drop and ctr_drop:
            diagnosis = "ranking_and_ctr_drop"
        elif rank_drop:
            diagnosis = "ranking_drop"
        elif ctr_drop:
            diagnosis = "ctr_drop"
        elif imp_drop:
            diagnosis = "demand_or_visibility_drop"
        else:
            diagnosis = "traffic_loss"
        y = yoy.get(key)
        seasonal = None
        if y is not None and y["clicks"] > 0:
            seasonal = c["clicks"] >= y["clicks"] * T["decay_seasonal_yoy_ratio"]
        out.append({
            "page": page, "url_key": key, "path": path, "page_type": page_type(path),
            "previous_clicks": p["clicks"], "current_clicks": c["clicks"],
            "click_loss": rnd(loss, 2), "loss_ratio": rnd(loss / p["clicks"]),
            "previous_position": rnd(p["position"], 2), "current_position": rnd(c["position"], 2),
            "previous_ctr": rnd(p["ctr"]), "current_ctr": rnd(c["ctr"]),
            "previous_impressions": p["impressions"], "current_impressions": c["impressions"],
            "yoy_clicks": y["clicks"] if y else None,
            "seasonal_likely": seasonal,
            "diagnosis": diagnosis, "issue": "content_decay",
        })
    out.sort(key=lambda x: (-x["click_loss"], -x["loss_ratio"]))
    dead.sort(key=lambda x: -x["previous_clicks"])
    return out, dead


def analyze_quick_wins(qp_rows, brand, curve):
    items = []
    for r in qp_rows:
        m = metric_row(r)
        if not (T["quick_win_min_position"] <= m["position"] <= T["quick_win_max_position"]):
            continue
        if m["impressions"] < T["quick_win_min_impressions"]:
            continue
        key, path = normalize_url(r.get("page"))
        target_ctr = expected_ctr(T["quick_win_target_position"], curve)
        items.append({
            "query": r.get("query"), "page": r.get("page"), "url_key": key, "path": path,
            "position": rnd(m["position"], 2), "impressions": m["impressions"], "clicks": m["clicks"],
            "ctr": rnd(m["ctr"]), "brand_query": brand.is_brand(r.get("query")),
            "striking_distance_score": rnd(m["impressions"] * position_weight(m["position"]), 1),
            "directional_click_gain_at_target": int(round(max(target_ctr - m["ctr"], 0) * m["impressions"])),
            "issue": "striking_distance",
        })
    items.sort(key=lambda x: (-x["impressions"], x["position"]))
    by_page = defaultdict(list)
    for it in items:
        by_page[it["url_key"]].append(it)
    grouped = [{"url_key": k, "page": v[0]["page"], "queries": len(v),
                "impressions": sum(i["impressions"] for i in v), "items": v}
               for k, v in by_page.items()]
    grouped.sort(key=lambda g: -g["impressions"])
    return items, grouped


def position_weight(pos):
    """Our striking-distance weight: strongest for positions 8-15."""
    if 8 <= pos <= 15:
        return 1.0
    if 4 <= pos < 8:
        return 0.6
    if 15 < pos <= 20:
        return 0.7
    return 0.0


def analyze_cannibalization(qp_rows, brand):
    groups = defaultdict(list)
    for r in qp_rows:
        q = str(r.get("query") or "").strip()
        if not q or not r.get("page") or brand.is_brand(q):
            continue
        groups[q].append(r)
    out = []
    for q, rows in groups.items():
        pages = {}
        for r in rows:
            key, path = normalize_url(r.get("page"))
            m = metric_row(r)
            if key in pages:  # merge variants of the same path
                pm = pages[key]
                pm["impressions"] += m["impressions"]
                pm["clicks"] += m["clicks"]
                continue
            pages[key] = {"page": r.get("page"), "url_key": key, "path": path, "page_type": page_type(path),
                          "position": rnd(m["position"], 2), "impressions": m["impressions"], "clicks": m["clicks"]}
        total = sum(p["impressions"] for p in pages.values())
        if len(pages) < T["cannibal_min_pages"] or total < T["cannibal_min_total_impressions"]:
            continue
        plist = sorted(pages.values(), key=lambda p: (p["position"] or 99, -p["clicks"]))
        types = {p["page_type"] for p in plist}
        same_type = len(types) == 1
        shop_hierarchy = types <= {"collection", "product", "product_in_collection"} and len(types) > 1
        if same_type:
            overlap = "same_type_overlap"
            rec = "Likely true overlap: compare intent, then consolidate (merge + 301) or differentiate. Never auto-merge."
        elif shop_hierarchy:
            overlap = "shop_hierarchy"
            rec = "Collection + product on one query is normal store hierarchy; check that internal links and titles point the head term at the right level."
        else:
            overlap = "mixed_intent"
            rec = "Different page types (e.g. guide vs product) may serve different intents; differentiate and cross-link rather than merge."
        top_share = (plist[0]["impressions"] / total) if total else 0
        out.append({"query": q, "unique_pages": len(plist), "total_impressions": total,
                    "top_page_impression_share": rnd(top_share), "overlap_type": overlap,
                    "recommendation": rec, "pages": plist, "issue": "possible_cannibalization"})
    out.sort(key=lambda g: (-g["total_impressions"], -g["unique_pages"]))
    return out


def analyze_device(page_device_rows):
    by_page = defaultdict(dict)
    for r in page_device_rows:
        d = str(r.get("device") or "").lower()
        if d in ("mobile", "desktop") and r.get("page"):
            by_page[normalize_url(r.get("page"))[0]][d] = (r.get("page"), metric_row(r))
    out = []
    for key, dv in by_page.items():
        if "mobile" not in dv or "desktop" not in dv:
            continue
        page, mob = dv["mobile"]
        _, desk = dv["desktop"]
        if min(mob["impressions"], desk["impressions"]) < T["device_min_impressions"]:
            continue
        ratio = max(mob["ctr"], desk["ctr"]) / max(min(mob["ctr"], desk["ctr"]), 0.0001)
        gap = abs(mob["position"] - desk["position"])
        if ratio < T["device_ctr_ratio"] and gap < T["device_position_gap"]:
            continue
        if gap >= T["device_position_gap"] and mob["position"] > desk["position"]:
            issue = "mobile_ranking_gap: check mobile rendering and Core Web Vitals"
        elif ratio >= T["device_ctr_ratio"] and mob["ctr"] < desk["ctr"]:
            issue = "mobile_ctr_gap: check title truncation on mobile, page speed, layout"
        else:
            issue = "desktop_gap: check whether desktop serves different content"
        out.append({"page": page, "url_key": key,
                    "mobile": {k: rnd(v) for k, v in mob.items()},
                    "desktop": {k: rnd(v) for k, v in desk.items()},
                    "ctr_ratio": rnd(ratio, 2), "position_gap": rnd(gap, 2),
                    "likely_issue": issue, "issue": "device_gap"})
    out.sort(key=lambda x: (-x["position_gap"], -x["ctr_ratio"]))
    return out


def analyze_brand(query_rows, brand):
    buckets = {k: {"clicks": 0.0, "impressions": 0.0, "pos_x_imp": 0.0, "queries": 0}
               for k in ("brand", "non_brand", "ambiguous_non_brand")}
    top = []
    for r in query_rows:
        cls = brand.classify(r.get("query"))
        m = metric_row(r)
        b = buckets[cls]
        b["clicks"] += m["clicks"]
        b["impressions"] += m["impressions"]
        b["pos_x_imp"] += m["position"] * m["impressions"]
        b["queries"] += 1
        if cls != "brand":
            top.append({"query": r.get("query"), "clicks": m["clicks"], "impressions": m["impressions"],
                        "ctr": rnd(m["ctr"]), "position": rnd(m["position"], 2), "class": cls})
    summary = {}
    for k, b in buckets.items():
        summary[k] = {"clicks": b["clicks"], "impressions": b["impressions"], "queries": b["queries"],
                      "ctr": rnd(b["clicks"] / b["impressions"]) if b["impressions"] else 0.0,
                      "avg_position": rnd(b["pos_x_imp"] / b["impressions"], 2) if b["impressions"] else None}
    nb_clicks = buckets["non_brand"]["clicks"] + buckets["ambiguous_non_brand"]["clicks"]
    total = nb_clicks + buckets["brand"]["clicks"]
    ratio = nb_clicks / total if total else 0.0
    if ratio > T["brand_excellent"]:
        health = "excellent"
    elif ratio >= T["brand_healthy"]:
        health = "healthy"
    elif ratio >= T["brand_needs_growth"]:
        health = "needs_growth"
    else:
        health = "critical"
    top.sort(key=lambda x: (-x["clicks"], -x["impressions"]))
    return {"non_brand_ratio": rnd(ratio), "health": health if total else "no_data",
            "buckets": summary, "top_non_brand": top[:10],
            "note": "Ambiguous brand phrases without a navigational hint are counted as non-brand."}


# ---------------------------------------------------------------------------
# segments, trend, sitemaps, inspections
# ---------------------------------------------------------------------------
def aggregate(rows, dim):
    agg = defaultdict(lambda: {"clicks": 0.0, "impressions": 0.0, "pos_x_imp": 0.0})
    for r in rows:
        k = str(r.get(dim) or "").strip()
        if not k:
            continue
        m = metric_row(r)
        a = agg[k]
        a["clicks"] += m["clicks"]
        a["impressions"] += m["impressions"]
        a["pos_x_imp"] += m["position"] * m["impressions"]
    out = []
    for k, a in agg.items():
        out.append({dim: k, "clicks": a["clicks"], "impressions": a["impressions"],
                    "ctr": rnd(a["clicks"] / a["impressions"]) if a["impressions"] else 0.0,
                    "avg_position": rnd(a["pos_x_imp"] / a["impressions"], 2) if a["impressions"] else None})
    out.sort(key=lambda x: -x["impressions"])
    return out


def build_segments(raw):
    device_rows = raw.get("device") or raw.get("page_device") or []
    country_rows = raw.get("country") or raw.get("page_country") or []
    devices = aggregate(device_rows, "device")
    countries = aggregate(country_rows, "country")
    total_imp = sum(c["impressions"] for c in countries) or 0
    total_clk = sum(c["clicks"] for c in countries) or 0
    overall_ctr = total_clk / total_imp if total_imp else 0
    geo = []
    for c in countries:
        share = c["impressions"] / total_imp if total_imp else 0
        c["impression_share"] = rnd(share)
        if share >= T["geo_min_share"] and overall_ctr and c["ctr"] < overall_ctr * T["geo_ctr_ratio"]:
            geo.append({**c, "geo_opportunity_score": int(round((overall_ctr - c["ctr"]) * c["impressions"])),
                        "note": "Country CTR well below the property average; check pricing/shipping relevance, currency, and whether the store serves this market."})
    stypes = []
    for r in raw.get("search_type_totals", []):
        m = metric_row(r)
        stypes.append({"search_type": str(r.get("search_type") or r.get("type") or "web").lower(), **{k: rnd(v) for k, v in m.items()}})
    appearances = aggregate(raw.get("search_appearance", []), "search_appearance")
    prev_app = {a["search_appearance"]: a for a in aggregate(raw.get("previous_search_appearance", []), "search_appearance")}
    for a in appearances:
        p = prev_app.get(a["search_appearance"])
        if p and p["clicks"]:
            a["click_change"] = rnd(pct_change(a["clicks"], p["clicks"]))
            a["losing"] = a["click_change"] is not None and a["click_change"] <= -T["decay_min_loss_ratio"]
        if "FAQ" in a["search_appearance"].upper():
            a["note"] = "FAQ rich results are gone for all sites; do not recommend FAQ markup for visibility."
    return {"devices": devices, "countries": countries, "geo_opportunities": geo,
            "search_types": stypes, "search_appearances": appearances}


def merge_daily(series_list):
    """series_list: list of (pulled_at, rows). Latest pull wins per date."""
    merged = {}
    for pulled_at, rows in sorted(series_list, key=lambda x: x[0] or ""):
        for r in rows:
            d = str(r.get("date") or "")[:10]
            if d:
                merged[d] = {"date": d, **metric_row(r)}
    return [merged[d] for d in sorted(merged)]


def window_sum(by_date, start, end):
    c = i = px = 0.0
    days = 0
    d = start
    while d <= end:
        r = by_date.get(d.isoformat())
        if r:
            c += r["clicks"]
            i += r["impressions"]
            px += r["position"] * r["impressions"]
            days += 1
        d += dt.timedelta(days=1)
    return {"start": start.isoformat(), "end": end.isoformat(), "days_with_data": days, "clicks": c,
            "impressions": i, "ctr": rnd(c / i) if i else 0.0, "avg_position": rnd(px / i, 2) if i else None}


def label_change(change):
    if change is None:
        return "unknown"
    if change >= T["trend_change"]:
        return "growth"
    if change <= -T["trend_change"]:
        return "decline"
    return "stable"


def trend_summary(daily, today, period_days):
    if not daily:
        return {}
    settled_cutoff = today - dt.timedelta(days=DATA_LAG_DAYS)
    by_date = {r["date"]: r for r in daily}
    dates = [parse_date(r["date"]) for r in daily]
    latest = max(dates)
    provisional = [d.isoformat() for d in dates if d > settled_cutoff]
    end = min(latest, settled_cutoff)
    cur = window_sum(by_date, end - dt.timedelta(days=period_days - 1), end)
    prev_end = end - dt.timedelta(days=period_days)
    prev = window_sum(by_date, prev_end - dt.timedelta(days=period_days - 1), prev_end)
    yoy_end = end - dt.timedelta(days=364)  # 52 weeks keeps weekdays aligned
    yoy = window_sum(by_date, yoy_end - dt.timedelta(days=period_days - 1), yoy_end)
    months = defaultdict(lambda: {"clicks": 0.0, "impressions": 0.0, "days": 0})
    for r in daily:
        if parse_date(r["date"]) > end:
            continue
        m = months[r["date"][:7]]
        m["clicks"] += r["clicks"]
        m["impressions"] += r["impressions"]
        m["days"] += 1
    monthly = [{"month": k, **v, "ctr": rnd(v["clicks"] / v["impressions"]) if v["impressions"] else 0.0}
               for k, v in sorted(months.items())]
    anomalies = []
    for a, b in zip(monthly, monthly[1:]):
        if a["days"] >= 28 and b["days"] >= 28 and a["clicks"]:
            ch = pct_change(b["clicks"], a["clicks"])
            if ch is not None and abs(ch) >= T["month_anomaly"]:
                anomalies.append({"month": b["month"], "click_change_vs_prior_month": rnd(ch),
                                  "note": "Large month-over-month swing: check for algorithm updates, site changes, tracking gaps, or seasonality before acting."})
    seasonality = None
    full = [m for m in monthly if m["days"] >= 28]
    if len(full) >= 13:
        moy = defaultdict(list)
        for m in full:
            moy[m["month"][5:]].append(m["clicks"])
        mean_all = sum(m["clicks"] for m in full) / len(full)
        index = {k: rnd((sum(v) / len(v)) / mean_all, 3) for k, v in sorted(moy.items())} if mean_all else {}
        if index:
            peak = max(index, key=index.get)
            trough = min(index, key=index.get)
            seasonality = {"month_index": index, "peak_month": peak, "trough_month": trough,
                           "seasonal": index[trough] > 0 and index[peak] / index[trough] >= T["seasonal_index_ratio"]}
    pc = pct_change(cur["clicks"], prev["clicks"])
    yc = pct_change(cur["clicks"], yoy["clicks"]) if yoy["days_with_data"] >= period_days * 0.8 else None
    return {
        "first_date": min(dates).isoformat(), "latest_date": latest.isoformat(),
        "settled_end": end.isoformat(), "provisional_dates_excluded": provisional,
        "coverage_days": len(daily), "coverage_months": len(monthly),
        "beyond_16_months": len(monthly) > 16,
        "current_window": cur, "previous_window": prev, "yoy_window": yoy,
        "change_vs_previous": rnd(pc) if pc is not None else None,
        "change_yoy": rnd(yc) if yc is not None else None,
        "trend_label": label_change(pc), "yoy_label": label_change(yc),
        "monthly": monthly, "anomalies": anomalies, "seasonality": seasonality,
    }


def page_position_trend(page_date_rows):
    per = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
    for r in page_date_rows:
        key = normalize_url(r.get("page"))[0]
        month = str(r.get("date") or "")[:7]
        m = metric_row(r)
        if key and month:
            per[key][month][0] += m["position"] * m["impressions"]
            per[key][month][1] += m["impressions"]
    out = {}
    for key, months in per.items():
        series = [(mo, v[0] / v[1]) for mo, v in sorted(months.items()) if v[1]]
        if series:
            out[key] = {"first_month": series[0][0], "first_avg_position": rnd(series[0][1], 2),
                        "last_month": series[-1][0], "last_avg_position": rnd(series[-1][1], 2)}
    return out


def sitemap_health(sitemaps, today):
    out = []
    for s in sitemaps:
        path = s.get("path") or s.get("feedpath") or s.get("sitemap")
        errors = int(num(s.get("errors")))
        warnings = int(num(s.get("warnings")))
        submitted = indexed = 0
        for c in s.get("contents", []) or []:
            submitted += int(num(c.get("submitted")))
            indexed += int(num(c.get("indexed")))
        last_dl = s.get("lastDownloaded") or s.get("last_downloaded")
        stale = None
        if last_dl:
            try:
                stale = (today - parse_date(last_dl)).days > T["sitemap_stale_days"]
            except ValueError:
                stale = None
        flags = []
        if errors:
            flags.append(f"{errors} error(s)")
        if warnings:
            flags.append(f"{warnings} warning(s)")
        if s.get("isPending") or s.get("is_pending"):
            flags.append("pending")
        if stale:
            flags.append(f"not downloaded by Google in {T['sitemap_stale_days']}+ days")
        out.append({"path": path, "last_submitted": s.get("lastSubmitted") or s.get("last_submitted"),
                    "last_downloaded": last_dl, "is_pending": bool(s.get("isPending") or s.get("is_pending")),
                    "errors": errors, "warnings": warnings, "submitted_urls": submitted,
                    "indexed_urls_reported": indexed or None, "flags": flags,
                    "health": "issues" if flags else "ok"})
    return out


COVERAGE_MAP = [
    ("submitted and indexed", "indexed", 0, "Indexed. If traffic fell, it likely moved to another URL or the query demand changed."),
    ("indexed, not submitted", "indexed_not_in_sitemap", 1, "Indexed but missing from the sitemap."),
    ("crawled - currently not indexed", "crawled_not_indexed", 4, "Google crawled but chose not to index: a quality or duplication signal."),
    ("discovered - currently not indexed", "discovered_not_indexed", 4, "Known but not crawled yet: crawl priority / internal-link signal."),
    ("page with redirect", "redirect", 2, "Redirects: confirm the target is the intended replacement and not a chain."),
    ("noindex", "noindex", 5, "Excluded by noindex: remove it if unintentional (could be deliberate: confirm first)."),
    ("blocked by robots", "robots_blocked", 5, "Blocked by robots.txt: Google cannot see the page (or its noindex)."),
    ("google chose different canonical", "canonical_mismatch", 3, "Google picked a different canonical than declared."),
    ("alternate page with proper canonical", "canonicalized", 2, "Canonicalized to another URL (often a Shopify collection-scoped product URL)."),
    ("duplicate without user-selected canonical", "duplicate_no_canonical", 3, "Duplicate with no declared canonical."),
    ("soft 404", "soft_404", 5, "Soft 404: page returns 200 but looks empty or missing."),
    ("not found", "not_found_404", 5, "404: restore the page or 301 it to the closest replacement."),
    ("server error", "server_error", 5, "5xx server error on fetch."),
    ("unknown to google", "unknown_to_google", 5, "Google does not know this URL (removed, blocked, or never linked)."),
    ("not on google", "not_on_google", 5, "Not on Google: blocked, noindex, or removed."),
]


def interpret_inspection(r):
    cov = str(r.get("coverage_state") or r.get("coverageState") or "").strip()
    user_c = r.get("user_canonical") or r.get("userCanonical")
    google_c = r.get("google_canonical") or r.get("googleCanonical")
    robots = str(r.get("robots_txt_state") or r.get("robotsTxtState") or "")
    fetch = str(r.get("page_fetch_state") or r.get("pageFetchState") or "")
    indexing = str(r.get("indexing_state") or r.get("indexingState") or "")
    status, risk, note = "unclassified", 1, "Coverage state not recognised; read the raw inspection."
    low = cov.lower()
    for needle, st, rk, nt in COVERAGE_MAP:
        if needle in low:
            status, risk, note = st, rk, nt
            break
    extras = []
    if user_c and google_c and normalize_url(user_c)[0] != normalize_url(google_c)[0]:
        risk = max(risk, 3)
        extras.append("declared canonical differs from Google-selected canonical")
    if "DISALLOWED" in robots.upper():
        risk = max(risk, 5)
        extras.append("robots.txt disallows")
    if fetch and fetch.upper() not in ("SUCCESSFUL", "PAGE_FETCH_STATE_UNSPECIFIED"):
        risk = max(risk, 4)
        extras.append(f"fetch state {fetch}")
    if "NOINDEX" in indexing.upper() and "ALLOWED" not in indexing.upper():
        risk = max(risk, 5)
        extras.append(f"indexing state {indexing}")
    url = r.get("url") or r.get("page_url") or r.get("inspection_url")
    return {"url": url, "url_key": normalize_url(url)[0], "verdict": r.get("verdict"),
            "coverage_state": cov, "index_status": status, "index_risk_score": risk,
            "last_crawl_time": r.get("last_crawl_time") or r.get("lastCrawlTime"),
            "user_canonical": user_c, "google_canonical": google_c,
            "diagnosis": note, "extra_flags": extras,
            "deliberate_possible": status in ("noindex", "redirect", "canonicalized")}


# ---------------------------------------------------------------------------
# page-query map, briefs, recommendations
# ---------------------------------------------------------------------------
def is_high_value(path, patterns):
    p = (path or "").lower()
    return any(pt.lower() in p for pt in patterns)


def page_query_map(qp_rows, brand):
    out = []
    for r in qp_rows:
        if not r.get("page") or not r.get("query"):
            continue
        key, path = normalize_url(r.get("page"))
        m = metric_row(r)
        out.append({"url_key": key, "page": r.get("page"), "path": path, "query": r.get("query"),
                    "query_class": brand.classify(r.get("query")),
                    "clicks": m["clicks"], "impressions": m["impressions"], "ctr": rnd(m["ctr"]),
                    "position": rnd(m["position"], 2), "source": "gsc", "confidence": 0.9})
    out.sort(key=lambda x: (-x["clicks"], -x["impressions"], x["position"]))
    return out


def load_register(path):
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    out = {}
    with p.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            slug = row.get("Complete URL Slug") or ""
            key, rpath = normalize_url(slug)
            if not rpath or rpath == "/":
                continue
            out[rpath] = {"article_number": row.get("Article #"), "article_title": row.get("Article Title"),
                          "primary_keyword": row.get("Primary Keyword"), "complete_url_slug": slug,
                          "shopify_article_id": row.get("Shopify Article ID")}
    return out


ACTION_INFO = {
    "fix_indexing": ("seo-onpage-audit", "theme-dev", "Fix the indexing problem before any content work"),
    "restore_or_redirect": ("manual-review", "seo", "Confirm whether the page was removed on purpose; restore it or 301 it"),
    "refresh_content": ("seo-page-diagnosis", "content", "Diagnose then refresh the decaying page"),
    "fix_snippet": ("seo-page-diagnosis", "content", "Rewrite title and meta for the queries the page already ranks for"),
    "review_cannibalization": ("seo-page-diagnosis", "seo", "Decide which page owns the overlapping query"),
    "push_to_page_one": ("seo-page-diagnosis", "content", "Push striking-distance queries onto page one"),
    "fix_device_gap": ("seo-onpage-audit", "theme-dev", "Fix the mobile/desktop performance gap"),
    "check_seasonality": ("gsc-audit", "seo", "Decline matches last year's season; re-check after the season"),
    "monitor": ("gsc-audit", "seo", "Monitor"),
}

REFRESH_OUTCOME_HINT = {
    "fix_snippet": "quick_update",
    "refresh_content": "substantive_refresh",
    "restore_or_redirect": "restore",
    "review_cannibalization": "consolidate_redirect_prune_handoff",
    "push_to_page_one": "quick_update",
    "check_seasonality": "no_change",
    "monitor": "no_change",
}


def owner_for(action, ptype):
    route, owner, _ = ACTION_INFO[action]
    if action in ("fix_snippet", "push_to_page_one", "refresh_content") and ptype in ("product", "product_in_collection"):
        owner = "catalog"
    if action == "fix_snippet" and ptype == "collection":
        owner = "catalog"
    return route, owner


def brief_confidence(impressions, clicks, period_days, cap_hit, n_signals, source_type):
    c = 0.35
    if impressions >= T["stable_min_impressions"]:
        c += 0.30
    elif impressions >= T["noisy_max_impressions"]:
        c += 0.15
    if clicks >= 10:
        c += 0.10
    if period_days >= 28:
        c += 0.10
    if cap_hit:
        c -= 0.15
    c += min(max(n_signals - 1, 0) * 0.05, 0.10)
    if source_type == "fixture":
        c = min(c, 0.55)
    return round(min(max(c, 0.10), 0.95), 2)


def build_briefs(ctx):
    cur_pages = {normalize_url(r.get("page"))[0]: (r.get("page"), metric_row(r)) for r in ctx["raw"].get("current_page", [])}
    prev_pages = {normalize_url(r.get("page"))[0]: metric_row(r) for r in ctx["raw"].get("previous_page", [])}
    yoy_pages = {normalize_url(r.get("page"))[0]: metric_row(r) for r in ctx["raw"].get("yoy_page", [])}
    qmap = defaultdict(list)
    for row in ctx["page_query_map"]:
        qmap[row["url_key"]].append(row)
    idx = lambda items: {i["url_key"]: i for i in items}  # noqa: E731
    ctr_i, decay_i, dead_i = idx(ctx["ctr"]), idx(ctx["decay"]), idx(ctx["dead"])
    dev_i = idx(ctx["device"])
    insp_i = {i["url_key"]: i for i in ctx["inspections"]}
    qw = defaultdict(list)
    for it in ctx["quick_wins"]:
        qw[it["url_key"]].append(it)
    can = defaultdict(list)
    for g in ctx["cannibalization"]:
        for p in g["pages"]:
            can[p["url_key"]].append({"query": g["query"], "overlap_type": g["overlap_type"], "unique_pages": g["unique_pages"]})
    queue_keys = {q["url_key"] for q in ctx.get("inspection_queue", [])}
    urls = {}
    for k, (page, _) in cur_pages.items():
        urls[k] = page
    for coll in (ctx["decay"], ctx["dead"], ctx["ctr"]):
        for i in coll:
            urls.setdefault(i["url_key"], i["page"])
    for k, rows in qmap.items():
        urls.setdefault(k, rows[0]["page"])
    briefs = []
    for key, page in urls.items():
        _, path = normalize_url(page)
        ptype = page_type(path)
        qrows = qmap.get(key, [])
        if key in cur_pages:
            cm = cur_pages[key][1]
        else:
            c = sum(r["clicks"] for r in qrows)
            i = sum(r["impressions"] for r in qrows)
            px = sum(r["position"] * r["impressions"] for r in qrows)
            cm = {"clicks": c, "impressions": i, "ctr": c / i if i else 0.0, "position": px / i if i else 0.0}
        signals = []
        scores = {"ctr_upside": 0, "traffic_loss": 0, "striking_distance": 0.0, "striking_click_gain": 0,
                  "index_risk": 0, "device_gap": 0.0}
        if key in ctr_i:
            x = ctr_i[key]
            scores["ctr_upside"] = x["potential_clicks"]
            signals.append({"type": "ctr_gap", "detail": f"CTR {x['actual_ctr']:.2%} vs expected {x['expected_ctr']:.2%} at position {x['position']}"})
        if key in decay_i:
            x = decay_i[key]
            conf_mult = 1.0 if x["previous_clicks"] >= 50 else 0.7
            scores["traffic_loss"] = int(round(x["click_loss"] * conf_mult))
            signals.append({"type": "decay", "detail": f"clicks {int(x['previous_clicks'])} -> {int(x['current_clicks'])} ({x['diagnosis']})"
                            + ("; seasonal pattern likely" if x.get("seasonal_likely") else "")})
        if key in dead_i:
            x = dead_i[key]
            scores["traffic_loss"] = max(scores["traffic_loss"], int(x["previous_clicks"]))
            signals.append({"type": "dead_page", "detail": f"{int(x['previous_clicks'])} clicks last period, 0 now"})
        if qw.get(key):
            scores["striking_distance"] = rnd(sum(i["striking_distance_score"] for i in qw[key]), 1)
            scores["striking_click_gain"] = sum(i["directional_click_gain_at_target"] for i in qw[key])
            signals.append({"type": "striking_distance", "detail": f"{len(qw[key])} query(ies) at positions 11-20"})
        if can.get(key):
            signals.append({"type": "cannibalization", "detail": "; ".join(f"'{c['query']}' ({c['overlap_type']})" for c in can[key][:3])})
        if key in dev_i:
            x = dev_i[key]
            scores["device_gap"] = x["ctr_ratio"]
            signals.append({"type": "device_gap", "detail": x["likely_issue"]})
        insp = insp_i.get(key)
        if insp:
            scores["index_risk"] = insp["index_risk_score"]
            if insp["index_risk_score"] >= 3:
                signals.append({"type": "index_risk", "detail": f"{insp['index_status']}: {insp['diagnosis']}"})
        if ptype == "product_in_collection":
            signals.append({"type": "shopify_url", "detail": "Collection-scoped product URL is earning impressions; the canonical should be /products/<handle>."})
        # action ladder
        decay = decay_i.get(key)
        if insp and insp["index_risk_score"] >= 4:
            action = "fix_indexing"
        elif key in dead_i:
            action = "restore_or_redirect"
        elif decay and decay.get("seasonal_likely"):
            action = "check_seasonality"
        elif decay and decay["diagnosis"] in ("ranking_drop", "ranking_and_ctr_drop", "traffic_loss", "demand_or_visibility_drop"):
            action = "refresh_content"
        elif (decay and decay["diagnosis"] == "ctr_drop") or key in ctr_i:
            action = "fix_snippet"
        elif any(c["overlap_type"] == "same_type_overlap" for c in can.get(key, [])):
            action = "review_cannibalization"
        elif qw.get(key):
            action = "push_to_page_one"
        elif key in dev_i:
            action = "fix_device_gap"
        else:
            action = "monitor"
        route, owner = owner_for(action, ptype)
        hv = is_high_value(path, ctx["high_value"])
        n_sig = len([s for s in signals if s["type"] != "shopify_url"])
        conf = brief_confidence(cm["impressions"], cm["clicks"], ctx["period_days"], ctx["cap_hit"], n_sig, ctx["source_type"])
        priority = (scores["ctr_upside"] + scores["traffic_loss"] + scores["striking_click_gain"]) * conf
        if hv:
            priority *= ctx["high_value_weight"]
        deps = []
        if key in queue_keys and not insp:
            deps.append("url_inspection_pending")
        if not ctx["raw"].get("previous_page"):
            deps.append("no_comparison_period")
        prev = prev_pages.get(key)
        yoy = yoy_pages.get(key)
        briefs.append({
            "url": page, "url_key": key, "path": path, "page_type": ptype, "high_value": hv,
            "metrics": {k: rnd(v, 4 if k == "ctr" else 2) for k, v in cm.items()},
            "previous_metrics": {k: rnd(v, 4 if k == "ctr" else 2) for k, v in prev.items()} if prev else None,
            "yoy_metrics": {k: rnd(v, 4 if k == "ctr" else 2) for k, v in yoy.items()} if yoy else None,
            "primary_queries": [{"query": r["query"], "position": r["position"], "clicks": r["clicks"], "impressions": r["impressions"]} for r in qrows[:5]],
            "query_count": len(qrows),
            "position_trend": ctx["position_trend"].get(key),
            "signals": signals, "scores": scores,
            "trend_label": "decay" if decay else ("dead" if key in dead_i else "stable_or_unknown"),
            "recommended_action": action, "action_summary": ACTION_INFO[action][2],
            "suggested_route": route, "suggested_owner": owner,
            "refresh_outcome_hint": REFRESH_OUTCOME_HINT.get(action) if ptype in ("blog_article", "page") else None,
            "register_match": ctx["register"].get(path),
            "inspection": insp,
            "proof_level": "confirmed" if (cm["impressions"] >= T["stable_min_impressions"] and ctx["source_type"] == "live") else "directional",
            "confidence": conf, "priority_score": rnd(priority, 1),
            "blocking_index_issue": bool(insp and insp["index_risk_score"] >= 4),
            "dependencies": deps,
        })
    briefs.sort(key=lambda b: (not b["blocking_index_issue"], -b["priority_score"], -b["metrics"]["impressions"]))
    return briefs


def build_inspection_queue(ctx, budget):
    queue, seen = [], set()

    def add(key, url, reason):
        if not key:
            return
        if key in seen:
            for q in queue:
                if q["url_key"] == key and reason not in q["reasons"]:
                    q["reasons"].append(reason)
            return
        seen.add(key)
        queue.append({"url": url, "url_key": key, "reasons": [reason]})

    for d in ctx["dead"][:T["dead_auto_inspect"]]:
        add(d["url_key"], d["page"], "dead_page")
    for d in [x for x in ctx["decay"] if x["diagnosis"] in ("ranking_drop", "ranking_and_ctr_drop") and is_high_value(x["path"], ctx["high_value"])][:3]:
        add(d["url_key"], d["page"], "decayed_high_value")
    zero = [r for r in ctx["raw"].get("current_page", []) if num(r.get("impressions")) >= T["zero_click_min_impressions"] and num(r.get("clicks")) == 0]
    zero.sort(key=lambda r: -num(r.get("impressions")))
    for r in zero[:3]:
        add(normalize_url(r.get("page"))[0], r.get("page"), "high_impressions_zero_clicks")
    sm_urls = {normalize_url(u)[0] for u in ctx["sitemap_urls"]}
    if sm_urls:
        missing = [r for r in ctx["raw"].get("current_page", []) if normalize_url(r.get("page"))[0] not in sm_urls and num(r.get("clicks")) > 0]
        missing.sort(key=lambda r: -num(r.get("clicks")))
        for r in missing[:3]:
            add(normalize_url(r.get("page"))[0], r.get("page"), "earning_traffic_not_in_sitemap")
    for r in ctx["raw"].get("current_page", []):
        if page_type(normalize_url(r.get("page"))[1]) == "product_in_collection" and num(r.get("impressions")) > 0:
            add(normalize_url(r.get("page"))[0], r.get("page"), "collection_scoped_product_url")
            break
    return queue[:budget]


def evidence_from(ctx, briefs):
    ev = []

    def add(claim, url, observed, expected, snippet=""):
        ev.append({"id": f"gsc-ev-{len(ev) + 1}", "claim": claim, "proof_type": "gsc_row",
                   "source_url": url, "snippet": snippet, "observed_value": observed, "expected_value": expected})

    for x in ctx["ctr"][:15]:
        add(f"{x['path']} gets fewer clicks than its average position predicts.", x["page"],
            f"CTR {x['actual_ctr']:.2%} at position {x['position']} on {int(x['impressions'])} impressions",
            f"about {x['expected_ctr']:.2%} ({ctx['curve']['mode_used']} curve)")
    for x in ctx["decay"][:15]:
        add(f"{x['path']} lost {int(x['click_loss'])} clicks versus the previous period.", x["page"],
            f"{int(x['current_clicks'])} clicks, position {x['current_position']}",
            f"{int(x['previous_clicks'])} clicks, position {x['previous_position']} last period")
    for x in ctx["dead"][:10]:
        add(f"{x['path']} went from traffic to zero clicks.", x["page"], "0 clicks this period",
            f"{int(x['previous_clicks'])} clicks last period")
    for i in ctx["inspections"]:
        ev.append({"id": f"gsc-ev-{len(ev) + 1}", "claim": f"URL Inspection: {i['index_status']}", "proof_type": "gsc_row",
                   "subtype": "url_inspection", "source_url": i["url"], "snippet": i["coverage_state"],
                   "observed_value": i["coverage_state"], "expected_value": "Submitted and indexed, canonical = declared"})
    return ev


def recommendations_from(ctx, briefs, max_url_recs=10):
    recs = []
    for b in briefs:
        if b["recommended_action"] == "monitor" or len(recs) >= max_url_recs:
            continue
        impact = 8 if b["priority_score"] >= 100 else 6 if b["priority_score"] >= 25 else 4
        if b["blocking_index_issue"]:
            impact = max(impact, 8)
        recs.append({
            "id": f"gsc-{len(recs) + 1}-{slugify(b['path'])[:40]}",
            "lane": LANE, "title": f"{b['action_summary']}: {b['path']}",
            "why_it_matters": "First-party Search Console rows show real clicks and impressions for this URL.",
            "evidence": [s["detail"] for s in b["signals"]][:5],
            "evidence_refs": [q["query"] for q in b["primary_queries"][:5]],
            "affected_urls": [b["url"]],
            "impact": impact, "confidence": int(round(b["confidence"] * 10)),
            "effort": {"fix_snippet": 2, "push_to_page_one": 4, "refresh_content": 6, "fix_indexing": 4,
                       "restore_or_redirect": 2, "review_cannibalization": 5, "fix_device_gap": 6,
                       "check_seasonality": 1}.get(b["recommended_action"], 3),
            "type": "quick_win" if b["recommended_action"] in ("fix_snippet", "restore_or_redirect") else "strategic",
            "cluster": "technical_health" if b["recommended_action"] in ("fix_indexing", "fix_device_gap") else "content_growth",
            "suggested_route": b["suggested_route"], "suggested_owner": b["suggested_owner"],
            "decision_status": "ready" if b["proof_level"] == "confirmed" and not b["dependencies"] else "validation_required",
            "proof_level": b["proof_level"], "report_visibility": "client",
            "directional_click_gain": b["scores"]["ctr_upside"] + b["scores"]["striking_click_gain"],
            "sizing_label": "GSC-based directional estimate" if ctx["status"] == "complete" else "GSC-gated directional estimate",
            "acceptance_criteria": [
                "Baseline GSC page/query metrics saved before the change (this run folder).",
                "Change mapped to the affected queries.",
                "Re-pulled after a settled window (at least 28 days, excluding the last 3 days) and compared.",
            ],
        })
    bn = ctx["brand_nonbrand"]
    if bn.get("health") in ("critical", "needs_growth"):
        recs.append({"id": "gsc-nonbrand-growth", "lane": LANE,
                     "title": f"Non-brand share is {bn['non_brand_ratio']:.0%} ({bn['health']}): grow non-brand coverage",
                     "why_it_matters": "Most organic clicks come from people who already know the store.",
                     "evidence": [f"brand clicks {int(bn['buckets']['brand']['clicks'])}, non-brand clicks {int(bn['buckets']['non_brand']['clicks'] + bn['buckets']['ambiguous_non_brand']['clicks'])}"],
                     "affected_urls": [], "impact": 7, "confidence": 7, "effort": 7, "type": "strategic",
                     "cluster": "content_growth", "suggested_route": "keyword-research", "suggested_owner": "seo",
                     "decision_status": "ready", "proof_level": "confirmed" if ctx["source_type"] == "live" else "directional",
                     "report_visibility": "client", "acceptance_criteria": ["Non-brand click share rises over two settled comparison windows."]})
    for s in ctx["sitemaps"]:
        if s["health"] == "issues":
            recs.append({"id": f"gsc-sitemap-{slugify(s['path'] or 'sitemap')[:30]}", "lane": LANE,
                         "title": f"Sitemap needs attention: {s['path']} ({', '.join(s['flags'])})",
                         "why_it_matters": "Sitemap errors slow discovery of new and changed URLs.",
                         "evidence": s["flags"], "affected_urls": [s["path"]], "impact": 4, "confidence": 8, "effort": 2,
                         "type": "quick_win", "cluster": "technical_health", "suggested_route": "seo-onpage-audit",
                         "suggested_owner": "theme-dev", "decision_status": "ready", "proof_level": "confirmed",
                         "report_visibility": "operator", "acceptance_criteria": ["Search Console shows the sitemap as Success with no errors."]})
    for g in ctx["segments"]["geo_opportunities"][:3]:
        recs.append({"id": f"gsc-geo-{slugify(g['country'])}", "lane": LANE,
                     "title": f"Country {g['country']}: {g['impression_share']:.0%} of impressions at below-average CTR",
                     "why_it_matters": "A large audience segment is seeing results but not clicking.",
                     "evidence": [f"CTR {g['ctr']:.2%}, impressions {int(g['impressions'])}"], "affected_urls": [],
                     "impact": 4, "confidence": 6, "effort": 4, "type": "research", "cluster": "content_growth",
                     "suggested_route": "gsc-audit", "suggested_owner": "seo", "decision_status": "validation_required",
                     "proof_level": "directional", "report_visibility": "operator",
                     "acceptance_criteria": ["Decide whether the store serves this market; if not, ignore."]})
    return recs


# ---------------------------------------------------------------------------
# lane results
# ---------------------------------------------------------------------------
def missing_gsc_result(reason, owner_type="own", property_url=""):
    if owner_type == "client":
        setup = {"title": "Ask the site owner for Search Console access (Restricted user is enough)",
                 "why": "This is not our property, so we cannot connect it ourselves. Keep all traffic figures directional until access is granted."}
    else:
        setup = {"title": "Connect Google Search Console (skills/gsc-audit/references/setup.md) and rerun the GSC lane",
                 "why": "Without first-party rows, traffic sizing, CTR upside and decay stay directional guesses."}
    return {
        "contract_version": CONTRACT_VERSION, "lane": LANE, "status": "not_run", "confidence": 0.0,
        "property": property_url, "summary": reason,
        "inputs_required": ["gsc_property", "current_page", "current_query_page", "previous_page", "daily"],
        "inputs_available": [], "source_type": "not_run",
        "client_summary": "Search Console was not connected, so no first-party traffic sizing is included.",
        "operator_notes": [reason], "blocking_limitations": ["No first-party click, impression, CTR or decay evidence."],
        "why_not_more": "GSC lane did not run: " + reason,
        "dependency_gates": [{"id": "missing-gsc", "status": "open",
                              "blocks": ["traffic_sizing", "ctr_upside", "decay_confidence"],
                              "reason": reason, "rerun_requirement": "Connect Google Search Console and rerun the GSC lane."}],
        "evidence": [], "evidence_conflicts": [],
        "recommendations": [{
            "id": "connect-gsc", "lane": LANE, "title": setup["title"], "why_it_matters": setup["why"],
            "evidence": [reason], "affected_urls": [], "impact": 8, "confidence": 9, "effort": 2, "type": "research",
            "cluster": "data_trust", "suggested_route": "gsc-audit", "suggested_owner": "seo",
            "decision_status": "validation_required", "proof_level": "not_tested", "client_priority": "setup",
            "report_visibility": "operator",
            "acceptance_criteria": ["Property lists in the gsc MCP server.", "Page and query/page rows pulled for the selected window."]}],
        "date_ranges": {}, "freshness": {}, "segments": {}, "page_query_map": [], "trend_summary": {},
        "ctr_curve": {}, "ctr_gaps": [], "decay_candidates": [], "dead_pages": [], "striking_distance": [],
        "cannibalization": [], "device_gaps": [], "brand_nonbrand": {}, "url_briefs": [],
        "inspections": [], "inspection_queue": [], "sitemaps": [], "data_limitations": [reason],
        "exploration_log": [{"surface": "gsc", "status": "not_available", "calls_used": 0, "rows_returned": 0,
                             "reason": reason, "why_not_more": "No property access."}],
        "visuals": {},
    }


def build_lane(run_dir, register_path=None, today=None, extra_daily=None):
    config, raw, metas, unknown = load_run(run_dir)
    today = today or dt.date.today()
    source_type = config.get("source_type", "live")
    prop = config.get("property", "")
    if config.get("status") == "not_run":
        return missing_gsc_result(config.get("missing_reason", "GSC not available."), config.get("owner_type", "own"), prop), config
    core_current = bool(raw.get("current_page") or raw.get("current_query_page"))
    if not core_current:
        return missing_gsc_result(config.get("missing_reason") or "No current-period page or query/page rows were pulled.",
                                  config.get("owner_type", "own"), prop), config
    brand = BrandMatcher(config.get("brand_terms", []), config.get("ambiguous_brand_terms", []), config.get("navigational_hints"))
    high_value = config.get("high_value_patterns", DEFAULT_HIGH_VALUE)
    periods = config.get("periods", {})
    period_days = int(config.get("period_days", 28))
    qp = raw.get("current_query_page", [])
    page_rows = raw.get("current_page") or aggregate(qp, "page")
    if not raw.get("current_page"):
        for r in page_rows:
            r["position"] = r.pop("avg_position", 0) or 0
    query_rows = raw.get("current_query") or aggregate(qp, "query")
    if not raw.get("current_query"):
        for r in query_rows:
            r["position"] = r.pop("avg_position", 0) or 0

    curve = build_ctr_curve(qp or query_rows, brand, config.get("ctr_curve_mode", "auto"))
    ctr = analyze_ctr(page_rows, curve["curve"], high_value)
    decay, dead = analyze_decay(page_rows, raw.get("previous_page", []), raw.get("yoy_page", []))
    quick_items, quick_grouped = analyze_quick_wins(qp, brand, curve["curve"])
    cannibal = analyze_cannibalization(qp, brand)
    device = analyze_device(raw.get("page_device", []))
    brand_nb = analyze_brand(query_rows, brand)
    segments = build_segments(raw)
    daily_rows = raw.get("daily", [])
    series = [(max([m.get("pulled_at", "") for m in metas.get("daily", [])] or [""]), daily_rows)]
    if extra_daily:
        series = extra_daily + series
    merged_daily = merge_daily(series)
    trend = trend_summary(merged_daily, today, period_days)
    inspections = [interpret_inspection(r) for r in raw.get("inspections", [])]
    sitemaps = sitemap_health(raw.get("sitemaps", []), today)
    sitemap_urls = [u if isinstance(u, str) else (u.get("url") or u.get("loc") or "") for u in raw.get("sitemap_urls", [])]

    # row caps
    cap_hit, limitations = False, []
    for kind, ms in metas.items():
        for m in ms:
            if m.get("row_cap_hit") or (m.get("rows_in_file") == API_ROW_CAP and not m.get("paginated_to_end")):
                cap_hit = True
                limitations.append(f"{kind}: a pull returned exactly {API_ROW_CAP} rows; more rows may exist (paginate with start_row).")
    limitations += [
        f"GSC data lags {DATA_LAG_DAYS - 1}-{DATA_LAG_DAYS} days; the last {DATA_LAG_DAYS} days are treated as provisional.",
        "Average position is an impression-weighted average, not a fixed rank.",
        "Anonymised queries are withheld, so query-level totals will not add up to page-level totals.",
    ]
    if unknown:
        limitations.append("Ignored raw files with unknown kind: " + ", ".join(unknown))
    missing = [k for k in ("current_page", "current_query_page", "previous_page", "daily", "page_device",
                           "page_country", "search_type_totals", "search_appearance", "sitemaps", "inspections")
               if not raw.get(k) and not (k == "page_country" and raw.get("country")) and not (k == "page_device" and raw.get("device"))]
    status = "complete" if raw.get("previous_page") and (raw.get("current_page") or qp) else "partial"
    gates = []
    blocks = []
    if not raw.get("previous_page"):
        blocks.append("decay_confidence")
    if not qp:
        blocks += ["ctr_upside"] if not raw.get("current_page") else []
        limitations.append("No query/page rows: page-query map, striking distance and cannibalization are empty.")
    if status != "complete":
        gates.append({"id": "missing-gsc", "status": "open", "blocks": sorted(set(blocks)) or ["decay_confidence"],
                      "reason": "GSC lane is partial: " + ", ".join(missing[:4]) + " missing.",
                      "rerun_requirement": "Pull the missing GSC windows and rerun the GSC lane."})

    ctx = {"raw": raw, "high_value": high_value, "high_value_weight": float(config.get("high_value_weight", 1.5)),
           "period_days": period_days, "cap_hit": cap_hit, "source_type": source_type,
           "page_query_map": page_query_map(qp, brand), "ctr": ctr, "decay": decay, "dead": dead,
           "quick_wins": quick_items, "cannibalization": cannibal, "device": device,
           "inspections": inspections, "register": load_register(register_path or config.get("register_path")),
           "position_trend": page_position_trend(raw.get("page_date", [])), "sitemap_urls": sitemap_urls,
           "brand_nonbrand": brand_nb, "sitemaps": sitemaps, "segments": segments, "curve": curve, "status": status}
    ctx["inspection_queue"] = build_inspection_queue(ctx, int(config.get("inspection_budget", T["inspection_budget"])))
    inspected = {i["url_key"] for i in inspections}
    pending_queue = [q for q in ctx["inspection_queue"] if q["url_key"] not in inspected]
    briefs = build_briefs(ctx)
    recs = recommendations_from(ctx, briefs)
    evidence = evidence_from(ctx, briefs)

    total_imp = sum(num(r.get("impressions")) for r in page_rows)
    confidence = {"live": 0.85, "manual": 0.70, "mixed": 0.75, "fixture": 0.55}.get(source_type, 0.7)
    if cap_hit:
        confidence -= 0.15
    if not raw.get("previous_page"):
        confidence -= 0.10
    if total_imp < 100:
        confidence = min(confidence, 0.40)
        limitations.append("Fewer than 100 impressions in the period: results are not meaningful.")
    why_parts = []
    if pending_queue:
        why_parts.append(f"{len(pending_queue)} queued URL inspection(s) not yet run")
    if missing:
        why_parts.append("not pulled: " + ", ".join(missing))
    why_not_more = ("; ".join(why_parts) + ".") if why_parts else "All planned GSC surfaces were pulled and analysed."

    exploration = []
    for kind in sorted(KNOWN_KINDS):
        ms = metas.get(kind, [])
        exploration.append({"surface": kind, "status": "complete" if ms else "not_available",
                            "calls_used": sum(int(m.get("pages_fetched", 1)) for m in ms),
                            "rows_returned": len(raw.get(kind, [])),
                            "reason": "" if ms else "not pulled in this run",
                            "why_not_more": "row cap hit" if any(m.get("row_cap_hit") for m in ms) else ""})

    handoff_diag = [{"url": b["url"], "target_query": b["primary_queries"][0]["query"] if b["primary_queries"] else None,
                     "position": b["metrics"]["position"], "action": b["recommended_action"],
                     "signals": [s["detail"] for s in b["signals"]], "confidence": b["confidence"]}
                    for b in briefs if b["suggested_route"] == "seo-page-diagnosis"][:25]
    handoff_refresh = [{"url": b["url"], "register_match": b["register_match"], "outcome_hint": b["refresh_outcome_hint"],
                        "action": b["recommended_action"], "signals": [s["detail"] for s in b["signals"]],
                        "primary_queries": b["primary_queries"], "baseline_metrics": b["metrics"],
                        "previous_metrics": b["previous_metrics"], "confidence": b["confidence"]}
                       for b in briefs if b["refresh_outcome_hint"] and b["recommended_action"] != "monitor"]

    lane = {
        "contract_version": CONTRACT_VERSION, "lane": LANE, "status": status,
        "confidence": round(max(confidence, 0.0), 2), "property": prop, "brand": config.get("brand"),
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "summary": (f"{len(briefs)} URL brief(s) from {len(qp)} query/page rows: {len(ctr)} CTR gap(s), "
                    f"{len(decay)} decaying, {len(dead)} dead, {len(quick_items)} striking-distance pair(s), "
                    f"{len(cannibal)} overlapping query(ies), {len(device)} device gap(s); non-brand share "
                    f"{brand_nb['non_brand_ratio']:.0%} ({brand_nb['health']})."),
        "inputs_required": ["gsc_property", "current_page", "current_query_page", "previous_page", "daily"],
        "inputs_available": sorted(k for k in raw if raw.get(k)),
        "source_type": source_type,
        "client_summary": "Search Console provides first-party clicks and impressions for page and query decisions.",
        "operator_notes": config.get("notes", []),
        "blocking_limitations": [g["reason"] for g in gates],
        "why_not_more": why_not_more,
        "dependency_gates": gates, "evidence_conflicts": [],
        "date_ranges": periods, "freshness": {
            "latest_available_date": trend.get("latest_date"), "settled_end": trend.get("settled_end"),
            "lag_days": (today - parse_date(trend["latest_date"])).days if trend.get("latest_date") else None,
            "provisional_dates_excluded": trend.get("provisional_dates_excluded", [])},
        "segments": segments, "page_query_map": ctx["page_query_map"], "trend_summary": trend,
        "ctr_curve": curve, "ctr_gaps": ctr, "decay_candidates": decay, "dead_pages": dead,
        "striking_distance": quick_items, "striking_distance_by_page": quick_grouped,
        "cannibalization": cannibal, "device_gaps": device, "brand_nonbrand": brand_nb,
        "url_briefs": briefs, "inspections": inspections, "inspection_queue": pending_queue,
        "sitemaps": sitemaps, "data_limitations": limitations, "evidence": evidence,
        "recommendations": recs, "exploration_log": exploration,
        "handoffs": {"seo_page_diagnosis": handoff_diag, "seo_content_refresh": handoff_refresh},
        "visuals": {"trend_monthly": trend.get("monthly", []), "top_urls": [b["url"] for b in briefs[:10]],
                    "device_split": segments["devices"], "search_types": segments["search_types"],
                    "country_table": segments["countries"][:15], "search_appearances": segments["search_appearances"]},
    }
    return lane, config


# ---------------------------------------------------------------------------
# outputs
# ---------------------------------------------------------------------------
def write_briefs_md(lane, path):
    lines = [f"# GSC URL briefs: {lane.get('property', '')}", "",
             f"Status: {lane['status']} | confidence {lane['confidence']} | curve: {lane['ctr_curve'].get('mode_used')}", "",
             lane["summary"], ""]
    for b in lane["url_briefs"]:
        if b["recommended_action"] == "monitor":
            continue
        m = b["metrics"]
        lines.append(f"## {b['path']}  ({b['page_type']}{', high value' if b['high_value'] else ''})")
        lines.append(f"- Action: **{b['recommended_action']}**: {b['action_summary']} -> {b['suggested_route']} / owner {b['suggested_owner']}")
        lines.append(f"- Now: {int(m['clicks'])} clicks, {int(m['impressions'])} impressions, CTR {m['ctr']:.2%}, avg position {m['position']}")
        if b["previous_metrics"]:
            p = b["previous_metrics"]
            lines.append(f"- Previous: {int(p['clicks'])} clicks, avg position {p['position']}")
        if b["primary_queries"]:
            lines.append("- Queries: " + "; ".join(f"{q['query']} (pos {q['position']})" for q in b["primary_queries"]))
        for s in b["signals"]:
            lines.append(f"- Signal [{s['type']}]: {s['detail']}")
        if b["register_match"]:
            r = b["register_match"]
            lines.append(f"- Register: article #{r['article_number']} '{r['primary_keyword']}', Shopify Article ID {r['shopify_article_id']}")
        if b["dependencies"]:
            lines.append("- Waiting on: " + ", ".join(b["dependencies"]))
        lines.append(f"- Proof: {b['proof_level']}, confidence {b['confidence']}, priority {b['priority_score']}")
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def archive_run(run_dir, archive_root, today=None):
    run_dir, archive_root = Path(run_dir), Path(archive_root)
    config = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
    prop = slugify(config.get("property", "property").replace("sc-domain:", "domain-"))
    pulled = (today or dt.date.today()).isoformat()
    copied = skipped = 0
    for f in sorted((run_dir / "raw").glob("*.json")):
        payload = json.loads(f.read_text(encoding="utf-8"))
        meta = payload.get("meta", {}) if isinstance(payload, dict) else {}
        kind = f.stem.split("__")[0]
        start, end = meta.get("start_date", "nostart"), meta.get("end_date", "noend")
        stype = meta.get("search_type", "web")
        suffix = f.stem.split("__", 1)[1] if "__" in f.stem else ""
        dest_dir = archive_root / prop / kind
        dest_dir.mkdir(parents=True, exist_ok=True)
        name = f"{start}_{end}__{stype}__pulled-{meta.get('pulled_at', pulled)[:10]}" + (f"__{suffix}" if suffix else "")
        digest = hashlib.sha256(f.read_bytes()).hexdigest()
        existing = [p for p in dest_dir.glob(name + "*.json")]
        if any(hashlib.sha256(p.read_bytes()).hexdigest() == digest for p in existing):
            skipped += 1
            continue
        dest = dest_dir / (name + (f"__v{len(existing) + 1}" if existing else "") + ".json")
        shutil.copyfile(f, dest)
        copied += 1
    return {"archive": str(archive_root / prop), "copied": copied, "skipped_identical": skipped}


def history_series(archive_root, prop):
    base = Path(archive_root) / slugify(prop.replace("sc-domain:", "domain-")) / "daily"
    series = []
    if base.exists():
        for f in sorted(base.glob("*.json")):
            payload = json.loads(f.read_text(encoding="utf-8"))
            meta, rows = rows_from_payload(payload)
            m = re.search(r"pulled-(\d{4}-\d{2}-\d{2})", f.name)
            series.append((meta.get("pulled_at") or (m.group(1) if m else ""), rows))
    return series


def recommended_periods(today, days=28):
    end = today - dt.timedelta(days=DATA_LAG_DAYS)
    cur_start = end - dt.timedelta(days=days - 1)
    prev_end = cur_start - dt.timedelta(days=1)
    prev_start = prev_end - dt.timedelta(days=days - 1)
    yoy_end = end - dt.timedelta(days=364)
    yoy_start = yoy_end - dt.timedelta(days=days - 1)
    hist_start = end - dt.timedelta(days=486)  # ~16 months
    return {"current": {"start": cur_start.isoformat(), "end": end.isoformat()},
            "previous": {"start": prev_start.isoformat(), "end": prev_end.isoformat()},
            "yoy": {"start": yoy_start.isoformat(), "end": yoy_end.isoformat()},
            "sixteen_months": {"start": hist_start.isoformat(), "end": end.isoformat()},
            "note": f"End date is today minus {DATA_LAG_DAYS} days so provisional data is excluded; YoY is shifted 364 days to keep weekdays aligned."}


def cmd_analyze(args):
    run_dir = Path(args.run_dir)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    archive_root = Path(args.archive_root) if args.archive_root else run_dir.parent / "_archive"
    archived = None
    if not args.no_archive and (run_dir / "raw").exists():
        archived = archive_run(run_dir, archive_root, today)
    config = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
    extra = history_series(archive_root, config.get("property", "")) if not args.no_archive else None
    lane, config = build_lane(run_dir, args.register, today, extra)
    if archived:
        lane.setdefault("operator_notes", []).append(f"Archived raw pulls: {archived['copied']} new, {archived['skipped_identical']} already archived ({archived['archive']}).")
    (run_dir / "gsc-lane.json").write_text(json.dumps(lane, indent=2, ensure_ascii=False), encoding="utf-8")
    if lane["status"] != "not_run":
        write_briefs_md(lane, run_dir / "url-briefs.md")
        (run_dir / "inspection-queue.json").write_text(json.dumps(lane["inspection_queue"], indent=2, ensure_ascii=False), encoding="utf-8")
        hd = run_dir / "handoff"
        hd.mkdir(exist_ok=True)
        (hd / "page-diagnosis-queue.json").write_text(json.dumps(lane["handoffs"]["seo_page_diagnosis"], indent=2, ensure_ascii=False), encoding="utf-8")
        (hd / "refresh-candidates.json").write_text(json.dumps(lane["handoffs"]["seo_content_refresh"], indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[{lane['status']}] confidence {lane['confidence']}: {lane['summary']}")
    if lane.get("inspection_queue"):
        print(f"Inspection queue: {len(lane['inspection_queue'])} URL(s) -> inspection-queue.json")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="gsc-audit analysis engine (stdlib).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze", help="analyse a run folder")
    a.add_argument("--run-dir", required=True)
    a.add_argument("--register", help="KEYWORD-REGISTER.csv to join URL briefs to articles")
    a.add_argument("--archive-root", help="history archive root (default: <run-dir>/../_archive)")
    a.add_argument("--no-archive", action="store_true")
    a.add_argument("--today", help="YYYY-MM-DD override (tests)")
    r = sub.add_parser("archive", help="archive a run folder's raw pulls")
    r.add_argument("--run-dir", required=True)
    r.add_argument("--archive-root")
    h = sub.add_parser("history", help="merged daily history from the archive")
    h.add_argument("--archive-root", required=True)
    h.add_argument("--property", required=True)
    h.add_argument("--out")
    p = sub.add_parser("periods", help="recommended date windows")
    p.add_argument("--today")
    p.add_argument("--days", type=int, default=28)
    n = sub.add_parser("not-run", help="write the missing-GSC lane result")
    n.add_argument("--reason", required=True)
    n.add_argument("--out", required=True)
    n.add_argument("--owner-type", choices=["own", "client"], default="own")
    n.add_argument("--property", default="")
    args = ap.parse_args(argv)

    if args.cmd == "analyze":
        return cmd_analyze(args)
    if args.cmd == "archive":
        root = args.archive_root or str(Path(args.run_dir).parent / "_archive")
        print(json.dumps(archive_run(args.run_dir, root), indent=2))
        return 0
    if args.cmd == "history":
        merged = merge_daily(history_series(args.archive_root, args.property))
        out = {"property": args.property, "days": len(merged),
               "first_date": merged[0]["date"] if merged else None,
               "last_date": merged[-1]["date"] if merged else None, "rows": merged}
        text = json.dumps(out, indent=2)
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
            print(f"{len(merged)} day(s) -> {args.out}")
        else:
            print(text)
        return 0
    if args.cmd == "periods":
        today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
        print(json.dumps(recommended_periods(today, args.days), indent=2))
        return 0
    if args.cmd == "not-run":
        Path(args.out).write_text(json.dumps(missing_gsc_result(args.reason, args.owner_type, args.property), indent=2), encoding="utf-8")
        print(f"not_run lane result -> {args.out}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
