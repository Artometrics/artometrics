import { createElement, useEffect, useLayoutEffect, useState } from "react";
import type { CSSProperties } from "react";
import { resolveSkinId, skinCssVars, skinStorageKey, type MagSkin } from "@/lib/magazine-skins";

type Props = {
  pageKey: string;
  label: string;
  bodyHtml: string;
  skins?: MagSkin[];
};

declare global {
  interface Window {
    ArtometricsMag?: { boot: () => void; destroy: () => void };
  }
}

function readSkinChoice(slug: string, skins: MagSkin[]): string {
  const fallback = skins[0]?.id || "ledger";
  if (typeof window === "undefined") return fallback;
  const query = new URLSearchParams(window.location.search).get("skin");
  let saved: string | null = null;
  try {
    saved = window.localStorage.getItem(skinStorageKey(slug));
  } catch {
    saved = null;
  }
  return resolveSkinId(slug, skins, query, saved);
}

function rememberSkin(slug: string, id: string) {
  try {
    window.localStorage.setItem(skinStorageKey(slug), id);
  } catch {
    /* private mode */
  }
}

function writeSkinUrl(id: string, skins: MagSkin[]) {
  const url = new URL(window.location.href);
  if (id === skins[0]?.id) url.searchParams.delete("skin");
  else url.searchParams.set("skin", id);
  const next = url.pathname + url.search + url.hash;
  if (next !== window.location.pathname + window.location.search + window.location.hash) {
    window.history.replaceState(null, "", next);
  }
}

function relayout() {
  window.dispatchEvent(new Event("resize"));
}

function SkinIcon({ id }: { id: string }) {
  if (id === "box") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <rect x="2" y="3" width="14" height="12" fill="none" stroke="currentColor" strokeWidth="1.4" />
        <circle cx="9" cy="2.2" r="1.3" fill="none" stroke="currentColor" strokeWidth="1.2" />
        <path d="M9 6.2l.7 1.6 1.7.2-1.3 1.1.4 1.7L9 9.9 7.5 10.8l.4-1.7-1.3-1.1 1.7-.2z" fill="#FFCC00" stroke="currentColor" strokeWidth="0.4" />
      </svg>
    );
  }
  if (id === "trade") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <path d="M3 4h12M3 8h12M3 12h9" fill="none" stroke="currentColor" strokeWidth="1.6" />
        <circle cx="4" cy="15.2" r="0.9" fill="#0047FF" />
        <circle cx="8" cy="15.2" r="0.9" fill="#0047FF" />
        <circle cx="12" cy="15.2" r="0.9" fill="#0047FF" />
      </svg>
    );
  }
  if (id === "chart") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <rect x="1.5" y="3" width="6" height="12" fill="none" stroke="currentColor" strokeWidth="1.3" />
        <path d="M4.1 6.2v6" fill="none" stroke="currentColor" strokeWidth="1.3" />
        <rect x="9.5" y="7" width="6.5" height="2.4" fill="#E4002B" />
        <path d="M9.5 12.2h6.5M9.5 14.6h4.2" fill="none" stroke="currentColor" strokeWidth="1.2" />
      </svg>
    );
  }
  if (id === "sleeve") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <rect x="2.5" y="2.5" width="13" height="13" fill="none" stroke="currentColor" strokeWidth="1.3" />
        <circle cx="9" cy="9" r="3.1" fill="none" stroke="#F2A900" strokeWidth="1.8" />
        <circle cx="9" cy="9" r="0.8" fill="currentColor" />
      </svg>
    );
  }
  if (id === "stream") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <circle cx="5" cy="6" r="2.6" fill="#0047FF" />
        <path d="M4.2 4.8v2.4l2.1-1.2z" fill="#ffffff" />
        <rect x="2" y="12.2" width="14" height="2" rx="1" fill="#D5DAE6" />
        <rect x="2" y="12.2" width="9" height="2" rx="1" fill="#12B886" />
      </svg>
    );
  }
  if (id === "shelf") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <path d="M2 14.6h14v1.5H2z" fill="currentColor" />
        <path d="M3 3.5h2.4V14.6H3zM7.2 8.6h2.1V14.6H7.2zM11.2 10h2.1v4.6h-2.1z" fill="currentColor" />
        <circle cx="14.4" cy="5" r="2.1" fill="#D9480F" />
      </svg>
    );
  }
  if (id === "guide") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <rect x="2" y="3" width="5.2" height="12" fill="none" stroke="currentColor" strokeWidth="1.3" />
        <path d="M2 6.2h5.2" stroke="#2B8A3E" strokeWidth="1.8" />
        <path d="M9.2 6h6.6M9.2 9.5h6.6M9.2 13h4.4" fill="none" stroke="currentColor" strokeWidth="1.3" />
      </svg>
    );
  }
  if (id === "late") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <path d="M2 5.6l4.4 2.7L2 11z" fill="currentColor" />
        <rect x="2" y="13.2" width="14" height="1.8" rx="0.9" fill="currentColor" opacity="0.35" />
        <rect x="2" y="13.2" width="9.5" height="1.8" rx="0.9" fill="#F2A900" />
      </svg>
    );
  }
  if (id === "filing") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <path d="M2 3.2h14M2 5.2h14" fill="none" stroke="currentColor" strokeWidth="1.1" />
        <rect x="2" y="7.4" width="14" height="7" fill="none" stroke="currentColor" strokeWidth="1.2" />
        <path d="M4 11h5.5" stroke="currentColor" strokeWidth="1.2" />
        <path d="M11.2 9.6v3.2M13.6 9.6v3.2" stroke="#B42318" strokeWidth="1.3" />
      </svg>
    );
  }
  if (id === "gauge") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <rect x="2" y="2.5" width="14" height="9" rx="2" fill="none" stroke="currentColor" strokeWidth="1.3" />
        <rect x="2" y="13.6" width="14" height="2.2" fill="none" stroke="currentColor" strokeWidth="1.1" />
        <rect x="2" y="13.6" width="2.2" height="2.2" fill="#2F9E44" />
      </svg>
    );
  }
  if (id === "onair") {
    return (
      <svg viewBox="0 0 18 18" aria-hidden="true">
        <rect x="1.8" y="2.4" width="14.4" height="6.4" fill="none" stroke="currentColor" strokeWidth="1.2" />
        <circle cx="4.6" cy="5.6" r="1.35" fill="#E8590C" />
        <path d="M7.4 4.6h6.2M7.4 6.6h4" stroke="currentColor" strokeWidth="1.1" />
        <path d="M2 12.2v2.4M5 11v4.2M8 13v1.6M11 10.4v5.2M14 12.4v2.2M16.4 11.6v3.2" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 18 18" aria-hidden="true">
      <path d="M3 5h12M3 9h12M3 13h12" fill="none" stroke="currentColor" strokeWidth="1" />
      <rect x="10" y="7" width="5" height="4" fill="none" stroke="#C8102E" strokeWidth="1.2" transform="rotate(-8 12.5 9)" />
    </svg>
  );
}

