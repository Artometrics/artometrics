#!/usr/bin/env python3
"""
Free, high-fidelity neural audio narration for Artometrics articles using edge-tts.
Produces studio-grade narration with zero API keys, zero token fees, and zero GPU overhead.

Usage:
  python3 scripts/content-os/narrate-edge.py --slug anime
  npm run cos:narrate:free -- --slug anime
  npm run cos:narrate:free -- --slug readmitted --voice en-US-AriaNeural
"""

import argparse
import asyncio
import os
import re
import sys

DEFAULT_VOICE = "en-US-ChristopherNeural"  # Authority, Reliable news voice

def clean_markdown_for_speech(content: str) -> str:
    # Separate frontmatter
    title = ""
    description = ""
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            title_m = re.search(r"^title:\s*[\"']?(.*?)[\"']?$", fm, re.M)
            if title_m:
                title = title_m.group(1).strip()
            desc_m = re.search(r"^description:\s*[\"']?(.*?)[\"']?$", fm, re.M)
            if desc_m:
                description = desc_m.group(1).strip()

    # Remove script, style, chart figures, and back matter
    body = re.sub(r"<script.*?</script>", "", body, flags=re.DOTALL)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.DOTALL)
    body = re.sub(r"<figure.*?</figure>", "", body, flags=re.DOTALL)
    body = re.sub(r"<section class=\"art-back-matter\".*?</section>", "", body, flags=re.DOTALL)
    body = re.sub(r"<div class=\"art-editorial-note\".*?</div>", "", body, flags=re.DOTALL)
    body = re.sub(r"<[^>]+>", " ", body)

    # Clean markdown formatting
    body = re.sub(r"!\[.*?\]\(.*?\)", "", body)
    body = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", body)
    body = re.sub(r"#{1,6}\s*", "", body)
    body = re.sub(r"[*_`]", "", body)
    body = re.sub(r"&amp;", "and", body)
    body = re.sub(r"&lt;", "<", body)
    body = re.sub(r"&gt;", ">", body)

    # Clean redundant whitespace
    body = re.sub(r"\s+", " ", body).strip()

    intro_lead = f"{title}."
    if description and description not in body:
        intro_lead += f" {description}."
    
    full_text = f"{intro_lead} {body}"
    return full_text

async def synthesize(slug: str, voice: str, write_vtt: bool = False):
    import edge_tts

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    md_path = os.path.join(root_dir, "src/content/blog", f"{slug}.md")

    if not os.path.exists(md_path):
        print(f"Error: Markdown file not found at {md_path}", file=sys.stderr)
        sys.exit(1)

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    speech_text = clean_markdown_for_speech(content)
    out_dir = os.path.join(root_dir, "public/audios")
    os.makedirs(out_dir, exist_ok=True)
    out_audio = os.path.join(out_dir, f"{slug}.mp3")

    word_count = len(speech_text.split())
    print(f"Synthesizing narration for '{slug}' ({word_count:,} words) using voice '{voice}'...")

    communicate = edge_tts.Communicate(speech_text, voice)
    
    if write_vtt:
        vtt_path = os.path.join(out_dir, f"{slug}.vtt")
        sub_maker = edge_tts.SubMaker()
        with open(out_audio, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    sub_maker.feed(chunk)
        with open(vtt_path, "w", encoding="utf-8") as file:
            file.write(sub_maker.get_vtt())
        print(f"Exported subtitles to {vtt_path}")
    else:
        await communicate.save(out_audio)

    file_size_mb = os.path.getsize(out_audio) / (1024 * 1024)
    print(f"Exported narration: {out_audio} ({file_size_mb:.2f} MB)")

def main():
    parser = argparse.ArgumentParser(description="Free neural voice narration using Edge TTS")
    parser.add_argument("--slug", required=True, help="Article slug, e.g. anime or readmitted")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"Voice identifier (default: {DEFAULT_VOICE})")
    parser.add_argument("--vtt", action="store_true", help="Also generate WebVTT subtitles file")
    args = parser.parse_args()

    asyncio.run(synthesize(args.slug, args.voice, args.vtt))

if __name__ == "__main__":
    main()
