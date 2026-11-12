import { createServer } from "node:http";
import { existsSync, readFileSync, statSync } from "node:fs";
import { extname, join, resolve } from "node:path";

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".webp": "image/webp",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".pdf": "application/pdf",
  ".mp4": "video/mp4",
  ".mp3": "audio/mpeg",
  ".csv": "text/csv; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml",
  ".woff2": "font/woff2",
  ".woff": "font/woff",
  ".ttf": "font/ttf",
  ".webmanifest": "application/manifest+json",
};

/** Minimal Firebase-like static server: cleanUrls, no trailing slash, honours dist/ only. */
export function startStaticServer(dir = "dist", port = 0) {
  const root = resolve(dir);
  const server = createServer((req, res) => {
    const url = new URL(req.url || "/", "http://localhost");
    let path = decodeURIComponent(url.pathname);
    if (path.length > 1) path = path.replace(/\/+$/, "");
    const candidates = [];
    if (path === "/" || path === "") candidates.push(join(root, "index.html"));
    else {
      candidates.push(join(root, path));
      if (!extname(path)) candidates.push(join(root, `${path}.html`), join(root, path, "index.html"));
    }
    const hit = candidates.find((file) => file.startsWith(root) && existsSync(file) && statSync(file).isFile());
    if (!hit) {
      res.writeHead(404, { "content-type": "text/html; charset=utf-8" });
      const nf = join(root, "404.html");
      res.end(existsSync(nf) ? readFileSync(nf) : "not found");
      return;
    }
    const body = readFileSync(hit);
    res.writeHead(200, {
      "content-type": TYPES[extname(hit)] || "application/octet-stream",
      "content-length": body.length,
      "cache-control": "no-store",
    });
    res.end(body);
  });
  return new Promise((ok) => {
    server.listen(port, "127.0.0.1", () => {
      const { port: bound } = server.address();
      ok({ server, origin: `http://127.0.0.1:${bound}`, close: () => new Promise((done) => server.close(done)) });
    });
  });
}
