import { createElement, useEffect, useRef } from "react";
import { hydrateReferences } from "@/lib/hydrateReferences.web";
import { initArtChartChrome } from "@/lib/artChartChrome.web";
import { initArtExhibits } from "@/lib/artExhibit.web";

function showFallback(live: HTMLElement, fallback: string, label: string | null) {
  live.innerHTML = "";
  const img = document.createElement("img");
  img.src = fallback;
  img.alt = label || live.getAttribute("data-title") || "Chart";
  img.className = "art-chart-fallback";
  // Eager: lazy + SPA re-renders left charts as empty gray boxes below the fold.
  img.loading = "eager";
  img.decoding = "async";
  live.appendChild(img);
  live.style.height = "";
  live.style.minHeight = "";
  live.style.paddingTop = "";
  live.classList.add("art-chart-live--static", "art-chart-live--ready");
  live.classList.remove("art-chart-live--loading");
}

function markReady(live: HTMLElement) {
  live.classList.add("art-chart-live--ready");
  live.classList.remove("art-chart-live--loading");
  live.classList.add("art-chart-live--static");
  live.dataset.hydrated = "1";
}

function hydrateCharts(root: HTMLElement) {
  const nodes = root.querySelectorAll<HTMLElement>(".art-chart-live[data-fallback]");
  for (const live of Array.from(nodes)) {
    if (live.dataset.hydrated === "1") continue;
    const fallback = live.getAttribute("data-fallback");
    if (!fallback) continue;
    showFallback(live, fallback, live.getAttribute("aria-label"));
    markReady(live);
  }
}

/**
 * Crawlable HTML in the static export (AEO), charts enhanced client-side with static PNG exports.
 *
 * Parent theme toggles re-render this component and can reset dangerouslySetInnerHTML
 * without changing `html`, wiping hydrated chart images. We therefore re-hydrate
 * whenever unhydrated chart nodes appear.
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
        '.art-chart-live[data-fallback]:not([data-hydrated="1"])',
      );
      if (needs) hydrateCharts(node);
      hydrateReferences(node);
      initArtExhibits(node);
      initArtChartChrome(node);
    };
    const schedule = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(run);
    };

    run();
    // React may replace children after paint when ancestors re-render (theme, layout).
    const mo = new MutationObserver(schedule);
    mo.observe(node, { childList: true, subtree: true });

    return () => {
      cancelled = true;
      cancelAnimationFrame(raf);
      mo.disconnect();
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
