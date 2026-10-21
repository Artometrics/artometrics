/**
 * House chart theme — Style Lab picks, applied when a chart hydrates.
 * 8C pink bars (offset shadow is CSS, not a data shift).
 * 9B area-to-zero only for a single line whose values already reach toward zero.
 * 10C scatter keeps its coordinates: red fill, cyan stroke.
 * 12A Equal Earth on geo traces. 15B recolors a series by sign only when the
 * title already says change — values are not recomputed.
 * Plotly typed arrays (`bdata`) are left untouched.
 */

export const ART_PLOTLY_FONT = "DM Mono, ui-monospace, monospace";
export const ART_PLOTLY_TITLE_FONT = "Anton, Impact, sans-serif";
export const ART_PLOTLY_BODY_FONT = "DM Sans, system-ui, sans-serif";

export const HOUSE_CHART = {
  ground: "#0e1110",
  ink: "#f4f7f6",
  muted: "#b7d0cb",
  grid: "#2a3330",
  pink: "#ff3d8a",
  tiffany: "#7fded6",
  red: "#e60000",
  cyan: "#21e4ff",
  splitRed: "#ff2a2a",
  cream: "#f3ead7",
  shadow: "#241820",
  land: "#1a1816",
  choroplethLow: "#1c3a36",
  choroplethHigh: "#9cf0e6",
} as const;

export const HOUSE_COLORWAY = [
  HOUSE_CHART.pink,
  HOUSE_CHART.tiffany,
  HOUSE_CHART.cream,
  HOUSE_CHART.red,
  HOUSE_CHART.cyan,
];

type Rec = Record<string, unknown>;

const CHANGE_RE = /year[- ]over[- ]year|\byoy\b|\bchange\b|percent change|pct change/i;
const SHARE_RE = /\bshares?\b|\bpercents?\b|%|\bcounts?\b|\bmembers\b/i;
const RED_LIKE = /e60000|ff0000|c0392b|ff3333|b03a2e|#e74c3c/i;

function asRec(v: unknown): Rec | null {
  return v && typeof v === "object" && !Array.isArray(v) ? (v as Rec) : null;
}

function textOf(v: unknown): string {
  if (typeof v === "string") return v;
  const o = asRec(v);
  if (!o) return "";
  return typeof o.text === "string" ? o.text : "";
}

/** Plain number arrays only. Typed `bdata` payloads return null. */
export function plainNumbers(v: unknown): number[] | null {
  if (!Array.isArray(v) || v.length === 0) return null;
  const out: number[] = [];
  for (const item of v) {
    if (typeof item !== "number" || !Number.isFinite(item)) return null;
    out.push(item);
  }
  return out;
}

function traceType(t: Rec): string {
  return typeof t.type === "string" ? t.type : "scatter";
}

function modeOf(t: Rec): string {
  return typeof t.mode === "string" ? t.mode : "";
}

function isBar(t: Rec): boolean {
  return traceType(t) === "bar";
}

function isHistogram(t: Rec): boolean {
  return traceType(t) === "histogram" || traceType(t) === "histogram2d";
}

function isGeo(t: Rec): boolean {
  const ty = traceType(t);
  return ty === "choropleth" || ty === "scattergeo";
}

function isLine(t: Rec): boolean {
  const ty = traceType(t);
  if (ty !== "scatter" && ty !== "scattergl") return false;
  const mode = modeOf(t);
  if (mode.includes("lines")) return true;
  return mode === "" && t.y != null && !asRec(t.marker)?.color;
}

function isMarkerScatter(t: Rec): boolean {
  const ty = traceType(t);
  if (ty !== "scatter" && ty !== "scattergl") return false;
  const mode = modeOf(t);
  return mode.includes("markers") && !mode.includes("lines");
}

