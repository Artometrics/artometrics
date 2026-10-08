/**
 * Artometrics brand tokens — KSM-energy zine (Anton + hot red) on Artometrics identity.
 * Wordmark: Chomsky. Display: Anton. Body: DM Sans. Data: DM Mono.
 * Accent UI #E60000 (KSM punch); print/editorial #C0392B kept as magazineAccent.
 * Canonical refs: docs/design-system/, Notion Brand & design / KSM Brand Kit.
 */

export type BrandStyle = "swiss" | "magazine";

export const Colors = {
  accent50: "#FBF7EE",
  accent100: "#F5EEDC",
  accent200: "#EBDCB9",
  accent300: "#D8C6A0",
  accent400: "#AE8B52",
  accent500: "#7D6222",
  accent600: "#6B531D",
  accent700: "#544117",
  accent800: "#3F3111",
  accent900: "#2A200B",
  accent950: "#151005",

  base50: "#FCFBF9",
  base100: "#F4F1EA",
  base200: "#EBE8E1",
  base300: "#D6D3CC",
  base400: "#B3B0AA",
  base500: "#8A8780",
  base600: "#68655C",
  base700: "#59564C",
  base800: "#2A2722",
  base900: "#202120",
  base950: "#111212",

  white: "#F4F1EA",
  black: "#1D1A15",
  cream: "#EBE8E1",
  chartHighlight: "#7D6222",
  chartDark: "#1D1A15",
  chartMid: "#59564C",

  /** Bellum Systems newsprint parchment & tactical ink */
  paper: "#F4F1EA",
  paperElevated: "#EBE8E1",
  ink: "#1D1A15",
  ink2: "#59564C",
  ink3: "#68655C",
  gold: "#A8862E",
  goldDeep: "#7D6222",
  paleGold: "#D8C6A0",
  night: "#111212",
  night2: "#202120",
  rule: "#D6D3CC",
  magazineAccent: "#7D6222",
  magazineAccentSoft: "#F5EEDC",
  /** Editorial gold — wordmark, titles, active nav links */
  editorialNavy: "#7D6222",
  editorialNavyDark: "#AE8B52",
} as const;

export type BrandFonts = {
  display: string;
  sans: string;
  serif: string;
  wordmark: string;
  mono: string;
};

/** Swiss Modern — Archivo sans + Piazzolla chiseled display. */
export const SwissFonts: BrandFonts = {
  display: "Piazzolla, Georgia, serif",
  sans: "Archivo, Helvetica Neue, Helvetica, Arial, system-ui, sans-serif",
  serif: "Piazzolla, Georgia, serif",
  wordmark: "Piazzolla, Georgia, serif",
  mono: "DM Mono, 'Courier New', Courier, monospace",
};

/**
 * Magazine default — Piazzolla chiseled serif display, Archivo technical sans, Chomsky masthead.
 */
export const MagazineFonts: BrandFonts = {
  display: "Piazzolla, Georgia, serif",
  sans: "Archivo, Helvetica Neue, Helvetica, Arial, system-ui, sans-serif",
  serif: "Piazzolla, Georgia, serif",
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
    accent: Colors.goldDeep,
    accentSoft: Colors.accent100,
    secondary: Colors.gold,
    inverse: Colors.paper,
    headerBg: Colors.paper,
    overlayBg: Colors.paperElevated,
    rule: Colors.rule,
  },
  dark: {
    mode: "dark",
    bg: Colors.night,
    bgElevated: Colors.night2,
    text: Colors.paper,
    textMuted: Colors.paleGold,
    textSubtle: Colors.base400,
    border: Colors.base800,
    accent: Colors.accent400,
    accentSoft: "#2A2316",
    secondary: Colors.paleGold,
    inverse: Colors.night,
    headerBg: Colors.night,
    overlayBg: Colors.night2,
    rule: Colors.base800,
  },
};

/** Bellum magazine: warm paper/ink/gold light; deep night/pale-gold dark. */
const MagazineThemes: Record<ThemeMode, ThemeColors> = {
  light: {
    mode: "light",
    bg: Colors.paper,
    bgElevated: Colors.paperElevated,
    text: Colors.ink,
    textMuted: Colors.ink2,
    textSubtle: Colors.ink3,
    border: Colors.rule,
    accent: Colors.goldDeep,
    accentSoft: Colors.accent100,
    secondary: Colors.gold,
    inverse: Colors.paper,
    headerBg: Colors.paper,
    overlayBg: Colors.paperElevated,
    rule: Colors.rule,
  },
  dark: {
    mode: "dark",
    bg: Colors.night,
    bgElevated: Colors.night2,
    text: Colors.paper,
    textMuted: Colors.paleGold,
    textSubtle: Colors.base400,
    border: Colors.base800,
    accent: Colors.accent400,
    accentSoft: "#2A2316",
    secondary: Colors.paleGold,
    inverse: Colors.night,
    headerBg: Colors.night,
    overlayBg: Colors.night2,
    rule: Colors.base800,
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
