#!/usr/bin/env python3
"""Phase 4a: fetch real assets, write asset_log.csv, ai_prompts.csv, update storyboards."""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

VIDEO_DIR = Path(__file__).resolve().parent
ASSETS_DIR = VIDEO_DIR / "assets"
CHARTS_SRC = VIDEO_DIR.resolve().parents[2] / "public/images/content/articles/franchise/charts"
UA = "ArtometricsResearch/1.0 (https://artometrics.com; franchise-video-assets)"

STORYBOARD_COLS = [
    "scene_id",
    "narration_words",
    "visual_type",
    "red_box_target",
    "count_up_number",
    "asset_id",
    "asset_file",
    "image_credit",
]

# Wikimedia file -> entity metadata (one row per downloadable asset)
WIKI_ASSETS: list[dict] = [
    {
        "asset_id": "logo_nintendo",
        "entity": "Nintendo",
        "wiki": "Nintendo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Nintendo logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_disney",
        "entity": "The Walt Disney Company",
        "wiki": "The Walt Disney Company Logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "The Walt Disney Company logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_marvel",
        "entity": "Marvel Entertainment",
        "wiki": "Marvel Studios logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Marvel wordmark, Wikimedia Commons",
    },
    {
        "asset_id": "logo_pokemon_intl",
        "entity": "Pokémon",
        "wiki": "International Pokémon logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "International Pokémon logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_pokemon_company",
        "entity": "The Pokémon Company",
        "wiki": "The Pokemon Company text logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "The Pokémon Company text logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_warner_bros",
        "entity": "Warner Bros.",
        "wiki": "Warner Bros. Pictures logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Warner Bros. Pictures logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_mattel",
        "entity": "Mattel",
        "wiki": "Mattel logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Mattel logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_universal",
        "entity": "Universal",
        "wiki": "Universal Pictures logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Universal Pictures logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_pixar",
        "entity": "Pixar",
        "wiki": "Pixar logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Pixar logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_lucasfilm",
        "entity": "Lucasfilm",
        "wiki": "Lucasfilm logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Lucasfilm logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_fox",
        "entity": "21st Century Fox",
        "wiki": "21st Century Fox logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "21st Century Fox logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_activision_blizzard",
        "entity": "Activision Blizzard",
        "wiki": "Activision Blizzard logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Activision Blizzard logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_microsoft",
        "entity": "Microsoft",
        "wiki": "Microsoft logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Microsoft logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_dc",
        "entity": "DC Entertainment",
        "wiki": "DC Comics logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "DC Comics logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_rockstar",
        "entity": "Rockstar Games",
        "wiki": "Rockstar Games Logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Rockstar Games logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_ubisoft",
        "entity": "Ubisoft",
        "wiki": "Ubisoft logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Ubisoft logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_shueisha",
        "entity": "Shueisha",
        "wiki": "Shueisha Logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "Shueisha logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_star_wars",
        "entity": "Star Wars",
        "wiki": "Star Wars Logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Star Wars logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_naruto",
        "entity": "Naruto",
        "wiki": "Naruto logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "Naruto logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_call_of_duty",
        "entity": "Call of Duty",
        "wiki": "Call of Duty logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Call of Duty logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_mortal_kombat",
        "entity": "Mortal Kombat",
        "wiki": "Mortal Kombat logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Mortal Kombat logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_angry_birds",
        "entity": "Angry Birds",
        "wiki": "Angry Birds logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Angry Birds logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_minecraft",
        "entity": "Minecraft",
        "wiki": "Minecraft Logo-en.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "Minecraft logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_ghostbusters",
        "entity": "Ghostbusters",
        "wiki": "Ghostbusters (franchise text logo).svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Ghostbusters franchise text logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_simpsons",
        "entity": "The Simpsons",
        "wiki": "The Simpsons yellow logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "The Simpsons logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_james_bond",
        "entity": "James Bond",
        "wiki": "007 Logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "James Bond 007 logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_gundam_wing",
        "entity": "Gundam",
        "wiki": "Gundam Wing logo full.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "Gundam Wing logo, Wikimedia Commons",
    },
    {
        "asset_id": "poster_hello_kitty",
        "entity": "Hello Kitty",
        "wiki": "Hello kitty cup.png",
        "type": "product shot",
        "license": "Wikimedia Commons — CC BY-SA 4.0",
        "credit_line": "Hello Kitty merchandise (cup), Wikimedia Commons",
    },
    {
        "asset_id": "poster_winnie_pooh",
        "entity": "Winnie the Pooh",
        "wiki": "The Many Adventures of Winnie the Pooh.jpg",
        "type": "poster",
        "license": "Wikimedia Commons — fair use editorial (film poster)",
        "credit_line": "The Many Adventures of Winnie the Pooh one-sheet, Wikimedia Commons",
        "fair_use": "Y",
    },
    {
        "asset_id": "poster_wizarding_world",
        "entity": "Wizarding World / Harry Potter",
        "wiki": "Goblet of Fire (Harry Potter movies).jpg",
        "type": "poster",
        "license": "Wikimedia Commons — fair use editorial (film poster)",
        "credit_line": "Harry Potter and the Goblet of Fire poster, Wikimedia Commons",
        "fair_use": "Y",
    },
    {
        "asset_id": "poster_mario_film",
        "entity": "Mario",
        "wiki": "The Super Mario Bros. Movie logo.png",
        "type": "official still",
        "license": "Wikimedia Commons — fair use editorial (film logo)",
        "credit_line": "The Super Mario Bros. Movie logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_spider_man",
        "entity": "Spider-Man",
        "wiki": "Spider-Man (Adelaide Productions) text logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Spider-Man wordmark, Wikimedia Commons",
    },
    {
        "asset_id": "logo_mcu",
        "entity": "Marvel Cinematic Universe",
        "wiki": "Marvel Studios logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Marvel Studios logo (MCU row), Wikimedia Commons",
        "notes": "Same source file as logo_marvel",
    },
    {
        "asset_id": "logo_spin_master",
        "entity": "Spin Master",
        "wiki": "Spin Master logo.png",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (corporate logo)",
        "credit_line": "Spin Master logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_smilegate",
        "entity": "CrossFire",
        "wiki": "Smilegate Logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (corporate logo)",
        "credit_line": "Smilegate logo (CrossFire publisher), Wikimedia Commons",
    },
    {
        "asset_id": "logo_dnf",
        "entity": "Dungeon Fighter Online",
        "wiki": "DNF logo.png",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (game logo)",
        "credit_line": "Dungeon Fighter Online (DNF) logo, Wikimedia Commons",
    },
    {
        "asset_id": "photo_netease",
        "entity": "Westward Journey",
        "wiki": "NetEaseHangzhouOffice.jpg",
        "type": "official still",
        "license": "Wikimedia Commons — CC BY-SA 4.0",
        "credit_line": "NetEase campus (Westward Journey publisher), Wikimedia Commons",
        "notes": "Franchise-specific art not on Commons; publisher campus photo",
    },
    {
        "asset_id": "logo_bob_builder",
        "entity": "Bob the Builder",
        "wiki": "Bob the Builder logo.png",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "Bob the Builder logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_thomas",
        "entity": "Thomas & Friends",
        "wiki": "Thomas & Friends logo 2000.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (text logo)",
        "credit_line": "Thomas & Friends logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_friends_tv",
        "entity": "Friends",
        "wiki": "Friends logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "Friends (TV) logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_assassins_creed",
        "entity": "Assassin's Creed",
        "wiki": "Assassin's Creed Revelations logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — fair use editorial (game logo)",
        "credit_line": "Assassin's Creed logo, Wikimedia Commons",
    },
    {
        "asset_id": "logo_uminn_press",
        "entity": "Marc Steinberg",
        "wiki": "University of Minnesota Press logo.svg",
        "type": "logo",
        "license": "Wikimedia Commons — Public domain (PD-textlogo)",
        "credit_line": "University of Minnesota Press logo (publisher of Anime's Media Mix), Wikimedia Commons",
        "notes": "No CC-licensed Steinberg headshot located; publisher logo for editorial context",
    },
]

