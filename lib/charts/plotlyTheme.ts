/**
 * Shared Plotly layout defaults — anaglyph tokens (DM Mono axes).
 * Used when interactive Plotly is enabled; static PNG exports inherit exhibit chrome in CSS.
 */
export const ART_PLOTLY_FONT = "DM Mono, ui-monospace, monospace";
export const ART_PLOTLY_TITLE_FONT = "DM Sans, system-ui, sans-serif";

export function artPlotlyLayout(partial: Record<string, unknown> = {}) {
  return {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { family: ART_PLOTLY_FONT, size: 11, color: "#000000" },
    title: {
      font: { family: ART_PLOTLY_TITLE_FONT, size: 14, color: "#000000" },
    },
    xaxis: {
      gridcolor: "#E5E5E5",
      linecolor: "#000000",
      tickfont: { family: ART_PLOTLY_FONT, size: 11 },
      titlefont: { family: ART_PLOTLY_FONT, size: 11 },
    },
    yaxis: {
      gridcolor: "#E5E5E5",
      linecolor: "#000000",
      tickfont: { family: ART_PLOTLY_FONT, size: 11 },
      titlefont: { family: ART_PLOTLY_FONT, size: 11 },
    },
    colorway: ["#E60000", "#3367E7", "#000000", "#525252"],
    ...partial,
  };
}
