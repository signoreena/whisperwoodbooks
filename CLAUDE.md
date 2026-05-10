# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Site overview

Static single-page website for **Whisperwood Books** (whisperwoodbooks.com), a children's book series for ages 4–6. Deployed via GitHub Pages using the `CNAME` file for the custom domain.

## Architecture

The entire site lives in one file: **`index.html`** — all HTML, CSS (inline `<style>` block), and layout in a single document. There is no JavaScript, no build step, no package manager, and no external stylesheet.

Character portrait images (`Vera.png`, `Pip.png`, `Sage.png`) are referenced directly from the repo root. Background/scene images are loaded from Unsplash CDN URLs embedded in the HTML.

## Fonts & design tokens

- Fonts: **Playfair Display** (headings) and **EB Garamond** (body) via Google Fonts
- Color palette defined as CSS custom properties at `:root` — parchment tones (`--parchment`, `--parchment-mid`, `--parchment-dark`), forest greens (`--forest-deep` through `--forest-pale`), and gold accents (`--gold-deep` through `--gold-pale`)

## Page sections

`index.html` is organized into five landmark sections in order: **Hero → Quote strip → Characters → Books → World → Footer**. Each section uses `.section-inner` (max-width 1100px) for layout containment.

## Deploying changes

Push to `main` — GitHub Pages serves the site automatically. No build or compile step needed.