# Fallback wiki filenames if primary missing
WIKI_FALLBACKS: dict[str, list[str]] = {
    "Marvel Studios logo.svg": ["Logo Marvel Rivals.svg"],
    "The Super Mario Bros. Movie logo.png": ["The Super Mario Bros Movie logo.png"],
}

ENTITY_TO_ASSET: dict[str, str] = {
    "Nintendo": "logo_nintendo",
    "The Walt Disney Company": "logo_disney",
    "Walt Disney": "logo_disney",
    "Disney Princess": "logo_disney",
    "Marvel Entertainment": "logo_marvel",
    "Marvel Cinematic Universe": "logo_mcu",
    "Pokémon": "logo_pokemon_intl",
    "The Pokémon Company": "logo_pokemon_company",
    "Warner Bros.": "logo_warner_bros",
    "Mattel": "logo_mattel",
    "Universal": "logo_universal",
    "Pixar": "logo_pixar",
    "Lucasfilm": "logo_lucasfilm",
    "21st Century Fox": "logo_fox",
    "Activision Blizzard": "logo_activision_blizzard",
    "King": "logo_king",
    "Microsoft": "logo_microsoft",
    "Minecraft": "logo_minecraft",
    "Candy Crush Saga": "logo_activision_blizzard",
    "King": "logo_activision_blizzard",
    "DC Entertainment": "logo_dc",
    "Rockstar Games": "logo_rockstar",
    "Grand Theft Auto": "logo_rockstar",
    "Ubisoft": "logo_ubisoft",
    "Shueisha": "logo_shueisha",
    "Star Wars": "logo_star_wars",
    "Naruto": "logo_naruto",
    "Call of Duty": "logo_call_of_duty",
    "Mortal Kombat": "logo_mortal_kombat",
    "Gundam": "logo_gundam_wing",
    "Angry Birds": "logo_angry_birds",
    "Ghostbusters": "logo_ghostbusters",
    "The Simpsons": "logo_simpsons",
    "James Bond": "logo_james_bond",
    "Hello Kitty": "poster_hello_kitty",
    "Winnie the Pooh": "poster_winnie_pooh",
    "Wizarding World / Harry Potter": "poster_wizarding_world",
    "Mario": "poster_mario_film",
    "Spider-Man": "logo_spider_man",
    "Spin Master": "logo_spin_master",
    "PAW Patrol": "logo_spin_master",
    "Marc Steinberg": "book_steinberg_media_mix",
    "Middle-earth / Lord of the Rings": "logo_warner_bros",
    "The Phantom of the Opera": "logo_warner_bros",
    "CrossFire": "logo_smilegate",
    "Dungeon Fighter Online": "logo_dnf",
    "Westward Journey": "photo_netease",
    "Friends": "logo_friends_tv",
    "Bob the Builder": "logo_bob_builder",
    "Thomas & Friends": "logo_thomas",
    "Assassin's Creed": "logo_assassins_creed",
    "Marc Steinberg": "logo_uminn_press",
    "Game Freak": "logo_game_freak",
    "Creatures Inc.": "logo_creatures",
    "Nexon": "logo_nexon",
    "Tencent": "logo_tencent",
    "Sony": "logo_sony",
    "LEGO": "logo_lego",
    "Peanuts": "logo_peanuts",
    "Toy Story": "logo_toy_story",
    "One Piece": "logo_one_piece",
    "Dragon Ball": "logo_dragon_ball",
    "Fast & Furious": "logo_fast_furious",
}

