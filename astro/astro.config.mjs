import { defineConfig } from "astro/config";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = fileURLToPath(new URL("..", import.meta.url));

export default defineConfig({
  site: "https://artometrics.com",
  trailingSlash: "never",
  build: { format: "directory" },
  publicDir: path.join(repoRoot, "public"),
  prefetch: false,
  compressHTML: true,
  vite: {
    resolve: {
      alias: { "@": repoRoot },
    },
    server: {
      fs: { allow: [repoRoot] },
    },
    esbuild: {
      tsconfigRaw: {
        compilerOptions: {
          target: "ES2022",
          module: "ESNext",
          moduleResolution: "bundler",
          jsx: "preserve",
          strict: false,
        },
      },
    },
  },
});
