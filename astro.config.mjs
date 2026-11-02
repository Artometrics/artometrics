import { defineConfig } from "astro/config";
import { fileURLToPath } from "node:url";

/** Static magazine. Firebase Hosting serves `dist/` with cleanUrls. */
export default defineConfig({
  site: "https://artometrics.com",
  srcDir: "./site",
  publicDir: "./public",
  outDir: "./dist",
  trailingSlash: "never",
  build: {
    format: "file",
  },
  vite: {
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./", import.meta.url)),
      },
    },
  },
});
