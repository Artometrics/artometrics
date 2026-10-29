import { createElement, useEffect } from "react";

type Props = {
  pageKey: string;
  label: string;
  bodyHtml: string;
};

declare global {
  interface Window {
    ArtometricsMag?: { boot: () => void; destroy: () => void };
  }
}

/**
 * Kindle-style page flip. The DOM matches the October 2026 edition
 * (`#view`, `#book`, `#pg`) so `public/mag.js` can measure columns.
 */
export function MagazineFrame({ pageKey, label, bodyHtml }: Props) {
  useEffect(() => {
    document.documentElement.classList.add("mag-mode");
    const root = document.getElementById("root");
    const prev = {
      bodyBg: document.body.style.backgroundColor,
      bodyColor: document.body.style.color,
      bodyOverflow: document.body.style.overflow,
      rootBg: root?.style.backgroundColor,
      rootOverflow: root?.style.overflow,
    };
    document.body.style.backgroundColor = "#ffffff";
    document.body.style.color = "#111111";
    document.body.style.overflow = "hidden";
    if (root) {
      root.style.backgroundColor = "#ffffff";
      root.style.overflow = "hidden";
    }

    let cancelled = false;
    const start = () => {
      if (!cancelled) window.ArtometricsMag?.boot();
    };
    const existing = document.querySelector('script[data-mag="1"]');
    if (window.ArtometricsMag) {
      start();
    } else if (existing) {
      existing.addEventListener("load", start, { once: true });
      if (window.ArtometricsMag) start();
    } else {
      const script = document.createElement("script");
      script.src = "/mag.js";
      script.dataset.mag = "1";
      script.onload = start;
      document.body.appendChild(script);
    }

    return () => {
      cancelled = true;
      window.ArtometricsMag?.destroy();
      document.documentElement.classList.remove("mag-mode");
      document.body.style.backgroundColor = prev.bodyBg;
      document.body.style.color = prev.bodyColor;
      document.body.style.overflow = prev.bodyOverflow;
      if (root) {
        root.style.backgroundColor = prev.rootBg || "";
        root.style.overflow = prev.rootOverflow || "";
      }
    };
  }, [pageKey, bodyHtml]);

  return createElement(
    "div",
    { className: "mag-shell", "data-magazine": pageKey },
    createElement(
      "header",
      { className: "bar" },
      createElement(
        "a",
        { href: "/", "aria-label": "Contents" },
        createElement("img", { src: "/logo.png", alt: "Artometrics" }),
      ),
      createElement("span", { className: "t" }, label),
      createElement("a", { className: "site", href: "/blog" }, "Site"),
      createElement("span", { id: "pg", "aria-live": "polite" }, "1"),
    ),
    createElement(
      "div",
      { id: "view" },
      createElement("div", { id: "fold" }),
      createElement("article", {
        id: "book",
        itemScope: true,
        itemType: "https://schema.org/Article",
        dangerouslySetInnerHTML: { __html: bodyHtml },
        suppressHydrationWarning: true,
      }),
    ),
    createElement(
      "footer",
      { className: "bar" },
      createElement("span", { "aria-hidden": true }, "←"),
      createElement("div", { className: "prog" }, createElement("i", { id: "bar" })),
      createElement("span", { "aria-hidden": true }, "→"),
      createElement("span", { id: "tot" }),
    ),
    createElement("div", { className: "hint", id: "hint" }, "Tap or swipe to turn"),
  );
}
