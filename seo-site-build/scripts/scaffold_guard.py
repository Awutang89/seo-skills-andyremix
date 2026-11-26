#!/usr/bin/env python
"""scaffold_guard.py - protect a folder before a framework CLI scaffold (stdlib only).

  python scaffold_guard.py check    [--dir .] [--temp .astro-scaffold]
      Exit 0 if the folder holds nothing but allowed entries (.claude, .git, .site-concepts,
      .gitignore, the temp scaffold folder). Otherwise exit 1 and list up to 12 conflicts.

  python scaffold_guard.py move-up  [--dir .] [--temp .astro-scaffold]
      Move everything from the temp scaffold folder into the folder, refusing (exit 1, nothing
      moved) if any destination already exists, then delete the empty temp folder.

Typical Astro flow:
  python scaffold_guard.py check
  npx create-astro@<major> .astro-scaffold --template minimal --no-install --no-git --yes --skip-houston
  python scaffold_guard.py move-up
"""

import argparse
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ALLOWED = {".claude", ".git", ".site-concepts", ".gitignore"}


def check(folder: Path, temp: str) -> int:
    conflicts = sorted(p.name for p in folder.iterdir() if p.name not in ALLOWED | {temp})
    if conflicts:
        shown = ", ".join(conflicts[:12]) + (f" (+{len(conflicts) - 12} more)" if len(conflicts) > 12 else "")
        print(f"STOP: {folder} is not empty. Scaffold in a new folder (or a sibling such as site/).")
        print(f"Existing entries that would be at risk: {shown}")
        return 1
    print(f"OK: {folder} is safe to scaffold into.")
    return 0


def move_up(folder: Path, temp: str) -> int:
    src = folder / temp
    if not src.is_dir():
        print(f"STOP: temp scaffold folder {src} not found (did the CLI fail?).")
        return 1
    items = list(src.iterdir())
    clashes = [i.name for i in items if (folder / i.name).exists()]
    if clashes:
        print("STOP: refusing to overwrite existing paths: " + ", ".join(sorted(clashes)))
        return 1
    for item in items:
        shutil.move(str(item), str(folder / item.name))
    src.rmdir()
    print(f"Moved {len(items)} entries from {temp}/ into {folder} and removed {temp}/.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", choices=["check", "move-up"])
    ap.add_argument("--dir", default=".")
    ap.add_argument("--temp", default=".astro-scaffold")
    args = ap.parse_args()
    folder = Path(args.dir).resolve()
    if not folder.is_dir():
        print(f"Folder not found: {folder}")
        sys.exit(2)
    sys.exit(check(folder, args.temp) if args.action == "check" else move_up(folder, args.temp))


if __name__ == "__main__":
    main()
