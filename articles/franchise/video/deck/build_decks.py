#!/usr/bin/env python3
"""Build franchise storyboard HTML decks in the Anime explainer layout."""
from __future__ import annotations

import csv
import html
import re
import sys
from pathlib import Path

DECK_DIR = Path(__file__).resolve().parent
VIDEO_DIR = DECK_DIR.parent
ASSETS = VIDEO_DIR / "assets"

DECKS = {
    "short": ("storyboard-short.csv", "16x9", "Short cut"),
    "deepdive": ("storyboard-deepdive.csv", "16x9", "Deep dive"),
    "vertical": ("storyboard-vertical.csv", "9x16", "Vertical"),
}

LOGO = "../../../../public/images/brand/chomsky-a-white.png"

from render_dark_charts import COPY as CHART_COPY  # noqa: E402

UNITS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19,
}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
SCALES = {"hundred": 100, "thousand": 1_000, "million": 1_000_000, "billion": 1_000_000_000, "trillion": 1_000_000_000_000}

ALIASES = [
    ("the pokémon company", "The Pokémon Company"),
    ("pokemon company", "The Pokémon Company"),
    ("21st century fox", "21st Century Fox"),
    ("twenty-first century fox", "21st Century Fox"),
    ("marvel cinematic universe", "Marvel Cinematic Universe"),
    ("wizarding world", "Wizarding World"),
    ("harry potter", "Wizarding World"),
    ("hello kitty", "Hello Kitty"),
    ("winnie the pooh", "Winnie the Pooh"),
    ("call of duty", "Call of Duty"),
    ("mortal kombat", "Mortal Kombat"),
    ("game freak", "Game Freak"),
    ("creatures", "Creatures Inc."),
    ("star wars", "Star Wars"),
    ("toy story", "Toy Story"),
    ("fast and furious", "Fast & Furious"),
    ("fast & furious", "Fast & Furious"),
    ("one piece", "One Piece"),
    ("dragon ball", "Dragon Ball"),
    ("bob the builder", "Bob the Builder"),
    ("thomas", "Thomas & Friends"),
    ("assassin", "Assassin's Creed"),
    ("spider-man", "Spider-Man"),
    ("spider man", "Spider-Man"),
    ("activision", "Activision Blizzard"),
    ("warner", "Warner Bros."),
    ("lucasfilm", "Lucasfilm"),
    ("pixar", "Pixar"),
    ("nintendo", "Nintendo"),
    ("disney", "The Walt Disney Company"),
    ("marvel", "Marvel Entertainment"),
    ("pokémon", "Pokémon"),
    ("pokemon", "Pokémon"),
    ("naruto", "Naruto"),
    ("sony", "Sony"),
    ("lego", "LEGO"),
    ("tencent", "Tencent"),
    ("nexon", "Nexon"),
    ("mattel", "Mattel"),
    ("ubisoft", "Ubisoft"),
    ("shueisha", "Shueisha"),
    ("minecraft", "Minecraft"),
    ("gundam", "Gundam"),
    ("peanuts", "Peanuts"),
    ("universal", "Universal"),
    ("microsoft", "Microsoft"),
]


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def load_assets() -> dict[str, dict]:
    path = ASSETS / "asset_log.csv"
    out = {}
    if not path.exists():
        return out
    for row in csv.DictReader(path.open(encoding="utf-8")):
        out[row["asset_id"]] = row
        if row.get("entity"):
            out[row["entity"]] = row
    return out


def tokenize(text: str) -> list[str]:
    return re.findall(r"[0-9]+(?:\.[0-9]+)?|[\w'’&-]+", text, flags=re.UNICODE)