# Scene text triggers (longest match first)
ENTITY_TRIGGERS: list[tuple[str, str]] = sorted(
    [
        ("pokémon company", "The Pokémon Company"),
        ("pokemon company", "The Pokémon Company"),
        ("twenty-first century fox", "21st Century Fox"),
        ("marvel cinematic universe", "Marvel Cinematic Universe"),
        ("wizarding world", "Wizarding World / Harry Potter"),
        ("harry potter", "Wizarding World / Harry Potter"),
        ("fantastic beasts", "Wizarding World / Harry Potter"),
        ("hello kitty", "Hello Kitty"),
        ("winnie the pooh", "Winnie the Pooh"),
        ("call of duty", "Call of Duty"),
        ("mortal kombat", "Mortal Kombat"),
        ("candy crush", "Candy Crush Saga"),
        ("grand theft auto", "Grand Theft Auto"),
        ("bob the builder", "Bob the Builder"),
        ("thomas and friends", "Thomas & Friends"),
        ("phantom of the opera", "The Phantom of the Opera"),
        ("dungeon fighter", "Dungeon Fighter Online"),
        ("westward journey", "Westward Journey"),
        ("angry birds", "Angry Birds"),
        ("disney princess", "Disney Princess"),
        ("spider-man", "Spider-Man"),
        ("middle-earth", "Middle-earth / Lord of the Rings"),
        ("paw patrol", "PAW Patrol"),
        ("game freak", "Nintendo"),
        ("creatures", "The Pokémon Company"),
        ("steinberg", "Marc Steinberg"),
        ("pokémon", "Pokémon"),
        ("pokemon", "Pokémon"),
        ("nintendo", "Nintendo"),
        ("disney", "The Walt Disney Company"),
        ("marvel", "Marvel Entertainment"),
        ("lucasfilm", "Lucasfilm"),
        ("warner", "Warner Bros."),
        ("mattel", "Mattel"),
        ("universal", "Universal"),
        ("pixar", "Pixar"),
        ("naruto", "Naruto"),
        ("gundam", "Gundam"),
        ("minecraft", "Minecraft"),
        ("simpsons", "The Simpsons"),
        ("ghostbusters", "Ghostbusters"),
        ("star wars", "Star Wars"),
        ("mario", "Mario"),
        ("batman", "DC Entertainment"),
        ("superman", "DC Entertainment"),
        ("dceu", "DC Entertainment"),
        ("dc entertainment", "DC Entertainment"),
        ("extended dc", "DC Entertainment"),
        ("shueisha", "Shueisha"),
        ("jump", "Shueisha"),
        ("fox", "21st Century Fox"),
        ("king", "King"),
        ("activision", "Activision Blizzard"),
        ("microsoft", "Microsoft"),
        ("crossfire", "CrossFire"),
        ("james bond", "James Bond"),
        ("game freak", "Game Freak"),
        ("creatures inc", "Creatures Inc."),
        ("creatures", "Creatures Inc."),
        ("nexon", "Nexon"),
        ("tencent", "Tencent"),
        ("sony", "Sony"),
        ("lego mario", "LEGO"),
        ("lego", "LEGO"),
        ("toy story", "Toy Story"),
        ("peanuts", "Peanuts"),
        ("one piece", "One Piece"),
        ("dragon ball", "Dragon Ball"),
        ("fast & furious", "Fast & Furious"),
    ],
    key=lambda x: -len(x[0]),
)

