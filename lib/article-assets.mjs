import { existsSync } from "node:fs";
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