function axisLabel(layout: Rec, trace?: Rec): string {
  const yKey = typeof trace?.yaxis === "string" ? trace.yaxis.replace(/^[xy]/, (a) => `${a}axis`) : "yaxis";
  const xRaw = typeof trace?.xaxis === "string" ? trace.xaxis : "x";
  const xKey = xRaw === "x" ? "xaxis" : `xaxis${xRaw.slice(1)}`;
  const yResolved = yKey === "yaxis" || yKey.startsWith("yaxis") ? yKey : "yaxis";
  return [
    textOf(asRec(layout[yResolved])?.title),
    textOf(asRec(layout[xKey])?.title),
    typeof trace?.name === "string" ? trace.name : "",
  ].join(" ");
}

function layoutSaysChange(layout: Rec): boolean {
  return CHANGE_RE.test(textOf(layout.title));
}

/**
 * Zero baseline only when it does not flatten a tight score-like scale.
 * Unknown typed arrays stay off unless the title already says share/count.
 */
export function shouldZeroBaseline(values: number[] | null, label: string): boolean {
  if (!values) return SHARE_RE.test(label);
  const min = Math.min(...values);
  const max = Math.max(...values);
  if (min <= 0) return true;
  if (max <= 0) return true;
  const span = max - min;
  if (span / max < 0.25 && min > 1) return false;
  if (min / max < 0.25) return true;
  return SHARE_RE.test(label);
}