def consume_number(words: list[str], i: int) -> tuple[float | None, int]:
    total = 0.0
    current = 0.0
    saw = False
    while i < len(words):
        raw = words[i].lower().strip(".,")
        w = raw.replace("twenty-", "twenty ").split()[0] if False else raw
        if w in ("and",) and saw:
            i += 1
            continue
        if w == "point" and saw:
            i += 1
            digits = ""
            while i < len(words):
                u = words[i].lower().strip(".,")
                if u in UNITS and UNITS[u] < 10:
                    digits += str(UNITS[u])
                    i += 1
                    saw = True
                else:
                    break
            if digits:
                val = total + current + float("0." + digits)
                if i < len(words) and words[i].lower().strip(".,") in SCALES:
                    val *= SCALES[words[i].lower().strip(".,")]
                    i += 1
                return val, i
            return total + current, i
        if w in UNITS:
            current += UNITS[w]
            saw = True
            i += 1
            continue
        if w in TENS:
            current += TENS[w]
            saw = True
            i += 1
            continue
        if w == "hundred":
            current = (current or 1) * 100
            saw = True
            i += 1
            continue
        if w in SCALES and w != "hundred":
            current = (current or 1) * SCALES[w]
            total += current
            current = 0
            saw = True
            i += 1
            continue
        break
    if not saw:
        return None, i
    return total + current, i


def fmt_num(n: float) -> str:
    if abs(n) >= 1_000_000_000_000:
        return f"{n / 1_000_000_000_000:.2f}".rstrip("0").rstrip(".") + "tn"
    if abs(n) >= 1_000_000_000:
        v = n / 1_000_000_000
        return f"{v:.2f}".rstrip("0").rstrip(".") + "bn"
    if abs(n) >= 1_000_000 and n >= 100_000:
        return f"{n / 1_000_000:.1f}".rstrip("0").rstrip(".") + "m"
    if abs(n - round(n)) < 0.001:
        return f"{int(round(n)):,}"
    return f"{n:.2f}".rstrip("0").rstrip(".")


def spoken_to_digits(text: str) -> str:
    text = re.sub(r"(?<=[A-Za-z])-(?=[A-Za-z])", " ", text)
    words = tokenize(text)
    out: list[str] = []
    i = 0
    while i < len(words):
        val, j = consume_number(words, i)
        if val is not None and j > i:
            piece = fmt_num(val)
            nxt = words[j].lower().strip(".,") if j < len(words) else ""
            if nxt == "percent":
                piece = piece + "%"
                j += 1
            elif nxt in ("dollar", "dollars"):
                piece = "$" + piece
                j += 1
            out.append(piece)
            i = j
        else:
            out.append(words[i])
            i += 1
    s = " ".join(out)
    s = s.replace(" ,", ",").replace(" .", ".")
    return s


def sentence(text: str) -> str:
    s = spoken_to_digits(text).strip()
    if not s:
        return ""
    s = s[0].upper() + s[1:]
    if s[-1] not in ".?!":
        s += "."
    return s


def caption(text: str) -> str:
    s = spoken_to_digits(text).strip().rstrip(".")
    words = s.split()
    if len(words) > 16:
        s = " ".join(words[:16])
    if s:
        s = s[0].upper() + s[1:]
    return s


def first_number(text: str) -> str | None:
    words = tokenize(text)
    val, j = consume_number(words, 0)
    # search anywhere
    i = 0
    while i < len(words):
        val, j = consume_number(words, i)
        if val is not None and j > i:
            return fmt_num(val)
        i += 1
    m = re.search(r"\d+(?:\.\d+)?", text)
    return m.group(0) if m else None


def section_for(narr: str, visual: str) -> str:
    n = narr.lower()
    if any(k in n for k in ("merchandise", "licensing", "retail", "box office", "video game", "percent")):
        return "THE MIX"
    if any(k in n for k in ("wikipedia", "2026", "twenty-twenty-six", "vintage", "which year", "pokémon", "pokemon", "quote")):
        return "THE YEAR"
    if any(k in n for k in ("disney", "owner", "warner", "fox", "acquisition", "subsidiary", "cheque", "marvel cost")):
        return "OWNERS"
    if any(k in n for k in ("committee", "licens", "royalt", "park", "flywheel", "advert")):
        return "THE MACHINE"
    if visual == "chart beat":
        return "THE FILE"
    if visual == "type card":
        return "THE SOURCE"
    return "THE FILE"


