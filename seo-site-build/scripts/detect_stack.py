#!/usr/bin/env python
"""detect_stack.py - Stage 0 project detection for seo-site-build (stdlib only).

Finds the site root (cwd or one level down), then reports what an agent must know before
building or editing: framework + version, package manager and its commands, Astro config facts
(site, trailingSlash, build.format, i18n, integrations), content-config location and how each
collection schema treats unknown keys, SEO/schema packages, headless-CMS integrations, draft
flags in content files, and the Node engines floor.

The config parsing is heuristic (regex over the source, no JS execution). Every value it prints
comes with the file it came from; confirm by reading that file before relying on it.

Usage:
  python detect_stack.py [project-path] [--json out.json]
Exit code: 0 when a site root is found, 2 when none is found.
"""

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKIP_DIRS = {"node_modules", ".git", "dist", ".astro", ".next", "out", ".wrangler", ".vercel"}

LOCKFILES = [
    ("pnpm-lock.yaml", "pnpm", "pnpm install", "pnpm run build", "pnpm run dev"),
    ("yarn.lock", "yarn", "yarn install", "yarn build", "yarn dev"),
    ("package-lock.json", "npm", "npm install", "npm run build", "npm run dev"),
    ("bun.lock", "bun", "bun install", "bun run build", "bun run dev"),
    ("bun.lockb", "bun", "bun install", "bun run build", "bun run dev"),
]

CMS_PACKAGES = {
    "@astrojs/storyblok": "Storyblok",
    "@storyblok/astro": "Storyblok",
    "@astrojs/contentful": "Contentful",
    "contentful": "Contentful",
    "astro-sanity": "Sanity",
    "@sanity/astro": "Sanity",
    "@sanity/client": "Sanity",
    "astro-wordpress": "WordPress",
    "wp-astrojs-integration": "WordPress",
    "@wordpress/api-fetch": "WordPress",
    "@directus/sdk": "Directus",
    "@prismicio/client": "Prismic",
    "@tinacms/cli": "TinaCMS (git-backed; files stay local)",
    "decap-cms-app": "Decap CMS (git-backed; files stay local)",
}

SEO_PACKAGES = ["astro-seo", "astro-seo-schema", "schema-dts", "@astrojs/sitemap", "@astrojs/mdx",
                "next-seo", "next-sitemap", "@astrojs/react", "@astrojs/cloudflare", "zod"]

DRAFT_PATTERNS = [
    re.compile(r"^draft:\s*true\s*$", re.M | re.I),
    re.compile(r"^status:\s*['\"]?(draft|paused)['\"]?\s*$", re.M | re.I),
    re.compile(r"^published:\s*false\s*$", re.M | re.I),
    re.compile(r"^active:\s*false\s*$", re.M | re.I),
]


