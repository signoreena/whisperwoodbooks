# Whisperwood Illustration Generator

Generates spread illustrations for the Whisperwood children's book series
using the OpenAI Images API (`gpt-image-2`).

---

## What it does

1. Reads the series-wide style guide from `illustrations/whisperwood-illustration-guide.md`.
2. Reads the spread prompts from `content/illustration-prompts/<book>-prompts.md`.
3. For each requested spread, extracts the **Full prompt:** section and builds a combined prompt:
   - **Style preamble** (smart extraction): art direction + only the character entries for
     characters who appear in this spread + world elements + forbidden elements. The full
     guide is not dumped into every call — only the sections that apply.
   - **Scene prompt**: the spread's Full prompt text verbatim.
4. Calls `gpt-image-2` via the OpenAI API and saves the returned image as a PNG.
5. Prints `✓ illo-01 saved` or `✗ illo-01 failed: [reason]` for each spread.
6. Prints a summary count at the end.

Output filenames match the naming convention expected by `production/place-illustrations.sh`
and `production/place-illustrations-book2.sh`, so you can run the placement script
immediately after generation.

---

## Prerequisites

- **Python 3.8 or later**
- **openai Python package**

  ```
  pip install openai
  ```

- **An OpenAI API key** — see the step-by-step guide below.

---

## How to get an OpenAI API key

You need an API key to use this script. Here is how to get one, step by step.

**Step 1 — Create an OpenAI account (if you don't have one)**

Go to https://platform.openai.com and click **Sign up**. Enter your email address
and follow the prompts. You can sign up with a Google account if that's easier.

**Step 2 — Add a payment method**

The API is not free — you pay per image generated. Before you can make API calls,
OpenAI requires a payment method on file.

- After signing in, click your profile icon (top right) → **Billing**.
- Click **Add payment method** and enter a credit or debit card.
- You can set a monthly spending limit here to avoid surprises (recommended: start
  with $10–$20 while you're experimenting).

**Step 3 — Create an API key**

- In the left sidebar, click **API keys** (or go to https://platform.openai.com/api-keys).
- Click **Create new secret key**.
- Give it a name (e.g. "Whisperwood illustrations") — this is just a label for you.
- Click **Create secret key**.
- **Copy the key immediately** — it starts with `sk-` and will look something like
  `sk-proj-abc123...`. OpenAI only shows it once. If you lose it, you can create a new one.

**Step 4 — Set the key as an environment variable (recommended)**

Rather than typing the key into every command, save it as an environment variable
so the script picks it up automatically.

On Mac or Linux, in your terminal:
```bash
export OPENAI_API_KEY="sk-proj-your-key-here"
```

To make this permanent, add that line to your `~/.zshrc` or `~/.bashrc` file,
then run `source ~/.zshrc` (or open a new terminal window).

On Windows (Command Prompt):
```
set OPENAI_API_KEY=sk-proj-your-key-here
```

---

## How to run

Run all commands from the **repo root** (the `whisperwoodbooks` folder), not from inside `scripts/`.

### Single spread

```bash
python scripts/generate-illustrations.py \
  --book book1 \
  --spread illo-01
```

### Cover illustration only

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
  --api-key sk-proj-your-key-here
```

### Arguments

| Argument | Required | Description |
|---|---|---|
| `--book` | Yes | Book identifier: `book1` through `book8` |
| `--spread` | Yes | Spread name (`illo-01`, `cover`, etc.) or `all` |
| `--api-key` | No | OpenAI API key; falls back to `OPENAI_API_KEY` env var |

If you pass an unknown spread name, the script prints the list of valid spread names
for that book and exits.

---

## Where output goes

Images are written to:

```
illustrations/<book>/<spread>.png
```

For example:

```
illustrations/book1/cover.png
illustrations/book1/illo-01.png
illustrations/book1/illo-06.png
```

These are the exact paths that the placement scripts scan. Once generation is done, run:

```bash
bash production/place-illustrations.sh        # Book 1
bash production/place-illustrations-book2.sh  # Book 2
```

The placement script copies images into the ePub source and print HTML,
rebuilds the ePub, and reports what was placed vs. still missing.

---

## Estimated cost per image

`gpt-image-2` at `high` quality, `1024×1024` size costs approximately **$0.19 per image**
as of May 2026. (OpenAI pricing can change — check https://openai.com/api/pricing for
current rates before running a large batch.)

Rough estimates for a full book:

| Spreads | Estimated cost |
|---|---|
| 1 cover + 12 spreads (Book 1) | ~$2.50 |
| Full series (8 books, ~100 spreads) | ~$19 |

These are small numbers. The more meaningful cost is your time reviewing and iterating —
plan for 2–3 generation rounds per spread to get a version you're happy with.

To reduce cost while experimenting, change `IMAGE_QUALITY = "high"` to `"medium"` at the
top of `generate-illustrations.py`. Medium quality costs roughly 60% less and is fine for
draft review.

---

## Known limitations

### Character consistency across spreads

`gpt-image-2` generates each image independently. Vera's fur shade, Pip's tunic color,
and the exact pattern on Sage's shell will vary from spread to spread even with the style
guide in every prompt. This is a fundamental limitation of text-to-image generation
without fine-tuning.

**Recommendation: generate the cover first.** The cover illustration establishes a strong
visual baseline for the whole book. Review it before generating interior spreads. If the
character designs look right on the cover, use the cover's visual language as your mental
reference when reviewing interior spreads — and note any details worth adding to the guide.
Then generate interior spreads. Plan for a consistency review pass after generation.

### Rate limits

The OpenAI API enforces per-minute rate limits. If you run `--spread all` on a long book
and hit a rate limit mid-run, the script will print the error for that spread and continue.
Re-run with the specific `--spread` name after a minute to retry failed spreads.

### Safety filters

Occasionally the API declines a generation due to automated content review, even for
benign children's book content. The script prints `✗ <spread> failed: [reason]` when
this happens. Re-running the same spread usually succeeds — safety filter results are
not fully deterministic.

### Output resolution

`gpt-image-2` at `1024×1024` may be below the minimum print resolution specified in
`illustrations/book1/NAMING-GUIDE.txt` (2625×2625 px for single-page, 5250×2625 px for
full-spread at 300 ppi). Generated images are well-suited for:

- ebook use (ePub)
- prompt iteration and review
- layout proofing

For final print-ready files, upscale the approved output using a tool such as
[Topaz Gigapixel AI](https://www.topazlabs.com/gigapixel-ai) or the free
[upscayl](https://upscayl.org) before uploading to KDP.
