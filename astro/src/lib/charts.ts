function attr(source: string, name: string): string {
  const match = source.match(new RegExp(`${name}="([^"]*)"`, "i"));
  return match?.[1] ?? "";
}

function escapeAttr(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;");
}

/** Replace Plotly mounts with a static image plus an on-demand interactive island. */
export function withChartIslands(html: string): string {
  const withCharts = html.replace(
    /<div\b(?=[^>]*\bclass="art-chart-live\b)([^>]*)>\s*<\/div>/gi,
    (_full, rawAttrs: string) => {
      const chart = attr(rawAttrs, "data-chart");
      const fallback = attr(rawAttrs, "data-fallback");
      const label = attr(rawAttrs, "aria-label") || "Data chart";
      const source = attr(rawAttrs, "data-source");
      const img = fallback
        ? `<img class="chart-still" src="${escapeAttr(fallback)}" alt="${escapeAttr(label)}" loading="lazy" decoding="async" />`
        : `<p class="chart-missing">Chart image unavailable.</p>`;
      const sourceHtml = source ? `<p class="chart-source">${escapeAttr(source)}</p>` : "";
      const button = chart
        ? `<button type="button" class="chart-open">Open interactive chart</button><div class="chart-plot" hidden></div>`
        : "";
      return `<div class="chart-island" data-chart="${escapeAttr(chart)}">${img}${sourceHtml}${button}</div>`;
    },
  );
  return withCharts.replace(/<img\b(?![^>]*\bloading=)/gi, '<img loading="lazy" decoding="async" ');
}
