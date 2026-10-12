import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

const base = process.env.PREVIEW_URL ?? "http://127.0.0.1:8081";
const phase = process.argv[2] ?? "before";
if (!["before", "after"].includes(phase)) {
  console.error("Usage: node scripts/capture-anaglyph-swap.mjs <before|after>");
  process.exit(1);
}

const outDir = path.join(
  process.cwd(),
  "docs/design-bible/screenshots",
  `anaglyph-swap-${phase}`,
);
fs.mkdirSync(outDir, { recursive: true });

const pages = [
  { name: "home", path: "/" },
  { name: "anime", path: "/anime" },
];

const viewports = [
  { label: "desktop-1440", width: 1440, height: 900 },
  { label: "mobile-390", width: 390, height: 844 },
];

const browser = await chromium.launch({ headless: true });

for (const vp of viewports) {
  const page = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
  for (const { name, path: route } of pages) {
    await page.goto(`${base}${route}`, { waitUntil: "networkidle", timeout: 120000 });
    if (route !== "/") {
      await page.waitForSelector(".artometrics-article-body, [role=heading]", {
        timeout: 60000,
      });
    }
    await page.waitForTimeout(800);
    const file = path.join(outDir, `${name}-${vp.label}.png`);
    await page.screenshot({ path: file, fullPage: true });
    console.log("wrote", file);
  }
  await page.close();
}

await browser.close();
console.log(`Done: ${phase} → ${outDir}`);