def entities_in(narr: str) -> list[str]:
    low = narr.lower()
    hits: list[tuple[int, str]] = []
    for needle, name in ALIASES:
        pos = low.find(needle)
        if pos >= 0:
            hits.append((pos, name))
    hits.sort()
    found: list[str] = []
    for _, name in hits:
        if name not in found:
            found.append(name)
    return found[:3]


def chart_key(asset_file: str, asset_id: str) -> str:
    blob = f"{asset_file} {asset_id}"
    m = re.search(r"chart\d+[a-z]?_[a-z0-9_]+", blob)
    if not m:
        m = re.search(r"(chart\d+[a-z]?_[a-z0-9_]+)", blob)
    if m:
        name = m.group(0)
        if name.startswith("chart_chart"):
            name = name[len("chart_") :]
        return name
    return ""


def diagram_svg(narr: str, prompt: str) -> str:
    blob = f"{narr} {prompt}".lower()
    if any(k in blob for k in ("park", "turnstile", "experiences", "flywheel")):
        return _flywheel()
    if any(k in blob for k in ("aisle", "sku", "plush", "retail", "merchandise")):
        return _sku_stack()
    if any(k in blob for k in ("committee", "publisher", "royalt", "licens", "contract")):
        return _royalty()
    if any(k in blob for k in ("cheque", "acquisition", "deal", "marvel", "lucasfilm", "consolidat")):
        return _rollup()
    if any(k in blob for k in ("premiere", "advert", "sequel", "pipeline")):
        return _pipeline()
    return _royalty()


def _box(x, y, w, h, label, sub=""):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#141414" stroke="#444" stroke-width="2"/>'
        f'<text x="{x + w/2}" y="{y + (36 if not sub else 32)}" text-anchor="middle" fill="#fff" font-size="20">{esc(label)}</text>'
        + (f'<text x="{x + w/2}" y="{y + 58}" text-anchor="middle" fill="#9a9a9a" font-size="14">{esc(sub)}</text>' if sub else "")
    )


def _royalty() -> str:
    return f'''<svg class="diagram-svg" viewBox="0 0 1400 640" xmlns="http://www.w3.org/2000/svg">
      {_box(80, 240, 280, 120, "LICENSOR", "owns the name")}
      {_box(1020, 80, 280, 100, "LICENSEE")}
      {_box(1020, 250, 280, 100, "TOY MAKER")}
      {_box(1020, 420, 280, 100, "PARK / RETAIL")}
      <line class="stage-data" x1="360" y1="300" x2="1020" y2="130" stroke="#E60000" stroke-width="3"/>
      <line class="stage-data" x1="360" y1="300" x2="1020" y2="300" stroke="#E60000" stroke-width="3"/>
      <line class="stage-data" x1="360" y1="300" x2="1020" y2="470" stroke="#0047FF" stroke-width="3"/>
      <text x="640" y="200" fill="#E60000" font-size="18">royalty</text>
      <text x="640" y="280" fill="#E60000" font-size="18">SKU licence</text>
      <text x="640" y="430" fill="#0047FF" font-size="18">gate + shelf</text>
      <circle cx="220" cy="210" r="18" fill="none" stroke="#fff" stroke-width="2"/>
      <line x1="220" y1="228" x2="220" y2="250" stroke="#fff" stroke-width="2"/>
    </svg>'''


def _sku_stack() -> str:
    bars = []
    colors = ["#6a6a6a", "#6a6a6a", "#0047FF", "#E60000", "#6a6a6a"]
    labels = ["Film", "TV", "Game", "Merch", "Music"]
    for i, (c, lab) in enumerate(zip(colors, labels)):
        h = 70 + i * 28
        if lab == "Merch":
            h = 280
        x = 180 + i * 200
        bars.append(
            f'<rect x="{x}" y="{520 - h}" width="120" height="{h}" fill="{c}"/>'
            f'<text x="{x + 60}" y="555" text-anchor="middle" fill="#ddd" font-size="18">{lab}</text>'
        )
        if lab == "Merch":
            bars.append(f'<rect x="{x - 8}" y="{520 - h - 8}" width="136" height="{h + 16}" fill="none" stroke="#E60000" stroke-width="3"/>')
    return '<svg class="diagram-svg" viewBox="0 0 1400 640" xmlns="http://www.w3.org/2000/svg">' + "".join(bars) + "</svg>"


