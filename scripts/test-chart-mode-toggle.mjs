import { chromium } from "playwright";

const base = process.env.PREVIEW_URL ?? "http://127.0.0.1:8081";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

try {
  await page.goto(`${base}/readmitted`, { waitUntil: "networkidle", timeout: 90000 });

  const figures = page.locator("figure.art-chart");
  const count = await figures.count();
  if (count < 5) {
    throw new Error(`Expected several charts on readmitted, found ${count}`);
  }

  const switchers = await page.locator(".art-chart-mode-switch").count();
  if (switchers !== 0) {
    throw new Error(`Expected no mode switchers, found ${switchers}`);
  }

  const firstChart = figures.first();
  await firstChart.scrollIntoViewIfNeeded();

  await page.waitForFunction(
    () => {
      const live = document.querySelector("figure.art-chart .art-chart-live");
      if (!live || live.dataset.hydrated !== "1") return false;
      return !!live.querySelector(".js-plotly-plot, .plotly");
    },
    { timeout: 30000 },
  );

  console.log("PASS: readmitted charts render interactive Plotly (exhibit chrome)");
} finally {
  await browser.close();
}