/**
 * Kindle-style page flip. The DOM matches the October 2026 edition
 * (`#view`, `#book`, `#pg`) so `public/mag.js` can measure columns.
 * Skins set `data-skin` on this shell, the reader root.
 */
export function MagazineFrame({ pageKey, label, bodyHtml, skins }: Props) {
  const palette = skins && skins.length ? skins : undefined;
  const [skinId, setSkinId] = useState(palette?.[0]?.id || "");
  const skin = palette?.find((item) => item.id === skinId) || palette?.[0];

  useLayoutEffect(() => {
    if (!palette?.length || pageKey === "contents") return;
    const next = readSkinChoice(pageKey, palette);
    setSkinId(next);
    rememberSkin(pageKey, next);
    writeSkinUrl(next, palette);
  }, [pageKey, palette]);

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
    const paper = skin?.tokens.paper || "#ffffff";
    const ink = skin?.tokens.ink || "#111111";
    document.body.style.backgroundColor = paper;
    document.body.style.color = ink;
    document.body.style.overflow = "hidden";
    if (root) {
      root.style.backgroundColor = paper;
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
  }, [pageKey, bodyHtml, skin?.tokens.paper, skin?.tokens.ink]);

  useEffect(() => {
    if (!skin) return;
    document.body.style.backgroundColor = skin.tokens.paper;
    document.body.style.color = skin.tokens.ink;
    const root = document.getElementById("root");
    if (root) root.style.backgroundColor = skin.tokens.paper;
    const fonts = document.fonts;
    if (fonts?.ready) {
      void fonts.ready.then(relayout);
      fonts.addEventListener?.("loadingdone", relayout, { once: true });
    } else {
      relayout();
    }
  }, [skin]);

  function choose(id: string) {
    if (!palette) return;
    setSkinId(id);
    rememberSkin(pageKey, id);
    writeSkinUrl(id, palette);
  }

  const shellStyle = (skin ? skinCssVars(skin) : undefined) as CSSProperties | undefined;

  return createElement(
    "div",
    {
      className: "mag-shell",
      "data-magazine": pageKey,
      "data-skin": skin?.id,
      style: shellStyle,
    },
    createElement(
      "header",
      { className: "bar" },
      createElement(
        "a",
        { href: "/", "aria-label": "Contents" },
        createElement("img", { src: "/logo.png", alt: "Artometrics" }),
      ),
      createElement("span", { className: "t" }, label),
      palette
        ? createElement(
            "div",
            {
              className: "skin-picker",
              role: "radiogroup",
              "aria-label": "Magazine skin",
              onClick: (event: { stopPropagation: () => void }) => event.stopPropagation(),
              onTouchStart: (event: { stopPropagation: () => void }) => event.stopPropagation(),
            },
            palette.map((item) =>
              createElement(
                "button",
                {
                  key: item.id,
                  type: "button",
                  role: "radio",
                  "aria-checked": item.id === skin?.id,
                  "aria-label": item.name,
                  "data-skin-id": item.id,
                  onClick: (event: { stopPropagation: () => void }) => {
                    event.stopPropagation();
                    choose(item.id);
                  },
                  onPointerDown: (event: { currentTarget: HTMLButtonElement; pointerType: string }) => {
                    if (event.pointerType !== "touch") return;
                    const button = event.currentTarget;
                    const timer = window.setTimeout(() => button.classList.add("is-held"), 380);
                    const clear = () => {
                      window.clearTimeout(timer);
                      button.classList.remove("is-held");
                      button.removeEventListener("pointerup", clear);
                      button.removeEventListener("pointercancel", clear);
                    };
                    button.addEventListener("pointerup", clear);
                    button.addEventListener("pointercancel", clear);
                  },
                },
                createElement(SkinIcon, { id: item.id }),
                createElement("span", { className: "tip" }, item.name),
              ),
            ),
          )
        : null,
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
