/**
 * Economist-inspired chart pairs for Franchise.
 * A is primary. Nothing in the repo marks B or C as the template.
 * A: cream paper, ink, pink lead series + electric blue comparison (Artometrics brand; no red).
 * B: dark ground, cream ink, the same pink/blue pair.
 * C: cream paper, blue lead, pink for the secondary/comparison series.
 * The live Franchise page uses A.
 */

export const ECONOMIST_A = {
  paper: "#f7f4ee",
  ink: "#14110e",
  muted: "#5c5148",
  grid: "#e6dfd4",
  accent: "#ff3d8a",
  blue: "#0047ff",
  source: "#6b6258",
} as const;

export const ECONOMIST_B = {
  paper: "#0e1110",
  ink: "#f4f7f6",
  muted: "#b7d0cb",
  grid: "#2a3330",
  accent: "#ff3d8a",
  blue: "#0047ff",
  source: "#8fb8b2",
} as const;

export const ECONOMIST_C = {
  paper: "#f7f4ee",
  ink: "#14110e",
  muted: "#5c5148",
  grid: "#e6dfd4",
  accent: "#0047ff",
  blue: "#ff3d8a",
  source: "#6b6258",
} as const;

type Rec = Record<string, unknown>;

function asRec(v: unknown): Rec | null {
  return v && typeof v === "object" && !Array.isArray(v) ? (v as Rec) : null;
}

/** Theme A layout. Leaves series colors as authored. Opens the margins. */
export function applyEconomistALayout(rawLayout: Rec): Rec {
  const margin = asRec(rawLayout.margin) ?? {};
  const next: Rec = {
    ...rawLayout,
    paper_bgcolor: ECONOMIST_A.paper,
    plot_bgcolor: ECONOMIST_A.paper,
    font: { family: "DM Sans, Helvetica, sans-serif", size: 13, color: ECONOMIST_A.ink },
    colorway: [ECONOMIST_A.accent, ECONOMIST_A.blue, ECONOMIST_A.ink, ECONOMIST_A.muted],
    margin: {
      l: Math.max(Number(margin.l ?? 72), 64),
      r: Math.max(Number(margin.r ?? 36), 28),
      t: Math.max(Number(margin.t ?? 84), 72),
      b: Math.max(Number(margin.b ?? 72), 64),
    },
    dragmode: false,
    hovermode: "closest",
  };
  for (const [key, value] of Object.entries(rawLayout)) {
    if (!/^xaxis|^yaxis/.test(key)) continue;
    const axis = asRec(value) ?? {};
    const tick = asRec(axis.tickfont) ?? {};
    const title = asRec(axis.title) ?? {};
    next[key] = {
      ...axis,
      automargin: true,
      fixedrange: true,
      gridcolor: key.startsWith("y") && axis.side !== "left" ? ECONOMIST_A.grid : ECONOMIST_A.grid,
      linecolor: ECONOMIST_A.grid,
      zerolinecolor: ECONOMIST_A.grid,
      tickfont: { ...tick, family: "DM Sans, Helvetica, sans-serif", size: 12, color: ECONOMIST_A.ink },
      titlefont: { family: "DM Sans, Helvetica, sans-serif", size: 12, color: ECONOMIST_A.muted },
      title: {
        ...title,
        font: { family: "DM Sans, Helvetica, sans-serif", size: 12, color: ECONOMIST_A.muted },
        standoff: 12,
      },
    };
  }
  return next;
}

export function cloneTraces(data: unknown[]): Rec[] {
  return data.map((d) => {
    const t = asRec(d);
    if (!t) return {};
    const marker = asRec(t.marker);
    const line = asRec(t.line);
    return {
      ...t,
      cliponaxis: false,
      ...(marker ? { marker: { ...marker } } : {}),
      ...(line ? { line: { ...line } } : {}),
    };
  });
}