def _flywheel() -> str:
    return '''<svg class="diagram-svg" viewBox="0 0 1400 640" xmlns="http://www.w3.org/2000/svg">
      <circle cx="700" cy="320" r="210" fill="none" stroke="#333" stroke-width="2"/>
      <circle cx="700" cy="90" r="64" fill="#141414" stroke="#E60000" stroke-width="3"/>
      <circle cx="930" cy="420" r="64" fill="#141414" stroke="#0047FF" stroke-width="3"/>
      <circle cx="470" cy="420" r="64" fill="#141414" stroke="#fff" stroke-width="2"/>
      <text x="700" y="96" text-anchor="middle" fill="#fff" font-size="16">FILM</text>
      <text x="930" y="426" text-anchor="middle" fill="#fff" font-size="16">PARK</text>
      <text x="470" y="426" text-anchor="middle" fill="#fff" font-size="16">SHELF</text>
      <path d="M760 120 C 900 160, 980 280, 960 360" fill="none" stroke="#E60000" stroke-width="3"/>
      <path d="M860 450 C 700 520, 540 480, 500 450" fill="none" stroke="#0047FF" stroke-width="3"/>
      <path d="M500 360 C 520 200, 600 120, 650 110" fill="none" stroke="#fff" stroke-width="3"/>
    </svg>'''


def _rollup() -> str:
    return f'''<svg class="diagram-svg" viewBox="0 0 1400 640" xmlns="http://www.w3.org/2000/svg">
      {_box(80, 80, 240, 90, "MARVEL")}
      {_box(80, 220, 240, 90, "LUCASFILM")}
      {_box(80, 360, 240, 90, "PIXAR")}
      {_box(80, 490, 240, 90, "FOX")}
      {_box(980, 240, 320, 140, "DISNEY", "one owner line")}
      <line x1="320" y1="125" x2="980" y2="280" stroke="#E60000" stroke-width="3"/>
      <line x1="320" y1="265" x2="980" y2="300" stroke="#E60000" stroke-width="3"/>
      <line x1="320" y1="405" x2="980" y2="330" stroke="#0047FF" stroke-width="3"/>
      <line x1="320" y1="535" x2="980" y2="360" stroke="#0047FF" stroke-width="3"/>
    </svg>'''


def _pipeline() -> str:
    return f'''<svg class="diagram-svg" viewBox="0 0 1400 640" xmlns="http://www.w3.org/2000/svg">
      {_box(60, 250, 240, 110, "PREMIERE")}
      {_box(460, 250, 240, 110, "ADVERT")}
      {_box(860, 250, 280, 110, "REPEAT SALE")}
      <line x1="300" y1="305" x2="460" y2="305" stroke="#E60000" stroke-width="3"/>
      <line x1="700" y1="305" x2="860" y2="305" stroke="#0047FF" stroke-width="3"/>
      <rect x="868" y="242" width="264" height="126" fill="none" stroke="#E60000" stroke-width="3"/>
    </svg>'''


def fact_line(narr: str) -> str:
    shown = spoken_to_digits(narr)
    m = re.search(r"(\$?\d[\d,\.]*%?(?:bn|tn|m)?)", shown)
    if not m:
        return ""
    fig = m.group(1)
    tail = shown.split(fig, 1)[1].strip(" .")
    tail = " ".join(tail.split()[:8])
    return f'<span class="fig hot">{esc(fig)}</span> <span class="dm-sans">{esc(tail)}</span>'


def render_bookend(deck_id: str, which: str, label: str) -> str:
    sid = f"{deck_id}-{which}"
    word = "Artometrics"
    return f'''<section class="slide slide-bookend" id="{sid}" data-scene-id="{sid}" data-visual-type="bookend">
      <div class="slide-frame">
        <img class="bookend-logo" src="{LOGO}" alt=""/>
        <p class="bookend-wordmark chomsky">{word}</p>
        <p class="bookend-sub dm-sans">{esc(label)}</p>
      </div>
      <aside class="speaker-notes">{which} bookend</aside>
    </section>'''


