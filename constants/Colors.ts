/**
 * Artometrics brand tokens — anaglyph magazine (red/blue on newsprint B&W).
 * Wordmark: Chomsky only. Display + body: DM Sans. Data/meta: DM Mono.
 * Canonical refs: docs/design-bible/tokens.md, docs/design-system/README.md
 */

export type BrandStyle = "swiss" | "magazine";

export const Colors = {
  accent50: "#FFE8E8",
  accent100: "#FFD1D1",
  accent200: "#FFB3B3",
  accent300: "#FF8080",
  accent400: "#FF3333",
  accent500: "#E60000",
  accent600: "#CC0000",
  accent700: "#A30000",
  accent800: "#7A0000",
  accent900: "#520000",
  accent950: "#290000",

  base50: "#FFFFFF",
  base100: "#F7F7F7",
  base200: "#F2F2F2",
  base300: "#E5E5E5",
  base400: "#A3A3A3",
  base500: "#767676",
  base600: "#525252",
  base700: "#404040",
  base800: "#262626",
  base900: "#171717",
  base950: "#000000",

  white: "#FFFFFF",
  black: "#000000",
  cream: "#F2F2F2",
  chartHighlight: "#E60000",
  chartDark: "#000000",
  chartMid: "#525252",

  paper: "#FFFFFF",
  paperElevated: "#F2F2F2",
  ink: "#000000",
  ink2: "#525252",
  ink3: "#767676",
  blue: "#3367E7",
  blueSoft: "#E8EFFF",
  redSoft: "#FFE8E8",
  night: "#000000",
  night2: "#171717",
  rule: "#E5E5E5",
  magazineAccent: "#E60000",
  magazineAccentSoft: "#FFE8E8",
  editorialNavy: "#3367E7",
  editorialNavyDark: "#1E4BB8",
} as const;

export type BrandFonts = {
  display: string;
  sans: string;
  serif: string;
  wordmark: string;
  mono: string;
};

/** Swiss Modern — optional alternate edition (Piazzolla + Archivo). */
export const SwissFonts: BrandFonts = {
  display: "Piazzolla, Georgia, serif",
  sans: "Archivo, Helvetica Neue, Helvetica, Arial, system-ui, sans-serif",
  serif: "Piazzolla, Georgia, serif",
  wordmark: "Chomsky, Georgia, serif",
  mono: "DM Mono, 'Courier New', Courier, monospace",
};

/** Magazine default — DM Sans display/body, Chomsky masthead only. */
export const MagazineFonts: BrandFonts = {
  display: "DM Sans, system-ui, sans-serif",
  sans: "DM Sans, system-ui, sans-serif",
  serif: "DM Sans, system-ui, sans-serif",
  wordmark: "Chomsky, Georgia, serif",
  mono: "DM Mono, ui-monospace, monospace",
};

/** Default static StyleSheets — magazine. Prefer useTheme().fonts when brand-aware. */
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
  secondary: string;
  inverse: string;
  headerBg: string;
  overlayBg: string;
  rule: string;
};

const SwissThemes: Record<ThemeMode, ThemeColors> = {
  light: {
    mode: "light",
    bg: Colors.paper,
    bgElevated: Colors.paperElevated,
    text: Colors.ink,
    textMuted: Colors.ink2,
    textSubtle: Colors.ink3,
    border: Colors.rule,
    accent: Colors.accent500,
    accentSoft: Colors.redSoft,
    secondary: Colors.blue,
    inverse: Colors.paper,
    headerBg: Colors.paper,
    overlayBg: Colors.paperElevated,
    rule: Colors.black,
  },
  dark: {
    mode: "dark",
    bg: Colors.night,
    bgElevated: Colors.night2,
    text: Colors.white,
    textMuted: Colors.base400,
    textSubtle: Colors.base500,
    border: Colors.base800,
    accent: Colors.accent400,
    accentSoft: "#3D1515",
    secondary: Colors.blue,
    inverse: Colors.black,
    headerBg: Colors.night,
    overlayBg: Colors.night2,
    rule: Colors.white,
  },
};

const MagazineThemes: Record<ThemeMode, ThemeColors> = {
  light: {
    mode: "light",
    bg: Colors.paper,
    bgElevated: Colors.paperElevated,
    text: Colors.ink,
    textMuted: Colors.ink2,
    textSubtle: Colors.ink3,
    border: Colors.rule,
    accent: Colors.accent500,
    accentSoft: Colors.redSoft,
    secondary: Colors.blue,
    inverse: Colors.paper,
    headerBg: Colors.paper,
    overlayBg: Colors.paperElevated,
    rule: Colors.black,
  },
  dark: {
    mode: "dark",
    bg: Colors.night,
    bgElevated: Colors.night2,
    text: Colors.white,
    textMuted: Colors.base400,
    textSubtle: Colors.base500,
    border: Colors.base800,
    accent: Colors.accent400,
    accentSoft: "#3D1515",
    secondary: Colors.blue,
    inverse: Colors.black,
    headerBg: Colors.night,
    overlayBg: Colors.night2,
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
  magazine: "Magazine (DM Sans / anaglyph)",
};

export const DEFAULT_BRAND_STYLE: BrandStyle = "magazine";
