import { chromium } from "playwright";

const base = process.env.PREVIEW_URL ?? "http://127.0.0.1:4321";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

try {
  await page.goto(`${base}/readmitted/`, { waitUntil: "networkidle" });

  const figures = page.locator("figure.art-chart");
  const count = await figures.count();
  if (count !== 8) {
    throw new Error(`Expected 8 charts on readmitted, found ${count}`);
  }

  const switchers = await page.locator(".art-chart-mode-switch").count();
  if (switchers !== 0) {
    throw new Error(`Expected no mode switchers, found ${switchers}`);
  }

  const firstChart = figures.first();
  await firstChart.scrollIntoViewIfNeeded();
  const firstLive = firstChart.locator(".art-chart-live");
  const firstFallback = firstLive.locator(".art-chart-fallback");

  await firstFallback.waitFor({ state: "visible", timeout: 15000 });
  await page.waitForFunction(() => {
    const img = document.querySelector("figure.art-chart .art-chart-fallback");
    return !!img && img.complete && img.naturalWidth > 0;
  }, { timeout: 15000 });
  if (!(await firstFallback.isVisible())) {
    throw new Error("Static PNG fallback should be visible");
  }

  const plotly = await firstLive.evaluate(
    (live) =>
      live.classList.contains("js-plotly-plot") || !!live.querySelector(".plotly"),
  );
  if (plotly) {
    throw new Error("Charts should not load interactive Plotly");
  }

  console.log("PASS: readmitted charts render static PNG only");
} finally {
  await browser.close();
}
