/**
 * Isolate the leading Chomsky A from each header wordmark.
 * Night keeps the white face. Day recolours only the near-white face to ink
 * so the mark reads on a light tab. Extrusion colours stay.
 */
import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";
import sharp from "sharp";

const root = new URL("..", import.meta.url).pathname;
const outDir = join(root, "public/images/brand/monograms");

const marks = [
  ["white", "public/images/brand/wordmarks/wordmark-white.webp"],
  ["svg", "public/images/brand/wordmarks/wordmark-white.svg"],
  ["halftone", "public/images/brand/wordmarks/wordmark-halftone.webp"],
  ["d01", "public/images/brand/wordmarks/wordmark-01-dotted-extrude.webp"],
  ["d02", "public/images/brand/wordmarks/wordmark-02-dotted-long-shadow.webp"],
  ["d03", "public/images/brand/wordmarks/wordmark-03-pink-blue-bands.webp"],
  ["d04", "public/images/brand/wordmarks/wordmark-04-dot-ring.webp"],
  ["d05", "public/images/brand/wordmarks/wordmark-05-dots-fade.webp"],
  ["d06", "public/images/brand/wordmarks/wordmark-06-blue-on-pink.webp"],
  ["d07", "public/images/brand/wordmarks/wordmark-07-blue-lip.webp"],
  ["d08", "public/images/brand/wordmarks/wordmark-08-riso.webp"],
];

function cropA(data, width, height, channels) {
  let minX = width;
  let minY = height;
  let maxX = 0;
  let maxY = 0;
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      if (data[(y * width + x) * channels + 3] > 30) {
        if (x < minX) minX = x;
        if (y < minY) minY = y;
        if (x > maxX) maxX = x;
        if (y > maxY) maxY = y;
      }
    }
  }
  const faceBottom = minY + Math.round((maxY - minY) * 0.48);
  const cols = [];
  for (let x = minX; x <= maxX; x += 1) {
    let n = 0;
    for (let y = minY; y < faceBottom; y += 1) {
      const i = (y * width + x) * channels;
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];
      const a = data[i + 3];
      if (a > 40 && r > 210 && g > 210 && b > 200) n += 1;
    }
    cols.push(n);
  }
  const runs = [];
  let start = null;
  for (let i = 0; i < cols.length; i += 1) {
    if (cols[i] > 2) {
      if (start === null) start = i;
    } else if (start !== null) {
      runs.push([start, i - 1]);
      start = null;
    }
  }
  if (start !== null) runs.push([start, cols.length - 1]);
  const merged = [];
  for (const run of runs) {
    const prev = merged[merged.length - 1];
    if (prev && run[0] - prev[1] <= 3) prev[1] = run[1];
    else merged.push(run.slice());
  }
  if (!merged.length) throw new Error("no A glyph");
  const [a0, a1] = merged[0];
  const left = Math.max(0, minX + a0 - 1);
  const top = Math.max(0, minY - 1);
  return {
    left,
    top,
    width: Math.min(a1 - a0 + 3, width - left),
    height: Math.min(maxY - minY + 3, height - top),
  };
}

function inkFace(data) {
  const out = Buffer.from(data);
  for (let i = 0; i < out.length; i += 4) {
    const r = out[i];
    const g = out[i + 1];
    const b = out[i + 2];
    const a = out[i + 3];
    if (a < 24) continue;
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    if (min > 186 && max - min < 42) {
      out[i] = 20;
      out[i + 1] = 17;
      out[i + 2] = 14;
    }
  }
  return out;
}

async function square(input, size) {
  return sharp(input)
    .trim({ threshold: 12 })
    .resize(size, size, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } })
    .png()
    .toBuffer();
}

await mkdir(outDir, { recursive: true });

for (const [id, rel] of marks) {
  const file = join(root, rel);
  const resized = await sharp(file, { density: 96 }).resize({ width: 1200 }).ensureAlpha().png().toBuffer();
  const raster = await sharp(resized).raw().toBuffer({ resolveWithObject: true });
  const box = cropA(raster.data, raster.info.width, raster.info.height, raster.info.channels);
  const cropped = await sharp(resized).extract(box).png().toBuffer();
  const { data, info } = await sharp(cropped).raw().toBuffer({ resolveWithObject: true });
  const dayRaw = inkFace(data);
  const day = await sharp(dayRaw, { raw: { width: info.width, height: info.height, channels: 4 } }).png().toBuffer();
  await writeFile(join(outDir, `${id}-night-32.png`), await square(cropped, 32));
  await writeFile(join(outDir, `${id}-day-32.png`), await square(day, 32));
  await writeFile(join(outDir, `${id}-night-180.png`), await square(cropped, 180));
  await writeFile(join(outDir, `${id}-day-180.png`), await square(day, 180));
  console.log(id, box);
}
