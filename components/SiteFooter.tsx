import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { House } from "@/constants/Colors";
import { Wrapper } from "@/components/Wrapper";

export function SiteFooter() {
  return (
    <View
      className="mt-20 border-t"
      style={{ backgroundColor: House.groundDeep, borderTopColor: "#2a3330" }}
    >
      <Wrapper className="py-10">
        <View className="flex-col gap-8 md:flex-row md:items-end md:justify-between">
          <View className="max-w-md gap-2">
            <Text className="font-serif text-lg italic" style={{ color: House.cream }}>
              Scientia potentia est. Data-science reports for the creative industries.
            </Text>
            <Text className="font-sans text-xs uppercase tracking-[0.16em]" style={{ color: House.muted }}>
              Artometrics Magazine — Independent Investigative Desk
            </Text>
          </View>

          <View className="flex-row flex-wrap items-center gap-x-6 gap-y-2">
            <Link href="/blog" asChild>
              <Pressable>
                <Text
                  className="font-sans text-xs uppercase tracking-[0.14em] hover:underline"
                  style={{ color: House.tiffany }}
                >
                  Reports
                </Text>
              </Pressable>
            </Link>
            <Link href="/podcast" asChild>
              <Pressable>
                <Text
                  className="font-sans text-xs uppercase tracking-[0.14em] hover:underline"
                  style={{ color: House.tiffany }}
                >
                  Podcast
                </Text>
              </Pressable>
            </Link>
            <Link href="/authors" asChild>
              <Pressable>
                <Text
                  className="font-sans text-xs uppercase tracking-[0.14em] hover:underline"
                  style={{ color: House.tiffany }}
                >
                  Authors
                </Text>
              </Pressable>
            </Link>
            <Link href="/studio" asChild>
              <Pressable>
                <Text
                  className="font-sans text-xs uppercase tracking-[0.14em] hover:underline"
                  style={{ color: House.tiffany }}
                >
                  Studio
                </Text>
              </Pressable>
            </Link>
            <Link href="/contact" asChild>
              <Pressable>
                <Text
                  className="font-sans text-xs uppercase tracking-[0.14em] hover:underline"
                  style={{ color: House.tiffany }}
                >
                  Dispatch
                </Text>
              </Pressable>
            </Link>
            <Link href="/legal" asChild>
              <Pressable>
                <Text
                  className="font-sans text-xs uppercase tracking-[0.14em] hover:underline"
                  style={{ color: House.tiffany }}
                >
                  Legal
                </Text>
              </Pressable>
            </Link>
          </View>
        </View>

        <View className="mt-8 flex-row items-center justify-between border-t border-border pt-4">
          <Text className="font-mono text-[11px]" style={{ color: House.muted }}>
            © {new Date().getFullYear()} Artometrics. All rights reserved.
          </Text>
          <Text className="font-mono text-[11px]" style={{ color: House.muted }}>
            artometrics.com
          </Text>
        </View>
      </Wrapper>
    </View>
  );
}
