#!/usr/bin/env bash
# =============================================================================
# place-illustrations.sh
# Whisperwood Book 1 — Illustration Placement Script
#
# Run from the repo root:   bash production/place-illustrations.sh
#
# What it does:
#   1. Checks illustrations/book1/ for correctly-named image files
#   2. Copies them into the ePub source (OEBPS/images/)
#   3. Copies spread images alongside the print HTML for local preview
#   4. Rebuilds book1-rising-river.epub
#   5. Reports what was placed and what is still missing
#
# After this script runs, Claude edits the XHTML and print HTML files
# to replace placeholder divs with <img> tags pointing to the placed files.
# =============================================================================

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ILLUS_DIR="$REPO_ROOT/illustrations/book1"
EPUB_IMAGES="$REPO_ROOT/production/book1-epub/OEBPS/images"
EPUB_SRC="$REPO_ROOT/production/book1-epub"
EPUB_OUT="$REPO_ROOT/production/book1-rising-river.epub"
PRINT_DIR="$REPO_ROOT/production/book1-print"

echo ""
echo "================================================"
echo "  Whisperwood Book 1 — Illustration Placement"
echo "================================================"
echo ""

# Expected files
# Book 1 has 12 illustration slots across 9 chapters:
#   illo-01  Ch1 full-bleed establishing spread (KEY SPREAD)
#   illo-02  Ch1 continued — Mapleaf veins dark / Pip lands on Vera
#   illo-03  Ch2 — Sage at river ringing bellflower
#   illo-04  Ch3 — Pip with stick, Vera's retreating silhouette
#   illo-05  Ch4 — Vera before Bram the beaver
#   illo-06  Ch4 — Sage and the boulder full-bleed spread (KEY SPREAD)
#   illo-07  Ch5 — Three friends, Vera's ears coming back up
#   illo-08  Ch6 — Split panel: bunnies underground / Vera at Mapleaf by night
#   illo-09  Ch7 — Community singing full-bleed spread (COMMUNITY IMAGE)
#   illo-10  Ch7 — The redirect working, collective exhale
#   illo-11  Ch8 — Four beavers moving the fallen oak at dawn
#   illo-12  Ch9 — Final spread: trio walking home (FINAL SPREAD)
declare -a NAMES=(
  "cover"
  "illo-01" "illo-02" "illo-03" "illo-04"
  "illo-05" "illo-06" "illo-07" "illo-08"
  "illo-09" "illo-10" "illo-11" "illo-12"
)

placed=0
missing=0

mkdir -p "$EPUB_IMAGES"
mkdir -p "$PRINT_DIR/images"

for name in "${NAMES[@]}"; do
  found=""
  for ext in jpg jpeg png; do
    candidate="$ILLUS_DIR/$name.$ext"
    if [ -f "$candidate" ]; then
      found="$candidate"
      found_ext="$ext"
      break
    fi
  done

  if [ -n "$found" ]; then
    # Copy to ePub images directory
    cp "$found" "$EPUB_IMAGES/$name.$found_ext"
    # Copy to print images directory (for local HTML preview)
    cp "$found" "$PRINT_DIR/images/$name.$found_ext"
    echo "  ✓  $name.$found_ext"
    placed=$((placed + 1))
  else
    echo "  —  $name  (not yet in illustrations/book1/)"
    missing=$((missing + 1))
  fi
done

echo ""
echo "  Placed: $placed / $((placed + missing))"

# Rebuild ePub
echo ""
echo "  Rebuilding ePub..."
rm -f "$EPUB_OUT"
cd "$EPUB_SRC"
zip -X "$EPUB_OUT" mimetype
zip -rg "$EPUB_OUT" META-INF OEBPS
cd "$REPO_ROOT"
echo "  ePub rebuilt: production/book1-rising-river.epub"

echo ""
if [ "$missing" -gt 0 ]; then
  echo "  $missing image(s) still missing. Drop them in illustrations/book1/"
  echo "  following the naming guide, then run this script again."
else
  echo "  All images placed. Tell Claude to update the XHTML and print HTML"
  echo "  to swap placeholder divs for <img> tags."
fi
echo ""
echo "================================================"
echo ""
