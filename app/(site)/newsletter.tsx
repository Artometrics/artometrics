import { useState } from "react";
import {
  ActivityIndicator,
  Platform,
  Text,
  TextInput,
  Pressable,
  View,
} from "react-native";
import { Link } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { trackEvent } from "@/lib/analytics/ga";
import { submitLeadToTwenty } from "@/lib/crm/twenty";

const FORM_NAME = "artometrics-newsletter";

export default function NewsletterScreen() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "saving" | "done" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    const value = email.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      setError("Enter a valid email address.");
      setStatus("error");
      return;
    }
    setStatus("saving");
    setError(null);
    try {
      if (Platform.OS === "web") {
        const body = new URLSearchParams({
          "form-name": FORM_NAME,
          email: value,
        });
        const res = await fetch("/", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: body.toString(),
        });
        if (!res.ok) throw new Error(`Form error (${res.status})`);
      }
      // Sync to Twenty CRM under company Artometrics
      await submitLeadToTwenty({ email: value, source: "newsletter_page" });
      trackEvent("newsletter_submit", { source: "newsletter_page" });
      setStatus("done");
    } catch {
      setError("Could not subscribe right now. Try again shortly.");
      setStatus("error");
    }
  }

  return (
    <Wrapper variant="narrow" className="gap-3.5 py-12">
      <PageSeo
        title="Newsletter"
        description="Notes from Artometrics — new reports, datasets, and interviews."
        path="/newsletter"
      />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Inbox</Text>
      <Text className="font-display text-[40px] uppercase text-fg">Newsletter</Text>
      <Text className="font-sans text-base leading-[26px] text-muted">
        Occasional notes when a report ships. No spam. Read the{" "}
        <Link href="/legal/privacy">
          <Text className="text-accent">privacy policy</Text>
        </Link>
        .
      </Text>
      {status === "done" ? (
        <Text className="font-sans text-base leading-[26px] text-fg">
          Thanks — you are on the list. We will write when something ships.
        </Text>
      ) : (
        <View className="flex-row border-2 border-border mt-2">
          <TextInput
            value={email}
            onChangeText={setEmail}
            placeholder="Enter your email"
            placeholderTextColorClassName="text-subtle"
            keyboardType="email-address"
            autoCapitalize="none"
            editable={status !== "saving"}
            className="flex-1 px-3 py-3 text-base text-fg"
            onSubmitEditing={() => void submit()}
          />
          <Pressable
            onPress={() => void submit()}
            disabled={status === "saving"}
            className="px-4 justify-center py-3.5 min-w-[96px] bg-accent"
          >
            {status === "saving" ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text className="text-white font-extrabold tracking-wide text-xs uppercase">
                Sign up
              </Text>
            )}
          </Pressable>
        </View>
      )}
      {error ? <Text className="text-sm text-accent">{error}</Text> : null}
      {Platform.OS !== "web" ? (
        <Text className="text-xs mt-1 text-subtle">
          Newsletter signup is available on the web at artometrics.com/newsletter.
        </Text>
      ) : null}
    </Wrapper>
  );
}
