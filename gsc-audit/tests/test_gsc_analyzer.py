"""Synthetic-fixture tests for gsc_analyzer.py (stdlib unittest).

Run from anywhere:
    python "skills/gsc-audit/tests/test_gsc_analyzer.py"

All data below is invented for the test. It is written to a temporary
folder and deleted afterwards; nothing is left in the repo.
"""

import datetime as dt
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import gsc_analyzer as ga  # noqa: E402

SITE = "https://example-outdoor.com"
TODAY = dt.date(2026, 9, 27)


def u(path):
    return SITE + path


def write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=1), encoding="utf-8")


def daily_rows(start, end, base_clicks=100):
    rows, d = [], start
    while d <= end:
        season = 1.6 if d.month in (4, 5, 6) else 0.8 if d.month in (11, 12, 1) else 1.0
        clicks = round(base_clicks * season)
        rows.append({"keys": [d.isoformat()], "clicks": clicks, "impressions": clicks * 25, "ctr": 0.04, "position": 12.0})
        d += dt.timedelta(days=1)
    return rows


def build_fixture(root, calibrate=False):
    run = root / "example-outdoor" / "gsc-runs" / "2026-09-27-example-outdoor"
    per = ga.recommended_periods(TODAY)
    write(run / "config.json", {
        "property": "sc-domain:example-outdoor.com", "brand": "example-outdoor", "owner_type": "own",
        "source_type": "fixture", "period_days": 28, "periods": per,
        "brand_terms": ["example outdoor", "example-outdoor"], "ambiguous_brand_terms": ["example outdoor"],
        "high_value_patterns": ["/products/", "/collections/", "/cart"], "ctr_curve_mode": "auto",
    })
    meta = lambda dims, p="current", **kw: {"meta": {"dimensions": dims, "start_date": per[p]["start"],  # noqa: E731
                                                     "end_date": per[p]["end"], "search_type": "web",
                                                     "pulled_at": "2026-09-27", **kw}}
    cur = [
        ([u("/products/cedar-gazebo")], 40, 2000, 3.0),          # CTR gap
        ([u("/blogs/fire-pit/patio-fire-pit-on-concrete")], 30, 750, 8.0),  # decay rank drop
        ([u("/collections/sheds")], 150, 3000, 6.0),              # healthy
        ([u("/products/playset-x")], 0, 600, 14.0),               # zero-click suspect
        ([u("/")], 1500, 5000, 1.2),                              # home
        ([u("/blogs/fire-pit/using-a-fire-pit-in-cold-weather")], 20, 900, 7.0),  # seasonal decay
    ]
    prev = [
        ([u("/products/cedar-gazebo")], 45, 2100, 3.1),
        ([u("/blogs/fire-pit/patio-fire-pit-on-concrete")], 80, 1600, 5.0),
        ([u("/collections/sheds")], 140, 2900, 6.2),
        ([u("/pages/old-sale")], 25, 700, 4.0),                   # dead page
        ([u("/")], 1450, 4900, 1.2),
        ([u("/blogs/fire-pit/using-a-fire-pit-in-cold-weather")], 40, 1000, 6.8),
    ]
    rows = lambda data: [{"keys": k, "clicks": c, "impressions": i, "ctr": c / i if i else 0, "position": p} for k, c, i, p in data]  # noqa: E731
    write(run / "raw" / "current_page.json", {**meta(["page"]), "rows": rows(cur)})
    write(run / "raw" / "previous_page.json", {**meta(["page"], "previous"), "rows": rows(prev)})
    write(run / "raw" / "yoy_page.json", {**meta(["page"], "yoy"), "rows": rows([([u("/blogs/fire-pit/using-a-fire-pit-in-cold-weather")], 21, 950, 7.0)])})
    qp = [
        (["example outdoor", u("/")], 900, 2000, 1.0),                       # brand (exact)
        (["example-outdoor reviews", u("/")], 100, 300, 1.1),                   # brand
        (["example outdoor ideas", u("/blogs/fire-pit/using-a-fire-pit-in-cold-weather")], 10, 400, 9.0),  # ambiguous -> non-brand
        (["cedar gazebo", u("/products/cedar-gazebo")], 30, 1500, 3.0),
        (["cedar gazebo", u("/collections/gazebos")], 5, 400, 9.0),         # shop hierarchy overlap
        (["fire pit on concrete", u("/blogs/fire-pit/patio-fire-pit-on-concrete")], 20, 800, 8.0),
        (["fire pit on concrete", u("/blogs/fire-pit/heat-shield-mats-for-patios")], 3, 300, 14.0),  # same-type overlap
        (["wooden playset with slide", u("/products/playset-x")], 0, 350, 13.0),        # striking distance
        (["storage shed 10x12", u("/collections/sheds")], 60, 1200, 6.0),
    ]
    if calibrate:
        for pos in range(1, 8):
            for n in range(35):
                qp.append(([f"generic query {pos}-{n}", u(f"/blogs/news/post-{pos}-{n}")], 2, 40, float(pos)))
    write(run / "raw" / "current_query_page.json", {**meta(["query", "page"]), "rows": rows(qp)})
    daily = daily_rows(dt.date(2025, 5, 20), dt.date(2026, 9, 26))
    write(run / "raw" / "daily.json", {**meta(["date"], "sixteen_months"), "rows": daily})
    write(run / "raw" / "page_device.json", {**meta(["page", "device"]), "rows": rows([
        ([u("/products/cedar-gazebo"), "MOBILE"], 12, 1200, 3.5),
        ([u("/products/cedar-gazebo"), "DESKTOP"], 28, 800, 2.8),
        ([u("/collections/sheds"), "MOBILE"], 80, 1600, 6.0),
        ([u("/collections/sheds"), "DESKTOP"], 70, 1400, 6.1),
    ])})
    write(run / "raw" / "page_country.json", {**meta(["page", "country"]), "rows": rows([
        ([u("/collections/sheds"), "usa"], 140, 2500, 6.0),
        ([u("/collections/sheds"), "can"], 2, 500, 7.0),
    ])})
    write(run / "raw" / "search_type_totals.json", {"meta": {"pulled_at": "2026-09-27"}, "rows": [
        {"search_type": "web", "clicks": 1740, "impressions": 13000, "position": 5.0},
        {"search_type": "image", "clicks": 30, "impressions": 9000, "position": 20.0},
    ]})
    write(run / "raw" / "search_appearance.json", {**meta(["searchAppearance"]), "rows": [
        {"keys": ["PRODUCT_SNIPPETS"], "clicks": 300, "impressions": 8000, "position": 6.0},
        {"keys": ["FAQ_RICH_RESULT"], "clicks": 1, "impressions": 50, "position": 4.0},
    ]})
    write(run / "raw" / "sitemaps.json", {"rows": [
        {"path": u("/sitemap.xml"), "lastSubmitted": "2026-01-01", "lastDownloaded": "2026-07-01", "isPending": False,
         "errors": 2, "warnings": 0, "contents": [{"type": "web", "submitted": 1200}]},
    ]})
    write(run / "raw" / "inspections.json", {"rows": [
        {"url": u("/pages/old-sale"), "verdict": "NEUTRAL", "coverageState": "URL is unknown to Google"},
    ]})
    reg = root / "KEYWORD-REGISTER.csv"
    reg.write_text("Article #,Pillar,Article Title,Primary Keyword,URL Slug,Complete URL Slug,Shopify Article ID\n"
                   "1,Fire Pit,Setting Up a Patio Fire Pit on Concrete,patio fire pit on concrete,x,"
                   + u("/blogs/fire-pit/patio-fire-pit-on-concrete") + ",100000000003\n",
                   encoding="utf-8")
    return run, reg


