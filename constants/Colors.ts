/**
 * Artometrics brand tokens — KSM-energy zine (Anton + hot red) on Artometrics identity.
 * Wordmark: Chomsky. Display: Anton. Body: DM Sans. Data: DM Mono.
 * Accent UI #E60000 (KSM punch); print/editorial #C0392B kept as magazineAccent.
 * Canonical refs: docs/design-system/, Notion Brand & design / KSM Brand Kit.
 */

export type BrandStyle = "swiss" | "magazine";

export const Colors = {
  accent50: "#FFF1F0",
  accent100: "#FFD9D6",
  accent200: "#FFB3AD",
  accent300: "#FF7A70",
  accent400: "#FF2E2E",
  accent500: "#E60000",
  accent600: "#B80000",
  accent700: "#A31812",
  accent800: "#7F120E",
  accent900: "#5C0D0A",
  accent950: "#3A0806",

  base50: "#FFFFFF",
  base100: "#F5F5F5",
  base200: "#E5E5E5",
  base300: "#D4D4D4",
  base400: "#A3A3A3",
  base500: "#737373",
  base600: "#525252",
  base700: "#2A2A2A",
  base800: "#141414",
  base900: "#0A0A0A",
  base950: "#000000",

  white: "#FFFFFF",
  black: "#000000",
  cream: "#FFFFFF",
  chartHighlight: "#C0392B",
  chartDark: "#000000",
  chartMid: "#525252",

  /** Kruger / newspaper — pure paper, hard red */
  paper: "#FFFFFF",
  paperElevated: "#FFFFFF",
  magazineAccent: "#C0392B",
  magazineAccentSoft: "#F9E8E6",
  /** Editorial blue — wordmark, report titles, links (site + article --art-secondary). */
  editorialNavy: "#3367E7",
  editorialNavyDark: "#6B94FF",
} as const;

export type BrandFonts = {
  display: string;
  sans: string;
  serif: string;
  wordmark: string;
  mono: string;
};

/** Swiss Modern — condensed display + system sans. */
export const SwissFonts: BrandFonts = {
  display: "Anton",
  sans: "Helvetica Neue, Helvetica, Arial, system-ui, sans-serif",
  serif: "Helvetica Neue, Helvetica, Arial, system-ui, sans-serif",
  wordmark: "Anton",
  mono: "'Courier New', Courier, monospace",
};

/**
 * Magazine default — Anton display (KSM energy), DM Sans body, DM Mono data.
 * Chomsky is reserved for the Logo / wordmark only.
 */
export const MagazineFonts: BrandFonts = {
  display: "Anton",
  sans: "DM Sans",
  serif: "DM Sans",
  wordmark: "Chomsky",
  mono: "DM Mono",
};

/** Default static StyleSheets — magazine / DM Sans+Mono. Prefer useTheme().fonts when brand-aware. */
export const Fonts = MagazineFonts;

export type ThemeMode = "light" | "dark";

export type ThemeColors = {
  mode: ThemeMode;
  bg: string;
  bgElevated: string;
  text: string;
  textMuted: string;
  textSubtle: string;
  border: string;
  accent: string;
  accentSoft: string;
  inverse: string;
  headerBg: string;
  overlayBg: string;
  rule: string;
};

const SwissThemes: Record<ThemeMode, ThemeColors> = {
  light: {
    mode: "light",
    bg: Colors.white,
    bgElevated: Colors.white,
    text: Colors.black,
    textMuted: Colors.base600,
    textSubtle: Colors.base500,
    border: Colors.black,
    accent: Colors.accent500,
    accentSoft: Colors.accent50,
    inverse: Colors.white,
    secondary: Colors.editorialNavy,
    inverse: Colors.white,
    headerBg: Colors.white,
    overlayBg: Colors.white,
    rule: Colors.black,
  },
  dark: {
    mode: "dark",
    bg: Colors.black,
    bgElevated: Colors.base900,
    text: Colors.white,
    textMuted: Colors.base400,
    textSubtle: Colors.base500,
    border: Colors.white,
    accent: Colors.accent400,
    accentSoft: Colors.accent950,
    secondary: Colors.editorialNavyDark,
    headerBg: Colors.black,
    overlayBg: Colors.black,
    rule: Colors.white,
  },
};

/** Kruger magazine: white/black/red light; inverted dark. */
const MagazineThemes: Record<ThemeMode, ThemeColors> = {
  light: {
    mode: "light",
    bg: Colors.white,
    bgElevated: Colors.white,
    text: Colors.black,
    textMuted: Colors.base600,
    textSubtle: Colors.base500,
    border: Colors.black,
    accent: Colors.accent500,
    accentSoft: Colors.accent50,
    inverse: Colors.white,
    secondary: Colors.editorialNavy,
    inverse: Colors.white,
    headerBg: Colors.white,
    overlayBg: Colors.white,
    rule: Colors.black,
  },
  dark: {
    mode: "dark",
    bg: Colors.black,
    bgElevated: Colors.base800,
    text: Colors.white,
    textMuted: "#C8C8C8",
    textSubtle: Colors.base500,
    border: Colors.white,
    accent: Colors.accent500,
    accentSoft: Colors.accent950,
    secondary: Colors.editorialNavyDark,
    headerBg: Colors.black,
    overlayBg: Colors.base800,
    rule: Colors.white,
  },
};

export const Themes = MagazineThemes;

export function resolveThemeColors(mode: ThemeMode, brand: BrandStyle): ThemeColors {
  return brand === "magazine" ? MagazineThemes[mode] : SwissThemes[mode];
}

export function resolveBrandFonts(brand: BrandStyle): BrandFonts {
  return brand === "magazine" ? MagazineFonts : SwissFonts;
}

export const BRAND_STYLE_LABELS: Record<BrandStyle, string> = {
  swiss: "Swiss Modern",
  magazine: "Magazine (Anton / DM Sans)",
};

export const DEFAULT_BRAND_STYLE: BrandStyle = "magazine";
