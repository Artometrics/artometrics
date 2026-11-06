import { readFileSync } from "node:fs";

export type BarRow = { label: string; value: number };

type PlotlyBarFile = {
  data?: Array<{
    y?: unknown;
    x?: { dtype?: string; bdata?: string } | number[];
  }>;
};

/** Decode a Plotly float64 `bdata` payload without rounding. */
export function decodeFloat64Bdata(bdata: string): number[] {
  const buf = Buffer.from(bdata, "base64");
  const values: number[] = [];
  for (let offset = 0; offset + 8 <= buf.length; offset += 8) {
    values.push(buf.readDoubleLE(offset));
  }
  return values;
}

export function readHorizontalBars(fileUrl: URL): BarRow[] {
  const parsed = JSON.parse(readFileSync(fileUrl, "utf8")) as PlotlyBarFile;
  const trace = parsed.data?.[0];
  const labels = Array.isArray(trace?.y) ? trace.y.map((label) => String(label)) : [];
  const x = trace?.x;
  const values = Array.isArray(x)
    ? x.map((value) => Number(value))
    : x && typeof x === "object" && x.dtype === "f8" && typeof x.bdata === "string"
      ? decodeFloat64Bdata(x.bdata)
      : [];
  if (!labels.length || labels.length !== values.length) {
    throw new Error(`Could not pair labels and values in ${fileUrl.pathname}`);
  }
  return labels.map((label, index) => ({ label, value: values[index] }));
}

const LEADERS_URL = new URL(
  "../../public/data/articles/longevity/charts/chart2_leaders.plotly.json",
  import.meta.url,
);

/** Published longevity leaders series, file order preserved. */
export function longevityLeaderRows(): BarRow[] {
  const rows = readHorizontalBars(LEADERS_URL);
  const hongKong = rows.find((row) => row.label === "Hong Kong");
  if (rows.length !== 12 || !hongKong || hongKong.value.toFixed(1) !== "75.6") {
    throw new Error("Longevity leaders series does not match the published Hong Kong value 75.6");
  }
  return rows;
}

export function formatChartYears(value: number): string {
  return value.toLocaleString("en-US", {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
    useGrouping: false,
  });
}

export function longevityLeadersForDisplay(): BarRow[] {
  return longevityLeaderRows()
    .slice()
    .sort((a, b) => b.value - a.value || a.label.localeCompare(b.label));
}
