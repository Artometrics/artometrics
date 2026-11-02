import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  type ReactNode,
} from "react";
import { Appearance, Platform } from "react-native";
import { Uniwind } from "uniwind";
import {
  DEFAULT_BRAND_STYLE,
  resolveBrandFonts,
  resolveThemeColors,
  type BrandFonts,
  type BrandStyle,
  type ThemeColors,
  type ThemeMode,
} from "@/constants/Colors";
import { brandThemeCssVars } from "@/lib/uniwind-theme";

type Preference = ThemeMode | "system";

type ThemeContextValue = {
  preference: Preference;
  mode: ThemeMode;
  colors: ThemeColors;
  brandStyle: BrandStyle;
  fonts: BrandFonts;
  setPreference: (p: Preference) => void;
  setBrandStyle: (b: BrandStyle) => void;
  toggle: () => void;
  toggleBrandStyle: () => void;
};

const ThemeContext = createContext<ThemeContextValue | null>(null);

/** Dark magazine only. Light and Swiss were a style toggle; they no longer apply. */
function applyDomTheme(mode: ThemeMode, brand: BrandStyle, colors: ThemeColors) {
  try {
    Appearance.setColorScheme?.(mode);
  } catch {
    /* older runtimes */
  }

  if (Platform.OS !== "web" || typeof document === "undefined") return;
  const bg = colors.bg;
  const fg = colors.text;
  const root = document.documentElement;
  root.dataset.theme = mode;
  root.dataset.brand = brand;
  root.style.setProperty("color-scheme", mode);
  root.style.colorScheme = mode;
  root.style.backgroundColor = bg;
  document.body.style.backgroundColor = bg;
  document.body.style.color = fg;
  const appRoot = document.getElementById("root");
  if (appRoot) {
    appRoot.style.backgroundColor = bg;
    appRoot.style.color = fg;
  }
  const meta = document.querySelector('meta[name="color-scheme"]');
  if (meta) meta.setAttribute("content", mode);
  const themeColor = document.querySelector('meta[name="theme-color"]');
  if (themeColor) themeColor.setAttribute("content", bg);
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const preference: Preference = "dark";
  const brandStyle: BrandStyle = DEFAULT_BRAND_STYLE;
  const mode: ThemeMode = "dark";
  const setPreference = useCallback((_next: Preference) => {}, []);
  const setBrandStyle = useCallback((_next: BrandStyle) => {}, []);
  const toggle = useCallback(() => {}, []);
  const toggleBrandStyle = useCallback(() => {}, []);

  const colors = useMemo(
    () => resolveThemeColors(mode, brandStyle),
    [mode, brandStyle],
  );
  const fonts = useMemo(() => resolveBrandFonts(brandStyle), [brandStyle]);

  useEffect(() => {
    Uniwind.setTheme("dark");
    const vars = brandThemeCssVars(brandStyle);
    Uniwind.updateCSSVariables("light", vars.dark);
    Uniwind.updateCSSVariables("dark", vars.dark);
    applyDomTheme(mode, brandStyle, colors);
  }, [mode, brandStyle, colors]);

  const value = useMemo(
    () => ({
      preference,
      mode,
      colors,
      brandStyle,
      fonts,
      setPreference,
      setBrandStyle,
      toggle,
      toggleBrandStyle,
    }),
    [
      preference,
      mode,
      colors,
      brandStyle,
      fonts,
      setPreference,
      setBrandStyle,
      toggle,
      toggleBrandStyle,
    ],
  );

  return (
    <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
  );
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    return {
      preference: "system" as Preference,
      mode: "dark" as ThemeMode,
      colors: resolveThemeColors("dark", DEFAULT_BRAND_STYLE),
      brandStyle: DEFAULT_BRAND_STYLE,
      fonts: resolveBrandFonts(DEFAULT_BRAND_STYLE),
      setPreference: () => {},
      setBrandStyle: () => {},
      toggle: () => {},
      toggleBrandStyle: () => {},
    };
  }
  return ctx;
}
