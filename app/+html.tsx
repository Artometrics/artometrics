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
        <meta name="robots" content="index, follow" />
        <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no, viewport-fit=cover" />
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
        <link rel="stylesheet" href="/css/mag.css" />
        <link rel="stylesheet" href="/css/mag-skins.css" />
        <link rel="stylesheet" href="/css/artometrics-article.css" />
        <link rel="stylesheet" href="/css/site-images.css" />
        <link rel="stylesheet" href="/css/shoegaze-theme.css" />
        <link rel="stylesheet" href="/css/house-style.css" />
        <style
          dangerouslySetInnerHTML={{
            __html: `
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
              html.site-document-scroll,
              html.site-document-scroll body {
                height: auto !important;
                min-height: 100%;
                max-width: 100%;
                overflow-x: hidden !important;
                overflow-y: auto !important;
                -webkit-overflow-scrolling: touch;
              }
              html.site-document-scroll #root {
                height: auto !important;
                min-height: 100%;
                max-width: 100%;
                overflow: visible !important;
              }
              html.site-document-scroll #root div:has(.site-document) {
                position: relative !important;
                top: auto !important;
                right: auto !important;
                bottom: auto !important;
                left: auto !important;
                width: 100% !important;
                max-width: 100% !important;
                min-width: 0 !important;
                height: auto !important;
                max-height: none !important;
                overflow: visible !important;
                transform: none !important;
                flex: none !important;
                min-height: 0 !important;
                background-color: transparent !important;
              }
              html.site-menu-open,
              html.site-menu-open body {
                overflow: hidden !important;
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
              html[data-theme="dark"],
              html.site-document-scroll {
                color-scheme: dark;
              }
              html[data-theme="dark"] body,
              html[data-theme="dark"] #root,
              html.site-document-scroll body,
              html.site-document-scroll #root {
                background: #0e1110 !important;
                color: #f4f7f6 !important;
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
                  var MAG_ROOT = "/mag";
                  var path = (location.pathname || "/").replace(/\\/$/, "") || "/";
                  var isMag =
                    path === MAG_ROOT ||
                    (path.indexOf(MAG_ROOT + "/") === 0 &&
                      path.slice(MAG_ROOT.length + 1).indexOf("/") === -1);
                  var rootEl = document.documentElement;
                  if (isMag) {
                    rootEl.classList.add("mag-mode");
                    rootEl.classList.remove("site-document-scroll");
                    rootEl.setAttribute("data-theme", "dark");
                    rootEl.style.backgroundColor = "#0e1110";
                    rootEl.style.color = "#f3ead7";
                    document.addEventListener("DOMContentLoaded", function () {
                      document.body.style.backgroundColor = "#0e1110";
                      document.body.style.color = "#f3ead7";
                      var app = document.getElementById("root");
                      if (app) {
                        app.style.backgroundColor = "#0e1110";
                        app.style.color = "#f3ead7";
                      }
                    });
                    return;
                  }
                  rootEl.classList.add("site-document-scroll");
                  rootEl.classList.remove("mag-mode");
                  rootEl.setAttribute("data-theme", "dark");
                  rootEl.style.colorScheme = "dark";
                  rootEl.style.backgroundColor = "#0e1110";
                  document.addEventListener("DOMContentLoaded", function () {
                    document.body.style.backgroundColor = "#0e1110";
                    document.body.style.color = "#f4f7f6";
                    var app = document.getElementById("root");
                    if (app) {
                      app.style.backgroundColor = "#0e1110";
                      app.style.color = "#f4f7f6";
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
