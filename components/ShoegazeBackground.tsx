import React from "react";
import { Platform, StyleSheet, View } from "react-native";
import { useTheme } from "@/lib/theme";

/**
 * ShoegazeBackground
 *
 * Renders an ambient, continuous, fuzzy and grainy moving lava-lamp background.
 * Colorway: Artometrics 3D glasses / Slurpee palette:
 *   - Hot Cherry Red (#E60000)
 *   - Cobalt Electric Blue (#3367E7)
 *   - Deep Void Neutrals (#07080D in dark, #F8F8F6 in light)
 *
 * Web: Pure CSS hardware-accelerated animated fluid orbs with SVG analog noise grain.
 * Native: Graceful static gradient fallback.
 */
export function ShoegazeBackground() {
  const { mode } = useTheme();
  const isDark = mode === "dark";

  if (Platform.OS !== "web") {
    return (
      <View
        pointerEvents="none"
        style={[
          styles.nativeContainer,
          { backgroundColor: isDark ? "#08090E" : "#FAFAF8" },
        ]}
      />
    );
  }

  return (
    <div
      aria-hidden="true"
      className={`shoegaze-stage shoegaze-stage--${mode}`}
      style={{
        position: "fixed",
        inset: 0,
        width: "100vw",
        height: "100vh",
        pointerEvents: "none",
        zIndex: 0,
        overflow: "hidden",
        backgroundColor: isDark ? "#06070B" : "#F7F7F5",
      }}
    >
      {/* Drifting fluid lava lamp orbs */}
      <div className="shoegaze-orb shoegaze-orb--red" />
      <div className="shoegaze-orb shoegaze-orb--blue" />
      <div className="shoegaze-orb shoegaze-orb--indigo" />
      <div className="shoegaze-orb shoegaze-orb--cyan" />

      {/* Analog noise grain texture overlay */}
      <div className="shoegaze-grain" />

      {/* Subtle vignette layer for photographic depth */}
      <div className="shoegaze-vignette" />
    </div>
  );
}

const styles = StyleSheet.create({
  nativeContainer: {
    ...StyleSheet.absoluteFillObject,
    zIndex: 0,
  },
});
