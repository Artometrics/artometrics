import { Pressable, Text, View } from "react-native";
import { Link, usePathname } from "expo-router";
import { Globe, Menu, Search } from "@/components/icons";
import { Logo } from "@/components/Logo";
import { Wrapper } from "@/components/Wrapper";
import { useChrome } from "@/lib/chrome";
import { useLocale } from "@/lib/locale";
import { useTheme } from "@/lib/theme";
import { SITE_PRIMARY_NAV } from "@/lib/site-nav";

export function SiteHeader() {
  const { setMenuOpen } = useChrome();
  const { toggleLocale } = useLocale();
  const { colors } = useTheme();
  const pathname = usePathname();

  return (
    <View className="z-40 border-b border-border bg-header">
      <Wrapper className="py-4">
        <View className="flex-row items-center justify-between">
          <View className="h-10 w-10 items-center justify-center">
            <Pressable
              onPress={() => setMenuOpen(true)}
              accessibilityLabel="Open menu"
              className="h-10 w-10 items-center justify-center lg:hidden"
              testID="site-menu-button"
            >
              <Menu size={22} color={colors.secondary} />
            </Pressable>
            <Pressable
              onPress={toggleLocale}
              accessibilityLabel="Change language"
              accessibilityRole="button"
              className="hidden h-10 w-10 items-center justify-center lg:flex"
            >
              <Globe size={20} color={colors.secondary} strokeWidth={1.75} />
            </Pressable>
          </View>

          <Link href="/" asChild>
            <Pressable accessibilityLabel="Artometrics home">
              <Logo size={42} align="center" className="text-secondary" />
            </Pressable>
          </Link>

          <Link href="/search" asChild>
            <Pressable
              accessibilityLabel="Search reports"
              accessibilityRole="link"
              className="h-10 w-10 items-center justify-center"
            >
              <Search size={20} color={colors.secondary} strokeWidth={1.75} />
            </Pressable>
          </Link>
        </View>
      </Wrapper>

      <View className="hidden border-t border-border lg:block">
        <Wrapper className="py-1">
          <View className="flex-row flex-wrap items-center justify-center gap-x-4 gap-y-1">
            {SITE_PRIMARY_NAV.map((item) => {
              const active = item.isActive(pathname);
              return (
                <Link key={item.href} href={item.href as `/`} asChild>
                  <Pressable className="px-0.5">
                    <Text
                      className={[
                        "font-sans text-[13px] font-semibold uppercase tracking-[2px] text-accent",
                        active ? "underline" : "",
                      ].join(" ")}
                    >
                      {item.label}
                    </Text>
                  </Pressable>
                </Link>
              );
            })}
          </View>
        </Wrapper>
      </View>
    </View>
  );
}
