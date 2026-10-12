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

## What each slide does

`build_decks.py` composes one slide per storyboard row, plus Chomsky bookends:

- Section label in red DM Mono, top left
- Headline sentence (digits, not spelled-out numbers; no internal ids)
- **Big number** — DM Mono at ~30% of frame height, 3px `#E60000` box, spoken line as the bottom caption
- **Chart beat** — dark SVG chart (`render_dark_charts.py`): black ground, DM Sans headline, n subtitle, grey bars, red highlight box, DM Mono labels, source line. Bars reveal after the axes.
- **Entity** — logo or still on a light plate, name, figure in DM Mono when the line has one, small credit. Two or three names sit side by side when the line compares them.
- **Type card** — claim in a red box, source in DM Mono
- **Mechanism** — inline SVG (royalty flow, SKU stack, parks flywheel, roll-up, premiere pipeline). Atmosphere lines keep an image slot under `assets/ai/` and do not print the prompt id.
- One burned-in caption, bottom center. Full narration stays in speaker notes.

Dark charts are written to `articles/franchise/video/assets/charts/` and the article chart HTML paths.

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
