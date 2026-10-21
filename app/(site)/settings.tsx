import { useEffect, useState } from "react";
import { Pressable, Text, TextInput, View } from "react-native";
import { Link, router } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PrimaryButton } from "@/components/PrimaryButton";
import { PageSeo } from "@/components/PageSeo";
import { BRAND_STYLE_LABELS, type BrandStyle } from "@/constants/Colors";
import { useTheme } from "@/lib/theme";
import { useAuth } from "@/lib/auth";
import { apiFetch } from "@/lib/supabase/client";
import { PLANS, type PlanTier } from "@/lib/product/plans";
import { openExternalUrl } from "@/lib/openExternal";
import { ensureProfileRow, getProfile, upsertProfile, normalizeHandle } from "@/lib/profile/service";
import { getAnalyticsConsent, setAnalyticsConsent } from "@/lib/analytics/ga";

function formatPlanLabel(planTier: string | null, status: string | null) {
  if (planTier) {
    const plan = PLANS.find((p) => p.tier === (planTier as PlanTier));
    if (plan) {
      const statusNote =
        status === "trialing" ? " (trial)" : status && status !== "active" ? ` (${status})` : "";
      return `${plan.title}${statusNote}`;
    }
  }
  if (status && status !== "inactive") return status;
  return null;
}

