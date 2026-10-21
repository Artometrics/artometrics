import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { Appearance, Platform } from "react-native";
import { kv } from "@/lib/storage/kv";
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
const STORAGE_KEY = "artometrics-theme";
const BRAND_KEY = "artometrics-brand-style";

function systemMode(): ThemeMode {
  if (Platform.OS === "web" && typeof window !== "undefined") {
    return window.matchMedia?.("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }
  return Appearance.getColorScheme() === "dark" ? "dark" : "light";
}

function readStoredPreferenceSync(): Preference | null {
  try {
    const saved = kv.getString(STORAGE_KEY);
    if (saved === "light" || saved === "dark" || saved === "system") return saved;
  } catch {
    /* ignore */
  }
  return null;
}

function readStoredBrandSync(): BrandStyle | null {
  try {
    const saved = kv.getString(BRAND_KEY);
    if (saved === "swiss" || saved === "magazine") return saved;
  } catch {
    /* ignore */
  }
  return null;
}

async function readStoredPreference(): Promise<Preference | null> {
  try {
    const saved = await kv.getItem(STORAGE_KEY);
    if (saved === "light" || saved === "dark" || saved === "system") return saved;
  } catch {
    /* ignore */
  }
  return null;
}

async function readStoredBrand(): Promise<BrandStyle | null> {
  try {
    const saved = await kv.getItem(BRAND_KEY);
    if (saved === "swiss" || saved === "magazine") return saved;
  } catch {
    /* ignore */
  }
  return null;
}

async function writeStoredPreference(p: Preference): Promise<void> {
  try {
    await kv.setItem(STORAGE_KEY, p);
  } catch {
    /* ignore */
  }
}

async function writeStoredBrand(b: BrandStyle): Promise<void> {
  try {
    await kv.setItem(BRAND_KEY, b);
  } catch {
    /* ignore */
  }
}

/** Keep html/body/#root + RN Appearance in lockstep (fixes light text on white). */
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
  const [preference, setPreferenceState] = useState<Preference>(
    () => readStoredPreferenceSync() ?? "dark",
  );
  const [brandStyle, setBrandStyleState] = useState<BrandStyle>(
    () => readStoredBrandSync() ?? DEFAULT_BRAND_STYLE,
  );
  const [system, setSystem] = useState<ThemeMode>(() => systemMode());

  useEffect(() => {
    setSystem(systemMode());
    let cancelled = false;
    void readStoredPreference().then((saved) => {
      if (!cancelled && saved) setPreferenceState(saved);
    });
    void readStoredBrand().then((saved) => {
      if (!cancelled && saved) setBrandStyleState(saved);
    });

    if (Platform.OS === "web" && typeof window !== "undefined") {
      const mq = window.matchMedia("(prefers-color-scheme: dark)");
      const onChange = () => setSystem(mq.matches ? "dark" : "light");
      mq.addEventListener?.("change", onChange);
      return () => {
        cancelled = true;
        mq.removeEventListener?.("change", onChange);
      };
    }

    const sub = Appearance.addChangeListener(({ colorScheme }) => {
      setSystem(colorScheme === "dark" ? "dark" : "light");
    });
    return () => {
      cancelled = true;
      sub.remove();
    };
  }, []);

  const setPreference = useCallback((p: Preference) => {
    setPreferenceState(p);
    void writeStoredPreference(p);
  }, []);

  const setBrandStyle = useCallback((b: BrandStyle) => {
    setBrandStyleState(b);
    void writeStoredBrand(b);
  }, []);

  const mode: ThemeMode = preference === "system" ? system : preference;

  const toggle = useCallback(() => {
    setPreference(mode === "dark" ? "light" : "dark");
  }, [mode, setPreference]);

  const toggleBrandStyle = useCallback(() => {
    setBrandStyle(brandStyle === "swiss" ? "magazine" : "swiss");
  }, [brandStyle, setBrandStyle]);

  const colors = useMemo(
    () => resolveThemeColors(mode, brandStyle),
    [mode, brandStyle],
  );
  const fonts = useMemo(() => resolveBrandFonts(brandStyle), [brandStyle]);

  useEffect(() => {
    // Keep Uniwind className themes in lockstep with preference + brand tokens.
    Uniwind.setTheme(preference === "system" ? "system" : preference);
    const vars = brandThemeCssVars(brandStyle);
    Uniwind.updateCSSVariables("light", vars.light);
    Uniwind.updateCSSVariables("dark", vars.dark);
    applyDomTheme(mode, brandStyle, colors);
  }, [preference, mode, brandStyle, colors]);

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
