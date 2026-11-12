import { existsSync } from "node:fs";
import { join } from "node:path";
import { darkVariant } from "./static-charts";

export type ChartSlide = {
  id: string;
  n: number;
  src: string;
  dark?: string;
  description: string;
};

const decode = (text: string) =>
  text
    .replace(/<[^>]+>/g, "")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/\s+/g, " ")
    .trim();

/**
 * Give every chart figure an anchor and collect the slides for the chart carousel.
 * Runs on the raw body, before the Plotly mounts are baked into images.
 */
export function chartSlides(body: string): { html: string; slides: ChartSlide[] } {
  const slides: ChartSlide[] = [];
  const html = body.replace(/<figure class="art-chart"([^>]*)>([\s\S]*?)<\/figure>/g, (full, attrs: string, inner: string) => {
    const src = /data-fallback="([^"]+)"/.exec(inner)?.[1];
    if (!src || /\sid="/.test(attrs)) return full;
    const n = slides.length + 1;
    const id = `chart-${n}`;
    const label = /aria-label="([^"]*)"/.exec(inner)?.[1];
    const caption = /<figcaption[^>]*>([\s\S]*?)<\/figcaption>/.exec(inner)?.[1];
    slides.push({
      id,
      n,
      src,
      dark: darkVariant(src),
      description: decode(label || caption || `Chart ${n}`),
    });
    return `<figure class="art-chart" id="${id}"${attrs}>${inner}</figure>`;
  });
  return { html, slides };
}

/** First clause of a key-point label, so a figure box stays short. Full text stays in the report. */
export function shortLabel(label: string): string {
  const cut = label.split(/\s+\(|\.\s|;\s/)[0].trim();
  return cut.replace(/[.,]$/, "");
}

export function articleBanner(slug: string, root = process.cwd()): { src: string; width: number; height: number } | null {
  for (const name of ["banner.webp", "banner.png"]) {
    const src = `/images/content/articles/${slug}/${name}`;
    if (existsSync(join(root, "public", src))) return { src, width: 1920, height: 1080 };
  }
  return null;
}

const ARTWORK_LABELS: Record<string, string> = {
  "banner-text": "Banner",
  "cover-title": "Cover",
  "wallpaper-iphone": "Phone wallpaper",
  "wallpaper-mac": "Mac wallpaper",
};

export type ArtworkTile = { href: string; label: string; sticker: boolean };

export function artworkTiles(items: { href: string }[]): ArtworkTile[] {
  return items.map((item) => {
    const name = item.href.split("/").pop()!.replace(/\.[a-z]+$/, "");
    const sticker = item.href.includes("/stickers/");
    return {
      href: item.href,
      sticker,
      label: sticker ? `Sticker: ${name.replaceAll("-", " ")}` : ARTWORK_LABELS[name] || name.replaceAll("-", " "),
    };
  });
}
