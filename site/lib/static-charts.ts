import { closeSync, existsSync, openSync, readSync } from "node:fs";
import { join } from "node:path";

export function darkVariant(src: string): string | undefined {
  if (!/^\/.+\.png$/.test(src)) return undefined;
  const dark = src.replace(/\.png$/, "-dark.png");
  return existsSync(join(process.cwd(), "public", dark)) ? dark : undefined;
}

/** Width and height from the PNG header, so a lazy image reserves its space before it loads. */
export function pngSize(src: string): { width: number; height: number } | null {
  if (!/^\/.+\.png$/.test(src)) return null;
  const file = join(process.cwd(), "public", src);
  if (!existsSync(file)) return null;
  const header = Buffer.alloc(24);
  const fd = openSync(file, "r");
  try {
    readSync(fd, header, 0, 24, 0);
  } finally {
    closeSync(fd);
  }
  if (header.toString("latin1", 1, 4) !== "PNG") return null;
  return { width: header.readUInt32BE(16), height: header.readUInt32BE(20) };
}

function sizeAttrs(src: string): string {
  const size = pngSize(src);
  return size ? ` width="${size.width}" height="${size.height}"` : "";
}

/** Bake each Plotly mount into the PNG already rendered for that chart. */
export function withStaticCharts(html: string): string {
  const withCharts = html.replace(
    /<div\s+class="(art-chart-live(?:\s[^"]*)?)"([^>]*)>\s*<\/div>/g,
    (full, className: string, attrs: string) => {
      const fallback = /data-fallback="([^"]+)"/.exec(attrs)?.[1];
      if (!fallback) return full;
      const label = /aria-label="([^"]*)"/.exec(attrs)?.[1] || "Chart";
      const alt = label
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/</g, "&lt;");
      const dark = darkVariant(fallback);
      if (!dark) {
        return `<div class="${className}"${attrs}><img class="art-chart-fallback" src="${fallback}"${sizeAttrs(fallback)} alt="${alt}" loading="lazy" decoding="async" /></div>`;
      }
      return `<div class="${className} art-chart-live--themed"${attrs}><img class="art-chart-fallback art-chart-fallback--light" src="${fallback}"${sizeAttrs(fallback)} alt="${alt}" loading="lazy" decoding="async" /><img class="art-chart-fallback art-chart-fallback--dark" src="${dark}"${sizeAttrs(dark)} alt="" aria-hidden="true" loading="lazy" decoding="async" /></div>`;
    },
  );
  const withTables = withCharts.replace(/<table\b[^>]*>[\s\S]*?<\/table>/gi, (table, offset) => {
    const before = withCharts.slice(Math.max(0, offset - 160), offset);
    if (/art-table-wrap|table-scroll/.test(before)) return table;
    return `<div class="table-scroll">${table}</div>`;
  });
  return withTables.replace(
    /<div class="(art-table-wrapper|table-scroll)"(?![^>]*\btabindex=)/g,
    '<div class="$1" tabindex="0" role="region" aria-label="Data table. Scroll sideways for more columns."',
  );
}

export function jsonForScript(value: unknown): string {
  return JSON.stringify(value).replace(/</g, "\\u003c");
}

export function mediaUrl(image: unknown): string | undefined {
  if (!image) return undefined;
  if (typeof image === "string") return image;
  if (typeof image === "object" && image && "url" in image) {
    const url = (image as { url?: unknown }).url;
    if (typeof url === "string" && url) return url;
  }
  return undefined;
}

export function readingMinutes(html: string): number {
  const text = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  const words = text ? text.split(" ").length : 0;
  return Math.max(1, Math.round(words / 200));
}
