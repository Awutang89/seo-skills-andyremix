#!/usr/bin/env bash
# ============================================================================
# doctor.sh - Marketing & SEO Skills installation verifier
# ============================================================================
# Checks that the shared framework and every installed skill are present.
#   ./doctor.sh
#   SKILLS_INSTALL_HOME=/path ./doctor.sh
# Exit 0 = all good, 1 = something missing.
# ============================================================================
set -euo pipefail

INSTALL_HOME="${SKILLS_INSTALL_HOME:-$HOME/.claude}"
SKILLS_DIR="$INSTALL_HOME/skills"
SYSTEM_DIR="$SKILLS_DIR/_system"
PASS=0; FAIL=0

ok()   { echo "  [ok]   $1"; PASS=$((PASS+1)); }
bad()  { echo "  [FAIL] $1"; FAIL=$((FAIL+1)); }
have() { [[ -f "$1" ]] && ok "$2" || bad "$2 (missing: $1)"; }

echo ""
echo "  Marketing & SEO Skills - Doctor"
echo "  Skills location: $SKILLS_DIR"
echo ""

if [[ ! -d "$SYSTEM_DIR" ]]; then
  echo "  System directory not found at $SYSTEM_DIR - run install.sh first."
  exit 1
fi

echo "  Framework"
have "$SYSTEM_DIR/brand-memory.md"  "brand-memory.md"
have "$SYSTEM_DIR/output-format.md" "output-format.md"
if [[ -d "$SYSTEM_DIR/schemas" ]]; then
  n=$(find "$SYSTEM_DIR/schemas" -name '*.json' | wc -l | tr -d ' ')
  [[ "$n" -ge 1 ]] && ok "schemas/ ($n json)" || bad "schemas/ (none found)"
else
  bad "schemas/ (directory missing)"
fi

echo ""
echo "  Skills"
skills=0
for dir in "$SKILLS_DIR"/*/; do
  name="$(basename "$dir")"
  [[ "$name" == "_system" ]] && continue
  have "$dir/SKILL.md" "$name"
  skills=$((skills+1))
done

echo ""
echo "  --------------------------------------"
echo "  $PASS checks passed, $FAIL failed, $skills skills found."
[[ "$FAIL" -eq 0 ]] && exit 0 || { echo "  Run install.sh to fix."; exit 1; }
