#!/usr/bin/env node
/**
 * Full-page QA screenshots (header to footer) at 320, 390 and 1280 px.
 * Usage: node scripts/capture-qa.mjs <outDir> [--dist dist] [--paths /,/pixar] [--themes dark,light] [--widths 320,390,1280]
 * Serves the chosen build directory itself. Run `npm run build` first.
 */
import { mkdirSync } from "node:fs";
import { join } from "node:path";
import { chromium } from "playwright";
import { startStaticServer } from "./lib/static-server.mjs";

function arg(name, fallback) {
  const at = process.argv.indexOf(`--${name}`);
  return at > -1 ? process.argv[at + 1] : fallback;
}

const out = process.argv[2] && !process.argv[2].startsWith("--") ? process.argv[2] : "docs/screenshots/after";
const dist = arg("dist", "dist");
const paths = arg("paths", "/,/pixar,/padres").split(",");
const themes = arg("themes", "dark").split(",");
const widths = arg("widths", "320,390,1280").split(",").map(Number);

mkdirSync(out, { recursive: true });
const { origin, close } = await startStaticServer(dist);
const browser = await chromium.launch();
for (const width of widths) {
  const mobile = width < 800;
  for (const theme of themes) {
    const context = await browser.newContext({
      viewport: { width, height: mobile ? 844 : 900 },
      deviceScaleFactor: 1,
      isMobile: mobile,
      hasTouch: mobile,
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
        document.querySelectorAll("img[loading=lazy]").forEach((img) => (img.loading = "eager"));
        const step = window.innerHeight * 0.8;
        for (let y = 0; y < document.body.scrollHeight; y += step) {
          window.scrollTo(0, y);
          await new Promise((r) => setTimeout(r, 60));
        }
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(500);
      const slug = path === "/" ? "home" : path.replace(/^\//, "").replace(/\//g, "-");
      const file = join(out, `${slug}-${width}-${theme}.jpg`);
      await page.screenshot({ path: file, fullPage: true, type: "jpeg", quality: 70 });
      console.log("wrote", file);
    }
    await context.close();
  }
}
await browser.close();
await close();