AI_PROMPTS: list[tuple[str, str]] = [
    (
        "ai01",
        "Flat anime mechanism scene on black and white: stick-figure executives at a licensing table, red #E60000 contract highlights and blue #0047FF SKU icons, no real people, no copyrighted characters, no logos.",
    ),
    (
        "ai02",
        "Flat anime retail aisle: generic plush silhouettes and price tags, red #E60000 sale badges, blue #0047FF shelf labels, black and white background, no branded characters.",
    ),
    (
        "ai03",
        "Stylised theme-park turnstile queue with merchandise cart silhouettes, red #E60000 ticket scanner, blue #0047FF queue rails, monochrome base, no Disney or real park branding.",
    ),
    (
        "ai04",
        "Anime production-committee table: publisher, broadcaster, and toy-company icons as abstract shapes, red #E60000 revenue arrows, blue #0047FF share splits, stick figures only.",
    ),
    (
        "ai05",
        "Abstract ledger totalling one point five trillion: stacked bar silhouettes, red #E60000 merchandise slice, blue #0047FF games slice, black and white chart room, no logos.",
    ),
    (
        "ai06",
        "Mechanism diagram: theatrical premiere marquee feeding a merchandise pipeline, red #E60000 poster frame, blue #0047FF repeat-purchase loop, stick-figure audience.",
    ),
    (
        "ai07",
        "CEO stick figure at podium beside revenue stream icons, red #E60000 emphasis on merch percent, blue #0047FF on box-office slice, flat infographic style.",
    ),
    (
        "ai08",
        "Hollywood vertical stack: character silhouette, park gate, and shop awning as generic shapes, red #E60000 acquisition arrow, blue #0047FF owner HQ pin, no studio logos.",
    ),
    (
        "ai09",
        "Japan media-mix vs Hollywood parks split screen, red #E60000 on committee table, blue #0047FF on park turnstile, stick-figure economists, no IP characters.",
    ),
    (
        "ai10",
        "Wikipedia revision arrows over a franchise table silhouette, red #E60000 for upward deltas, blue #0047FF for gray revision bars, black and white UI mock.",
    ),
    (
        "ai11",
        "Partnership diagram: three company blocks feeding one Pokémon-row silhouette, red #E60000 warning on double-count, blue #0047FF on Nintendo-only label, no logos.",
    ),
    (
        "ai12",
        "UK origin map pins versus US owner HQ pins, red #E60000 origin tags, blue #0047FF headquarters tags, stick-figure analyst, no real flags or characters.",
    ),
    (
        "ai13",
        "M&A cheque mechanism: small deal price tag beside huge franchise row bar, red #E60000 price, blue #0047FF lifetime revenue, monochrome boardroom.",
    ),
    (
        "ai14",
        "Franchise slate failure: broken film-reel icon beside restarted logo placeholder shapes, red #E60000 stop sign, blue #0047FF reboot arrow, no studio marks.",
    ),
    (
        "ai15",
        "Domestic top-ten bar chart with nine franchise slots filled, red #E60000 highlight on 90 percent label, blue #0047FF year markers 2010–2024, stick-figure coder.",
    ),
    (
        "ai16",
        "Original-medium extraction layers: game, manga, film, and TV icons as stacks, red #E60000 merch layer, blue #0047FF box-office layer, flat anime infographic.",
    ),
    (
        "ai17",
        "Box-office share thin slice for mascot IP versus thick slice for film universe, red #E60000 MCU slice, blue #0047FF Hello Kitty near-zero slice, abstract mascots only.",
    ),
    (
        "ai18",
        "Revenue-per-year speedometer: Pokémon fast tick versus Hello Kitty slow tick, red #E60000 numerator, blue #0047FF denominator years, stick-figure analyst.",
    ),
    (
        "ai19",
        "Owner consolidation flowchart: separate Marvel and Lucasfilm boxes merging into Disney, red #E60000 rollup arrow, blue #0047FF consolidated total, no logos.",
    ),
    (
        "ai20",
        "DC versus Wizarding World two-column chart, red #E60000 Batman stack, blue #0047FF separate Potter stack, stick-figure lawyer, no characters.",
    ),
    (
        "ai21",
        "Selective Mario licensing: film reel, theme-park gate, and brick-toy icons with approval stamp, red #E60000 creative-control seal, blue #0047FF partner icons, generic plumber silhouette only.",
    ),
    (
        "ai22",
        "Mobile versus fighting-game correction: Mortal Kombat icon separate from mobile pile, red #E60000 small delta arrow, blue #0047FF Pokémon large delta, abstract icons.",
    ),
    (
        "ai23",
        "Vertical hook slide: question mark over two Pokémon vintage numbers, red #E60000 2019 tag, blue #0047FF 2026 tag, black and white boardroom.",
    ),
    (
        "ai24",
        "Coverage gap: empty English table rows beside missing icons, red #E60000 gap highlight, blue #0047FF Mortal Kombat low-row marker, stick-figure editor.",
    ),
    (
        "ai25",
        "Generic minimal mechanism scene: abstract shapes and arrows on black and white, red #E60000 accent box, blue #0047FF secondary accent, no people or IP.",
    ),
]


