import { createElement, useEffect, useRef } from "react";
import { hydrateReferences } from "@/lib/hydrateReferences.web";
import { initArtChartChrome } from "@/lib/artChartChrome.web";
import { initArtExhibits } from "@/lib/artExhibit.web";
import { hydrateCharts } from "@/lib/hydrateCharts.web";

/**
 * Crawlable HTML in the static export (AEO); charts enhanced client-side with
 * interactive Plotly (anaglyph theme) and PNG fallback.
 */
export function ArticleBody({ html }: { html: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;

    let cancelled = false;
    let raf = 0;
    const run = () => {
      if (cancelled) return;
      const needs = node.querySelector(
        '.art-chart-live:not([data-hydrated="1"])',
      );
      if (needs) void hydrateCharts(node);
      hydrateReferences(node);
      initArtExhibits(node);
      initArtChartChrome(node);
    };
    const schedule = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(run);
    };

    run();
    const mo = new MutationObserver(schedule);
    mo.observe(node, { childList: true, subtree: true });

    return () => {
      cancelled = true;
      cancelAnimationFrame(raf);
      mo.disconnect();
      const cleanup = (node as HTMLElement & { __artChartCleanup?: () => void })
        .__artChartCleanup;
      cleanup?.();
    };
  }, [html]);

  return createElement("div", {
    ref,
    className: "artometrics-article-body w-full min-w-0 flex-1 shrink",
    dangerouslySetInnerHTML: { __html: html },
    suppressHydrationWarning: true,
    style: { width: "100%", minWidth: 0, alignSelf: "stretch" },
  });
}
