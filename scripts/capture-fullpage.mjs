#!/usr/bin/env node
/**
 * Full-page screenshots (header to footer) for the home page and Franchise.
 * Usage: node scripts/capture-fullpage.mjs <outDir> [--paths /,/franchise]
 * Serves dist/ itself. Run `npm run build` first.
 */
import { mkdirSync } from "node:fs";
import { join } from "node:path";
import { chromium } from "playwright";
import { startStaticServer } from "./lib/static-server.mjs";

const out = process.argv[2] || "docs/screenshots/after";
const pathsArg = process.argv.indexOf("--paths");
const paths = pathsArg > -1 ? process.argv[pathsArg + 1].split(",") : ["/", "/franchise"];
const viewports = [
  { name: "mobile", width: 390, height: 844 },
  { name: "desktop", width: 1440, height: 900 },
];
const themes = ["light", "dark"];

mkdirSync(out, { recursive: true });
const { origin, close } = await startStaticServer("dist");
const browser = await chromium.launch();
for (const vp of viewports) {
  for (const theme of themes) {
    const context = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      deviceScaleFactor: 1,
      isMobile: vp.name === "mobile",
      hasTouch: vp.name === "mobile",
      reducedMotion: "reduce",
      timezoneId: "America/Los_Angeles",
    });
    await context.addInitScript((value) => {
      try { localStorage.setItem("artometrics-theme", value); } catch {}
    }, theme);
    const page = await context.newPage();
    for (const path of paths) {
      await page.goto(origin + path, { waitUntil: "networkidle" });
      await page.evaluate(async () => {
        const step = window.innerHeight * 0.8;
        for (let y = 0; y < document.body.scrollHeight; y += step) {
          window.scrollTo(0, y);
          await new Promise((r) => setTimeout(r, 60));
        }
        window.scrollTo(0, 0);
        document.querySelectorAll("img[loading=lazy]").forEach((img) => (img.loading = "eager"));
      });
      await page.waitForTimeout(500);
      const slug = path === "/" ? "home" : path.replace(/^\//, "").replace(/\//g, "-");
      const file = join(out, `${slug}-${vp.name}-${theme}.jpg`);
      await page.screenshot({ path: file, fullPage: true, type: "jpeg", quality: 72 });
      console.log("wrote", file);
    }
    await context.close();
  }
}
await browser.close();
await close();
