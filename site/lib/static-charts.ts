/** Bake each Plotly mount into the PNG already rendered for that chart. */
export function withStaticCharts(html: string): string {
  return html.replace(
    /<div\s+class="art-chart-live"([^>]*)>\s*<\/div>/g,
    (full, attrs: string) => {
      const fallback = /data-fallback="([^"]+)"/.exec(attrs)?.[1];
      if (!fallback) return full;
      const label = /aria-label="([^"]*)"/.exec(attrs)?.[1] || "Chart";
      const alt = label
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/</g, "&lt;");
      return `<div class="art-chart-live"${attrs}><img class="art-chart-fallback" src="${fallback}" alt="${alt}" loading="lazy" decoding="async" /></div>`;
    },
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
