import { Pressable, Text, View } from "react-native";
import { Link } from "expo-router";
import { Wrapper } from "@/components/Wrapper";

export function SiteFooter() {
  return (
    <View className="mt-20 border-t border-border bg-header">
      <Wrapper className="py-10">
        <View className="flex-col gap-8 md:flex-row md:items-end md:justify-between">
          <View className="max-w-md gap-2">
            <Text className="font-serif text-lg italic text-muted">
              Scientia potentia est. Data-science reports for the creative industries.
            </Text>
            <Text className="font-sans text-xs uppercase tracking-[0.16em] text-subtle">
              Artometrics Magazine — Independent Investigative Desk
            </Text>
          </View>

          <View className="flex-row flex-wrap items-center gap-x-6 gap-y-2">
            <Link href="/blog" asChild>
              <Pressable>
                <Text className="font-sans text-xs uppercase tracking-[0.14em] text-accent hover:underline">
                  Reports
                </Text>
              </Pressable>
            </Link>
            <Link href="/podcast" asChild>
              <Pressable>
                <Text className="font-sans text-xs uppercase tracking-[0.14em] text-accent hover:underline">
                  Podcast
                </Text>
              </Pressable>
            </Link>
            <Link href="/authors" asChild>
              <Pressable>
                <Text className="font-sans text-xs uppercase tracking-[0.14em] text-accent hover:underline">
                  Authors
                </Text>
              </Pressable>
            </Link>
            <Link href="/studio" asChild>
              <Pressable>
                <Text className="font-sans text-xs uppercase tracking-[0.14em] text-accent hover:underline">
                  Studio
                </Text>
              </Pressable>
            </Link>
            <Link href="/contact" asChild>
              <Pressable>
                <Text className="font-sans text-xs uppercase tracking-[0.14em] text-accent hover:underline">
                  Dispatch
                </Text>
              </Pressable>
            </Link>
            <Link href="/legal" asChild>
              <Pressable>
                <Text className="font-sans text-xs uppercase tracking-[0.14em] text-accent hover:underline">
                  Legal
                </Text>
              </Pressable>
            </Link>
          </View>
        </View>

        <View className="mt-8 flex-row items-center justify-between border-t border-border pt-4">
          <Text className="font-mono text-[11px] text-subtle">
            © {new Date().getFullYear()} Artometrics. All rights reserved.
          </Text>
          <Text className="font-mono text-[11px] text-subtle">
            artometrics.com
          </Text>
        </View>
      </Wrapper>
    </View>
  );
}
