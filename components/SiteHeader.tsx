import { Pressable, Text, View } from "react-native";
import { Link, usePathname } from "expo-router";
import { Globe, Menu, Search } from "@/components/icons";
import { Logo } from "@/components/Logo";
import { Wrapper } from "@/components/Wrapper";
import { useChrome } from "@/lib/chrome";
import { useLocale } from "@/lib/locale";
import { House } from "@/constants/Colors";
import { SITE_PRIMARY_NAV } from "@/lib/site-nav";
import { formatHeaderDateline } from "@/lib/headerDateline";

export function SiteHeader() {
  const { setMenuOpen } = useChrome();
  const { toggleLocale } = useLocale();
  const pathname = usePathname();

  const dateline = formatHeaderDateline();

  return (
    <View
      className="z-40 border-b"
      style={{ backgroundColor: House.groundDeep, borderBottomColor: "#2a3330" }}
    >
      <View className="border-b" style={{ borderBottomColor: "#2a3330" }}>
        <Wrapper className="py-1.5">
          <Text
            className="text-center font-mono text-[10px] font-medium uppercase tracking-[0.14em]"
            style={{ color: House.muted }}
            accessibilityRole="text"
          >
            {dateline}
          </Text>
        </Wrapper>
      </View>
      <Wrapper className="py-4">
        <View className="flex-row items-center justify-between">
          <View className="h-10 w-10 items-center justify-center">
            <Pressable
              onPress={() => setMenuOpen(true)}
              accessibilityRole="button"
              accessibilityLabel="Open menu"
              className="h-10 w-10 items-center justify-center lg:hidden"
              testID="site-menu-button"
            >
              <Menu size={22} color={House.muted} />
            </Pressable>
            <Pressable
              onPress={toggleLocale}
              accessibilityLabel="Change language"
              accessibilityRole="button"
              className="hidden h-10 w-10 items-center justify-center lg:flex"
            >
              <Globe size={20} color={House.muted} strokeWidth={1.75} />
            </Pressable>
          </View>

          <Link href="/" asChild>
            <Pressable accessibilityLabel="Artometrics home">
              <Logo size={42} align="center" />
            </Pressable>
          </Link>

          <Link href="/search" asChild>
            <Pressable
              accessibilityLabel="Search reports"
              accessibilityRole="link"
              className="h-10 w-10 items-center justify-center"
            >
              <Search size={20} color={House.muted} strokeWidth={1.75} />
            </Pressable>
          </Link>
        </View>
      </Wrapper>

      <View className="hidden border-t lg:block" style={{ borderTopColor: "#2a3330" }}>
        <Wrapper className="py-2">
          <View className="flex-row flex-wrap items-center justify-center gap-2">
            {SITE_PRIMARY_NAV.map((item) => {
              const active = item.isActive(pathname);
              return (
                <Link key={item.href} href={item.href as `/`} asChild>
                  <Pressable
                    className={active ? "house-nav-tab house-nav-tab--on" : "house-nav-tab"}
                    style={{
                      borderWidth: 1,
                      borderColor: House.cream,
                      backgroundColor: active ? House.cream : "transparent",
                      paddingHorizontal: 10,
                      minHeight: 36,
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <Text
                      className="font-mono text-[12px] uppercase tracking-[0.08em]"
                      style={{ color: active ? House.groundDeep : House.cream }}
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
