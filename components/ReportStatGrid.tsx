import React from "react";
import { View, Text, StyleSheet, Platform, Pressable } from "react-native";
import { useTheme } from "@/lib/theme";

export interface StatItem {
  value: string;
  label?: string;
  badge?: string;
  citation?: string;
  isAccentRed?: boolean;
}

interface ReportStatGridProps {
  keyPoints?: string[];
  stats?: StatItem[];
  subject?: string | null;
  sourceLabel?: string | null;
}

/**
 * Infer a smart category badge based on stat value and description
 */
function inferBadge(val: string, text: string, idx: number): string {
  const lower = text.toLowerCase();
  if (lower.includes("risk") || lower.includes("penalty") || lower.includes("loss")) {
    return "Financial Risk";
  }
  if (lower.includes("mandat") || lower.includes("hospital") || lower.includes("cohort")) {
    return "Mandatory Scope";
  }
  if (lower.includes("revenue") || lower.includes("growth") || lower.includes("opportunity") || lower.includes("gain")) {
    return "Market Opportunity";
  }
  if (lower.includes("cost") || lower.includes("spend") || lower.includes("price") || lower.includes("budget")) {
    return "Cost Analysis";
  }
  if (lower.includes("ratio") || lower.includes("rate") || lower.includes("percent") || val.includes("%")) {
    return idx === 0 ? "Core Metric" : "Performance Rate";
  }
  if (lower.includes("rank") || lower.includes("lead") || lower.includes("top") || lower.includes("highest")) {
    return "Field Leader";
  }
  if (lower.includes("median") || lower.includes("average") || lower.includes("mean")) {
    return "Statistical Baseline";
  }
  if (lower.includes("record") || lower.includes("sample") || lower.includes("dataset") || lower.includes("scope")) {
    return "Dataset Scale";
  }
  const fallbackBadges = ["Key Finding", "Audited Metric", "System Metric", "Observed Value"];
  return fallbackBadges[idx % fallbackBadges.length];
}

/**
 * Parse raw "Stat — Description" strings into structured StatItem objects
 */
function parseKeyPoint(raw: string, idx: number, defaultSource: string): StatItem {
  const parts = raw.split(/\s+[—–-]\s+/);
  if (parts.length >= 2) {
    const value = parts[0].trim();
    const label = parts.slice(1).join(" — ").trim();
    const badge = inferBadge(value, label, idx);
    // Alternate 3D glasses blue and red accents
    const isAccentRed = idx === 0 || idx === 3;
    return {
      value,
      label,
      badge,
      citation: defaultSource,
      isAccentRed,
    };
  }
  return {
    value: raw.trim(),
    label: "",
    badge: "Key Finding",
    citation: defaultSource,
    isAccentRed: idx === 0,
  };
}

/**
 * ReportStatGrid
 *
 * Renders a tactile floating grid of stat boxes with drop shadows,
 * matching the user's reference design (Image 2).
 */
export function ReportStatGrid({
  keyPoints,
  stats: explicitStats,
  subject,
  sourceLabel,
}: ReportStatGridProps) {
  const { mode } = useTheme();
  const isDark = mode === "dark";

  const defaultSource = sourceLabel || (subject ? `${subject} Analysis` : "Artometrics Audit");

  const items: StatItem[] = explicitStats?.length
    ? explicitStats
    : (keyPoints || [])
        .slice(0, 4) // Show top 4 key findings
        .map((kp, idx) => parseKeyPoint(kp, idx, defaultSource));

  if (!items.length) return null;

  return (
    <View className="w-full my-6">
      <View className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {items.map((item, idx) => {
          const isRed = item.isAccentRed;
          const valueColor = isRed
            ? isDark
              ? "#FF5555"
              : "#E60000"
            : isDark
              ? "#7AA2FF"
              : "#3367E7";

          return (
            <View
              key={idx}
              className="art-floating-box flex flex-col justify-between p-5 min-h-[220px]"
              style={
                Platform.OS === "web"
                  ? undefined
                  : {
                      backgroundColor: isDark ? "#0E1018" : "#FFFFFF",
                      borderRadius: 16,
                      borderWidth: 1,
                      borderColor: isDark ? "rgba(255,255,255,0.14)" : "rgba(0,0,0,0.12)",
                      shadowColor: "#000000",
                      shadowOffset: { width: 0, height: 8 },
                      shadowOpacity: isDark ? 0.6 : 0.15,
                      shadowRadius: 16,
                      elevation: 6,
                    }
              }
            >
              {/* Header: Category Badge / Pill in top right */}
              <View className="flex-row items-center justify-between w-full mb-3">
                <View className="h-1 w-6 rounded-full" style={{ backgroundColor: valueColor }} />
                <View
                  className={`art-stat-pill ${isRed ? "art-stat-pill--red" : ""}`}
                  style={
                    Platform.OS === "web"
                      ? undefined
                      : {
                          backgroundColor: isRed
                            ? isDark
                              ? "rgba(230,0,0,0.2)"
                              : "rgba(230,0,0,0.08)"
                            : isDark
                              ? "rgba(51,103,231,0.2)"
                              : "rgba(51,103,231,0.08)",
                          paddingHorizontal: 10,
                          paddingVertical: 3,
                          borderRadius: 9999,
                        }
                  }
                >
                  <Text
                    style={{
                      fontFamily: "DM Mono",
                      fontSize: 11,
                      fontWeight: "600",
                      color: valueColor,
                      letterSpacing: 0.5,
                    }}
                  >
                    {item.badge}
                  </Text>
                </View>
              </View>

              {/* Big Stat Value */}
              <Text
                className={`art-stat-value ${isRed ? "art-stat-value--red" : ""}`}
                style={
                  Platform.OS === "web"
                    ? undefined
                    : {
                        fontFamily: "Anton",
                        fontSize: 36,
                        lineHeight: 40,
                        color: valueColor,
                        marginBottom: 8,
                      }
                }
              >
                {item.value}
              </Text>

              {/* Descriptive Narrative Text */}
              {item.label ? (
                <Text
                  className="art-stat-body"
                  style={
                    Platform.OS === "web"
                      ? undefined
                      : {
                          fontFamily: "DM Sans",
                          fontSize: 13,
                          lineHeight: 18,
                          color: isDark ? "#E2E2E6" : "#1C1C1E",
                          marginBottom: 16,
                        }
                  }
                >
                  {item.label}
                </Text>
              ) : null}

              {/* Footer: Citation Link with Arrow Icon */}
              <View className="mt-auto pt-2 flex-row items-center justify-between border-t border-black/5 dark:border-white/10">
                <Text
                  className="art-stat-citation"
                  style={
                    Platform.OS === "web"
                      ? undefined
                      : {
                          fontFamily: "DM Sans",
                          fontSize: 11,
                          fontWeight: "600",
                          color: isDark ? "#8BAAFE" : "#3367E7",
                        }
                  }
                >
                  {item.citation || defaultSource}
                  <Text style={{ fontSize: 13, fontWeight: "bold" }}> ↗</Text>
                </Text>
              </View>
            </View>
          );
        })}
      </View>
    </View>
  );
}