export default function SettingsScreen() {
  const { mode, toggle, setPreference, brandStyle, setBrandStyle } = useTheme();
  const { user, loading, signOut } = useAuth();
  const [planLabel, setPlanLabel] = useState<string | null>(null);
  const [active, setActive] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);
  const [displayName, setDisplayName] = useState("");
  const [penName, setPenName] = useState("");
  const [fullName, setFullName] = useState("");
  const [handle, setHandle] = useState("");
  const [bio, setBio] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [birthPlace, setBirthPlace] = useState("");
  const [profileMsg, setProfileMsg] = useState<string | null>(null);
  const [analyticsPref, setAnalyticsPref] = useState<"accepted" | "declined" | null>(null);

  useEffect(() => {
    setAnalyticsPref(getAnalyticsConsent());
  }, []);

  useEffect(() => {
    if (!user) return;
    (async () => {
      try {
        await ensureProfileRow(user.id, user.email, user.user_metadata?.full_name);
        const profile = await getProfile(user.id);
        if (profile) {
          setDisplayName(profile.display_name ?? "");
          setPenName(profile.pen_name ?? "");
          setFullName(profile.full_name ?? "");
          setHandle(profile.handle ?? "");
          setBio(profile.bio ?? "");
          setBirthDate(profile.birth_date ?? "");
          setBirthPlace(profile.birth_place ?? "");
        }
      } catch {
        /* soft */
      }
      try {
        const res = await apiFetch("subscription-status");
        if (res.ok) {
          const data = (await res.json()) as {
            planTier?: string | null;
            status?: string | null;
            active?: boolean;
          };
          setActive(Boolean(data.active));
          setPlanLabel(formatPlanLabel(data.planTier ?? null, data.status ?? null));
        }
      } catch {
        /* soft */
      }
    })();
  }, [user]);

  if (loading) {
    return (
      <Wrapper variant="narrow" className="gap-3.5 py-12">
        <Text className="font-serif text-base leading-7 text-muted">Loading settings…</Text>
      </Wrapper>
    );
  }

  if (!user) {
    return (
      <Wrapper variant="narrow" className="gap-3.5 py-12">
        <PageSeo title="Settings" description="Artometrics account settings." path="/settings" />
        <Text className="font-serif text-[36px] font-bold text-fg">Settings</Text>
        <Text className="font-serif text-base leading-7 text-muted">Log in to manage your account.</Text>
        <Link href="/login" asChild>
          <PrimaryButton label="Log in" />
        </Link>
      </Wrapper>
    );
  }

  async function openPortal() {
    setActionError(null);
    try {
      const res = await apiFetch("create-portal", { method: "POST", body: "{}" });
      const data = (await res.json()) as { url?: string; error?: string };
      if (data.url) {
        const opened = await openExternalUrl(data.url);
        if (opened) return;
      }
      setActionError(data.error ?? "Unable to open billing portal.");
    } catch {
      setActionError("Unable to open billing portal.");
    }
  }

  return (
    <Wrapper variant="narrow" className="gap-3.5 py-12">
      <PageSeo title="Settings" description="Your Artometrics settings." path="/settings" />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Account</Text>
      <Text className="font-serif text-[36px] font-bold text-fg">Settings</Text>
      <Text className="font-serif text-base leading-7 text-muted">{user.email}</Text>
      {planLabel ? (
        <Text className="font-serif text-base leading-7 text-fg">Plan: {planLabel}</Text>
      ) : (
        <Text className="font-serif text-base leading-7 text-subtle">
          No active plan —{" "}
          <Link href="/pricing">
            <Text className="text-accent">view membership</Text>
          </Link>
          .
        </Text>
      )}
      {actionError ? <Text className="font-serif text-base leading-7 text-accent">{actionError}</Text> : null}

      <View className="mt-3 gap-2.5">
        <Text className="font-serif text-[22px] font-bold text-fg">Appearance</Text>
        <Pressable
          onPress={toggle}
          className="border border-border p-3.5 flex-row justify-between items-center"
        >
          <Text className="font-serif text-base leading-7 text-fg">
            {mode === "dark" ? "Dark mode" : "Light mode"}
          </Text>
          <Text className="text-accent font-bold">Switch</Text>
        </Pressable>
        <Pressable onPress={() => setPreference("system")} className="mt-2">
          <Text className="text-muted text-sm">Use system setting</Text>
        </Pressable>

        <Text className="font-serif text-[22px] font-bold mt-5 text-fg">Brand style</Text>
        <Text className="font-serif text-base leading-7 text-muted mb-2">
          Magazine (Anton display, DM Sans body) is the default. Swiss is an alternate condensed chrome.
        </Text>
        {(["swiss", "magazine"] as BrandStyle[]).map((style) => {
          const isSelected = brandStyle === style;
          return (
            <Pressable
              key={style}
              onPress={() => setBrandStyle(style)}
              className={[
                "border p-3.5 flex-row justify-between items-center mt-2",
                isSelected ? "border-accent bg-accent-soft" : "border-border bg-transparent",
              ].join(" ")}
            >
              <Text className="font-serif text-base leading-7 text-fg">
                {BRAND_STYLE_LABELS[style]}
              </Text>
              <Text className="text-accent font-bold">{isSelected ? "Selected" : "Use"}</Text>
            </Pressable>
          );
        })}
      </View>

      <View className="mt-3 gap-2.5">
        <Text className="font-serif text-[22px] font-bold text-fg">Analytics</Text>
        <Text className="font-serif text-base leading-7 text-muted mb-2">
          Optional Google Analytics after consent. You can also accept or decline from the site footer.
        </Text>
        <Pressable
          onPress={() => {
            setAnalyticsConsent(true);
            setAnalyticsPref("accepted");
          }}
          className={[
            "border p-3.5 flex-row justify-between items-center",
            analyticsPref === "accepted" ? "border-accent bg-accent-soft" : "border-border",
          ].join(" ")}
        >
          <Text className="font-serif text-base leading-7 text-fg">Accept analytics</Text>
          <Text className="text-accent font-bold">
            {analyticsPref === "accepted" ? "On" : "Enable"}
          </Text>
        </Pressable>
        <Pressable
          onPress={() => {
            setAnalyticsConsent(false);
            setAnalyticsPref("declined");
          }}
          className={[
            "border p-3.5 flex-row justify-between items-center mt-2",
            analyticsPref === "declined" ? "border-accent bg-accent-soft" : "border-border",
          ].join(" ")}
        >
          <Text className="font-serif text-base leading-7 text-fg">Decline analytics</Text>
          <Text className="text-accent font-bold">
            {analyticsPref === "declined" ? "Off" : "Disable"}
          </Text>
        </Pressable>
      </View>

      <View className="mt-3 gap-2.5">
        <Text className="font-serif text-[22px] font-bold text-fg">Public profile</Text>
        <Text className="font-serif text-[15px] leading-6 text-muted">
          Claim a handle to get `/u/yourname`. Work stays private until you publish.
        </Text>
        {(
          [
            ["Handle", handle, setHandle, "@yourname"],
            ["Display name", displayName, setDisplayName, ""],
            ["Pen name", penName, setPenName, ""],
            ["Bio", bio, setBio, "A short line about your work"],
            ["Full name", fullName, setFullName, ""],
            ["Birth date (YYYY-MM-DD)", birthDate, setBirthDate, ""],
            ["Birth place", birthPlace, setBirthPlace, ""],
          ] as const
        ).map(([label, value, set, ph]) => (
          <View key={label} className="gap-1">
            <Text className="text-xs tracking-wide uppercase font-bold text-muted">{label}</Text>
            <TextInput
              value={value}
              onChangeText={set}
              placeholder={ph}
              placeholderTextColorClassName="text-subtle"
              className="border border-border px-3 py-2.5 text-base text-fg bg-bg-elevated"
              autoCapitalize={label === "Handle" ? "none" : "sentences"}
            />
          </View>
        ))}
        {profileMsg ? <Text className="font-serif text-base leading-7 text-accent">{profileMsg}</Text> : null}
        <PrimaryButton
          label="Save profile"
          onPress={async () => {
            setProfileMsg(null);
            try {
              const normalized = normalizeHandle(handle);
              if (handle.trim() && normalized.length < 3) {
                setProfileMsg("Handle must be at least 3 characters (letters, numbers, _).");
                return;
              }
              await upsertProfile(user.id, {
                display_name: displayName.trim() || null,
                pen_name: penName.trim() || null,
                full_name: fullName.trim() || null,
                handle: handle.trim() ? normalized : null,
                bio: bio.trim() || null,
                birth_date: birthDate.trim() || null,
                birth_place: birthPlace.trim() || null,
              });
              setHandle(normalized || "");
              setProfileMsg("Saved.");
            } catch (e) {
              setProfileMsg(e instanceof Error ? e.message : "Could not save.");
            }
          }}
        />
      </View>

      <View className="flex-row flex-wrap gap-3 mt-4">
        {active ? (
          <PrimaryButton label="Manage billing" onPress={openPortal} />
        ) : (
          <Link href="/pricing" asChild>
            <PrimaryButton label="Start free trial" className="bg-muted" />
          </Link>
        )}
        <Link href="/studio" asChild>
          <PrimaryButton label="Open Studio" />
        </Link>
        <PrimaryButton
          label="Sign out"
          className="bg-muted"
          onPress={async () => {
            await signOut();
            router.replace("/");
          }}
        />
      </View>
    </Wrapper>
  );
}
