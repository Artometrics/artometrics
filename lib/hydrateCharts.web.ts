/**
 * Client-side chart hydration: interactive Plotly when data-chart is present,
 * PNG fallback on failure or reduced motion.
 */
import { artPlotlyLayout, ART_PLOTLY_FONT, ART_PLOTLY_TITLE_FONT } from "@/lib/charts/plotlyTheme";

export type PlotlyLike = {
  newPlot: (
    el: HTMLElement,
    data: unknown[],
    layout?: Record<string, unknown>,
    config?: Record<string, unknown>,
  ) => Promise<unknown> | unknown;
  purge?: (el: HTMLElement) => void;
  Plots?: { resize?: (el: HTMLElement) => void };
};

declare global {
  interface Window {
    Plotly?: PlotlyLike;
  }
}

const PLOTLY_CDN =
  "https://cdn.plot.ly/plotly-2.35.2.min.js";

function prefersStaticCharts(): boolean {
  if (typeof window === "undefined") return true;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

export function loadPlotlyFromCdn(): Promise<PlotlyLike | null> {
  if (typeof window === "undefined") return Promise.resolve(null);
  if (window.Plotly) return Promise.resolve(window.Plotly);

  return new Promise((resolve) => {
    const existing = document.querySelector<HTMLScriptElement>(
      'script[data-artometrics-plotly="1"]',
    );
    if (existing) {
      existing.addEventListener("load", () => resolve(window.Plotly ?? null), {
        once: true,
      });
      existing.addEventListener("error", () => resolve(null), { once: true });
      return;
    }

    const script = document.createElement("script");
    script.src = PLOTLY_CDN;
    script.async = true;
    script.dataset.artometricsPlotly = "1";
    script.onload = () => resolve(window.Plotly ?? null);
    script.onerror = () => resolve(null);
    document.head.appendChild(script);
  });
}

function showFallback(live: HTMLElement, fallback: string, label: string | null) {
  live.innerHTML = "";
  const img = document.createElement("img");
  img.src = fallback;
  img.alt = label || live.getAttribute("data-title") || "Chart";
  img.className = "art-chart-fallback";
  img.loading = "eager";
  img.decoding = "async";
  live.appendChild(img);
  live.style.height = "";
  live.style.minHeight = "";
  live.style.paddingTop = "";
  live.classList.add("art-chart-live--static", "art-chart-live--ready");
  live.classList.remove("art-chart-live--loading");
}

export function markChartReady(live: HTMLElement, isStatic: boolean) {
  live.classList.add("art-chart-live--ready");
  live.classList.remove("art-chart-live--loading");
  live.classList.toggle("art-chart-live--static", isStatic);
  live.dataset.hydrated = "1";
}

function isDarkTheme(): boolean {
  return document.documentElement.dataset.theme === "dark";
}

function mergePlotlyLayout(
  rawLayout: Record<string, unknown>,
): Record<string, unknown> {
  const dark = isDarkTheme();
  const ink = dark ? "#FFFFFF" : "#000000";
  const grid = dark ? "#262626" : "#E5E5E5";
  const base = artPlotlyLayout({
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { family: ART_PLOTLY_FONT, size: 11, color: ink },
  });

  const axisLocks: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(rawLayout)) {
    if (!/^xaxis|^yaxis/.test(key)) continue;
    const axis = (value && typeof value === "object" ? value : {}) as Record<
      string,
      unknown
    >;
    axisLocks[key] = {
      ...axis,
      fixedrange: true,
      showgrid: axis.showgrid ?? true,
      gridcolor: axis.gridcolor ?? grid,
      zeroline: axis.zeroline ?? false,
      automargin: true,
      tickfont: {
        ...((axis.tickfont as Record<string, unknown>) ?? {}),
        family: ART_PLOTLY_FONT,
        size: 11,
        color: ink,
      },
      titlefont: {
        ...((axis.titlefont as Record<string, unknown>) ?? {}),
        family: ART_PLOTLY_FONT,
        size: 11,
        color: ink,
      },
    };
  }

  const rawTitle = rawLayout.title;
  let title = rawTitle;
  if (rawTitle && typeof rawTitle === "object") {
    const titleObj = { ...(rawTitle as Record<string, unknown>) };
    titleObj.font = {
      ...((titleObj.font as Record<string, unknown>) ?? {}),
      family: ART_PLOTLY_TITLE_FONT,
      size: Math.min(
        Number((titleObj.font as { size?: number } | undefined)?.size ?? 14),
        15,
      ),
      color: ink,
    };
    title = titleObj;
  }

  const margin = (rawLayout.margin as Record<string, number> | undefined) ?? {};
  return {
    ...base,
    ...rawLayout,
    ...axisLocks,
    title,
    margin: {
      ...margin,
      l: Math.min(Math.max(Number(margin.l ?? 56), 44), 96),
      r: Math.min(Math.max(Number(margin.r ?? 28), 16), 48),
      t: Math.min(Math.max(Number(margin.t ?? 48), 28), 72),
      b: Math.min(Math.max(Number(margin.b ?? 52), 40), 84),
    },
    colorway: ["#E60000", "#3367E7", "#000000", "#525252"],
    dragmode: false,
    hovermode: "closest",
  };
}

