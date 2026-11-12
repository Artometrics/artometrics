#!/usr/bin/env node
/**
 * One chart style, two modes. Checks the shared tokens (contrast) and the rendered PNGs
 * (background matches the mode, every light chart has a dark twin). Renders the R demo when R is installed.
 */
import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, readdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const style = JSON.parse(readFileSync(join(ROOT, "scripts/charts/art-chart-style.json"), "utf8"));
let failed = 0;
const check = (ok, message) => {
  if (!ok) {
    failed += 1;
    console.error("FAIL", message);
  }
};

const lum = (hex) => {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const ratio = (a, b) => {
  const [hi, lo] = [lum(a), lum(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
};

for (const mode of ["light", "dark"]) {
  const p = style[mode];
  check(JSON.stringify(Object.keys(p)) === JSON.stringify(Object.keys(style.light)), `${mode} has the same roles as light`);
  for (const text of ["ink", "muted"]) check(ratio(p[text], p.paper) >= 4.5, `${mode} ${text} text is AA on paper (${ratio(p[text], p.paper).toFixed(2)})`);
  for (const series of ["red", "blue", "other"]) check(ratio(p[series], p.paper) >= 3, `${mode} ${series} bars are 3:1 on paper (${ratio(p[series], p.paper).toFixed(2)})`);
}

async function corner(file) {
  const { data } = await sharp(file).extract({ left: 0, top: 0, width: 1, height: 1 }).raw().toBuffer({ resolveWithObject: true });
  return `#${[...data.slice(0, 3)].map((v) => v.toString(16).padStart(2, "0")).join("")}`;
}
const close = (a, b) => [1, 3, 5].every((i) => Math.abs(parseInt(a.slice(i, i + 2), 16) - parseInt(b.slice(i, i + 2), 16)) <= 2);

const body = readFileSync(join(ROOT, "src/content/blog/franchise.md"), "utf8");
const used = [...new Set([...body.matchAll(/(?:data-fallback|src)="(\/[^"]+\.png)"/g)].map((m) => m[1]))]
  .filter((src) => /\/charts\//.test(src));
let pairs = 0;
for (const src of used) {
  const light = join(ROOT, "public", src);
  const darkSrc = src.replace(/\.png$/, "-dark.png");
  const dark = join(ROOT, "public", darkSrc);
  check(existsSync(light), `${src} exists`);
  check(existsSync(dark), `${src} has a dark twin`);
  if (!existsSync(light) || !existsSync(dark)) continue;
  pairs += 1;
  check(close(await corner(light), style.light.paper), `${src} is on the light paper`);
  check(close(await corner(dark), style.dark.paper), `${darkSrc} is on the dark paper`);
}
check(pairs >= 20, `at least 20 light/dark chart pairs (found ${pairs})`);

const hasR = spawnSync("Rscript", ["--version"], { encoding: "utf8" }).status === 0;
if (hasR) {
  const out = mkdtempSync(join(tmpdir(), "art-r-"));
  const run = spawnSync("Rscript", ["scripts/r/render-chart-style-demo.R", out], { cwd: ROOT, encoding: "utf8", env: { ...process.env, LANG: "C.UTF-8" } });
  check(run.status === 0, `R demo renders\n${run.stderr}`);
  if (run.status === 0) {
    check(close(await corner(join(out, "chart16-r.png")), style.light.paper), "R light chart is on the light paper");
    check(close(await corner(join(out, "chart16-r-dark.png")), style.dark.paper), "R dark chart is on the dark paper");
  }
} else {
  console.log("Rscript not found: skipped the R render.");
}

if (failed) process.exit(1);
console.log(`chart style ok (${pairs} chart pairs${hasR ? ", R rendered" : ""})`);
