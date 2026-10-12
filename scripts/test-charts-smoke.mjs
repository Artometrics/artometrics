import { chromium } from "playwright";

const base = process.env.PREVIEW_URL ?? "http://127.0.0.1:8081";
const pages = [
  "/readmitted",
  "/yankees",
  "/anime",
];

const browser = await chromium.launch({ headless: true });
const notes = [];

async function assertCharts(page, label) {
  const figures = page.locator("figure.art-chart");
  const count = await figures.count();
  if (count < 1) throw new Error(`${label}: expected charts, found ${count}`);

  const first = figures.first();
  await first.scrollIntoViewIfNeeded();

  await page.waitForFunction(
    () => {
      const fig = document.querySelector("figure.art-chart");
      if (!fig) return false;
      const live = fig.querySelector(".art-chart-live");
      if (!live || live.dataset.hydrated !== "1") return false;
      const plotly = live.querySelector(".js-plotly-plot, .plotly");
      const img = live.querySelector(".art-chart-fallback");
      if (plotly) {
        const rect = plotly.getBoundingClientRect();
        return rect.height > 80;
      }
      if (img) return img.complete && img.naturalWidth > 0;
      return false;
    },
    { timeout: 30000 },
  );

  const switchers = await page.locator(".art-chart-mode-switch").count();
  if (switchers !== 0) {
    throw new Error(`${label}: mode switchers should be removed, found ${switchers}`);
  }

  const exhibit = await first.locator(".art-exhibit__label").count();
  if (exhibit < 1) {
    throw new Error(`${label}: expected exhibit label on first chart`);
  }

  const mode = await first.evaluate(() => {
    const live = document.querySelector("figure.art-chart .art-chart-live");
    return live?.querySelector(".js-plotly-plot, .plotly") ? "plotly" : "png";
  });

  notes.push(`PASS charts ${label} (${count} figures, first=${mode})`);
}

try {
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    for (const path of pages) {
      await page.goto(`${base}${path}`, { waitUntil: "networkidle", timeout: 90000 });
      await assertCharts(page, `desktop${path}`);
    }

    await page.goto(`${base}/readmitted`, { waitUntil: "networkidle", timeout: 90000 });
    await page.evaluate(() => {
      const cur = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = cur;
    });
    await page.waitForTimeout(800);
    await assertCharts(page, "desktop-after-data-theme-flip");
    await page.close();
  }

  {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    for (const path of pages) {
      await page.goto(`${base}${path}`, { waitUntil: "networkidle", timeout: 90000 });
      await assertCharts(page, `mobile${path}`);
      const overflow = await page.evaluate(() => {
        const doc = document.documentElement;
        return doc.scrollWidth > doc.clientWidth + 2;
      });
      if (overflow) throw new Error(`mobile${path}: horizontal overflow`);
    }
    await page.close();
  }

  console.log(notes.join("\n"));
  console.log("PASS: charts smoke (desktop + mobile + theme)");
} finally {
  await browser.close();
}
