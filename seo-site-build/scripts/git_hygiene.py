#!/usr/bin/env python
"""git_hygiene.py - classify every changed path after a build or edit (stdlib only).

Runs `git status --short` and `git status --short --ignored` in the repo and sorts each path:
  ALLOWED     matches an --allow glob (the approved target files, justified shared files, notes)
  UNEXPECTED  tracked/untracked change that matches no --allow glob -> restore if you are sure
              it came from this run, otherwise report it as a side effect
  BUILD       ignored build/dependency output (dist, .astro, .next, node_modules, .wrangler...)
  IGNORED     any other ignored path

It never restores, deletes or stages anything; it only reports and suggests commands.

Usage:
  python git_hygiene.py [--repo .] --allow "src/content/blog/en/x.md" --allow "docs/seo-notes/*"
Exit code: 0 = no UNEXPECTED paths, 1 = at least one, 2 = not a git repo.
"""

import argparse
import fnmatch
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BUILD_DIRS = ("dist/", ".astro/", ".next/", "out/", "node_modules/", ".wrangler/", ".vercel/",
              ".turbo/", ".cache/", "__pycache__/")


def status(repo, ignored):
    # Untracked files individually for the plain run; ignored directories collapsed for the
    # --ignored run (otherwise every file under node_modules would be listed).
    cmd = ["git", "-C", repo, "status", "--short"]
    cmd.append("--ignored" if ignored else "--untracked-files=all")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(res.stderr.strip() or "git status failed")
        sys.exit(2)
    rows = []
    for line in res.stdout.splitlines():
        if len(line) < 4:
            continue
        code, path = line[:2], line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        rows.append((code, path.strip('"')))
    return rows


def main():
    ap = argparse.ArgumentParser(description="Classify changed files after a build or edit.")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--allow", action="append", default=[], help="glob of an allowed path (repeatable)")
    args = ap.parse_args()

    plain = status(args.repo, False)
    full = status(args.repo, True)
    buckets = {"ALLOWED": [], "UNEXPECTED": [], "BUILD": [], "IGNORED": []}
    for code, path in full:
        norm = path.replace("\\", "/")
        if code == "!!":
            low = "/" + norm
            key = "BUILD" if any(("/" + d) in low for d in BUILD_DIRS) else "IGNORED"
            buckets[key].append((code, norm))
        elif any(fnmatch.fnmatch(norm, g.replace("\\", "/")) for g in args.allow):
            buckets["ALLOWED"].append((code, norm))
        else:
            buckets["UNEXPECTED"].append((code, norm))

    print(f"git status --short: {len(plain)} path(s); with --ignored: {len(full)} path(s)")
    for key in ("ALLOWED", "UNEXPECTED", "BUILD", "IGNORED"):
        rows = buckets[key]
        print(f"\n{key} ({len(rows)})")
        for code, p in rows[:60]:
            print(f"  {code} {p}")
        if len(rows) > 60:
            print(f"  ... {len(rows) - 60} more")
    if buckets["UNEXPECTED"]:
        print("\nFor each UNEXPECTED path you are sure this run created or modified:")
        print("  tracked:   git restore -- <path>")
        print("  untracked: delete it only if you created it in this run")
        print("Anything you cannot safely restore goes in the summary as a side effect; do not call the run clean.")
    if buckets["BUILD"] or buckets["IGNORED"]:
        print("\nList the BUILD entries under 'ignored build/dependency output' in the summary. Keep installed deps.")
    sys.exit(1 if buckets["UNEXPECTED"] else 0)


if __name__ == "__main__":
    main()