def wiki_fetch_url(filename: str) -> tuple[str, str]:
    """Return download URL and commons page URL."""
    for name in [filename] + WIKI_FALLBACKS.get(filename, []):
        api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
            {
                "action": "query",
                "titles": f"File:{name}",
                "prop": "imageinfo",
                "iiprop": "url",
                "format": "json",
            }
        )
        req = urllib.request.Request(api, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.load(resp)
        page = next(iter(data["query"]["pages"].values()))
        if "missing" in page:
            continue
        url = page["imageinfo"][0]["url"]
        page_url = f"https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(name.replace(' ', '_'))}"
        return url, page_url
    raise FileNotFoundError(f"No Wikimedia file for {filename}")


def download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def rasterize_logo(src: Path, dest_png: Path, width: int = 2000) -> None:
    if src.suffix.lower() == ".svg":
        subprocess.run(
            ["rsvg-convert", "-w", str(width), "-a", "-o", str(dest_png), str(src)],
            check=True,
        )
    elif src.suffix.lower() == ".png":
        subprocess.run(
            [
                "convert",
                str(src),
                "-resize",
                f"{width}x{width}>",
                "-background",
                "none",
                str(dest_png),
            ],
            check=True,
        )
    else:
        subprocess.run(
            [
                "convert",
                str(src),
                "-resize",
                "1600x1600>",
                "-quality",
                "80",
                str(dest_png.with_suffix(".jpg")),
            ],
            check=True,
        )


def optimize_photo(src: Path, dest_jpg: Path, max_px: int = 1600, quality: int = 80) -> None:
    subprocess.run(
        [
            "convert",
            str(src),
            "-resize",
            f"{max_px}x{max_px}>",
            "-quality",
            str(quality),
            str(dest_jpg),
        ],
        check=True,
    )


def fetch_wiki_assets() -> dict[str, dict]:
    meta_by_id: dict[str, dict] = {}
    for spec in WIKI_ASSETS:
        aid = spec["asset_id"]
        existing = ASSETS_DIR / f"{aid}.png"
        existing_jpg = ASSETS_DIR / f"{aid}.jpg"
        if existing.exists() or existing_jpg.exists():
            out_rel = f"assets/{aid}.png" if existing.exists() else f"assets/{aid}.jpg"
            meta_by_id[aid] = {**spec, "file": out_rel, "source_url": spec.get("source_url", ""), "notes": spec.get("notes", "")}
            if not meta_by_id[aid]["source_url"]:
                try:
                    _, page_url = wiki_fetch_url(spec["wiki"])
                    meta_by_id[aid]["source_url"] = page_url
                except FileNotFoundError:
                    meta_by_id[aid]["source_url"] = ""
            print(f"Skip fetch {aid} (exists)")
            continue
        wiki_name = spec["wiki"]
        raw_dir = ASSETS_DIR / "_raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        url, page_url = wiki_fetch_url(wiki_name)
        ext = Path(urllib.parse.urlparse(url).path).suffix or ".bin"
        raw_path = raw_dir / f"{aid}{ext}"
        download_file(url, raw_path)

        out_rel = f"assets/{aid}"
        notes = spec.get("notes", "")
        if spec["type"] == "logo" or ext.lower() == ".svg":
            out_path = ASSETS_DIR / f"{aid}.png"
            rasterize_logo(raw_path, out_path)
            out_rel = f"assets/{aid}.png"
        elif spec["type"] in ("poster", "official still", "product shot"):
            out_path = ASSETS_DIR / f"{aid}.jpg"
            optimize_photo(raw_path, out_path)
            out_rel = f"assets/{aid}.jpg"
        else:
            out_path = ASSETS_DIR / f"{aid}{ext}"
            shutil.copy2(raw_path, out_path)
            out_rel = f"assets/{aid}{ext}"

        fair = spec.get("fair_use", "")
        if fair == "Y":
            notes = (notes + "; fair_use=Y").strip("; ")

        meta_by_id[aid] = {
            **spec,
            "file": out_rel,
            "source_url": page_url,
            "notes": notes,
        }
        print(f"Fetched {aid} -> {out_rel}")
    return meta_by_id


def copy_chart_assets() -> dict[str, dict]:
    charts_out = ASSETS_DIR / "charts"
    charts_out.mkdir(parents=True, exist_ok=True)
    meta: dict[str, dict] = {}
    for chart in [
        "chart6_revenue_streams",
        "chart10_wiki_2019_vs_2026",
        "chart15_region_japan_us_other",
        "chart7_top10_franchise_share",
        "chart9_disney_segments_fy2024",
        "chart1_top20_revenue",
        "chart3b_disney_consolidated",
    ]:
        src = CHARTS_SRC / f"{chart}.png"
        if not src.exists():
            continue
        dest_name = f"chart_{chart}.png"
        shutil.copy2(src, charts_out / dest_name)
        aid = f"chart_{chart}"
        meta[aid] = {
            "asset_id": aid,
            "entity": chart,
            "type": "chart",
            "file": f"assets/charts/{dest_name}",
            "source_url": f"https://artometrics.com/images/content/articles/franchise/charts/{chart}.png",
            "license": "Artometrics / franchise dataset (S001)",
            "credit_line": f"Artometrics chart export — {chart}",
            "notes": "Generated by npm run brief:franchise",
        }
    return meta


def detect_entity(text: str) -> str | None:
    low = text.lower()
    for trigger, entity in ENTITY_TRIGGERS:
        if trigger in low:
            return entity
    return None


def detect_entities(text: str) -> list[str]:
    low = text.lower()
    found: list[str] = []
    seen: set[str] = set()
    for trigger, entity in ENTITY_TRIGGERS:
        if trigger in low and entity not in seen:
            found.append(entity)
            seen.add(entity)
    return found


def pick_ai_prompt(row: dict) -> str:
    blob = " ".join(
        [row.get("narration_words", ""), row.get("red_box_target", ""), row.get("visual_type", "")]
    ).lower()
    rules: list[tuple[str, str]] = [
        ("licensing", "ai01"),
        ("toy aisle", "ai02"),
        ("retail aisle", "ai02"),
        ("theme park", "ai03"),
        ("turnstile", "ai03"),
        ("production committee", "ai04"),
        ("committee", "ai04"),
        ("one point five", "ai05"),
        ("trillion", "ai05"),
        ("premiere", "ai06"),
        ("advert", "ai06"),
        ("chief executive", "ai07"),
        ("parks and shops", "ai08"),
        ("hollywood", "ai09"),
        ("japan", "ai09"),
        ("wikipedia", "ai10"),
        ("twenty-twenty-six", "ai10"),
        ("double-count", "ai11"),
        ("partner", "ai11"),
        ("united kingdom", "ai12"),
        ("burbank", "ai12"),
        ("cheque", "ai13"),
        ("billion in enterprise", "ai13"),
        ("dark universe", "ai14"),
        ("backlash", "ai14"),
        ("restarted", "ai14"),
        ("top ten", "ai15"),
        ("nine of ten", "ai15"),
        ("video games sum", "ai16"),
        ("manga origins", "ai16"),
        ("box office share", "ai17"),
        ("sixty-eight percent", "ai17"),
        ("per year", "ai18"),
        ("denominator", "ai18"),
        ("consolidat", "ai19"),
        ("fold", "ai19"),
        ("wizarding world", "ai20"),
        ("dc entertainment", "ai20"),
        ("batman", "ai20"),
        ("lego mario", "ai21"),
        ("super nintendo world", "ai21"),
        ("mortal kombat", "ai22"),
        ("mobile pile", "ai22"),
        ("which pokémon", "ai23"),
        ("which pokemon", "ai23"),
        ("coverage gap", "ai24"),
        ("english table", "ai24"),
    ]
    for key, pid in rules:
        if key in blob:
            return pid
    if "stick-figure" in blob or "mechanism" in blob:
        return "ai25"
    return "ai25"


def collect_entity_mentions() -> tuple[list[dict], dict[str, set[str]]]:
    """All storyboard rows and entity -> scene_ids where entity is named."""
    all_rows: list[dict] = []
    mentions: dict[str, set[str]] = defaultdict(set)
    for sb_path in sorted(VIDEO_DIR.glob("storyboard-*.csv")):
        for row in csv.DictReader(sb_path.open(encoding="utf-8")):
            all_rows.append(row)
            sid = row["scene_id"]
            blob = " ".join(
                [row["narration_words"], row["red_box_target"], row.get("image_credit", "")]
            )
            for ent in detect_entities(blob):
                mentions[ent].add(sid)
    return all_rows, mentions


def assign_scene_assets(
    asset_meta: dict[str, dict],
    all_rows: list[dict],
    entity_mentions: dict[str, set[str]],
) -> tuple[list[dict], dict[str, str], dict[str, str]]:
    """Return log rows, scene->asset_id map, scene->ai prompt id."""
    scene_asset: dict[str, str] = {}
    scene_ai: dict[str, str] = {}
    display_ids_by_asset: dict[str, list[str]] = defaultdict(list)
    first_mention: dict[str, str] = {}

    for ent, sids in entity_mentions.items():
        first_mention[ent] = sorted(sids)[0]

    for row in all_rows:
        sid = row["scene_id"]
        vtype = row["visual_type"]
        red = row["red_box_target"]
        blob = " ".join([row["narration_words"], red])
        ent = detect_entity(blob)

        if vtype == "chart beat":
            chart_name = red.strip()
            aid = f"chart_{chart_name}"
            if aid not in asset_meta:
                aid = "chart_chart6_revenue_streams"
            scene_asset[sid] = aid
            continue

        if vtype == "official logo":
            entity = red.strip()
            aid = ENTITY_TO_ASSET.get(entity) or ENTITY_TO_ASSET.get(ent or "", "logo_disney")
            scene_asset[sid] = aid
            continue

        if vtype in ("big number", "title card"):
            if ent and ent in ENTITY_TO_ASSET:
                scene_asset[sid] = ENTITY_TO_ASSET[ent]
            elif "disney" in blob.lower():
                scene_asset[sid] = "logo_disney"
            elif "pokémon" in blob.lower() or "pokemon" in blob.lower():
                scene_asset[sid] = "logo_pokemon_intl"
            else:
                scene_ai[sid] = pick_ai_prompt(row)
            continue

        if ent and ent in ENTITY_TO_ASSET and sid == first_mention.get(ent):
            scene_asset[sid] = ENTITY_TO_ASSET[ent]
            continue

        if ent and ent in ENTITY_TO_ASSET and prefers_entity_still(ent, row):
            scene_asset[sid] = ENTITY_TO_ASSET[ent]
            continue

        scene_ai[sid] = pick_ai_prompt(row)

    for sid, aid in scene_asset.items():
        display_ids_by_asset[aid].append(sid)

    log_rows: list[dict] = []
    for aid, meta in sorted(asset_meta.items()):
        ent = meta["entity"]
        mention_scenes = set()
        for e, sids in entity_mentions.items():
            if ENTITY_TO_ASSET.get(e) == aid or e == ent:
                mention_scenes |= sids
        scenes = ",".join(sorted(mention_scenes or display_ids_by_asset.get(aid, [])))
        log_rows.append(
            {
                "asset_id": aid,
                "scene_ids": scenes,
                "entity": meta["entity"],
                "type": meta["type"],
                "file": meta["file"],
                "source_url": meta["source_url"],
                "license": meta["license"],
                "credit_line": meta["credit_line"],
                "notes": meta.get("notes", ""),
            }
        )

    ai_scene_ids: dict[str, list[str]] = defaultdict(list)
    for sid, pid in scene_ai.items():
        ai_scene_ids[pid].append(sid)
    for pid, scenes in sorted(ai_scene_ids.items()):
        prompt = next(p for i, p in AI_PROMPTS if i == pid)
        log_rows.append(
            {
                "asset_id": pid,
                "scene_ids": ",".join(sorted(scenes)),
                "entity": "(AI illustration)",
                "type": "AI illustration (prompt only — not rendered)",
                "file": "",
                "source_url": "",
                "license": "Artometrics house style — generate at render time",
                "credit_line": "Artometrics AI prompt",
                "notes": prompt[:240],
            }
        )

    return log_rows, scene_asset, scene_ai


def prefers_entity_still(entity: str, row: dict) -> bool:
    """Use franchise still on AI scenes when the name is spoken clearly."""
    narr = row["narration_words"].lower()
    if entity == "Hello Kitty" and "hello kitty" in narr:
        return True
    if entity == "Winnie the Pooh" and "pooh" in narr:
        return True
    if entity == "Wizarding World / Harry Potter" and (
        "wizarding" in narr or "potter" in narr or "warner" in narr
    ):
        return True
    if entity == "Mario" and "mario" in narr and "nintendo" not in narr:
        return True
    if entity == "Star Wars" and "star wars" in narr:
        return True
    if entity == "Marc Steinberg" and "steinberg" in narr.lower():
        return True
    return False


def write_storyboards(scene_asset: dict[str, str], scene_ai: dict[str, str], asset_meta: dict[str, dict]) -> None:
    prompt_map = {pid: text for pid, text in AI_PROMPTS}
    for sb_path in sorted(VIDEO_DIR.glob("storyboard-*.csv")):
        rows = list(csv.DictReader(sb_path.open(encoding="utf-8")))
        out_rows = []
        for row in rows:
            sid = row["scene_id"]
            aid = scene_asset.get(sid, "")
            if not aid and sid in scene_ai:
                aid = scene_ai[sid]
            file_path = asset_meta.get(aid, {}).get("file", "") if aid in asset_meta else ""
            credit = asset_meta.get(aid, {}).get("credit_line", "") if aid in asset_meta else ""
            if sid in scene_ai and not file_path:
                credit = f"Artometrics AI — {scene_ai[sid]}: {prompt_map[scene_ai[sid]][:120]}…"
            out_rows.append(
                {
                    "scene_id": sid,
                    "narration_words": row["narration_words"],
                    "visual_type": row["visual_type"],
                    "red_box_target": row["red_box_target"],
                    "count_up_number": row.get("count_up_number", ""),
                    "asset_id": aid,
                    "asset_file": file_path,
                    "image_credit": credit,
                }
            )
        with sb_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=STORYBOARD_COLS)
            w.writeheader()
            w.writerows(out_rows)


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    asset_meta = fetch_wiki_assets()
    asset_meta.update(copy_chart_assets())
    if "logo_mcu" in asset_meta and (ASSETS_DIR / "logo_marvel.png").exists():
        shutil.copy2(ASSETS_DIR / "logo_marvel.png", ASSETS_DIR / "logo_mcu.png")
        asset_meta["logo_mcu"]["file"] = "assets/logo_mcu.png"

    from remap_storyboard_visuals import main as remap_main

    remap_main()


if __name__ == "__main__":
    main()
