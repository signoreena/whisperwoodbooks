#!/usr/bin/env python3
"""
generate-illustrations.py
Whisperwood Books — AI Illustration Generator

Calls the OpenAI Images API (gpt-image-2) to generate spread illustrations
for the Whisperwood children's book series.

Usage:
    python scripts/generate-illustrations.py --book book1 --spread illo-01 --api-key sk-...
    python scripts/generate-illustrations.py --book book1 --spread all
    python scripts/generate-illustrations.py --book book2 --spread cover

See scripts/README-illustration-generator.md for full documentation.
"""

import argparse
import base64
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (all relative to the repo root, resolved at runtime)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
GUIDE_PATH = REPO_ROOT / "illustrations" / "whisperwood-illustration-guide.md"
PROMPTS_DIR = REPO_ROOT / "content" / "illustration-prompts"
ILLUSTRATIONS_DIR = REPO_ROOT / "illustrations"

# ---------------------------------------------------------------------------
# Model configuration
# ---------------------------------------------------------------------------
MODEL_ID = "gpt-image-2"

# Output image format — PNG so the placement script can find .png files.
# The placement scripts also accept .jpg / .jpeg, but PNG avoids re-compression.
OUTPUT_FORMAT = "png"
OUTPUT_EXTENSION = ".png"

# Image size.  gpt-image-2 supports: 1024x1024 | 1024x1536 | 1536x1024 | auto
# 1024x1024 works for both portrait pages and double-page spreads (the model
# crops/composes within the square).  Switch to 1536x1024 if you want a
# landscape-native canvas for double-page spreads.
IMAGE_SIZE = "1024x1024"

# Quality.  Options: low | medium | high | auto
# "high" gives the best detail for illustration work; "medium" costs ~40 % less.
IMAGE_QUALITY = "high"


# ---------------------------------------------------------------------------
# Character name detection — used for smart prompt construction
# ---------------------------------------------------------------------------