def find_root(start: Path):
    """Return (root, framework) looking in start, then one level down."""
    def classify(d: Path):
        for name in ("astro.config.mjs", "astro.config.ts", "astro.config.mts", "astro.config.js"):
            if (d / name).is_file():
                return "astro", d / name
        for name in ("next.config.ts", "next.config.mjs", "next.config.js"):
            if (d / name).is_file():
                return "next", d / name
        if (d / "layout" / "theme.liquid").is_file():
            return "shopify-theme", d / "layout" / "theme.liquid"
        return None, None

    fw, cfg = classify(start)
    if fw:
        return start, fw, cfg
    for child in sorted(p for p in start.iterdir() if p.is_dir() and p.name not in SKIP_DIRS):
        fw, cfg = classify(child)
        if fw:
            return child, fw, cfg
    return None, None, None


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def strip_js_comments(src: str) -> str:
    """Remove // and /* */ comments while leaving string literals intact
    (a glob such as '**/*.{md,mdx}' must not be mistaken for a comment)."""
    out, i, n = [], 0, len(src)
    quote = None
    while i < n:
        ch = src[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(src[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "'\"`":
            quote = ch
            out.append(ch)
            i += 1
            continue
        if src.startswith("/*", i):
            end = src.find("*/", i + 2)
            i = n if end == -1 else end + 2
            continue
        if src.startswith("//", i):
            end = src.find("\n", i)
            i = n if end == -1 else end
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def astro_config_facts(cfg_path: Path) -> dict:
    raw = read(cfg_path)
    src = strip_js_comments(raw)
    facts = {"file": str(cfg_path)}
    m = re.search(r"\bsite\s*:\s*(['\"`])(.*?)\1", src)
    if m:
        facts["site"] = m.group(2)
    else:
        m = re.search(r"\bsite\s*:\s*([A-Za-z_$][\w$]*)", src)
        if m:
            var = m.group(1)
            m2 = re.search(r"(?:const|let|var)\s+" + re.escape(var) + r"\s*=\s*(['\"`])(.*?)\1", src)
            facts["site"] = m2.group(2) if m2 else f"<variable {var}>"
            if re.search(re.escape(var) + r"\s*=\s*process\.env|import\.meta\.env", src):
                facts["site_from_env"] = True
    if "site" in facts and re.search(r"localhost|127\.0\.0\.1", facts["site"]):
        facts["site_warning"] = "site points at localhost; ask the user for the live URL"
    if "site" not in facts:
        facts["site_warning"] = "no site set; canonicals and sitemap cannot be absolute. Ask for the live URL"
    m = re.search(r"trailingSlash\s*:\s*['\"](always|never|ignore)['\"]", src)
    facts["trailingSlash"] = m.group(1) if m else "ignore (default)"
    m = re.search(r"format\s*:\s*['\"](file|directory|preserve)['\"]", src)
    facts["build_format"] = m.group(1) if m else "directory (default)"
    m = re.search(r"output\s*:\s*['\"](static|server|hybrid)['\"]", src)
    facts["output"] = m.group(1) if m else "static (default)"
    facts["adapter"] = bool(re.search(r"\badapter\s*:", src))
    m = re.search(r"compressHTML\s*:\s*(true|false)", src)
    facts["compressHTML"] = m.group(1) if m else "default"
    i18n = re.search(r"i18n\s*:\s*\{(.*?)\}\s*,\s*\n", src, re.S)
    if i18n:
        block = i18n.group(1)
        dl = re.search(r"defaultLocale\s*:\s*['\"]([^'\"]+)['\"]", block)
        locs = re.search(r"locales\s*:\s*\[([^\]]*)\]", block)
        pdl = re.search(r"prefixDefaultLocale\s*:\s*(true|false)", block)
        facts["i18n"] = {
            "defaultLocale": dl.group(1) if dl else None,
            "locales": re.findall(r"['\"]([^'\"]+)['\"]", locs.group(1)) if locs else [],
            "prefixDefaultLocale": pdl.group(1) if pdl else "false (default)",
        }
    facts["integrations_mentioned"] = sorted(set(re.findall(r"\b(sitemap|mdx|react|vue|svelte|tailwind|partytown|cloudflare)\s*\(", src)))
    facts["build_hooks"] = re.findall(r"['\"](astro:[a-z:]+)['\"]", src)
    # Consistency warnings.
    warn = []
    if facts["trailingSlash"] == "never" and facts["build_format"].startswith("directory"):
        warn.append("trailingSlash 'never' with directory output: hosts such as Cloudflare Pages "
                    "redirect /x to /x/, contradicting slashless canonicals. Use build.format 'file'.")
    if facts["trailingSlash"] == "always" and facts["build_format"] == "file":
        warn.append("trailingSlash 'always' with build.format 'file': emitted x.html files are served at /x, not /x/.")
    if facts["trailingSlash"].startswith("ignore"):
        warn.append("trailingSlash 'ignore': both URL forms resolve; pick 'always' or 'never' and match links to it.")
    if facts.get("site_from_env"):
        warn.append("site comes from an env var: hard-code the canonical host instead.")
    facts["warnings"] = warn
    return facts


def content_config(root: Path) -> dict:
    out = {"found": None, "collections": {}}
    for rel, era in (("src/content.config.ts", "Astro 5+ content layer"),
                     ("src/content.config.mjs", "Astro 5+ content layer"),
                     ("src/content.config.js", "Astro 5+ content layer"),
                     ("src/content/config.ts", "Astro 4 style (legacy location)"),
                     ("src/content/config.mjs", "Astro 4 style (legacy location)"),
                     ("src/content/config.js", "Astro 4 style (legacy location)")):
        p = root / rel
        if p.is_file():
            out["found"] = str(p)
            out["era"] = era
            src = strip_js_comments(read(p))
            m = re.search(r"import\s*\{[^}]*\bz\b[^}]*\}\s*from\s*['\"]([^'\"]+)['\"]", src)
            out["zod_import"] = m.group(1) if m else None
            if out["zod_import"] == "astro:content":
                out["zod_note"] = "z imported from astro:content (older style; newer Astro uses astro/zod or zod)"
            out["uses_type_content"] = bool(re.search(r"type\s*:\s*['\"](content|data)['\"]", src))
            for cm in re.finditer(r"(?:const|let)\s+(\w+)\s*=\s*defineCollection\s*\(", src):
                name = cm.group(1)
                start = cm.end()
                depth, i = 1, start
                while i < len(src) and depth:
                    depth += {"(": 1, ")": -1}.get(src[i], 0)
                    i += 1
                body = src[start:i]
                if re.search(r"\.strict\s*\(|z\.strictObject\s*\(", body):
                    mode = "strict: unknown keys FAIL the build"
                elif re.search(r"\.passthrough\s*\(|\.loose\s*\(|z\.looseObject\s*\(", body):
                    mode = "loose/passthrough: unknown keys are kept"
                else:
                    mode = "default: unknown keys are silently STRIPPED (never reach the page)"
                # Top-level-ish field names: identifiers followed by ':' and z.
                fields = sorted(set(re.findall(r"\b([A-Za-z_]\w*)\s*:\s*z\.", body)) - {"schema"})
                loader = re.search(r"glob\s*\(\s*\{([^}]*)\}", body)
                out["collections"][name] = {
                    "unknown_keys": mode,
                    "fields": fields,
                    "loader": loader.group(1).strip() if loader else None,
                }
            break
    if not out["found"]:
        out["note"] = "no content config: no schema validation; the layout decides which fields are used"
    return out


def package_info(root: Path) -> dict:
    pj = root / "package.json"
    info = {}
    if not pj.is_file():
        return {"package_json": None}
    try:
        data = json.loads(read(pj))
    except json.JSONDecodeError as e:
        return {"package_json": str(pj), "error": f"package.json does not parse: {e}"}
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    info["package_json"] = str(pj)
    info["name"] = data.get("name")
    info["scripts"] = data.get("scripts", {})
    info["packageManager_field"] = data.get("packageManager")
    info["versions"] = {k: deps[k] for k in ("astro", "next", "react", "tailwindcss", "zod", "typescript") if k in deps}
    info["seo_packages"] = {k: deps[k] for k in SEO_PACKAGES if k in deps}
    info["legacy_tailwind_integration"] = "@astrojs/tailwind" in deps
    info["cms"] = sorted({v for k, v in CMS_PACKAGES.items() if k in deps})
    info["fonts"] = sorted(k for k in deps if k.startswith("@fontsource"))
    # Node floor from the installed framework.
    for fw in ("astro", "next"):
        p = root / "node_modules" / fw / "package.json"
        if p.is_file():
            try:
                fwd = json.loads(read(p))
                info.setdefault("installed", {})[fw] = fwd.get("version")
                if fwd.get("engines", {}).get("node"):
                    info.setdefault("node_engines", {})[fw] = fwd["engines"]["node"]
            except json.JSONDecodeError:
                pass
    return info


def package_manager(root: Path, pkg: dict) -> dict:
    found = [(f, pm, i, b, d) for (f, pm, i, b, d) in LOCKFILES if (root / f).is_file()]
    if not found:
        return {"manager": "npm (no lockfile found)", "install": "npm install", "build": "npm run build",
                "dev": "npm run dev", "lockfiles": []}
    pick = found[0]
    field = (pkg.get("packageManager_field") or "").split("@")[0]
    if len(found) > 1 and field:
        for row in found:
            if row[1] == field:
                pick = row
    res = {"manager": pick[1], "install": pick[2], "build": pick[3], "dev": pick[4],
           "lockfiles": [r[0] for r in found]}
    if len(found) > 1:
        res["warning"] = "more than one lockfile; confirm which manager the project uses"
    if "check" in pkg.get("scripts", {}):
        res["check"] = pick[3].replace("build", "check")
    return res


def route_facts(root: Path) -> dict:
    pages = root / "src" / "pages"
    if not pages.is_dir():
        return {}
    dyn, cms_fetch = [], []
    for p in pages.rglob("*"):
        if p.suffix not in (".astro", ".ts", ".js", ".md", ".mdx"):
            continue
        rel = p.relative_to(root).as_posix()
        if "[" in p.name:
            src = read(p)
            dyn.append({
                "route": rel,
                "uses_entry_id": bool(re.search(r"\.id\b", src)),
                "uses_data_slug": bool(re.search(r"data\.slug", src)),
                "filters_draft": bool(re.search(r"draft", src)),
            })
        src = read(p)
        if re.search(r"getLiveEntry|getLiveCollection|fetch\(\s*['\"`]https?://", src):
            cms_fetch.append(rel)
    layouts = sorted(p.relative_to(root).as_posix() for p in (root / "src" / "layouts").glob("*.astro")) \
        if (root / "src" / "layouts").is_dir() else []
    return {"dynamic_routes": dyn, "remote_fetch_routes": cms_fetch, "layouts": layouts}


def drafts(root: Path) -> list:
    content = root / "src" / "content"
    hits = []
    if not content.is_dir():
        return hits
    for p in content.rglob("*"):
        if p.suffix.lower() not in (".md", ".mdx", ".mdoc", ".yaml", ".yml", ".json"):
            continue
        head = read(p)[:4000]
        if p.suffix.lower() in (".md", ".mdx", ".mdoc"):
            m = re.match(r"^---\s*\n(.*?)\n---", head, re.S)
            head = m.group(1) if m else ""
        if any(rx.search(head) for rx in DRAFT_PATTERNS):
            hits.append(p.relative_to(root).as_posix())
    return sorted(hits)


def main():
    ap = argparse.ArgumentParser(description="Detect site stack facts before building or editing.")
    ap.add_argument("path", nargs="?", default=".", help="project folder (default: cwd)")
    ap.add_argument("--json", help="also write the report to this JSON file")
    args = ap.parse_args()

    start = Path(args.path).resolve()
    root, fw, cfg = find_root(start)
    if not root:
        print(f"No astro.config.*, next.config.* or layout/theme.liquid in {start} or one level down.")
        print("Run from the site's project root, or pass its path.")
        sys.exit(2)

    report = {"root": str(root), "framework": fw, "config": str(cfg)}
    pkg = package_info(root) if fw != "shopify-theme" else {}
    report["package"] = pkg
    if fw != "shopify-theme":
        report["package_manager"] = package_manager(root, pkg)
    if fw == "astro":
        report["astro_config"] = astro_config_facts(cfg)
        report["content_config"] = content_config(root)
        report["routes"] = route_facts(root)
        report["draft_or_paused_files"] = drafts(root)
    if fw == "next":
        src = strip_js_comments(read(cfg))
        m = re.search(r"trailingSlash\s*:\s*(true|false)", src)
        report["next_config"] = {"file": str(cfg), "trailingSlash": m.group(1) if m else "false (default)",
                                 "static_export": bool(re.search(r"output\s*:\s*['\"]export['\"]", src))}
    if fw == "shopify-theme":
        report["note"] = ("Shopify theme working copy: content lives in the admin (API/metafields); "
                          "theme files are code. Verify on an unpublished preview theme.")

    print(f"Site root:      {report['root']}")
    print(f"Framework:      {fw}  (config: {cfg})")
    if pkg.get("versions"):
        print(f"Versions:       {pkg['versions']}")
    if pkg.get("node_engines"):
        print(f"Node floor:     {pkg['node_engines']}")
    if "package_manager" in report:
        pm = report["package_manager"]
        print(f"Package mgr:    {pm['manager']}  build: {pm['build']}  dev: {pm['dev']}"
              + (f"  check: {pm['check']}" if pm.get("check") else ""))
        if pm.get("warning"):
            print(f"  WARNING: {pm['warning']}")
    if pkg.get("cms"):
        print(f"Headless CMS:   {', '.join(pkg['cms'])} -> edit content in the CMS, not local files")
    if pkg.get("legacy_tailwind_integration"):
        print("WARNING: @astrojs/tailwind (v3 integration) installed; Tailwind v4 uses @tailwindcss/vite")
    if pkg.get("seo_packages"):
        print(f"SEO packages:   {', '.join(pkg['seo_packages'])}")
    ac = report.get("astro_config")
    if ac:
        print(f"site:           {ac.get('site', '<missing>')}")
        print(f"trailingSlash:  {ac['trailingSlash']}   build.format: {ac['build_format']}   output: {ac['output']}")
        if ac.get("i18n"):
            print(f"i18n:           {ac['i18n']}")
        for w in ([ac["site_warning"]] if ac.get("site_warning") else []) + ac["warnings"]:
            print(f"  WARNING: {w}")
    cc = report.get("content_config")
    if cc:
        if cc["found"]:
            print(f"Content config: {cc['found']} ({cc['era']}); zod from {cc.get('zod_import')}")
            for name, c in cc["collections"].items():
                print(f"  - {name}: {c['unknown_keys']}")
                print(f"      fields: {', '.join(c['fields'])}")
        else:
            print(f"Content config: none ({cc['note']})")
    rt = report.get("routes") or {}
    for d in rt.get("dynamic_routes", []):
        how = "entry.id" if d["uses_entry_id"] else ("data.slug" if d["uses_data_slug"] else "?")
        print(f"Route:          {d['route']}  (URL from {how}; draft filter: {'yes' if d['filters_draft'] else 'NO'})")
    if rt.get("remote_fetch_routes"):
        print(f"Remote fetch:   {', '.join(rt['remote_fetch_routes'])} (content may come from a CMS/API)")
    if rt.get("layouts"):
        print(f"Layouts:        {', '.join(rt['layouts'])}")
    if report.get("draft_or_paused_files"):
        print(f"Draft/paused:   {len(report['draft_or_paused_files'])} file(s): "
              + ", ".join(report["draft_or_paused_files"][:10]))
    if report.get("note"):
        print(report["note"])

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"\nJSON written: {args.json}")


if __name__ == "__main__":
    main()
