#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════
# place-illustrations-book2.sh
# Whisperwood Book 2: The Noisy Night — Illustration Placement Script
#
# USAGE:
#   bash production/place-illustrations-book2.sh
#
# WHAT IT DOES:
#   1. Checks illustrations/book2/ for correctly-named files
#   2. Copies found images into OEBPS/images/ and book2-print/images/
#   3. Rebuilds the epub
#   4. Reports placed vs. missing
#
# EXPECTED FILE NAMES (in illustrations/book2/):
#   cover.jpg  or  cover.jpeg  or  cover.png
#   illo-01.jpg  or  illo-01.jpeg  or  illo-01.png
#   illo-02.jpg  ...
#   illo-03.jpg  ...
#   illo-04.jpg  ...
#   illo-05.jpg  ...
#   illo-06.jpg  ...
#   illo-07.jpg  ...
#   illo-08.jpg  ...
#   illo-09.jpg  ...
#
# ILLUSTRATION DESCRIPTIONS:
#   cover    : Sage at forked elm, hand on bark, visual chaos above — full-bleed cover
#   illo-01  : KEY SPREAD — Wednesday evening establishing shot, songbird relay, Sage at her window
#   illo-02  : Spread 2 — Pip at the bakery, Hazel with untied apron on her step, shutters closed
#   illo-03  : Spread 3 — Vera mid-stride toward canopy, Pip running behind
#   illo-04  : KEY SPREAD — Library tree interior, Vera before Oswin, folded list
#   illo-05  : Spread 5 — Pip and Sage on the step of the willow hollow, stick beside Pip
#   illo-06  : KEY IMAGE — Sage at the forked elm, jaw set, three relay chains converging
#   illo-07  : Spread 7 — Quietcap mushroom grove, Oswin leads, Sage breathing at grove edge
#   illo-08  : COMMUNITY IMAGE — Path bend by the brook, mushrooms placed, relay thinning
#   illo-09  : FINAL SPREAD — Trio walking home at night, lantern mushrooms, sleeping bird in elm
#
# AFTER RUNNING:
#   Review the epub source in production/book2-epub/OEBPS/pages/ — each .xhtml
#   placeholder has a TO REPLACE comment showing the exact <img> tag to use.
#   Rebuild manually if you replace art after running this script.
# ══════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Paths ─────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

ILLUSTRATIONS_DIR="$REPO_ROOT/illustrations/book2"
EPUB_IMAGES_DIR="$SCRIPT_DIR/book2-epub/OEBPS/images"
PRINT_IMAGES_DIR="$SCRIPT_DIR/book2-print/images"
EPUB_SOURCE_DIR="$SCRIPT_DIR/book2-epub"
EPUB_OUTPUT="$SCRIPT_DIR/book2-the-noisy-night.epub"

# ── Expected illustrations ─────────────────────────────────────────────
declare -a EXPECTED=(
  "cover"
  "illo-01"
  "illo-02"
  "illo-03"
  "illo-04"
  "illo-05"
  "illo-06"
  "illo-07"
  "illo-08"
  "illo-09"
)

# ── Setup ──────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Whisperwood Book 2: The Noisy Night"
echo "  Illustration Placement Script"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Create output image directories if they don't exist
mkdir -p "$EPUB_IMAGES_DIR"
mkdir -p "$PRINT_IMAGES_DIR"

# Check that illustrations/book2/ exists
if [ ! -d "$ILLUSTRATIONS_DIR" ]; then
  echo "ERROR: Illustrations directory not found: $ILLUSTRATIONS_DIR"
  echo "       Create this directory and add illustration files before running."
  echo ""
  exit 1
fi

# ── Scan and copy ──────────────────────────────────────────────────────
PLACED=()
MISSING=()

for name in "${EXPECTED[@]}"; do
  FOUND=""
  for ext in jpg jpeg png; do
    candidate="$ILLUSTRATIONS_DIR/${name}.${ext}"
    if [ -f "$candidate" ]; then
      FOUND="$candidate"
      FOUND_EXT="$ext"
      break
    fi
  done

  if [ -n "$FOUND" ]; then
    # Copy to epub images directory
    cp "$FOUND" "$EPUB_IMAGES_DIR/${name}.${FOUND_EXT}"
    # Copy to print images directory
    cp "$FOUND" "$PRINT_IMAGES_DIR/${name}.${FOUND_EXT}"
    PLACED+=("$name.${FOUND_EXT}")
    echo "  PLACED:  $name.${FOUND_EXT}"
  else
    MISSING+=("$name")
    echo "  MISSING: $name (.jpg / .jpeg / .png not found in $ILLUSTRATIONS_DIR)"
  fi
done

echo ""

# ── Rebuild epub if any files were placed ──────────────────────────────
if [ ${#PLACED[@]} -gt 0 ]; then
  echo "Rebuilding epub..."
  # Remove existing epub
  rm -f "$EPUB_OUTPUT"
  # Package per spec: mimetype first (no compression), then directories
  cd "$EPUB_SOURCE_DIR"
  zip -X "$EPUB_OUTPUT" mimetype
  zip -rg "$EPUB_OUTPUT" META-INF OEBPS
  cd "$SCRIPT_DIR"
  echo "epub rebuilt: $EPUB_OUTPUT"
  echo ""
fi

# ── Summary ────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════════════"
echo "  Summary"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "  Placed:  ${#PLACED[@]} of ${#EXPECTED[@]} illustrations"
echo "  Missing: ${#MISSING[@]} of ${#EXPECTED[@]} illustrations"
echo ""

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "  Still missing:"
  for m in "${MISSING[@]}"; do
    echo "    - $m  (place as ${m}.jpg, ${m}.jpeg, or ${m}.png in $ILLUSTRATIONS_DIR)"
  done
  echo ""
  echo "  NOTE: epub placeholders remain for missing illustrations."
  echo "  Run this script again when remaining art is delivered."
fi

if [ ${#MISSING[@]} -eq 0 ]; then
  echo "  All illustrations placed."
  echo ""
  echo "  NEXT STEPS:"
  echo "  1. Run epubcheck on $EPUB_OUTPUT (if available)"
  echo "  2. Open book2-print/book2-print.html in Chrome and export to PDF"
  echo "  3. Upload to KDP per the KDP Upload Checklist in the production report"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