async function renderInteractive(live: HTMLElement, Plotly: PlotlyLike) {
  const chartUrl = live.getAttribute("data-chart");
  if (!chartUrl) throw new Error("missing data-chart");

  live.classList.add("art-chart-live--loading");
  live.querySelectorAll(".art-chart-fallback").forEach((n) => n.remove());
  live.classList.remove("art-chart-live--static");

  const res = await fetch(chartUrl);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const payload = (await res.json()) as {
    data?: unknown[];
    layout?: Record<string, unknown>;
    config?: Record<string, unknown>;
  };

  live.innerHTML = "";
  const hostWidth = Math.max(
    live.clientWidth || live.parentElement?.clientWidth || 640,
    280,
  );
  const hostHeight = Math.min(Math.max(Math.round(hostWidth * 0.58), 300), 460);

  await Plotly.newPlot(
    live,
    payload.data ?? [],
    {
      ...mergePlotlyLayout(payload.layout ?? {}),
      autosize: true,
      height: hostHeight,
    },
    {
      ...(payload.config ?? {}),
      responsive: true,
      displayModeBar: false,
      displaylogo: false,
      scrollZoom: false,
      staticPlot: false,
    },
  );

  markChartReady(live, false);
  requestAnimationFrame(() => {
    try {
      Plotly.Plots?.resize?.(live);
    } catch {
      /* ignore */
    }
  });
}

async function hydrateOne(live: HTMLElement, Plotly: PlotlyLike | null) {
  if (live.dataset.hydrated === "1") return;

  const fallback = live.getAttribute("data-fallback");
  const chartUrl = live.getAttribute("data-chart");
  const label = live.getAttribute("aria-label");

  if (prefersStaticCharts() || !chartUrl || !Plotly) {
    if (fallback) {
      showFallback(live, fallback, label);
      markChartReady(live, true);
    }
    return;
  }

  try {
    await renderInteractive(live, Plotly);
  } catch {
    if (fallback) {
      showFallback(live, fallback, label);
      markChartReady(live, true);
    }
  }
}

/** Hydrate all chart mounts under `root` (lazy via IntersectionObserver). */
export async function hydrateCharts(root: HTMLElement) {
  const nodes = root.querySelectorAll<HTMLElement>(
    ".art-chart-live[data-chart], .art-chart-live[data-fallback]",
  );
  if (!nodes.length) return;

  const pending: HTMLElement[] = [];
  for (const live of Array.from(nodes)) {
    if (live.dataset.hydrated === "1") continue;
    pending.push(live);
  }
  if (!pending.length) return;

  const Plotly = await loadPlotlyFromCdn();

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const live = entry.target as HTMLElement;
        observer.unobserve(live);
        void hydrateOne(live, Plotly);
      }
    },
    { threshold: 0, rootMargin: "120px 0px 80px 0px" },
  );

  pending.forEach((node) => {
    if (node.getAttribute("data-chart") && !prefersStaticCharts()) {
      observer.observe(node);
    } else {
      void hydrateOne(node, Plotly);
    }
  });

  const onResize = () => {
    if (!Plotly?.Plots?.resize) return;
    root.querySelectorAll<HTMLElement>(".art-chart-live .js-plotly-plot").forEach((plot) => {
      const host = plot.closest<HTMLElement>(".art-chart-live");
      if (!host) return;
      try {
        Plotly.Plots?.resize?.(host);
      } catch {
        /* ignore */
      }
    });
  };

  window.addEventListener("resize", onResize, { passive: true });
  (root as HTMLElement & { __artChartCleanup?: () => void }).__artChartCleanup =
    () => {
      observer.disconnect();
      window.removeEventListener("resize", onResize);
    };
}
