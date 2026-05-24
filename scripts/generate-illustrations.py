#!/usr/bin/env python3
"""
generate-illustrations.py
Whisperwood Books — AI Illustration Generator

Calls the Google Imagen API (via google-genai SDK) to generate spread
illustrations for the Whisperwood children's book series.

Usage:
    python scripts/generate-illustrations.py --book book1 --spread illo-01 --api-key YOUR_KEY
    python scripts/generate-illustrations.py --book book1 --spread all
    python scripts/generate-illustrations.py --book book2 --spread cover

See scripts/README-illustration-generator.md for full documentation.
"""

import argparse
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
# "Google Nano Banana 2" is the internal codename for Gemini 3.1 Flash Image,
# which maps to the Imagen 4 API model identifier in the google-genai SDK.
MODEL_ID = "imagen-4.0-generate-001"

# Output image format — PNG so the placement script can find .png files.
# The placement scripts also accept .jpg / .jpeg, but PNG avoids re-compression.
OUTPUT_MIME_TYPE = "image/png"
OUTPUT_EXTENSION = ".png"


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Whisperwood book illustrations using Google Imagen.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single spread
  python scripts/generate-illustrations.py --book book1 --spread illo-01

  # All spreads for a book
  python scripts/generate-illustrations.py --book book1 --spread all

  # Explicit API key
  python scripts/generate-illustrations.py --book book2 --spread cover --api-key AIza...
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
        help="Google API key. Falls back to the GOOGLE_API_KEY environment variable.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# File reading helpers
# ---------------------------------------------------------------------------

def load_style_guide() -> str:
    """
    Return the full content of the series illustration guide.
    The guide is prepended to every prompt as a style anchor.
    """
    if not GUIDE_PATH.exists():
        sys.exit(f"ERROR: Style guide not found at {GUIDE_PATH}")
    return GUIDE_PATH.read_text(encoding="utf-8")


def load_prompts_file(book: str) -> str:
    """
    Return the raw markdown content of the prompts file for the given book.
    """
    prompts_path = PROMPTS_DIR / f"{book}-prompts.md"
    if not prompts_path.exists():
        sys.exit(
            f"ERROR: Prompts file not found at {prompts_path}\n"
            f"Available books: {sorted(p.stem.replace('-prompts', '') for p in PROMPTS_DIR.glob('*-prompts.md'))}"
        )
    return prompts_path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Prompt extraction
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

    '## Spread 1 — ...'   -> 'illo-01'
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


def build_full_prompt(style_guide: str, spread_prompt: str) -> str:
    """
    Combine the series style guide and the spread-specific prompt into the
    single string that will be sent to the API.

    The style guide is included in a clearly labelled preamble so the model
    treats it as authoritative context before reading the scene description.
    """
    return (
        "=== WHISPERWOOD SERIES STYLE GUIDE (applies to all illustrations) ===\n\n"
        + style_guide.strip()
        + "\n\n"
        + "=== SPREAD-SPECIFIC SCENE PROMPT ===\n\n"
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

def generate_image(client, prompt: str, spread_name: str) -> bytes | None:
    """
    Call the Imagen API and return the raw image bytes, or None on failure.

    Uses google-genai SDK:
        client.models.generate_images(model=..., prompt=..., config=...)

    Response structure:
        response.generated_images[0].image.image_bytes  -> bytes
    """
    try:
        from google.genai import types  # local import to defer ImportError

        response = client.models.generate_images(
            model=MODEL_ID,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type=OUTPUT_MIME_TYPE,
            ),
        )

        if not response.generated_images:
            return None

        return response.generated_images[0].image.image_bytes

    except Exception as exc:  # noqa: BLE001
        # Caller prints the error; we just propagate via return None + message
        raise RuntimeError(str(exc)) from exc


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    # --- Resolve API key ---
    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        sys.exit(
            "ERROR: No API key provided.\n"
            "Pass --api-key or set the GOOGLE_API_KEY environment variable."
        )

    # --- Import SDK (fail fast with a clear message) ---
    try:
        from google import genai  # type: ignore[import]
    except ImportError:
        sys.exit(
            "ERROR: google-genai package not installed.\n"
            "Install it with:  pip install google-genai"
        )

    client = genai.Client(api_key=api_key)

    # --- Load content ---
    style_guide = load_style_guide()
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
    print(f"Book:   {args.book}")
    print(f"Model:  {MODEL_ID}")
    print(f"Spreads to generate: {total}")
    print()

    for spread_name in targets:
        spread_prompt = all_spreads[spread_name]
        full_prompt = build_full_prompt(style_guide, spread_prompt)
        dest = output_path(args.book, spread_name)

        try:
            image_bytes = generate_image(client, full_prompt, spread_name)

            if image_bytes is None:
                print(f"  ✗ {spread_name} failed: API returned no images (possible safety filter)")
                continue

            dest.write_bytes(image_bytes)
            print(f"  ✓ {spread_name} saved  →  {dest.relative_to(REPO_ROOT)}")
            generated += 1

        except RuntimeError as exc:
            print(f"  ✗ {spread_name} failed: {exc}")

    print()
    print(f"Generated {generated} of {total} illustrations")
    print()


if __name__ == "__main__":
    main()
