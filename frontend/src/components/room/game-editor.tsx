"use client";

import { useEffect, useState } from "react";

import { SimpleSelect } from "@/components/simple-select";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { api } from "@/lib/api";
import { attempt, notifyInfo } from "@/lib/notify";
import type { GameSpec, RoomView } from "@/lib/types";

import { SharedFiles } from "./shared-files";

// "key = value" lines <-> a number map, for private values and item counts.
const toLines = (m: Record<string, number>) =>
  Object.entries(m)
    .map(([k, v]) => `${k} = ${v}`)
    .join("\n");
function fromLines(text: string): Record<string, number> {
  const out: Record<string, number> = {};
  for (const line of text.split("\n")) {
    const [k, v] = line.split("=").map((s) => s.trim());
    if (k && v !== undefined && v !== "" && !Number.isNaN(Number(v))) out[k] = Number(v);
  }
  return out;
}

export function GameEditor({ room, onChange }: { room: RoomView; onChange: () => void }) {
  // My unsaved edits; without them I follow the latest saved version (including the other person's).
  const [local, setLocal] = useState<GameSpec | null>(null);
  const [loads, setLoads] = useState(0); // bumps when a template replaces the draft
  const draft = local ?? room.game.spec;
  const dirty = local !== null;
  const resetKey = `${room.game.version}-${loads}`;
  const [templates, setTemplates] = useState<Record<string, GameSpec>>({});
  const locked = room.game.locked;
  const meAgreed = room.participants.find((p) => p.name === room.me.name)?.agreed;

  useEffect(() => {
    api.templates().then(setTemplates).catch(() => {});
  }, []);

  function edit(patch: Partial<GameSpec>) {
    setLocal((d) => ({ ...(d ?? room.game.spec), ...patch }));
  }

  async function run(fn: () => Promise<unknown>, success: string, errorTitle: string) {
    if (await attempt(fn, success, errorTitle)) onChange();
  }

  const save = () =>
    run(
      async () => {
        await api.putGame(room.id, draft);
        setLocal(null);
      },
      `Saved as version ${room.game.version + 1}`,
      "Couldn't save the game",
    );

  return (
    <div className="flex flex-col gap-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between gap-4">
          <div>
            <CardTitle>Version {room.game.version}</CardTitle>
            <CardDescription>
              {locked
                ? "Locked: everyone agreed. Set up your agent next."
                : "Either person can edit. Every edit makes a new version and clears agreement."}
            </CardDescription>
          </div>
          <div className="flex gap-2">
            {locked ? (
              <Button variant="outline" onClick={() => run(() => api.unlock(room.id), "Game unlocked for editing", "Couldn't unlock")}
              >
                Unlock to edit
              </Button>
            ) : (
              <>
                <Button variant="outline" onClick={save} disabled={!dirty}>
                  Save version
                </Button>
                <Button
                  onClick={() =>
                    run(() => api.agree(room.id, room.game.version), `You agreed to version ${room.game.version}`, "Couldn't agree")
                  }
                  disabled={dirty || meAgreed}
                >
                  {meAgreed ? "You agreed" : "Agree"} ({room.participants.filter((p) => p.agreed).length}/
                  {room.capacity})
                </Button>
              </>
            )}
          </div>
        </CardHeader>
      </Card>

      <fieldset disabled={locked} className="flex flex-col gap-4 disabled:opacity-80">
        <Card>
          <CardHeader>
            <CardTitle>Scenario</CardTitle>
            <CardDescription>Write the game in your own words, or start from a template.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <div className="flex flex-col gap-2">
              <Label>Start from a template</Label>
              <SimpleSelect
                value=""
                placeholder="Choose a template…"
                disabled={locked}
                onChange={(name) => {
                  setLocal(templates[name]);
                  setLoads((n) => n + 1);
                  notifyInfo(`Loaded “${templates[name].title}”`, "Not saved yet. Review it, then press Save version.");
                }}
                options={Object.entries(templates).map(([k, t]) => ({ value: k, label: t.title }))}
              />
            </div>
            <Label>Title</Label>
            <Input value={draft.title} onChange={(e) => edit({ title: e.target.value })} />
            <Label>Shared context (both agents see this)</Label>
            <Textarea
              rows={4}
              value={draft.shared_context}
              onChange={(e) => edit({ shared_context: e.target.value })}
              placeholder="A 2015 Civic is for sale. The seller and buyer negotiate the price…"
            />
            <SharedFiles
              roomId={room.id}
              files={draft.files ?? []}
              context={draft.shared_context}
              disabled={locked}
              onFiles={(files) => edit({ files })}
              onContext={(shared_context) => edit({ shared_context })}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Roles</CardTitle>
            <CardDescription>
              Each role&apos;s brief and values are shown only to the agent playing it. Seats swap roles between runs.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 @3xl:grid-cols-2">
            {draft.roles.map((r, i) => (
              <div key={i} className="flex flex-col gap-2 rounded-md border p-3">
                <Label>Role name</Label>
                <Input
                  value={r.name}
                  onChange={(e) => {
                    const roles = [...draft.roles];
                    roles[i] = { ...r, name: e.target.value };
                    edit({ roles });
                  }}
                />
                <Label>Private brief</Label>
                <Textarea
                  rows={3}
                  value={r.private_brief}
                  onChange={(e) => {
                    const roles = [...draft.roles];
                    roles[i] = { ...r, private_brief: e.target.value };
                    edit({ roles });
                  }}
                />
                <Label>Private values (one per line: name = number)</Label>
                <ValuesBox
                  key={`${resetKey}-${i}`}
                  value={r.private_values}
                  onChange={(private_values) => {
                    const roles = [...draft.roles];
                    roles[i] = { ...r, private_values };
                    edit({ roles });
                  }}
                />
              </div>
            ))}
          </CardContent>
        </Card>
      </fieldset>
    </div>
  );
}

// Keeps the raw text while typing and reports parsed values. Remount (change `key`) to reset it.
function ValuesBox({ value, onChange }: { value: Record<string, number>; onChange: (v: Record<string, number>) => void }) {
  const [text, setText] = useState(() => toLines(value));
  return (
    <Textarea
      rows={2}
      className="font-mono text-sm"
      value={text}
      onChange={(e) => {
        setText(e.target.value);
        onChange(fromLines(e.target.value));
      }}
      placeholder="reservation = 8000"
    />
  );
}
