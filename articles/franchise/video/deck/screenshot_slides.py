#!/usr/bin/env python3
"""
Screenshot franchise storyboard decks to PNG (Mac mini / CI).

Examples:
  python3 screenshot_slides.py --deck short --all
  python3 screenshot_slides.py --deck vertical --slide v007
  python3 screenshot_slides.py --deck short --contact-sheet
  python3 screenshot_slides.py --deck short --samples 6 --out-dir /tmp/samples
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DECK_DIR = Path(__file__).resolve().parent

SIZES = {
    "16x9": (1920, 1080),
    "9x16": (1080, 1920),
}


def find_chrome() -> str:
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        p = shutil.which(name)
        if p:
            return p
    raise RuntimeError("Chrome/Chromium not found for headless screenshots")


def slide_ids_from_html(html_path: Path) -> list[str]:
    text = html_path.read_text(encoding="utf-8")
    return re.findall(r'<section class="slide[^"]*" id="([^"]+)"', text)


def screenshot_slide_playwright(html_path: Path, slide_id: str, out_png: Path, size: tuple[int, int]) -> None:
    from playwright.sync_api import sync_playwright

    url = html_path.as_uri() + f"?capture=1&slide={slide_id}&freeze=1"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": size[0], "height": size[1]})
        page.goto(url, wait_until="networkidle", timeout=120_000)
        page.wait_for_selector("body[data-deck-ready='1']", timeout=30_000)
        page.locator(f"#{slide_id}").screenshot(path=str(out_png))
        browser.close()


def screenshot_slide_chrome(
    chrome: str,
    html_path: Path,
    slide_id: str,
    out_png: Path,
    size: tuple[int, int],
    user_data_dir: Path,
) -> None:
    url = html_path.as_uri() + f"?capture=1&slide={slide_id}&freeze=1"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--user-data-dir={user_data_dir}",
        "--virtual-time-budget=8000",
        f"--window-size={size[0]},{size[1]}",
        "--screenshot=" + str(out_png),
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        raise RuntimeError(f"Chrome screenshot failed for {slide_id}: {r.stderr[-1500:]}")


def screenshot_slide(
    html_path: Path,
    slide_id: str,
    out_png: Path,
    size: tuple[int, int],
    chrome: str | None,
    user_data_dir: Path | None,
) -> None:
    try:
        screenshot_slide_playwright(html_path, slide_id, out_png, size)
        return
    except Exception as e:
        if not chrome or not user_data_dir:
            raise
        print(f"Playwright failed ({e}); falling back to Chrome CLI", file=sys.stderr)
    screenshot_slide_chrome(chrome, html_path, slide_id, out_png, size, user_data_dir)


def deck_aspect(deck_id: str) -> str:
    return "9x16" if deck_id == "vertical" else "16x9"


def build_contact_sheet(
    pngs: list[Path],
    pdf_path: Path,
    cols: int = 4,
    rows: int = 3,
) -> None:
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError("Pillow required for contact sheets: pip install Pillow")

    per_page = cols * rows
    page_w, page_h = 2480, 3508  # A4 @ ~300dpi
    margin = 80
    gutter = 24
    cell_w = (page_w - 2 * margin - (cols - 1) * gutter) // cols
    cell_h = (page_h - 2 * margin - (rows - 1) * gutter) // rows

    pages: list[Image.Image] = []
    batch: list[Path] = []
    for p in pngs:
        batch.append(p)
        if len(batch) >= per_page:
            pages.append(_compose_page(batch, cell_w, cell_h, cols, rows, margin, gutter, page_w, page_h))
            batch = []
    if batch:
        pages.append(_compose_page(batch, cell_w, cell_h, cols, rows, margin, gutter, page_w, page_h))

    if not pages:
        return
    pages[0].save(pdf_path, "PDF", resolution=300, save_all=True, append_images=pages[1:])


def _compose_page(
    paths: list[Path],
    cell_w: int,
    cell_h: int,
    cols: int,
    rows: int,
    margin: int,
    gutter: int,
    page_w: int,
    page_h: int,
):
    from PIL import Image, ImageDraw, ImageFont

    page = Image.new("RGB", (page_w, page_h), "white")
    draw = ImageDraw.Draw(page)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except OSError:
        font = ImageFont.load_default()

    for i, path in enumerate(paths):
        row, col = divmod(i, cols)
        if row >= rows:
            break
        x = margin + col * (cell_w + gutter)
        y = margin + row * (cell_h + gutter)
        im = Image.open(path).convert("RGB")
        im.thumbnail((cell_w, cell_h - 28), Image.Resampling.LANCZOS)
        ox = x + (cell_w - im.width) // 2
        oy = y + 24
        page.paste(im, (ox, oy))
        draw.text((x, y), path.stem, fill="#333", font=font)
    return page


def pick_sample_ids(ids: list[str], n: int, html_path: Path | None = None) -> list[str]:
    """Pick representative slides: bookend + spread across visual types when possible."""
    open_id = next((i for i in ids if i.endswith("-open")), ids[0] if ids else "")
    close_id = next((i for i in ids if i.endswith("-close")), ids[-1] if ids else "")
    content = [i for i in ids if i not in (open_id, close_id)]
    if n <= 2:
        return [open_id, close_id][:n]
    if not html_path:
        step = (len(content) - 1) / max(1, n - 3)
        mid = [content[int(round(k * step))] for k in range(max(0, n - 2))]
        return [open_id] + mid[: n - 2] + [close_id]

    text = html_path.read_text(encoding="utf-8")
    by_type: dict[str, list[str]] = {}
    for sid in content:
        idx = text.find(f'id="{sid}"')
        chunk = text[idx : idx + 500] if idx >= 0 else ""
        m = re.search(r'data-visual-type="([^"]+)"', chunk)
        vt = m.group(1) if m else "other"
        by_type.setdefault(vt, []).append(sid)

    preferred = [
        "logo",
        "chart beat",
        "big-number card",
        "type card",
        "AI illustration",
        "poster",
    ]
    chosen: list[str] = [open_id]
    for vt in preferred:
        if vt in by_type and by_type[vt]:
            chosen.append(by_type[vt][0])
        if len(chosen) >= n - 1:
            break
    if len(chosen) < n - 1:
        for sid in content:
            if sid not in chosen:
                chosen.append(sid)
            if len(chosen) >= n - 1:
                break
    chosen.append(close_id)
    return chosen[:n]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", required=True, choices=["short", "deepdive", "vertical"])
    ap.add_argument("--slide", action="append", default=[], help="Scene id (repeatable)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--samples", type=int, default=0, help="Screenshot N representative slides")
    ap.add_argument("--contact-sheet", action="store_true", help="PDF contact sheet (12 per page)")
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--manifest", type=Path, default=None, help="Write JSON list of PNG paths")
    args = ap.parse_args()

    html_path = DECK_DIR / f"deck-{args.deck}.html"
    if not html_path.exists():
        print(f"Missing {html_path}; run build_decks.py first.", file=sys.stderr)
        return 1

    try:
        chrome = find_chrome()
    except RuntimeError:
        chrome = None
    aspect = deck_aspect(args.deck)
    size = SIZES[aspect]
    ids = slide_ids_from_html(html_path)

    out_dir = args.out_dir or (DECK_DIR / "png" / args.deck)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.all:
        targets = ids
    elif args.samples:
        targets = pick_sample_ids(ids, args.samples, html_path)
    elif args.slide:
        targets = args.slide
    else:
        print("Specify --all, --samples N, or --slide id", file=sys.stderr)
        return 1

    pngs: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="franchise-deck-chrome-") as chrome_profile:
        profile = Path(chrome_profile)
        for sid in targets:
            dest = out_dir / f"{sid}.png"
            print(f"Capture {sid} -> {dest}")
            screenshot_slide(html_path, sid, dest, size, chrome, profile)
            pngs.append(dest)

    if args.manifest:
        args.manifest.write_text(json.dumps([str(p) for p in pngs], indent=2), encoding="utf-8")

    if args.contact_sheet:
        all_pngs = []
        with tempfile.TemporaryDirectory(prefix="franchise-deck-chrome-") as chrome_profile:
            profile = Path(chrome_profile)
            for sid in ids:
                p = out_dir / f"{sid}.png"
                if not p.exists():
                    screenshot_slide(html_path, sid, p, size, chrome, profile)
                all_pngs.append(p)
        pdf = DECK_DIR / f"contact-sheet-{args.deck}.pdf"
        build_contact_sheet(all_pngs, pdf)
        print(f"Wrote {pdf} ({len(all_pngs)} thumbs, 12/page)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
