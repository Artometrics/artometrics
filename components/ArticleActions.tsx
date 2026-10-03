import { useEffect, useMemo, useState } from "react";
import { Pressable, Share, Text, View, Platform } from "react-native";
import { Link } from "expo-router";
import { useAuth } from "@/lib/auth";
import { apiFetch } from "@/lib/supabase/client";
import { assetUrl } from "@/lib/assets";
import { openExternalUrl } from "@/lib/openExternal";
import { trackEvent } from "@/lib/analytics/ga";
import downloadsManifest from "@/src/generated/downloads.json";

type Pack = {
  slug: string;
  dataset?: string | null;
  quarto?: string | null;
  html?: string | null;
  pdf?: string | null;
  epub?: string | null;
  audio?: string | null;
  transcript?: string | null;
  github?: string | null;
};

type Props = {
  slug: string;
  title: string;
  description?: string;
  /** Frontmatter narration URL when not yet in downloads manifest */
  audioSrc?: string | null;
  /** Top: share + save. Header: share + EPUB/transcript/listen. Bottom: download menu. */
  placement?: "top" | "header" | "bottom" | "all";
  /** Breadcrumb bar: compact chips, right-aligned (flex-row-reverse). */
  variant?: "default" | "inline";
};

type DownloadItem = { key: string; label: string; href: string };

function openUrl(url: string) {
  const absolute = assetUrl(url) ?? url;
  if (Platform.OS === "web" && typeof window !== "undefined") {
    window.open(absolute, "_blank", "noopener,noreferrer");
    return;
  }
  void openExternalUrl(absolute);
}

async function downloadAll(items: DownloadItem[]) {
  if (!items.length) return;
  // iOS often ignores/fails rapid successive openURL calls — share a list instead.
  if (Platform.OS !== "web") {
    const lines = items.map((i) => {
      const href = assetUrl(i.href) ?? i.href;
      return `${i.label}\n${href}`;
    });
    try {
      await Share.share({
        message: lines.join("\n\n"),
        title: "Artometrics downloads",
      });
    } catch {
      openUrl(items[0].href);
    }
    return;
  }
  for (const item of items) {
    openUrl(item.href);
    await new Promise((r) => setTimeout(r, 350));
  }
}

