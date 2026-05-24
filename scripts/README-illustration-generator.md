# Whisperwood Illustration Generator

Generates spread illustrations for the Whisperwood children's book series
using the Google Imagen API (accessed via the `google-genai` SDK).

---

## What it does

1. Reads the series-wide style guide from `illustrations/whisperwood-illustration-guide.md`.
2. Reads the spread prompts from `content/illustration-prompts/<book>-prompts.md`.
3. For each requested spread, extracts the **Full prompt:** section, prepends the full style guide as a style anchor, and sends the combined prompt to the Imagen API.
4. Saves the returned image to `illustrations/<book>/<spread>.png`.
5. Prints a per-spread status line and a final summary count.

Output filenames match the naming convention expected by `production/place-illustrations.sh` and `production/place-illustrations-book2.sh`, so you can run the placement script immediately after generation.

---

## Prerequisites

- **Python 3.10+**
- **google-genai package**
  ```
  pip install google-genai
  ```
- **Google API key** with the Gemini / Imagen API enabled.
  Get one at https://aistudio.google.com/app/apikey
  Set it as an environment variable (recommended):
  ```
  export GOOGLE_API_KEY="AIza..."
  ```

---

## Usage

### Single spread

```bash
python scripts/generate-illustrations.py \
  --book book1 \
  --spread illo-01
```

### Cover illustration

```bash
python scripts/generate-illustrations.py \
  --book book2 \
  --spread cover
```

### All spreads for a book

```bash
python scripts/generate-illustrations.py \
  --book book1 \
  --spread all
```

### Passing the API key explicitly (instead of via env var)

```bash
python scripts/generate-illustrations.py \
  --book book1 \
  --spread illo-06 \
  --api-key AIza...
```

---

## Arguments

| Argument | Required | Description |
|---|---|---|
| `--book` | Yes | Book identifier: `book1` … `book8` |
| `--spread` | Yes | Spread name (`illo-01`, `cover`, etc.) or `all` |
| `--api-key` | No | Google API key; falls back to `GOOGLE_API_KEY` env var |

Valid spread names for each book are printed in the error message if you pass an unknown name.

---

## Where output files go

Images are written to:

```
illustrations/<book>/<spread>.png
```

For example:

```
illustrations/book1/illo-01.png
illustrations/book1/cover.png
```

These are the exact paths the placement scripts scan. Once generation is done, run:

```bash
bash production/place-illustrations.sh        # Book 1
bash production/place-illustrations-book2.sh  # Book 2
```

The placement script copies images into the ePub source and print HTML,
rebuilds the ePub, and reports what was placed vs. still missing.

---

## Known limitations

### Rate limits
The Imagen API enforces per-minute and per-day quota limits depending on your Google Cloud project tier. Generating all spreads for a book in one call (`--spread all`) may hit rate limits mid-run. If a spread fails with a quota error, re-run the script for that individual spread name after the rate limit window resets.

### Visual consistency across spreads
The Imagen API generates each image independently. The style guide and character descriptions in `illustrations/whisperwood-illustration-guide.md` provide a strong anchor, but character appearance (exact fur colour, clothing details, prop design) will vary between spreads. This is a fundamental limitation of text-to-image generation without fine-tuning. For production use, plan for manual consistency review and touch-up after generation.

### Safety filters
Occasionally the API returns no images due to automated safety filtering, even for benign children's book content. The script prints `✗ <spread> failed: API returned no images (possible safety filter)` when this occurs. Re-running the spread usually succeeds — the filter result is not fully deterministic.

### Output resolution
The Imagen 4 API (`imagen-4.0-generate-001`) generates images at its default resolution. This may not match the minimum print dimensions specified in `illustrations/book1/NAMING-GUIDE.txt` (2625×2625 px single-page, 5250×2625 px full-spread). Generated images are suitable for ebook preview and prompt iteration; for final print-ready art, upscale or regenerate at a higher resolution via the API's aspect ratio / resolution options if your API tier supports them.

### Prompt length
The full style guide is prepended to every prompt. The combined prompt is long. Imagen 4 handles this well, but if the API returns an error citing prompt length, shorten the style guide preamble in `build_full_prompt()` inside the script.
