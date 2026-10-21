import {
  Text,
  View,
  type StyleProp,
  type TextStyle,
  type ViewStyle,
} from "react-native";
import { Image } from "expo-image";
import { House } from "@/constants/Colors";
import { assetUrl } from "@/lib/assets";
import { useTheme } from "@/lib/theme";

type Props = {
  style?: StyleProp<TextStyle>;
  size?: number;
  /** Force compact A mark (0–1). Omit to always show full wordmark. */
  compact?: number;
  containerStyle?: StyleProp<ViewStyle>;
  align?: "left" | "center";
  /** Override mark color for dark footers while site is in light mode. */
  markVariant?: "auto" | "light" | "dark";
  /** Show wordmark text. Default true when not fully compact. */
  showWordmark?: boolean;
  className?: string;
  containerClassName?: string;
};

/**
 * 1A lockup — cream Chomsky wordmark plus the standalone A.
 * Header ground is near-black in both themes, so the mark stays cream.
 */
export function Logo({
  style,
  size = 36,
  compact = 0,
  containerStyle,
  align = "left",
  markVariant = "auto",
  showWordmark = true,
  className,
  containerClassName,
}: Props) {
  const { brandStyle } = useTheme();
  const progress = Math.max(0, Math.min(1, compact));
  const markSize = Math.round(size * (0.95 + progress * 0.15));
  const useMark = progress > 0.5;
  const mark = assetUrl("/images/brand/chomsky-a-white.png");
  const markColor = House.cream;
  const isLeft = align === "left";
  const isMagazine = brandStyle === "magazine";
  const alignClass = isLeft ? "items-start" : "items-center";
  const forcedWordColor = markVariant !== "auto" ? markColor : undefined;

  if (useMark) {
    return (
      <View
        className={[
          "min-w-10 justify-center",
          alignClass,
          containerClassName,
        ]
          .filter(Boolean)
          .join(" ")}
        style={[{ height: markSize + 2, width: markSize + 4 }, containerStyle]}
        accessibilityLabel="Artometrics"
      >
        {mark ? (
          <Image
            source={{ uri: mark }}
            style={{ width: markSize, height: markSize }}
            contentFit="contain"
          />
        ) : (
          <Text
            className="text-accent"
            style={{
              fontFamily: isMagazine ? "Chomsky" : "Anton",
              fontSize: markSize,
              lineHeight: markSize * 1.05,
            }}
          >
            A.
          </Text>
        )}
      </View>
    );
  }

  return (
    <View
      className={[
        "min-w-10 flex-row items-center justify-center gap-2",
        alignClass,
        containerClassName,
      ]
        .filter(Boolean)
        .join(" ")}
      style={[{ height: Math.max(size + 2, markSize + 2) }, containerStyle]}
      accessibilityLabel="Artometrics"
    >
      {mark ? (
        <Image
          source={{ uri: mark }}
          style={{ width: Math.round(size * 0.85), height: Math.round(size * 0.85) }}
          contentFit="contain"
          accessibilityElementsHidden
        />
      ) : null}
      {showWordmark ? (
        <Text
          className={[
            isMagazine ? "tracking-wide" : "uppercase tracking-wider",
            isLeft ? "text-left" : "text-center",
            className,
          ]
            .filter(Boolean)
            .join(" ")}
          style={[
            {
              fontFamily: isMagazine ? "Chomsky" : "Anton",
              fontSize: size * (isMagazine ? 0.88 : 0.92),
              color: forcedWordColor ?? markColor,
            },
            style,
          ]}
          numberOfLines={1}
        >
          Artometrics
          {!isMagazine ? <Text style={{ color: House.tiffany }}>.</Text> : null}
        </Text>
      ) : null}
    </View>
  );
}
