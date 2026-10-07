#!/usr/bin/env node
/**
 * Narrate a blog article with ElevenLabs TTS → public/audios/<slug>.mp3
 *
 * Requires: ELEVENLABS_API_KEY in env (and optional ELEVENLABS_VOICE_ID).
 * Usage: npm run cos:narrate -- --slug readmitted
 *
 * Prefer Higgsfield generate_audio / voice tools when MCP is authenticated
 * and you want UI-driven voice selection instead of raw API keys.
 */
import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

const ROOT = process.cwd();

// Auto-load .env if needed
if (!process.env.ELEVENLABS_API_KEY && fs.existsSync(path.join(ROOT, ".env"))) {
  if (typeof process.loadEnvFile === "function") {
    try { process.loadEnvFile(path.join(ROOT, ".env")); } catch {}
  }
  if (!process.env.ELEVENLABS_API_KEY) {
    const envLines = fs.readFileSync(path.join(ROOT, ".env"), "utf8").split("\n");
    for (const line of envLines) {
      const m = line.match(/^\s*([A-Za-z0-9_]+)\s*=\s*(.*)?\s*$/);
      if (m && !process.env[m[1]]) {
        process.env[m[1]] = (m[2] || "").replace(/(^['"]|['"]$)/g, "").trim();
      }
    }
  }
}

const args = process.argv.slice(2);
const slugIdx = args.indexOf("--slug");
const slug = slugIdx >= 0 ? args[slugIdx + 1] : null;
const scriptIdx = args.indexOf("--script");
const customScriptPath = scriptIdx >= 0 ? args[scriptIdx + 1] : null;
const voiceIdx = args.indexOf("--voice");
const customVoiceId = voiceIdx >= 0 ? args[voiceIdx + 1] : null;
const apiKey = process.env.ELEVENLABS_API_KEY;
const voiceId = customVoiceId || process.env.ELEVENLABS_VOICE_ID || "SAz9YHcvj6GT2YYXdXww"; // River (Relaxed, Neutral, Informative)

if (!slug) {
  console.error("Usage: npm run cos:narrate -- --slug <slug> [--script <path>] [--voice <voiceId>]");
  process.exit(1);
}
if (!apiKey) {
  console.error(
    "Missing ELEVENLABS_API_KEY.\n" +
      "Add it to .env / Netlify, or use Higgsfield MCP generate_audio instead.",
  );
  process.exit(1);
}

let plain = "";
if (customScriptPath && fs.existsSync(path.resolve(ROOT, customScriptPath))) {
  plain = fs.readFileSync(path.resolve(ROOT, customScriptPath), "utf8").trim();
} else {
  const mdPath = path.join(ROOT, "src/content/blog", `${slug}.md`);
  if (!fs.existsSync(mdPath)) {
    console.error(`Missing ${mdPath}`);
    process.exit(1);
  }
  const { data, content } = matter(fs.readFileSync(mdPath, "utf8"));
  const title = data.title || slug;
  plain = `${title}.\n\n${stripHtml(content)}`
    .replace(/\s+/g, " ")
    .trim();
}

const outDir = path.join(ROOT, "public/audios");
const outPath = path.join(outDir, `${slug}.mp3`);
fs.mkdirSync(outDir, { recursive: true });

const chunks = chunkText(plain, 4500);
console.log(`Synthesizing '${slug}' with voice '${voiceId}' across ${chunks.length} chunk(s) (${plain.length.toLocaleString()} total characters)...`);

const audioBuffers = [];
const url = `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`;

for (let i = 0; i < chunks.length; i++) {
  console.log(`Chunk ${i + 1}/${chunks.length} (${chunks[i].length.toLocaleString()} chars)...`);
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "xi-api-key": apiKey,
      "Content-Type": "application/json",
      Accept: "audio/mpeg",
    },
    body: JSON.stringify({
      text: chunks[i],
      model_id: "eleven_multilingual_v2",
    }),
  });

  if (!res.ok) {
    const body = await res.text();
    console.error(`ElevenLabs HTTP ${res.status}: ${body.slice(0, 400)}`);
    process.exit(1);
  }

  const buf = Buffer.from(await res.arrayBuffer());
  audioBuffers.push(buf);
}

const finalBuf = Buffer.concat(audioBuffers);
fs.writeFileSync(outPath, finalBuf);
console.log(`Audio → ${path.relative(ROOT, outPath)} (${finalBuf.length.toLocaleString()} bytes)`);
console.log("Ready: Audio exported and linked to article.");

function chunkText(text, maxChars = 4500) {
  const paragraphs = text.split("\n\n");
  const chunks = [];
  let current = "";
  for (const para of paragraphs) {
    if ((current + "\n\n" + para).length <= maxChars) {
      current = current ? current + "\n\n" + para : para;
    } else {
      if (current) chunks.push(current);
      if (para.length > maxChars) {
        const sentences = para.match(/[^.!?]+[.!?]+(\s|$)/g) || [para];
        current = "";
        for (const s of sentences) {
          if ((current + " " + s).length <= maxChars) {
            current = current ? current + " " + s : s;
          } else {
            if (current) chunks.push(current);
            current = s;
          }
        }
      } else {
        current = para;
      }
    }
  }
  if (current) chunks.push(current);
  return chunks;
}

function stripHtml(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">");
}