# Maps lowercase keywords that appear in a spread prompt to the heading that
# names the corresponding section in the style guide.
CHARACTER_KEYWORDS: dict[str, str] = {
    "vera": "### Vera",
    "pip": "### Pip",
    "sage": "### Sage",
    "bram": "### Bram",
    "oswin": "### Oswin",
    "hazel": "### Hazel",
    "otter": "### The Otter",
    "mouse family": "### The Mouse Family",
    "mouse": "### The Mouse Family",
    "ma mouse": "### The Mouse Family",
    "pa mouse": "### The Mouse Family",
    "big daughter": "### The Mouse Family",
    "middle son": "### The Mouse Family",
    "baby": "### The Mouse Family",
}


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Whisperwood book illustrations using OpenAI gpt-image-2.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single spread
  python scripts/generate-illustrations.py --book book1 --spread illo-01

  # All spreads for a book
  python scripts/generate-illustrations.py --book book1 --spread all

  # Cover only
  python scripts/generate-illustrations.py --book book2 --spread cover

  # Explicit API key
  python scripts/generate-illustrations.py --book book1 --spread illo-06 --api-key sk-...
        """,
    )
    parser.add_argument(
        "--book",
        required=True,
        help='Book identifier, e.g. "book1", "book2" … "book8"',
    )
    parser.add_argument(
        "--spread",
        required=True,
        help='Spread name (e.g. "illo-01", "cover") or "all" to generate every spread',
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="OpenAI API key. Falls back to the OPENAI_API_KEY environment variable.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# File reading helpers
# ---------------------------------------------------------------------------

def load_style_guide() -> str:
    """Return the full content of the series illustration guide."""
    if not GUIDE_PATH.exists():
        sys.exit(f"ERROR: Style guide not found at {GUIDE_PATH}")
    return GUIDE_PATH.read_text(encoding="utf-8")


def load_prompts_file(book: str) -> str:
    """Return the raw markdown content of the prompts file for the given book."""
    prompts_path = PROMPTS_DIR / f"{book}-prompts.md"
    if not prompts_path.exists():
        available = sorted(
            p.stem.replace("-prompts", "")
            for p in PROMPTS_DIR.glob("*-prompts.md")
        )
        sys.exit(
            f"ERROR: Prompts file not found at {prompts_path}\n"
            f"Available books: {available}"
        )
    return prompts_path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Style guide extraction — smart sections only
# ---------------------------------------------------------------------------

def _extract_guide_section(guide_text: str, heading: str) -> str:
    """
    Return the text of a single ## or ### section from the style guide,
    from the given heading up to (but not including) the next heading at
    the same or higher level.
    """
    # Escape the heading for regex use
    heading_escaped = re.escape(heading.lstrip())
    pattern = re.compile(
        r"(?:^|\n)(" + heading_escaped + r".*?)\n(.*?)(?=\n#{1,3} |\Z)",
        re.DOTALL,
    )
    m = pattern.search(guide_text)
    if m:
        return m.group(1) + "\n" + m.group(2)
    return ""


def _extract_named_section(guide_text: str, section_number: str, section_title: str) -> str:
    """
    Extract a top-level numbered section (e.g. '## 1. Series Art Direction').
    Returns everything from that heading to the next ## heading.
    """
    pattern = re.compile(
        r"(## " + re.escape(section_number) + r"\..*?)\n(.*?)(?=\n## |\Z)",
        re.DOTALL,
    )
    m = pattern.search(guide_text)
    if m:
        return m.group(1) + "\n" + m.group(2)
    return ""


def build_smart_style_preamble(guide_text: str, spread_prompt: str) -> str:
    """
    Extract only the relevant sections from the style guide for this spread:

      1. Section 1 — Series Art Direction (always included; it's the style anchor)
      2. Character canon entries for each character mentioned in the spread prompt
      3. Section 5 — World Elements (always included; lantern mushrooms, singing mud, etc.)
      4. Section 6 — Forbidden Elements (always included)
      5. Section 7 — Closing Spread Rule (included only for final/closing spreads)

    Section 4 (Mouse Family arc detail) is included whenever the mouse family appears.
    The mouse family arc text is long and only relevant when they are present.
    """
    spread_lower = spread_prompt.lower()
    sections: list[str] = []

    # --- Always: art direction ---
    art_direction = _extract_named_section(guide_text, "1", "Series Art Direction")
    if art_direction:
        sections.append(art_direction)

    # --- Characters: include each character's entry if they appear in the prompt ---
    # Deduplicate: track which guide headings have already been added
    added_headings: set[str] = set()

    # Main characters
    for keyword, heading in CHARACTER_KEYWORDS.items():
        if keyword in spread_lower and heading not in added_headings:
            char_text = _extract_guide_section(guide_text, heading)
            if char_text:
                sections.append(char_text)
                added_headings.add(heading)

    # If the mouse family is included, also pull the full Section 4 (arc context)
    if "### The Mouse Family" in added_headings:
        mouse_arc = _extract_named_section(guide_text, "4", "The Mouse Family")
        if mouse_arc:
            # Replace the character-level entry with the full section 4 (superset)
            sections = [s for s in sections if "The Mouse Family" not in s]
            sections.append(mouse_arc)

    # --- Always: world elements ---
    world_elements = _extract_named_section(guide_text, "5", "World Elements")
    if world_elements:
        sections.append(world_elements)

    # --- Always: forbidden elements ---
    forbidden = _extract_named_section(guide_text, "6", "Forbidden Elements")
    if forbidden:
        sections.append(forbidden)

    # --- Closing spreads: include the closing spread rule ---
    closing_keywords = ("closing spread", "final spread", "walking home", "walks home")
    if any(kw in spread_lower for kw in closing_keywords):
        closing_rule = _extract_named_section(guide_text, "7", "Closing Spread Rule")
        if closing_rule:
            sections.append(closing_rule)

    return "\n\n---\n\n".join(s.strip() for s in sections if s.strip())


# ---------------------------------------------------------------------------
# Prompt extraction from the book's prompts file
# ---------------------------------------------------------------------------

# Each spread in the prompts file is introduced by a heading that includes
# the spread name.  Examples from the actual files:
#
#   ## Spread 1 — Opening Establishing Spread
#   ## COVER ILLUSTRATION
#   ## Spread 10 — FINAL SPREAD: Walking Home
#
# The "Full prompt:" subsection contains the ready-to-use prompt text.

FULL_PROMPT_RE = re.compile(
    r"\*\*Full prompt:\*\*\s*\n+(.*?)(?=\n---|\Z)",
    re.DOTALL,
)

SPREAD_SECTION_RE = re.compile(
    r"(##\s+(?:COVER ILLUSTRATION|Spread\s+\d+\b.*?))\n(.*?)(?=\n## |\Z)",
    re.DOTALL | re.IGNORECASE,
)


def _spread_name_from_heading(heading: str) -> str:
    """
    Convert a section heading to the canonical spread filename stem.

    '## Spread 1 — ...'    -> 'illo-01'
    '## COVER ILLUSTRATION' -> 'cover'
    """
    heading_clean = heading.lstrip("#").strip()
    if heading_clean.upper().startswith("COVER"):
        return "cover"
    m = re.search(r"Spread\s+(\d+)", heading_clean, re.IGNORECASE)
    if m:
        n = int(m.group(1))
        return f"illo-{n:02d}"
    # Fallback: slugify the heading
    slug = re.sub(r"[^a-z0-9]+", "-", heading_clean.lower()).strip("-")
    return slug


def extract_all_spreads(prompts_text: str) -> dict[str, str]:
    """
    Parse the prompts markdown and return a dict mapping spread names
    (e.g. 'illo-01', 'cover') to their extracted "Full prompt:" text.
    """
    spreads: dict[str, str] = {}

    for match in SPREAD_SECTION_RE.finditer(prompts_text):
        heading = match.group(1)
        section_body = match.group(2)
        spread_name = _spread_name_from_heading(heading)

        fp_match = FULL_PROMPT_RE.search(section_body)
        if fp_match:
            prompt_text = fp_match.group(1).strip()
            spreads[spread_name] = prompt_text

    return spreads


# ---------------------------------------------------------------------------
# Final prompt assembly
# ---------------------------------------------------------------------------

def build_full_prompt(guide_text: str, spread_prompt: str) -> str:
    """
    Build the prompt sent to gpt-image-2.

    Structure:
      1. A concise style anchor extracted from the parent guide (art direction,
         relevant characters, world elements, forbidden elements).
      2. The spread-specific "Full prompt:" text verbatim.

    Keeping the preamble focused — rather than dumping the entire guide —
    leaves more of the model's effective context window for the scene detail
    and avoids the guide's prose-heavy character arcs drowning out scene direction.
    """
    preamble = build_smart_style_preamble(guide_text, spread_prompt)

    return (
        "=== WHISPERWOOD SERIES STYLE GUIDE (authoritative; governs all details "
        "not specified in the scene prompt below) ===\n\n"
        + preamble
        + "\n\n"
        + "=== SCENE PROMPT (scene-specific details; these take priority over the "
        "style guide for this illustration) ===\n\n"
        + spread_prompt.strip()
    )


# ---------------------------------------------------------------------------
# Output path
# ---------------------------------------------------------------------------

def output_path(book: str, spread_name: str) -> Path:
    """
    Return the path where the generated image should be saved.
    Matches the convention expected by place-illustrations.sh:
        illustrations/<book>/<spread_name>.png
    """
    out_dir = ILLUSTRATIONS_DIR / book
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"{spread_name}{OUTPUT_EXTENSION}"


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def generate_image(client, prompt: str) -> bytes:
    """
    Call the OpenAI Images API (gpt-image-2) and return the raw PNG bytes.

    API call:
        client.images.generate(
            model="gpt-image-2",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="high",
            output_format="png",
            response_format="b64_json",
        )

    Response structure:
        response.data[0].b64_json  ->  base64-encoded PNG string

    Raises RuntimeError on any API or decoding failure.
    """
    try:
        response = client.images.generate(
            model=MODEL_ID,
            prompt=prompt,
            n=1,
            size=IMAGE_SIZE,
            quality=IMAGE_QUALITY,
            output_format=OUTPUT_FORMAT,
            response_format="b64_json",
        )
    except Exception as exc:
        raise RuntimeError(str(exc)) from exc

    if not response.data:
        raise RuntimeError("API returned an empty data list (no images generated)")

    b64_data = response.data[0].b64_json
    if not b64_data:
        raise RuntimeError(
            "API returned a data entry with no b64_json field. "
            "Check that response_format='b64_json' is supported for this model."
        )

    try:
        return base64.b64decode(b64_data)
    except Exception as exc:
        raise RuntimeError(f"Failed to decode base64 image data: {exc}") from exc


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    # --- Resolve API key ---
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit(
            "ERROR: No API key provided.\n"
            "Pass --api-key or set the OPENAI_API_KEY environment variable.\n"
            "See scripts/README-illustration-generator.md for setup instructions."
        )

    # --- Import SDK (fail fast with a clear message) ---
    try:
        from openai import OpenAI  # type: ignore[import]
    except ImportError:
        sys.exit(
            "ERROR: openai package not installed.\n"
            "Install it with:  pip install openai"
        )

    client = OpenAI(api_key=api_key)

    # --- Load content ---
    guide_text = load_style_guide()
    prompts_text = load_prompts_file(args.book)
    all_spreads = extract_all_spreads(prompts_text)

    if not all_spreads:
        sys.exit(
            f"ERROR: No spreads with 'Full prompt:' sections found in "
            f"{PROMPTS_DIR / (args.book + '-prompts.md')}"
        )

    # --- Determine which spreads to generate ---
    if args.spread.lower() == "all":
        targets = sorted(all_spreads.keys())
    else:
        target = args.spread.lower()
        if target not in all_spreads:
            available = ", ".join(sorted(all_spreads.keys()))
            sys.exit(
                f"ERROR: Spread '{target}' not found in {args.book} prompts.\n"
                f"Available spreads: {available}"
            )
        targets = [target]

    total = len(targets)
    generated = 0

    print(f"\nWhisperwood Illustration Generator")
    print(f"Book:    {args.book}")
    print(f"Model:   {MODEL_ID}")
    print(f"Size:    {IMAGE_SIZE}  |  Quality: {IMAGE_QUALITY}")
    print(f"Spreads: {total}")
    print()

    for spread_name in targets:
        spread_prompt = all_spreads[spread_name]
        full_prompt = build_full_prompt(guide_text, spread_prompt)
        dest = output_path(args.book, spread_name)

        try:
            image_bytes = generate_image(client, full_prompt)
            dest.write_bytes(image_bytes)
            print(f"  ✓ {spread_name} saved  →  {dest.relative_to(REPO_ROOT)}")
            generated += 1

        except RuntimeError as exc:
            print(f"  ✗ {spread_name} failed: {exc}")

    print()
    print(f"Generated {generated} of {total} illustrations.")
    if generated < total:
        failed = total - generated
        print(f"{failed} spread(s) failed — re-run with the specific --spread name to retry.")
    print()


if __name__ == "__main__":
    main()
