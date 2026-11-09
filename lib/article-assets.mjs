import { existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

/** Incoming text-free square. Absent until the asset handoff lands. */
export const INCOMING_SQUARE = "square-plain.webp";
/** Incoming magazine cover that keeps its typography. */
export const INCOMING_COVER = "cover-title.webp";

function file(root, slug, name) {
  return join(root, "public/images/content/articles", slug, name);
}

function url(slug, name) {
  return `/images/content/articles/${slug}/${name}`;
}

/**
 * Story-tile bitmap. HTML title is added only for the incoming text-free square.
 * Older heroes and square-text files are not marked text-free.
 */
export function storySquare(slug, hero, root = process.cwd()) {
  if (existsSync(file(root, slug, INCOMING_SQUARE))) {
    return { src: url(slug, INCOMING_SQUARE), htmlTitle: true, textStatus: "text-free" };
  }
  if (existsSync(file(root, slug, "square-text.webp"))) {
    return { src: url(slug, "square-text.webp"), htmlTitle: false, textStatus: "text-bearing" };
  }
  if (hero) return { src: hero, htmlTitle: false, textStatus: "unknown" };
  return { src: "", htmlTitle: false, textStatus: "missing" };
}

/** Magazine cover. Typography stays in the bitmap. No HTML title. */
export function coverSrc(slug, root = process.cwd()) {
  if (existsSync(file(root, slug, INCOMING_COVER))) {
    return { src: url(slug, INCOMING_COVER), textStatus: "text-bearing" };
  }
  if (existsSync(file(root, slug, "cover.webp"))) {
    return { src: url(slug, "cover.webp"), textStatus: "text-bearing" };
  }
  return { src: "", textStatus: "missing" };
}

/**
 * Display lines from the published title. "FRANCHISE: Merchandise Owns the Ledger"
 * becomes the cover word and the existing subtitle. No translation and no new claim.
 */
export function magazineLines(title) {
  const text = String(title || "").trim();
  const idx = text.indexOf(":");
  if (idx === -1) return { word: text, sub: "" };
  const word = text.slice(0, idx).trim();
  const sub = text.slice(idx + 1).trim();
  if (!word || !sub) return { word: text, sub: "" };
  return { word, sub };
}

/** Wallpaper images, sticker PNGs, and title-baked banner/cover derivatives. */
export function artworkDownloads(slug, root = process.cwd()) {
  const out = [];
  if (existsSync(file(root, slug, "banner-text.webp"))) {
    out.push({
      href: url(slug, "banner-text.webp"),
      label: "Banner image with the title in the picture",
    });
  }
  if (existsSync(file(root, slug, INCOMING_COVER))) {
    out.push({
      href: url(slug, INCOMING_COVER),
      label: "Cover image with the title in the picture",
    });
  }
  if (existsSync(file(root, slug, "wallpaper-iphone.webp"))) {
    out.push({
      href: url(slug, "wallpaper-iphone.webp"),
      label: "Phone wallpaper image",
    });
  }
  if (existsSync(file(root, slug, "wallpaper-mac.webp"))) {
    out.push({
      href: url(slug, "wallpaper-mac.webp"),
      label: "Mac wallpaper image",
    });
  }
  const stickers = join(root, "public/images/content/articles", slug, "stickers");
  if (existsSync(stickers)) {
    for (const name of readdirSync(stickers).filter((item) => item.endsWith(".png")).sort()) {
      out.push({
        href: `/images/content/articles/${slug}/stickers/${name}`,
        label: `PNG sticker art (${name.replace(/\.png$/, "").replaceAll("-", " ")}). Not a WhatsApp or iMessage pack.`,
      });
    }
  }
  return out;
}
