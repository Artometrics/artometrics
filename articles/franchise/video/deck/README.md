# Franchise video storyboard decks (Phase 4b)

HTML storyboard decks generated from `storyboard-*.csv`, styled to match the Anime explainer gold standard (black/white, `#E60000` / `#0047FF`, DM Sans + DM Mono, Chomsky bookends only).

## Build

```bash
cd articles/franchise/video/deck
python3 build_decks.py          # short, deepdive, vertical
python3 build_decks.py short    # one deck
```

Outputs:

| File | Slides |
|------|--------|
| `deck-short.html` | CSV rows + open/close bookends |
| `deck-deepdive.html` | |
| `deck-vertical.html` | 9:16 layout |

## Scene templates (`templates/`)

Ported from the Anime v4 explainer patterns (text card, chart beat, asset + credit, type/citation card, AI mechanism frame, Artometrics bookend):

- `slide-bookend.html` — Chomsky wordmark + monogram
- `slide-big-number.html` — DM Mono count-up + red box on the stat
- `slide-chart.html` — motion chart iframe + beat label
- `slide-asset.html` — logo / poster / still / product + entity on screen + credit
- `slide-type-card.html` — quote + source line
- `slide-ai.html` — `assets/ai/{prompt_id}_16x9.png` (or `_9x16` vertical) with placeholder fallback

Narration lives in `<aside class="speaker-notes">` on every slide.

## PNG export (Mac mini)

Recommended: **Playwright** (`pip install playwright && python3 -m playwright install chromium`), used automatically by `screenshot_slides.py`. Falls back to headless Chrome if Playwright is unavailable.

**1920×1080** (short/deepdive) or **1080×1920** (vertical):

```bash
python3 screenshot_slides.py --deck short --all --out-dir png/short
python3 screenshot_slides.py --deck vertical --slide v007
```

Capture one slide (no zoom, final count-up / chart frame):

`deck-short.html?capture=1&slide=s004&freeze=1`

## Contact sheet PDF

12 thumbnails per page (requires Pillow):

```bash
python3 screenshot_slides.py --deck short --all --contact-sheet
```

Writes `contact-sheet-short.pdf` (and `png/short/*.png` cache).

## Review in browser

Open `deck-short.html` in Chrome. Append `?capture=1&slide=s010` to inspect a single frame at deck resolution.