class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="gsc test "))  # space on purpose

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_analyze(self, calibrate=False):
        run, reg = build_fixture(self.tmp, calibrate)
        rc = ga.main(["analyze", "--run-dir", str(run), "--register", str(reg), "--today", TODAY.isoformat()])
        self.assertEqual(rc, 0)
        return run, json.loads((run / "gsc-lane.json").read_text(encoding="utf-8"))

    def test_lane_contract_and_analyses(self):
        run, lane = self.run_analyze()
        for key in ("lane", "status", "confidence", "summary", "evidence", "recommendations", "why_not_more",
                    "inputs_required", "inputs_available", "source_type", "client_summary", "operator_notes",
                    "blocking_limitations", "visuals", "dependency_gates", "url_briefs", "page_query_map"):
            self.assertIn(key, lane)
        self.assertEqual(lane["lane"], "gsc")
        self.assertEqual(lane["status"], "complete")
        self.assertLessEqual(lane["confidence"], 0.55)  # fixture cap
        ctr_paths = {x["path"] for x in lane["ctr_gaps"]}
        self.assertIn("/products/cedar-gazebo", ctr_paths)
        self.assertNotIn("/collections/sheds", ctr_paths)
        decay = {x["path"]: x for x in lane["decay_candidates"]}
        self.assertEqual(decay["/blogs/fire-pit/patio-fire-pit-on-concrete"]["diagnosis"], "ranking_drop")
        self.assertTrue(decay["/blogs/fire-pit/using-a-fire-pit-in-cold-weather"]["seasonal_likely"])
        self.assertEqual([d["path"] for d in lane["dead_pages"]], ["/pages/old-sale"])
        sd = {(x["query"], x["path"]) for x in lane["striking_distance"]}
        self.assertIn(("wooden playset with slide", "/products/playset-x"), sd)
        can = {g["query"]: g["overlap_type"] for g in lane["cannibalization"]}
        self.assertEqual(can["cedar gazebo"], "shop_hierarchy")
        self.assertEqual(can["fire pit on concrete"], "same_type_overlap")
        self.assertNotIn("example outdoor", can)
        self.assertEqual(len(lane["device_gaps"]), 1)
        bn = lane["brand_nonbrand"]
        self.assertEqual(bn["buckets"]["brand"]["queries"], 2)
        self.assertEqual(bn["buckets"]["ambiguous_non_brand"]["queries"], 1)
        self.assertEqual(lane["ctr_curve"]["mode_used"], "default")
        self.assertTrue(lane["segments"]["geo_opportunities"])
        self.assertEqual(lane["sitemaps"][0]["health"], "issues")
        faq = [a for a in lane["segments"]["search_appearances"] if "FAQ" in a["search_appearance"]]
        self.assertIn("note", faq[0])

    def test_briefs_handoffs_and_queue(self):
        run, lane = self.run_analyze()
        briefs = {b["path"]: b for b in lane["url_briefs"]}
        self.assertEqual(len(briefs), len(lane["url_briefs"]), "one brief per URL")
        self.assertEqual(briefs["/pages/old-sale"]["recommended_action"], "fix_indexing")
        self.assertTrue(lane["url_briefs"][0]["blocking_index_issue"])
        fp = briefs["/blogs/fire-pit/patio-fire-pit-on-concrete"]
        self.assertEqual(fp["recommended_action"], "refresh_content")
        self.assertEqual(fp["register_match"]["shopify_article_id"], "100000000003")
        self.assertEqual(fp["refresh_outcome_hint"], "substantive_refresh")
        self.assertEqual(briefs["/products/cedar-gazebo"]["recommended_action"], "fix_snippet")
        self.assertEqual(briefs["/products/cedar-gazebo"]["suggested_owner"], "catalog")
        self.assertEqual(briefs["/blogs/fire-pit/using-a-fire-pit-in-cold-weather"]["recommended_action"], "check_seasonality")
        queue = {q["url_key"].split("/", 1)[-1] for q in lane["inspection_queue"]}
        self.assertIn("products/playset-x", queue)  # zero-click suspect still pending
        refresh = json.loads((run / "handoff" / "refresh-candidates.json").read_text(encoding="utf-8"))
        self.assertTrue(any(r["register_match"] for r in refresh))
        self.assertTrue((run / "url-briefs.md").exists())
        self.assertTrue(lane["recommendations"])
        for rec in lane["recommendations"]:
            for f in ("id", "lane", "title", "impact", "confidence", "effort", "suggested_route", "proof_level", "acceptance_criteria"):
                self.assertIn(f, rec)

    def test_trend_and_history_archive(self):
        run, lane = self.run_analyze()
        tr = lane["trend_summary"]
        self.assertEqual(tr["settled_end"], "2026-09-24")
        self.assertTrue(tr["provisional_dates_excluded"])
        self.assertIsNotNone(tr["change_yoy"])
        self.assertIsNotNone(tr["seasonality"])
        # an older pull, archived earlier, extends history past 16 months
        old = run.parent / "_archive" / "domain-example-outdoor-com" / "daily"
        write(old / "2024-01-01_2025-05-19__web__pulled-2025-05-20.json",
              {"meta": {"dimensions": ["date"], "pulled_at": "2025-05-20"},
               "rows": daily_rows(dt.date(2024, 1, 1), dt.date(2025, 5, 19))})
        ga.main(["analyze", "--run-dir", str(run), "--today", TODAY.isoformat()])
        lane2 = json.loads((run / "gsc-lane.json").read_text(encoding="utf-8"))
        self.assertTrue(lane2["trend_summary"]["beyond_16_months"])
        self.assertTrue(any("0 new" in n for n in lane2["operator_notes"]), "second run must not duplicate archive files")

    def test_calibrated_curve(self):
        _, lane = self.run_analyze(calibrate=True)
        self.assertEqual(lane["ctr_curve"]["mode_used"], "calibrated_own_gsc")
        curve = {int(k): v for k, v in lane["ctr_curve"]["curve"].items()}
        self.assertTrue(all(curve[p] <= curve[p - 1] for p in range(2, 21)), "curve must be non-increasing")

    def test_not_run_gate(self):
        out = self.tmp / "gsc-lane.json"
        self.assertEqual(ga.main(["not-run", "--reason", "gsc MCP not connected", "--out", str(out), "--owner-type", "client"]), 0)
        lane = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(lane["status"], "not_run")
        gate = lane["dependency_gates"][0]
        self.assertEqual(gate["id"], "missing-gsc")
        self.assertEqual(set(gate["blocks"]), {"traffic_sizing", "ctr_upside", "decay_confidence"})
        self.assertFalse(lane["ctr_gaps"] or lane["decay_candidates"] or lane["url_briefs"])
        self.assertIn("site owner", lane["recommendations"][0]["title"])

    def test_partial_without_comparison(self):
        run, reg = build_fixture(self.tmp)
        (run / "raw" / "previous_page.json").unlink()
        ga.main(["analyze", "--run-dir", str(run), "--today", TODAY.isoformat(), "--no-archive"])
        lane = json.loads((run / "gsc-lane.json").read_text(encoding="utf-8"))
        self.assertEqual(lane["status"], "partial")
        self.assertIn("decay_confidence", lane["dependency_gates"][0]["blocks"])
        self.assertFalse(lane["decay_candidates"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