def render_row(row: dict, assets: dict[str, dict], aspect: str) -> str:
    sid = row["scene_id"]
    vt = row["visual_type"]
    narr = row["narration_words"]
    section = section_for(narr, vt)
    cap = caption(narr)
    notes = esc(narr)
    head = sentence(narr)

    if vt == "chart beat":
        key = chart_key(row.get("asset_file", ""), row.get("asset_id", ""))
        if key in CHART_COPY:
            head = CHART_COPY[key][0]
        src = f"../assets/charts/chart_{key}.html" if key else ""
        hl = ""
        num = first_number(row.get("count_up_number") or narr)
        if num:
            hl = f"?hl={esc(num)}"
        return f'''<section class="slide slide-chart" id="{sid}" data-scene-id="{sid}" data-visual-type="chart beat">
          <div class="slide-frame">
            <p class="section-label dm-mono">{esc(section)}</p>
            <h2 class="headline dm-sans">{esc(head)}</h2>
            <div class="stage chart-stage"><iframe class="chart-embed" src="{src}{hl}" title="{esc(head)}"></iframe></div>
            <p class="caption-burn dm-sans">{esc(cap)}</p>
          </div>
          <aside class="speaker-notes">{notes}</aside>
        </section>'''

    if vt == "big-number card":
        raw = row.get("count_up_number") or narr
        num = first_number(raw) or first_number(narr) or "—"
        low = narr.lower()
        if "franchise" in low:
            meaning_short = "franchises in the mid-2019 file"
        elif "percent" in low:
            meaning_short = "share of the file"
        elif "billion" in low:
            meaning_short = "billion dollars"
        elif "year" in low:
            meaning_short = "years on the clock"
        else:
            meaning_short = "the figure on this beat"
        head = f"{num} {meaning_short}."
        cap = caption(narr)
        meaning_html = "" if meaning_short.lower() in head.lower() else f'<p class="meaning dm-sans">{esc(meaning_short)}</p>'
        return f'''<section class="slide slide-bignum" id="{sid}" data-scene-id="{sid}" data-visual-type="big-number card">
          <div class="slide-frame">
            <p class="section-label dm-mono">{esc(section)}</p>
            <h2 class="headline dm-sans">{esc(head if head != sentence(narr) else meaning)}</h2>
            <div class="stage"><div class="bignum-wrap">
              <div class="red-box-target"><span class="count-up dm-mono" data-count-up="{esc(num)}">{esc(num)}</span></div>
              {meaning_html}
            </div></div>
            <p class="caption-burn dm-sans">{esc(cap)}</p>
          </div>
          <aside class="speaker-notes">{notes}</aside>
        </section>'''

    if vt in {"logo", "poster", "official still", "product shot"}:
        names = entities_in(narr)
        if not names and row.get("red_box_target"):
            names = [row["red_box_target"].split(".")[0][:48]]
        if names:
            head = sentence(narr)
        cards = []
        for name in names or ["Franchise"]:
            meta = assets.get(name) or assets.get(row.get("asset_id", "")) or {}
            src = meta.get("file") or row.get("asset_file") or ""
            rel = f"../{src}" if src else ""
            credit = meta.get("credit_line") or row.get("image_credit") or ""
            cards.append(
                f'''<figure class="entity-card">
                  <img src="{esc(rel)}" alt="{esc(name)}"/>
                  <figcaption class="entity-name dm-sans">{esc(name)}</figcaption>
                  <p class="entity-fact">{fact_line(narr)}</p>
                  <p class="entity-credit dm-mono">{esc(credit)}</p>
                </figure>'''
            )
        return f'''<section class="slide slide-entity" id="{sid}" data-scene-id="{sid}" data-visual-type="{esc(vt)}">
          <div class="slide-frame">
            <p class="section-label dm-mono">{esc(section)}</p>
            <h2 class="headline dm-sans">{esc(head)}</h2>
            <div class="stage"><div class="entity-row">{''.join(cards)}</div></div>
            <p class="caption-burn dm-sans">{esc(cap)}</p>
          </div>
          <aside class="speaker-notes">{notes}</aside>
        </section>'''

    if vt == "type card":
        source = row.get("image_credit") or row.get("red_box_target") or "Source on file"
        claim = sentence(narr)
        head = "Cite the file the figure comes from."
        cap = source if len(source) < 90 else caption(narr)
        return f'''<section class="slide slide-type" id="{sid}" data-scene-id="{sid}" data-visual-type="type card">
          <div class="slide-frame">
            <p class="section-label dm-mono">THE SOURCE</p>
            <h2 class="headline dm-sans">{esc(head)}</h2>
            <div class="stage" style="align-items:flex-start">
              <div>
                <p class="type-quote dm-sans"><span class="red-box-target">{esc(claim)}</span></p>
                <p class="type-source dm-mono">{esc(source)}</p>
              </div>
            </div>
            <p class="caption-burn dm-sans">{esc(cap)}</p>
          </div>
          <aside class="speaker-notes">{notes}</aside>
        </section>'''

    if any(k in narr.lower() for k in ("playground", "photograph", "another room", "cardboard")):
        suffix = "9x16" if aspect == "9x16" else "16x9"
        pid = row.get("asset_id") or "ai25"
        src = f"../assets/ai/{pid}_{suffix}.png"
        return f'''<section class="slide slide-atmo" id="{sid}" data-scene-id="{sid}" data-visual-type="atmosphere">
          <div class="slide-frame">
            <p class="section-label dm-mono">THE SCENE</p>
            <h2 class="headline dm-sans">{esc(sentence(narr))}</h2>
            <div class="stage"><div class="ai-stage"><img class="ai-image" src="{esc(src)}" alt=""/></div></div>
            <p class="caption-burn dm-sans">{esc(cap)}</p>
          </div>
          <aside class="speaker-notes">{notes}</aside>
        </section>'''

    # Mechanism -> SVG diagram. No prompt ids on screen.
    svg = diagram_svg(narr, row.get("asset_id", ""))
    head_d = {
        "royalty": "The licence is the business. The premiere is the advert.",
    }.get("x", head)
    if "park" in narr.lower() or "experiences" in narr.lower():
        head_d = "The character is sold again after the credits."
    elif "merchandise" in narr.lower() or "licensing" in narr.lower():
        head_d = "Licensing and the shelf outrun the ticket."
    else:
        head_d = head
    return f'''<section class="slide slide-diagram" id="{sid}" data-scene-id="{sid}" data-visual-type="diagram">
      <div class="slide-frame">
        <p class="section-label dm-mono">THE MACHINE</p>
        <h2 class="headline dm-sans">{esc(head_d)}</h2>
        <div class="stage">{svg}</div>
        <p class="caption-burn dm-sans">{esc(cap)}</p>
      </div>
      <aside class="speaker-notes">{notes}</aside>
    </section>'''


def build(deck_id: str, assets: dict[str, dict]) -> tuple[Path, int]:
    fname, aspect, label = DECKS[deck_id]
    rows = list(csv.DictReader((VIDEO_DIR / fname).open(encoding="utf-8")))
    slides = [render_bookend(deck_id, "open", label)]
    slides += [render_row(r, assets, aspect) for r in rows]
    slides.append(render_bookend(deck_id, "close", label))
    doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>Franchise storyboard — {esc(label)}</title>
<link rel="stylesheet" href="deck.css"/>
<script defer src="slide-runtime.js"></script>
</head>
<body class="deck deck-{deck_id} aspect-{aspect}" data-deck="{deck_id}" data-aspect="{aspect}">
{''.join(slides)}
</body></html>'''
    dest = DECK_DIR / f"deck-{deck_id}.html"
    dest.write_text(doc, encoding="utf-8")
    return dest, len(slides)


def main() -> int:
    assets = load_assets()
    targets = sys.argv[1:] or list(DECKS)
    for deck_id in targets:
        path, n = build(deck_id, assets)
        print(f"Wrote {path} ({n} slides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
