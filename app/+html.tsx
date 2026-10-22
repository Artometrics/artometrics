import { ScrollViewStyleReset } from "expo-router/html";
import type { PropsWithChildren } from "react";

/**
 * Root HTML shell for static web export.
 * Favicons: SVG (auto light/dark) first; PNG media pairs as fallbacks.
 */
export default function Root({ children }: PropsWithChildren) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="robots" content="noindex, nofollow" />
        <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta property="og:site_name" content="Artometrics" />
        <meta property="og:image" content="https://artometrics.com/images/brand/og-default.png" />
        <link rel="alternate" type="application/rss+xml" title="Artometrics Reports" href="/rss.xml" />
        <link rel="alternate" type="application/rss+xml" title="Artometrics Podcast" href="/podcast.xml" />
        <link rel="alternate" type="text/plain" title="llms.txt" href="/llms.txt" />
        {/* SVG switches fill via prefers-color-scheme */}
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/images/brand/favicon-light-32.png"
          media="(prefers-color-scheme: light)"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/images/brand/favicon-dark-32.png"
          media="(prefers-color-scheme: dark)"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/images/brand/favicon-light-16.png"
          media="(prefers-color-scheme: light)"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/images/brand/favicon-dark-16.png"
          media="(prefers-color-scheme: dark)"
        />
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="mask-icon" href="/favicon.svg" color="#E60000" />
        <link rel="manifest" href="/manifest.webmanifest" />
        <meta name="theme-color" content="#0e1110" />
        <meta name="color-scheme" content="dark" />
        <ScrollViewStyleReset />
        <link rel="stylesheet" href="/css/artometrics-article.css" />
        <link rel="stylesheet" href="/css/site-images.css" />
        <link rel="stylesheet" href="/css/shoegaze-theme.css" />
        <link rel="stylesheet" href="/css/house-style.css" />
        <style
          dangerouslySetInnerHTML={{
            __html: `
              @font-face {
                font-family: "Piazzolla";
                src: url("/fonts/Piazzolla.woff2") format("woff2");
                font-weight: 100 900;
                font-style: normal;
                font-display: swap;
              }
              @font-face {
                font-family: "Piazzolla";
                src: url("/fonts/Piazzolla-Italic.woff2") format("woff2");
                font-weight: 100 900;
                font-style: italic;
                font-display: swap;
              }
              @font-face {
                font-family: "Archivo";
                src: url("/fonts/Archivo.woff2") format("woff2");
                font-weight: 100 900;
                font-style: normal;
                font-display: swap;
              }
              @font-face {
                font-family: "Chomsky";
                src: url("/fonts/Chomsky.otf") format("opentype");
                font-weight: normal;
                font-style: normal;
                font-display: block;
              }
              @font-face {
                font-family: "Anton";
                src: url("/fonts/Anton-Regular.ttf") format("truetype");
                font-weight: 400;
                font-style: normal;
                font-display: swap;
              }
              @font-face {
                font-family: "DM Sans";
                src: url("/fonts/DMSans.ttf") format("truetype");
                font-weight: 100 900;
                font-style: normal;
                font-display: swap;
              }
              @font-face {
                font-family: "DM Sans";
                src: url("/fonts/DMSans-Italic.ttf") format("truetype");
                font-weight: 100 900;
                font-style: italic;
                font-display: swap;
              }
              @font-face {
                font-family: "DM Mono";
                src: url("/fonts/DMMono-Regular.ttf") format("truetype");
                font-weight: 400;
                font-style: normal;
                font-display: swap;
              }
              @font-face {
                font-family: "DM Mono";
                src: url("/fonts/DMMono-Medium.ttf") format("truetype");
                font-weight: 500;
                font-style: normal;
                font-display: swap;
              }
              html, body, #root {
                min-height: 100%;
              }
              ::selection {
                background: rgba(230, 0, 0, 0.18);
                color: inherit;
              }
              body {
                margin: 0;
                background: #0e1110;
                font-family: "DM Sans", system-ui, sans-serif;
                color: #f4f7f6;
              }
              /* Prefer explicit site theme over OS preference alone */
              html[data-theme="light"] {
                color-scheme: light only;
              }
              html[data-theme="light"] body,
              html[data-theme="light"] #root {
                background: #f3ead7 !important;
                color: #14110e !important;
              }
              html[data-theme="dark"] {
                color-scheme: dark;
              }
              html[data-theme="dark"] body,
              html[data-theme="dark"] #root {
                background: #0e1110 !important;
                color: #f4f7f6 !important;
              }
              @media (prefers-color-scheme: dark) {
                html:not([data-theme]) body,
                html:not([data-theme]) #root,
                html[data-theme="dark"] body,
                html[data-theme="dark"] #root {
                  background: #0e1110;
                  color: #f4f7f6;
                }
                html[data-theme="light"] body,
                html[data-theme="light"] #root {
                  background: #f3ead7 !important;
                  color: #14110e !important;
                }
              }
              a { color: inherit; text-decoration: none; }
              /* KSM-style breakpoint helpers (Uniwind may also emit these) */
              .lg\\:flex { display: none; }
              .lg\\:hidden { display: flex; }
              @media (min-width: 1024px) {
                .lg\\:flex { display: flex !important; }
                .lg\\:hidden { display: none !important; }
              }
            `,
          }}
        />
        {/* Apply saved theme before paint to avoid white-on-white flash */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function () {
                try {
                  var key = "artometrics-theme";
                  var saved = localStorage.getItem(key);
                  // Default dark (KSM-energy magazine) unless user saved light/system.
                  var mode = "dark";
                  if (saved === "light") mode = "light";
                  else if (saved === "system") {
                    mode = (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches)
                      ? "dark"
                      : "light";
                  } else if (saved === "dark") mode = "dark";
                  var bg = mode === "dark" ? "#0e1110" : "#f3ead7";
                  var fg = mode === "dark" ? "#f4f7f6" : "#14110e";
                  var root = document.documentElement;
                  root.setAttribute("data-theme", mode);
                  root.style.setProperty("color-scheme", mode === "dark" ? "dark" : "light only");
                  root.style.colorScheme = mode;
                  root.style.backgroundColor = bg;
                  document.addEventListener("DOMContentLoaded", function () {
                    document.body.style.backgroundColor = bg;
                    document.body.style.color = fg;
                    var app = document.getElementById("root");
                    if (app) {
                      app.style.backgroundColor = bg;
                      app.style.color = fg;
                    }
                  });
                } catch (e) {}
              })();
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
