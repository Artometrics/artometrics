#!/usr/bin/env node
/**
 * Single-A logo assets must not be clipped. Every raster is decoded and every SVG is
 * rasterised; no non-transparent pixel may sit on the outer edge of the canvas, and the
 * ink must keep a small transparent margin so the shape is visibly whole.
 */
import { readdirSync } from "node:fs";
import { join } from "node:path";
import sharp from "sharp";

const ROOT = new URL("..", import.meta.url).pathname;
const MIN_MARGIN = 0.04;
let failed = 0;

async function edgeReport(input, label, size) {
  const base = sharp(input, { density: 192 });
  const { data, info } = await (size ? base.resize(size, size, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } }) : base)
    .ensureAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });
  const { width, height } = info;
  let minX = width;
  let minY = height;
  let maxX = -1;
  let maxY = -1;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      if (data[(y * width + x) * 4 + 3] > 0) {
        if (x < minX) minX = x;
        if (y < minY) minY = y;
        if (x > maxX) maxX = x;
        if (y > maxY) maxY = y;
      }
    }
  }
  const problems = [];
  if (maxX < 0) problems.push("empty image");
  else {
    const margin = {
      top: minY / height,
      bottom: (height - 1 - maxY) / height,
      left: minX / width,
      right: (width - 1 - maxX) / width,
    };
    for (const [side, value] of Object.entries(margin)) {
      if (value === 0) problems.push(`ink touches ${side} edge`);
      else if (value < MIN_MARGIN) problems.push(`${side} margin ${(value * 100).toFixed(1)}% < ${MIN_MARGIN * 100}%`);
    }
  }
  if (problems.length) {
    failed += 1;
    console.error(`✗ ${label} (${width}x${height}): ${problems.join("; ")}`);
  } else {
    console.log(`✓ ${label} (${width}x${height})`);
  }
}

const VARIANTS = ["white", "svg", "halftone", "d01", "d02", "d03", "d04", "d05", "d06", "d07", "d08"];
const files = [];
for (const id of VARIANTS) {
  for (const theme of ["night", "day"]) {
    for (const size of [32, 180]) files.push(`/images/brand/monograms/${id}-${theme}-${size}.png`);
  }
}
const dir = join(ROOT, "public/images/brand/monograms");
for (const name of readdirSync(dir).filter((n) => n.endsWith(".png"))) files.push(`/images/brand/monograms/${name}`);
for (const rel of [...new Set(files)].sort()) await edgeReport(join(ROOT, "public", rel), rel);

const svgDir = join(ROOT, "public/images/brand/svg");
for (const name of readdirSync(svgDir).filter((n) => /^monogram-a-.*\.svg$/.test(n))) {
  await edgeReport(join(svgDir, name), `/images/brand/svg/${name}`, 256);
}

const present = new Set(files.filter((f) => f.startsWith("/images/brand/monograms/")));
if (present.size !== VARIANTS.length * 4) {
  failed += 1;
  console.error(`✗ expected ${VARIANTS.length * 4} monogram files, found ${present.size}`);
}
if (failed) {
  console.error(`logo clipping: ${failed} failure(s)`);
  process.exit(1);
}
console.log(`logos OK (${present.size} monograms, ${VARIANTS.length} colour variants, night + day)`);
