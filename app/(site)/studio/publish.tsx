import { useEffect, useState } from "react";
import { Text, TextInput, View } from "react-native";
import { router, useLocalSearchParams } from "expo-router";
import { Wrapper } from "@/components/Wrapper";
import { PageSeo } from "@/components/PageSeo";
import { PrimaryButton } from "@/components/PrimaryButton";
import { useAuth } from "@/lib/auth";
import {
  createOrUpdateDraft,
  publishToProfile,
  submitToMagazine,
} from "@/lib/platform/posts";
import { getProfile } from "@/lib/profile/service";
import { apiFetch } from "@/lib/supabase/client";
import { paramString } from "@/lib/params";

export default function StudioPublishScreen() {
  const { user, loading } = useAuth();
  const params = useLocalSearchParams<{
    title?: string | string[];
    body?: string | string[];
    source?: string | string[];
    sourceId?: string | string[];
  }>();
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [sourceKind, setSourceKind] = useState<string>("freeform");
  const [sourceId, setSourceId] = useState<string | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    const t = paramString(params.title);
    const b = paramString(params.body);
    const s = paramString(params.source);
    const sid = paramString(params.sourceId);
    if (t) setTitle(t);
    if (b) setBody(b);
    if (s) setSourceKind(s);
    if (sid) setSourceId(sid);
  }, [params.title, params.body, params.source, params.sourceId]);

  if (loading || !user) {
    if (!loading && !user) router.replace("/login?next=%2Fstudio%2Fpublish");
    return (
      <Wrapper className="gap-2.5 py-10">
        <Text className="text-muted">Loading…</Text>
      </Wrapper>
    );
  }

  async function saveDraft() {
    setBusy(true);
    setMsg(null);
    try {
      const post = await createOrUpdateDraft(user!.id, {
        title,
        body,
        source_kind: sourceKind as "freeform" | "twilda_journal" | "aftercare_journal" | "novel",
        source_id: sourceId,
      });
      setMsg(`Draft saved (${post.id.slice(0, 8)}…).`);
      return post.id;
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Could not save draft");
      return null;
    } finally {
      setBusy(false);
    }
  }

  return (
    <Wrapper variant="narrow" className="gap-2.5 py-10">
      <PageSeo
        title="Publish"
        description="Publish writing to your Artometrics profile or submit to the magazine."
        path="/studio/publish"
      />
      <Text className="text-xs tracking-[1.8px] uppercase font-bold text-accent">Studio</Text>
      <Text className="font-sans text-[36px] font-bold text-fg">Publish</Text>
      <Text className="font-sans text-base leading-[26px] text-muted">
        Profile posts go live on your public page. Magazine submissions need editorial review (and can
        sync into Sanity when configured).
      </Text>

      <Text className="text-[11px] tracking-[1.2px] uppercase font-bold mt-2 text-muted">Title</Text>
      <TextInput
        value={title}
        onChangeText={setTitle}
        placeholder="Title"
        placeholderTextColorClassName="text-subtle"
        className="border border-border px-3 py-2.5 text-base font-sans text-fg bg-bg-elevated"
      />
      <Text className="text-[11px] tracking-[1.2px] uppercase font-bold mt-2 text-muted">Body</Text>
      <TextInput
        value={body}
        onChangeText={setBody}
        placeholder="Write freely…"
        placeholderTextColorClassName="text-subtle"
        multiline
        className="border border-border px-3 py-2.5 text-base font-sans min-h-[200px] text-fg bg-bg-elevated"
        style={{ textAlignVertical: "top" }}
      />

      {msg ? <Text className="font-sans text-base leading-[26px] text-accent">{msg}</Text> : null}

      <View className="gap-2.5 mt-3">
        <PrimaryButton label="Save draft" onPress={() => void saveDraft()} disabled={busy} />
        <PrimaryButton
          label="Publish to profile"
          disabled={busy}
          onPress={async () => {
            setBusy(true);
            setMsg(null);
            try {
              const profile = await getProfile(user.id);
              if (!profile?.handle) {
                setMsg("Claim a handle in Settings before publishing to your profile.");
                return;
              }
              const id = await saveDraft();
              if (!id) return;
              await publishToProfile(user.id, id);
              setMsg("Published to your profile.");
              router.push(`/u/${profile.handle}`);
            } catch (e) {
              setMsg(e instanceof Error ? e.message : "Publish failed");
            } finally {
              setBusy(false);
            }
          }}
        />
        <PrimaryButton
          label="Submit to magazine"
          disabled={busy}
          className="bg-muted"
          onPress={async () => {
            setBusy(true);
            setMsg(null);
            try {
              const id = await saveDraft();
              if (!id) return;
              const post = await submitToMagazine(user.id, id);
              let sanityNote = "";
              try {
                const syncRes = await apiFetch("sanity-sync", {
                  method: "POST",
                  body: JSON.stringify({ postId: post.id }),
                });
                if (syncRes.status === 503) {
                  sanityNote =
                    " Sanity CMS is not configured yet — submission is saved in Supabase for editorial review.";
                } else if (!syncRes.ok) {
                  sanityNote =
                    " Sanity sync failed — submission is still saved for review.";
                } else {
                  sanityNote = " Draft also queued in Sanity.";
                }
              } catch {
                sanityNote =
                  " Sanity unreachable — submission is saved in Supabase for review.";
              }
              setMsg(`Submitted for magazine review.${sanityNote}`);
            } catch (e) {
              setMsg(e instanceof Error ? e.message : "Submit failed");
            } finally {
              setBusy(false);
            }
          }}
        />
      </View>
    </Wrapper>
  );
}
