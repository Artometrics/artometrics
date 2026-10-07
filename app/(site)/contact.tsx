import { useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  Text,
  TextInput,
  View,
} from "react-native";
import { Link } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PrimaryButton } from "@/components/PrimaryButton";
import { PageSeo } from "@/components/PageSeo";
import { openExternalUrl } from "@/lib/openExternal";
import { submitLeadToTwenty } from "@/lib/crm/twenty";
import { trackEvent } from "@/lib/analytics/ga";

export default function ContactScreen() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<"idle" | "saving" | "done" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  async function handleSendTip() {
    const cleanEmail = email.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(cleanEmail)) {
      setError("Please provide a valid email address.");
      setStatus("error");
      return;
    }
    setStatus("saving");
    setError(null);
    try {
      await submitLeadToTwenty({
        name: name.trim() || undefined,
        email: cleanEmail,
        message: message.trim() || undefined,
        source: "contact_editorial_tip",
      });
      trackEvent("contact_tip_submit", { source: "contact_page" });
      setStatus("done");
      setName("");
      setEmail("");
      setMessage("");
    } catch {
      setError("Unable to transmit right now. Please try hello@artometrics.com directly.");
      setStatus("error");
    }
  }

  return (
    <Wrapper variant="narrow" className="gap-3.5 py-12">
      <PageSeo
        title="Contact"
        description="Editorial tips, press, corrections, and partnerships for Artometrics."
        path="/contact"
      />
      <Text className="text-[11px] font-semibold uppercase tracking-[2.5px] text-accent">
        Contact
      </Text>
      <Text role="heading" aria-level={1} className="font-display text-[36px] text-fg">Get in touch</Text>
      <Text className="mb-2 font-serif text-base leading-7 text-muted">
        Editorial tips, dataset corrections, press, and partnership notes go to the Artometrics
        desk.
      </Text>

      <View className="gap-3 border-t-2 border-fg pt-4">
        <Text className="font-serif text-[22px] font-bold text-fg">Direct dispatch & tips</Text>
        <Text className="font-serif text-base leading-7 text-muted">
          Send confidential leads, story inquiries, or partner proposals directly to the desk CRM.
        </Text>

        {status === "done" ? (
          <View className="p-4 bg-muted/10 border-l-2 border-accent my-2">
            <Text className="font-serif text-base text-fg font-medium">
              Dispatch received. The Artometrics desk will review your submission.
            </Text>
          </View>
        ) : (
          <View className="gap-3 my-2">
            <TextInput
              value={name}
              onChangeText={setName}
              placeholder="Your name / affiliation"
              placeholderTextColorClassName="text-subtle"
              editable={status !== "saving"}
              className="border border-border px-3 py-2.5 text-base text-fg font-sans"
            />
            <TextInput
              value={email}
              onChangeText={setEmail}
              placeholder="Your email address (required)"
              placeholderTextColorClassName="text-subtle"
              keyboardType="email-address"
              autoCapitalize="none"
              editable={status !== "saving"}
              className="border border-border px-3 py-2.5 text-base text-fg font-sans"
            />
            <TextInput
              value={message}
              onChangeText={setMessage}
              placeholder="Your note or lead summary..."
              placeholderTextColorClassName="text-subtle"
              multiline
              numberOfLines={4}
              editable={status !== "saving"}
              className="border border-border px-3 py-2.5 text-base text-fg font-sans min-h-[96px]"
            />
            {error ? <Text className="text-sm text-accent">{error}</Text> : null}
            <Pressable
              onPress={() => void handleSendTip()}
              disabled={status === "saving"}
              className="bg-accent px-5 py-3 self-start items-center justify-center min-w-[140px]"
            >
              {status === "saving" ? (
                <ActivityIndicator color="#FFFFFF" size="small" />
              ) : (
                <Text className="text-white font-extrabold tracking-wide text-xs uppercase">
                  Transmit dispatch
                </Text>
              )}
            </Pressable>
          </View>
        )}
      </View>

      <View className="gap-3 border-t border-border pt-4">
        <Text className="font-serif text-[22px] font-bold text-fg">Email editorial</Text>
        <Text className="font-serif text-base leading-7 text-muted">
          Story ideas, corrections, and data leads via client: hello@artometrics.com
        </Text>
        <PrimaryButton
          label="Open mail client"
          onPress={() => void openExternalUrl("mailto:hello@artometrics.com")}
        />
      </View>

      <View className="gap-3 border-t border-border pt-4">
        <Text className="font-serif text-[22px] font-bold text-fg">Press</Text>
        <Text className="font-serif text-base leading-7 text-muted">
          Boilerplate, brand assets, and interview requests live on the press page.
        </Text>
        <Link href="/press" asChild>
          <PrimaryButton label="Press kit" className="bg-muted" />
        </Link>
      </View>

      <View className="gap-3 border-t border-border pt-4">
        <Text className="font-serif text-[22px] font-bold text-fg">Ethics</Text>
        <Link href="/legal/ethics-statement" asChild>
          <PrimaryButton label="Ethics statement" className="bg-muted" />
        </Link>
      </View>
    </Wrapper>
  );
}
