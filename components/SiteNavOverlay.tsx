import { useEffect, useMemo, useRef, useState } from "react";
import { Platform, Pressable, ScrollView, Text, TextInput, View } from "react-native";
import { Link, usePathname, router } from "expo-router";
import { Globe } from "@/components/icons";
import { Wrapper } from "@/components/Wrapper";
import { useChrome } from "@/lib/chrome";
import { useLocale } from "@/lib/locale";
import { useTheme } from "@/lib/theme";
import { SITE_PRIMARY_NAV } from "@/lib/site-nav";
import {
  getRecentNavSearches,
  rememberNavSearch,
  searchNavAutocomplete,
  type NavAutocompleteHit,
} from "@/lib/search";
import { getNavFunFact } from "@/lib/nav-fun-fact";

const overlayPosition =
  Platform.OS === "web"
    ? ({ position: "fixed" as const })
    : ({ position: "absolute" as const });

function NavSearchRow({
  hit,
  onSelect,
  onPressIn,
}: {
  hit: NavAutocompleteHit;
  onSelect: () => void;
  onPressIn?: () => void;
}) {
  return (
    <Link href={hit.href as `/`} asChild>
      <Pressable
        onPressIn={onPressIn}
        onPress={onSelect}
        className="border-b border-border px-3 py-2.5"
      >
        <Text className="text-[10px] font-bold uppercase tracking-[1.5px] text-accent">
          {hit.meta ?? (hit.kind === "topic" ? "Topic" : "Report")}
        </Text>
        <Text className="font-serif text-lg leading-6 text-accent" numberOfLines={2}>
          {hit.title}
        </Text>
      </Pressable>
    </Link>
  );
}

export function SiteNavOverlay() {
  const pathname = usePathname();
  const { menuOpen, setMenuOpen } = useChrome();
  const { toggleLocale, label } = useLocale();
  const { colors } = useTheme();
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(false);
  const [recent, setRecent] = useState<string[]>([]);
  const blurTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const suggestions = useMemo(() => searchNavAutocomplete(query), [query]);
  const funFact = useMemo(
    () => (menuOpen ? getNavFunFact() : null),
    [menuOpen],
  );
  const showDropdown =
    query.length > 0 ? suggestions.length > 0 : focused && recent.length > 0;

  function refreshRecent() {
    setRecent(getRecentNavSearches());
  }

  function closeAndRemember(term?: string) {
    if (term) rememberNavSearch(term);
    refreshRecent();
    setQuery("");
    setFocused(false);
    setMenuOpen(false);
  }

  function onSearchFocus() {
    if (blurTimer.current) clearTimeout(blurTimer.current);
    setFocused(true);
    refreshRecent();
  }

  function onSearchBlur() {
    blurTimer.current = setTimeout(() => setFocused(false), 120);
  }

  function keepDropdownOpen() {
    if (blurTimer.current) clearTimeout(blurTimer.current);
  }

  useEffect(() => {
    if (!menuOpen) {
      setQuery("");
      setFocused(false);
    }
  }, [menuOpen]);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname, setMenuOpen]);

  useEffect(() => {
    if (Platform.OS !== "web" || typeof document === "undefined") return;
    const prev = document.body.style.overflow;
    if (menuOpen) document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [menuOpen]);

  if (!menuOpen) return null;

  return (
    <View
      className="inset-0 z-[2000] bg-bg"
      style={overlayPosition}
      accessibilityViewIsModal
    >
      <Wrapper className="gap-0 pt-14" variant="narrow">
        <View className="mb-4">
          <View className="flex-row items-center gap-2">
            <View className="min-w-0 flex-1 border border-border pl-3">
              <TextInput
                value={query}
                onChangeText={setQuery}
                onFocus={onSearchFocus}
                onBlur={onSearchBlur}
                placeholder="Search reports & topics…"
                placeholderTextColorClassName="text-subtle"
                className="flex-1 py-2.5 font-sans text-base text-fg"
                returnKeyType="search"
                autoCorrect={false}
                autoCapitalize="none"
                onSubmitEditing={() => {
                  const q = query.trim();
                  if (q.length < 2) return;
                  rememberNavSearch(q);
                  refreshRecent();
                  setMenuOpen(false);
                  router.push(`/search?q=${encodeURIComponent(q)}`);
                }}
              />
            </View>
            <Pressable
              onPress={toggleLocale}
              className="shrink-0 flex-row items-center gap-1 px-0.5 py-1"
              accessibilityLabel="Change language"
              accessibilityRole="button"
            >
              <Globe size={16} color={colors.text} strokeWidth={1.75} />
              <Text className="font-sans text-[10px] font-semibold uppercase tracking-[2px] text-fg">
                {label}
              </Text>
            </Pressable>
            <Pressable
              onPress={() => setMenuOpen(false)}
              className="shrink-0 py-1"
              accessibilityLabel="Close menu"
            >
              <Text className="font-sans text-[10px] font-semibold uppercase tracking-[2px] text-accent">
                Close
              </Text>
            </Pressable>
          </View>
          {showDropdown ? (
            <ScrollView
              className="mt-1 max-h-56 border border-border bg-bg"
              keyboardShouldPersistTaps="handled"
            >
              {query.length > 0
                ? suggestions.map((hit) => (
                    <NavSearchRow
                      key={`${hit.kind}-${hit.href}-${hit.title}`}
                      hit={hit}
                      onPressIn={keepDropdownOpen}
                      onSelect={() => closeAndRemember(query)}
                    />
                  ))
                : recent.map((term) => (
                    <Pressable
                      key={term}
                      onPressIn={keepDropdownOpen}
                      onPress={() => setQuery(term)}
                      className="border-b border-border px-3 py-2.5"
                    >
                      <Text className="text-[10px] font-bold uppercase tracking-[1.5px] text-subtle">
                        Recent
                      </Text>
                      <Text className="font-sans text-sm text-fg">{term}</Text>
                    </Pressable>
                  ))}
            </ScrollView>
          ) : null}
        </View>
        {SITE_PRIMARY_NAV.map((item) => (
          <Link key={item.href} href={item.href as `/`} asChild>
            <Pressable
              onPress={() => setMenuOpen(false)}
              className="flex-row items-center justify-between border-b border-border py-3"
            >
              <Text className="font-sans text-[11px] font-bold uppercase tracking-[2.5px] text-accent">
                {item.label}
              </Text>
              {item.descriptor ? (
                <Text
                  className="ml-3 max-w-[52%] shrink text-right font-sans text-[10px] leading-[14px] text-muted"
                  numberOfLines={2}
                >
                  {item.descriptor}
                </Text>
              ) : null}
            </Pressable>
          </Link>
        ))}
        {funFact ? (
          <View className="mt-16 items-center pb-10 pt-4">
            <Link href={funFact.href} asChild>
              <Pressable
                onPress={() => setMenuOpen(false)}
                accessibilityRole="link"
                accessibilityLabel={`${funFact.text}. ${funFact.title}`}
                accessibilityHint="Opens the full data report"
                className="max-w-md items-center"
              >
                <Text className="mb-3 text-center font-serif text-[22px] italic leading-snug text-accent md:text-[24px]">
                  Did you know?
                </Text>
                <Text
                  className="text-center font-serif text-[26px] italic leading-[1.35] tracking-tight text-fg md:text-[30px]"
                  style={{ transform: [{ rotate: "-1.25deg" }] }}
                >
                  {funFact.text}
                </Text>
              </Pressable>
            </Link>
          </View>
        ) : null}
      </Wrapper>
    </View>
  );
}