export function ArticleActions({
  slug,
  title,
  description,
  audioSrc,
  placement = "all",
  variant = "default",
}: Props) {
  const { user } = useAuth();
  const [saved, setSaved] = useState(false);
  const [busy, setBusy] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const pack = (downloadsManifest as Record<string, Pack>)[slug] ?? { slug };

  useEffect(() => {
    if (!user) {
      setSaved(false);
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const res = await apiFetch("saved-articles");
        if (!res.ok) return;
        const data = (await res.json()) as { items?: { article_slug: string }[] };
        if (!cancelled) {
          setSaved(Boolean(data.items?.some((i) => i.article_slug === slug)));
        }
      } catch {
        /* soft fail */
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [user, slug]);

  async function toggleSave() {
    if (!user) return;
    setBusy(true);
    try {
      if (saved) {
        await apiFetch(`saved-articles?slug=${encodeURIComponent(slug)}`, {
          method: "DELETE",
        });
        setSaved(false);
      } else {
        await apiFetch("saved-articles", {
          method: "POST",
          body: JSON.stringify({ slug }),
        });
        setSaved(true);
      }
    } catch {
      /* soft fail */
    } finally {
      setBusy(false);
    }
  }

  const reportUrl = `https://artometrics.com/${slug}`;
  const shareText = description
    ? `${title} — ${description}`
    : `${title} — Artometrics`;

  async function copyReportLink() {
    trackEvent("report_share", { slug, method: "copy_link" });
    if (
      typeof navigator !== "undefined" &&
      navigator.clipboard &&
      typeof navigator.clipboard.writeText === "function"
    ) {
      try {
        await navigator.clipboard.writeText(reportUrl);
        return;
      } catch {
        /* fall through */
      }
    }
    openUrl(reportUrl);
  }

  function shareOnX() {
    trackEvent("report_share", { slug, method: "x" });
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(reportUrl)}`;
    openUrl(url);
  }

  function shareOnLinkedIn() {
    trackEvent("report_share", { slug, method: "linkedin" });
    const url = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(reportUrl)}`;
    openUrl(url);
  }

  async function share() {
    trackEvent("report_share", { slug, method: Platform.OS });
    if (Platform.OS !== "web") {
      try {
        await Share.share({ message: `${title}\n${reportUrl}`, url: reportUrl, title });
      } catch {
        openUrl(reportUrl);
      }
      return;
    }
    if (typeof navigator !== "undefined" && typeof navigator.share === "function") {
      navigator
        .share({ title, text: shareText, url: reportUrl })
        .catch(() => void copyReportLink());
      return;
    }
    void copyReportLink();
  }

  const audioHref = pack.audio || audioSrc || null;

  const downloads = useMemo(() => {
    const items: DownloadItem[] = [];
    // Prefer site-hosted exports; GitHub is demoted to last resort.
    if (pack.pdf) items.push({ key: "pdf", label: "PDF", href: pack.pdf });
    if (pack.epub) items.push({ key: "epub", label: "Ebook (EPUB)", href: pack.epub });
    if (pack.transcript) {
      items.push({ key: "transcript", label: "Transcript (TXT)", href: pack.transcript });
    }
    if (pack.html) items.push({ key: "html", label: "Article HTML", href: pack.html });
    if (pack.dataset) items.push({ key: "data", label: "Dataset (CSV)", href: pack.dataset });
    if (audioHref) {
      items.push({ key: "audio", label: "Narration (MP3)", href: audioHref });
    }
    if (pack.quarto) {
      items.push({ key: "code", label: "Quarto / source", href: pack.quarto });
    } else if (pack.github && items.length === 0) {
      items.push({ key: "code", label: "Source (GitHub)", href: pack.github });
    }
    return items;
  }, [pack, audioHref]);

  const chipBtn =
    variant === "inline"
      ? "bg-accent px-2 py-1.5 active:opacity-90 hover:opacity-90 md:px-2.5 md:py-1.5"
      : "bg-accent px-3 py-2 active:opacity-90 hover:opacity-90 md:px-4 md:py-2.5";
  const chipBtnLg = "bg-accent px-5 py-3 active:opacity-90 hover:opacity-90";
  const chipBtnText =
    variant === "inline"
      ? "font-display text-[9px] uppercase tracking-[1.4px] text-white md:text-[10px] md:tracking-[1.6px]"
      : "font-display text-[11px] uppercase tracking-[1.6px] text-white md:text-[12px] md:tracking-[2px]";
  const chipBtnTextLg =
    "font-display text-[13px] uppercase tracking-[2px] text-white";

  function downloadChipLabel(item: DownloadItem) {
    if (item.key === "pdf") return "Download";
    if (item.key === "data") return "Data";
    if (item.key === "epub") return "EPUB";
    if (item.key === "transcript") return "Transcript";
    if (item.key === "audio") return "Listen";
    if (item.key === "html") return "HTML";
    if (item.key === "code") return "Source";
    return item.label;
  }

  const showTop = placement === "top" || placement === "all";
  const showHeader = placement === "header" || placement === "all";
  const showBottom = placement === "bottom" || placement === "all";

  return (
    <View
      className={[
        variant === "inline" ? "shrink-0" : "gap-3.5 py-1",
        placement === "bottom" ? "mt-1" : "",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      {showHeader ? (
        <View
          className={[
            "flex-row flex-wrap items-center",
            variant === "inline"
              ? "flex-row-reverse justify-end gap-1.5 md:gap-2"
              : "gap-2 md:gap-3",
          ].join(" ")}
        >
          <Pressable
            onPress={share}
            accessibilityRole="button"
            accessibilityLabel="Share this report"
            className={chipBtn}
          >
            <Text className={chipBtnText}>Share</Text>
          </Pressable>
          {Platform.OS === "web" ? (
            <>
              <Pressable
                onPress={shareOnX}
                accessibilityRole="button"
                accessibilityLabel="Share on X"
                className={chipBtn}
              >
                <Text className={chipBtnText}>X</Text>
              </Pressable>
              <Pressable
                onPress={shareOnLinkedIn}
                accessibilityRole="button"
                accessibilityLabel="Share on LinkedIn"
                className={chipBtn}
              >
                <Text className={chipBtnText}>LinkedIn</Text>
              </Pressable>
              <Pressable
                onPress={() => void copyReportLink()}
                accessibilityRole="button"
                accessibilityLabel="Copy report link"
                className={chipBtn}
              >
                <Text className={chipBtnText}>Copy link</Text>
              </Pressable>
            </>
          ) : null}
          {downloads.map((item) => (
            <Pressable
              key={item.key}
              onPress={() => {
                trackEvent("report_download", { slug, format: item.key });
                openUrl(item.href);
              }}
              accessibilityRole="button"
              accessibilityLabel={item.label}
              className={chipBtn}
            >
              <Text className={chipBtnText}>{downloadChipLabel(item)}</Text>
            </Pressable>
          ))}
          {downloads.length > 1 ? (
            <Pressable
              onPress={() => void downloadAll(downloads)}
              accessibilityRole="button"
              accessibilityLabel={
                Platform.OS === "web" ? "Download all files" : "Share all download links"
              }
              className={chipBtn}
            >
              <Text className={chipBtnText}>
                {Platform.OS === "web" ? "Download all" : "Share all"}
              </Text>
            </Pressable>
          ) : null}
        </View>
      ) : null}

      {showTop ? (
        <View className="flex-row flex-wrap items-center gap-3">
          <Pressable
            onPress={share}
            accessibilityRole="button"
            accessibilityLabel="Share this report"
            className={chipBtnLg}
          >
            <Text className={chipBtnTextLg}>Share</Text>
          </Pressable>
          {user ? (
            <Pressable
              onPress={toggleSave}
              disabled={busy}
              accessibilityRole="button"
              className={[chipBtnLg, busy ? "opacity-50" : ""].filter(Boolean).join(" ")}
            >
              <Text className={chipBtnTextLg}>{saved ? "Saved" : "Save"}</Text>
            </Pressable>
          ) : (
            <Link href="/login" asChild>
              <Pressable className={chipBtnLg}>
                <Text className={chipBtnTextLg}>Sign in to save</Text>
              </Pressable>
            </Link>
          )}
        </View>
      ) : null}

      {showBottom && downloads.length ? (
        <View className="gap-3">
          <Text className="font-display text-[12px] uppercase tracking-[2px] text-accent">
            Downloads
          </Text>
          <View className="flex-row flex-wrap items-center gap-3">
            <Pressable
              onPress={() => setMenuOpen((v) => !v)}
              accessibilityRole="button"
              accessibilityState={{ expanded: menuOpen }}
              className={chipBtnLg}
            >
              <Text className={chipBtnTextLg}>
                {menuOpen ? "Close" : "Download"}
              </Text>
            </Pressable>
            {primaryDownloads.map((item) => (
              <Pressable
                key={item.key}
                onPress={() => {
                  trackEvent("report_download", { slug, format: item.key });
                  openUrl(item.href);
                }}
                className={chipBtnLg}
              >
                <Text className={chipBtnTextLg}>
                  {item.key === "pdf"
                    ? "PDF"
                    : item.key === "epub"
                      ? "EPUB"
                      : item.key === "transcript"
                        ? "Transcript"
                        : item.key === "audio"
                          ? "Listen"
                          : item.key === "data"
                            ? "Data"
                            : item.label}
                </Text>
              </Pressable>
            ))}
            {downloads.length > 1 ? (
              <Pressable
                onPress={() => void downloadAll(downloads)}
                className={chipBtnLg}
              >
                <Text className={chipBtnTextLg}>
                  {Platform.OS === "web" ? "Download all" : "Share all links"}
                </Text>
              </Pressable>
            ) : null}
          </View>

          {menuOpen ? (
            <View className="border-2 border-border bg-bg py-1">
              {downloads.map((item) => (
                <Pressable
                  key={item.key}
                  onPress={() => {
                    openUrl(item.href);
                    setMenuOpen(false);
                  }}
                  className="border-b border-border px-4 py-3 last:border-b-0"
                >
                  <Text className="font-display text-base uppercase tracking-[1px] text-fg">
                    {item.label}
                  </Text>
                </Pressable>
              ))}
              {downloads.length > 1 ? (
                <Pressable
                  onPress={() => {
                    void downloadAll(downloads);
                    setMenuOpen(false);
                  }}
                  className="px-4 py-3"
                >
                  <Text className="font-display text-base uppercase tracking-[1px] text-accent">
                    {Platform.OS === "web"
                      ? `Download all (${downloads.length} files)`
                      : `Share all links (${downloads.length})`}
                  </Text>
                </Pressable>
              ) : null}
            </View>
          ) : null}
        </View>
      ) : null}
    </View>
  );
}