function hexAlpha(hex: string, alpha: number): string {
  const h = hex.replace("#", "");
  const n = Number.parseInt(h, 16);
  const r = (n >> 16) & 255;
  const g = (n >> 8) & 255;
  const b = n & 255;
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function remapHighlight(colors: unknown[], highlight: string, rest: string): string[] {
  const strs = colors.map((c) => String(c));
  const hasRed = strs.some((c) => RED_LIKE.test(c));
  if (hasRed) {
    return strs.map((c) => (RED_LIKE.test(c) ? highlight : rest));
  }
  const counts = new Map<string, number>();
  for (const c of strs) counts.set(c, (counts.get(c) ?? 0) + 1);
  let rare = strs[0] ?? rest;
  let n = Infinity;
  for (const [c, count] of counts) {
    if (count < n) {
      n = count;
      rare = c;
    }
  }
  if (counts.size < 2) return strs.map(() => highlight);
  return strs.map((c) => (c === rare ? highlight : rest));
}

export type HouseTraceResult = {
  traces: Rec[];
  hasBars: boolean;
  hasGeo: boolean;
  /** Plotly axis ids (`yaxis`, `yaxis2`, `xaxis`) that should include zero. */
  zeroAxes: string[];
};

function axisId(trace: Rec, axis: "x" | "y"): string {
  const raw = trace[axis === "y" ? "yaxis" : "xaxis"];
  if (typeof raw !== "string" || raw === "x" || raw === "y") return `${axis}axis`;
  return `${axis}axis${raw.slice(1)}`;
}

export function applyHouseTraces(data: unknown[], layout: Rec): HouseTraceResult {
  const cloned: Rec[] = data.map((d) => {
    const t = asRec(d);
    if (!t) return {};
    const marker = asRec(t.marker);
    const line = asRec(t.line);
    return {
      ...t,
      ...(marker ? { marker: { ...marker } } : {}),
      ...(line ? { line: { ...line } } : {}),
    };
  });

  const lineIndexes = cloned
    .map((t, i) => (isLine(t) ? i : -1))
    .filter((i) => i >= 0);
  const stacked = cloned.some((t) => t.stackgroup != null || t.fill === "tonexty");
  const connectorCloud = lineIndexes.length > 3;
  const onlyLine = lineIndexes.length === 1 ? cloned[lineIndexes[0]] : null;
  const onlyValues = onlyLine ? plainNumbers(onlyLine.y ?? onlyLine.x) : null;
  const onlyAxis = onlyLine ? asRec(layout[axisId(onlyLine, "y")]) : null;
  const singleArea = Boolean(
    onlyLine &&
      !stacked &&
      !connectorCloud &&
      onlyAxis?.type !== "log" &&
      shouldZeroBaseline(onlyValues, axisLabel(layout, onlyLine)),
  );
  const change = layoutSaysChange(layout);
  const zeroAxes = new Set<string>();
  let barSeries = 0;
  let hasBars = false;
  let hasGeo = false;

  cloned.forEach((t, i) => {
    if (isGeo(t)) {
      hasGeo = true;
      if (traceType(t) === "choropleth") {
        t.colorscale = [
          [0, HOUSE_CHART.choroplethLow],
          [1, HOUSE_CHART.choroplethHigh],
        ];
        const marker = { ...(asRec(t.marker) ?? {}) };
        marker.line = { color: "#2c2926", width: 0.4 };
        t.marker = marker;
      }
      return;
    }

    if (isHistogram(t)) {
      const marker = { ...(asRec(t.marker) ?? {}) };
      marker.color = HOUSE_CHART.pink;
      t.marker = marker;
      zeroAxes.add(axisId(t, "y"));
      return;
    }

    if (isBar(t)) {
      hasBars = true;
      const marker = { ...(asRec(t.marker) ?? {}) };
      const horizontal = t.orientation === "h";
      const values = plainNumbers(horizontal ? t.x : t.y);
      const label = axisLabel(layout, t);
      if (change && values) {
        marker.color = values.map((n) =>
          n < 0 ? HOUSE_CHART.tiffany : n > 0 ? HOUSE_CHART.pink : HOUSE_CHART.muted,
        );
      } else if (Array.isArray(marker.color)) {
        marker.color = remapHighlight(
          marker.color as unknown[],
          HOUSE_CHART.pink,
          HOUSE_CHART.tiffany,
        );
      } else {
        marker.color = HOUSE_COLORWAY[barSeries % HOUSE_COLORWAY.length];
        barSeries += 1;
      }
      t.marker = marker;
      if (shouldZeroBaseline(values, label)) {
        zeroAxes.add(axisId(t, horizontal ? "x" : "y"));
      }
      return;
    }

    if (isLine(t)) {
      const line = { ...(asRec(t.line) ?? {}) };
      const width = typeof line.width === "number" && line.width > 0 ? line.width : 2.5;
      if (t.stackgroup != null) {
        const color = HOUSE_COLORWAY[i % HOUSE_COLORWAY.length];
        line.color = color;
        line.width = width;
        t.line = line;
        t.fillcolor = hexAlpha(color, 0.72);
        return;
      }
      if (t.fill === "tonexty") {
        line.color = HOUSE_CHART.tiffany;
        line.width = 0;
        t.line = line;
        t.fillcolor = "rgba(127, 222, 214, 0.18)";
        return;
      }
      if (connectorCloud && t.showlegend === false) {
        line.color = HOUSE_CHART.muted;
        line.width = width;
        t.line = line;
        return;
      }
      const color = singleArea
        ? HOUSE_CHART.tiffany
        : HOUSE_COLORWAY[Math.max(lineIndexes.indexOf(i), 0) % HOUSE_COLORWAY.length];
      line.color = color;
      if (singleArea) line.width = Math.max(width, 2.5);
      t.line = line;
      const marker = asRec(t.marker);
      if (marker && Array.isArray(marker.color)) {
        t.marker = {
          ...marker,
          color: remapHighlight(marker.color as unknown[], HOUSE_CHART.pink, HOUSE_CHART.tiffany),
        };
      }
      if (singleArea && t === onlyLine) {
        t.fill = "tozeroy";
        t.fillcolor = "rgba(127, 222, 214, 0.28)";
        zeroAxes.add(axisId(t, "y"));
      } else if (!stacked && t.fill && t.fill !== "none" && t.fill !== "tonexty") {
        t.fill = "none";
      }
      return;
    }

    if (isMarkerScatter(t)) {
      const marker = { ...(asRec(t.marker) ?? {}) };
      if (Array.isArray(marker.color)) {
        marker.color = remapHighlight(
          marker.color as unknown[],
          HOUSE_CHART.splitRed,
          HOUSE_CHART.tiffany,
        );
      } else {
        marker.color = HOUSE_CHART.splitRed;
      }
      marker.line = { color: HOUSE_CHART.cyan, width: 2 };
      t.marker = marker;
    }
  });

  return { traces: cloned, hasBars, hasGeo, zeroAxes: [...zeroAxes] };
}

function patchAxis(raw: unknown, zero: boolean): Rec {
  const axis = asRec(raw) ?? {};
  const tick = asRec(axis.tickfont) ?? {};
  const titlefont = asRec(axis.titlefont) ?? {};
  const next: Rec = {
    ...axis,
    gridcolor: HOUSE_CHART.grid,
    linecolor: HOUSE_CHART.muted,
    zerolinecolor: HOUSE_CHART.grid,
    tickfont: { ...tick, family: ART_PLOTLY_FONT, size: 11, color: HOUSE_CHART.ink },
    titlefont: {
      ...titlefont,
      family: ART_PLOTLY_FONT,
      size: 11,
      color: HOUSE_CHART.muted,
    },
  };
  if (!zero || axis.type === "log" || axis.type === "date" || axis.type === "category") {
    return next;
  }
  const range = axis.range;
  if (
    Array.isArray(range) &&
    range.length === 2 &&
    typeof range[0] === "number" &&
    typeof range[1] === "number"
  ) {
    next.range = [Math.min(range[0], range[1], 0), Math.max(range[0], range[1], 0)];
  } else {
    next.rangemode = "tozero";
  }
  return next;
}

export function applyHouseLayout(
  rawLayout: Rec,
  flags: { zeroAxes: string[]; hasGeo: boolean },
): Rec {
  const zero = new Set(flags.zeroAxes);
  const axisLocks: Rec = {};
  for (const [key, value] of Object.entries(rawLayout)) {
    if (/^xaxis|^yaxis/.test(key)) axisLocks[key] = patchAxis(value, zero.has(key));
  }
  for (const key of zero) {
    if (!axisLocks[key]) axisLocks[key] = patchAxis({}, true);
  }
  if (!axisLocks.xaxis) axisLocks.xaxis = patchAxis(rawLayout.xaxis, false);
  if (!axisLocks.yaxis) axisLocks.yaxis = patchAxis(rawLayout.yaxis, zero.has("yaxis"));

  let title: unknown = rawLayout.title;
  const titleRec = asRec(rawLayout.title);
  if (titleRec) {
    const font = asRec(titleRec.font) ?? {};
    title = {
      ...titleRec,
      font: {
        ...font,
        family: ART_PLOTLY_TITLE_FONT,
        size: Math.min(Number(font.size ?? 16), 18),
        color: HOUSE_CHART.cream,
      },
    };
  }

  const next: Rec = {
    ...rawLayout,
    ...axisLocks,
    paper_bgcolor: HOUSE_CHART.ground,
    plot_bgcolor: HOUSE_CHART.ground,
    font: { family: ART_PLOTLY_BODY_FONT, size: 12, color: HOUSE_CHART.ink },
    title,
    colorway: [...HOUSE_COLORWAY],
    legend: {
      ...(asRec(rawLayout.legend) ?? {}),
      font: { family: ART_PLOTLY_FONT, size: 11, color: HOUSE_CHART.muted },
      bgcolor: "rgba(0,0,0,0)",
    },
    hoverlabel: {
      bgcolor: "#121014",
      bordercolor: HOUSE_CHART.cream,
      font: { family: ART_PLOTLY_BODY_FONT, size: 12, color: HOUSE_CHART.ink },
    },
  };

  if (flags.hasGeo) {
    const geo = asRec(rawLayout.geo) ?? {};
    const projection = asRec(geo.projection) ?? {};
    next.geo = {
      ...geo,
      projection: { ...projection, type: "equal earth" },
      bgcolor: HOUSE_CHART.land,
      landcolor: HOUSE_CHART.land,
      lakecolor: HOUSE_CHART.land,
      coastlinecolor: "#2c2926",
      showframe: false,
    };
  }

  return next;
}

export function artPlotlyLayout(partial: Rec = {}) {
  return applyHouseLayout(
    { xaxis: {}, yaxis: {}, ...partial },
    { zeroAxes: [], hasGeo: false },
  );
}
