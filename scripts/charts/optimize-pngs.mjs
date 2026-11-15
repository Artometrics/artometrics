#!/usr/bin/env node
/**
 * Quantize chart PNGs in place (256-colour palette, same pixels to the eye).
 * Usage: node scripts/charts/optimize-pngs.mjs <dir> [<dir> ...]
 */
import { readdirSync, readFileSync, writeFileSync, statSync } from "node:fs";
import { join } from "node:path";
import sharp from "sharp";

let before = 0;
let after = 0;
for (const dir of process.argv.slice(2)) {
  for (const name of readdirSync(dir).filter((n) => n.endsWith(".png"))) {
    const file = join(dir, name);
    const input = readFileSync(file);
    const out = await sharp(input).png({ palette: true, quality: 92, effort: 8, colours: 256 }).toBuffer();
    before += input.length;
    if (out.length < input.length) {
      writeFileSync(file, out);
      after += out.length;
    } else {
      after += input.length;
    }
  }
}
console.log(`optimized: ${(before / 1024).toFixed(0)} KB -> ${(after / 1024).toFixed(0)} KB`);
