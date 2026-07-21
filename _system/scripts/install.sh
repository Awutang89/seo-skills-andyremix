#!/usr/bin/env bash
# ============================================================================
# install.sh - Marketing & SEO Skills installer
# ============================================================================
# Copies every skill in this package into your Claude skills directory so the
# skills are available in Claude Code / Claude Desktop conversations.
#
# Usage:
#   ./install.sh                 Install all skills
#   ./install.sh --claude-only   Skip the 'creative' skill (needs a Replicate key)
#
# Override the install root (default: ~/.claude):
#   SKILLS_INSTALL_HOME=/path/to/home ./install.sh
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INSTALL_HOME="${SKILLS_INSTALL_HOME:-$HOME/.claude}"
SKILLS_DIR="$INSTALL_HOME/skills"
CLAUDE_ONLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --claude-only) CLAUDE_ONLY=true; shift ;;
    --help|-h) echo "Usage: $0 [--claude-only]"; exit 0 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

echo ""
echo "  Marketing & SEO Skills - Installer"
echo "  ----------------------------------"
echo "  Source: $SKILLS_ROOT"
echo "  Target: $SKILLS_DIR"
echo ""

if [[ ! -f "$SKILLS_ROOT/_system/brand-memory.md" ]]; then
  echo "Error: run this from inside the skills package (cannot find _system/)."
  exit 1
fi

mkdir -p "$SKILLS_DIR"

copy_tree() {
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude='.DS_Store' --exclude='.git' "$1/" "$2/"
  else
    mkdir -p "$2"; cp -R "$1/." "$2/"; find "$2" -name '.DS_Store' -delete 2>/dev/null || true
  fi
}

# Shared framework
copy_tree "$SKILLS_ROOT/_system" "$SKILLS_DIR/_system"
echo "  [done] _system/"

# Auto-discover every skill (any directory containing SKILL.md)
count=0
for dir in "$SKILLS_ROOT"/*/; do
  name="$(basename "$dir")"
  [[ "$name" == "_system" ]] && continue
  [[ ! -f "$dir/SKILL.md" ]] && continue
  if $CLAUDE_ONLY && [[ "$name" == "creative" ]]; then
    echo "  [skip] creative (--claude-only)"; continue
  fi
  copy_tree "$dir" "$SKILLS_DIR/$name"
  echo "  [done] $name/"
  count=$((count + 1))
done

echo ""
echo "  Installed $count skills to $SKILLS_DIR"
if ! $CLAUDE_ONLY && [[ -z "${REPLICATE_API_TOKEN:-}" ]]; then
  echo "  Note: the 'creative' skill needs REPLICATE_API_TOKEN in your environment."
fi
echo "  Run ./doctor.sh to verify."
echo ""
