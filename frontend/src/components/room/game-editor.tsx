"use client";

import { useEffect, useState } from "react";

import { SimpleSelect } from "@/components/simple-select";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { api } from "@/lib/api";
import { attempt, notifyInfo } from "@/lib/notify";
import type { DealField, GameSpec, Protocol, RoomView, Scoring } from "@/lib/types";

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
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Roles</CardTitle>
            <CardDescription>
              Each role&apos;s brief and values are shown only to the agent playing it. Seats swap roles between runs.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2">
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

        <ScoringCard draft={draft} edit={edit} resetKey={resetKey} />
        <ProtocolCard draft={draft} edit={edit} />

        <Card>
          <CardHeader>
            <CardTitle>Judge</CardTitle>
            <CardDescription>
              The judge reads every transcript, rates behaviour, and extracts deals agreed only in words. Leave empty
              for the default rubric (honesty, cooperativeness, assertiveness, consistency).
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <Textarea
              rows={3}
              value={draft.judge_rubric ?? ""}
              onChange={(e) => edit({ judge_rubric: e.target.value || null })}
            />
            <div className="flex items-center gap-2">
              <Label>Runs per match</Label>
              <Input
                className="w-24"
                type="number"
                min={1}
                value={draft.runs}
                onChange={(e) => edit({ runs: Number(e.target.value) })}
              />
            </div>
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

function ScoringCard({
  draft,
  edit,
  resetKey,
}: {
  draft: GameSpec;
  edit: (p: Partial<GameSpec>) => void;
  resetKey: string;
}) {
  const roles = draft.roles.map((r) => r.name);
  const s = draft.scoring;

  function setKind(kind: string) {
    let scoring: Scoring;
    if (kind === "surplus") {
      const field = draft.deal_fields[0]?.name ?? "price";
      scoring = { kind, field, direction: Object.fromEntries(roles.map((r, i) => [r, i === 0 ? "up" : "down"])) };
      if (!draft.deal_fields.length) {
        edit({ scoring, deal_fields: [{ name: field, type: "number", min: 0, max: null, description: "" }] });
        return;
      }
    } else if (kind === "valuations") {
      scoring = { kind, items: { item: 1 }, allocation_role: roles[0] };
    } else if (kind === "matrix") {
      return; // only via the prisoner's dilemma template
    } else {
      scoring = { kind: "judge_only" };
    }
    edit({ scoring });
  }

  function setFields(deal_fields: DealField[]) {
    edit({ deal_fields });
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Deal & scoring</CardTitle>
        <CardDescription>
          Structured scoring gives exact payoffs and theory baselines. &ldquo;Judge only&rdquo; works for any free-form
          scenario.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <SimpleSelect
          value={s.kind}
          onChange={setKind}
          options={[
            { value: "judge_only", label: "Judge only (free-form)" },
            { value: "surplus", label: "Surplus: one number, e.g. a price" },
            { value: "valuations", label: "Valuations: split items valued privately" },
            ...(s.kind === "matrix" ? [{ value: "matrix", label: "Payoff matrix (from template)" }] : []),
          ]}
        />

        {s.kind !== "judge_only" && s.kind !== "matrix" && (
          <div className="flex flex-col gap-2">
            <Label>Deal fields (what an offer must specify)</Label>
            {draft.deal_fields.map((f, i) => (
              <div key={i} className="grid grid-cols-12 gap-2">
                <Input
                  className="col-span-3"
                  value={f.name}
                  placeholder="name"
                  onChange={(e) => setFields(draft.deal_fields.map((x, j) => (j === i ? { ...x, name: e.target.value } : x)))}
                />
                <div className="col-span-2">
                  <SimpleSelect
                    value={f.type}
                    onChange={(type) =>
                      setFields(draft.deal_fields.map((x, j) => (j === i ? { ...x, type: type as DealField["type"] } : x)))
                    }
                    options={[{ value: "number" }, { value: "integer" }]}
                  />
                </div>
                {(["min", "max"] as const).map((k) => (
                  <Input
                    key={k}
                    className="col-span-2"
                    type="number"
                    placeholder={k}
                    value={f[k] ?? ""}
                    onChange={(e) =>
                      setFields(
                        draft.deal_fields.map((x, j) =>
                          j === i ? { ...x, [k]: e.target.value === "" ? null : Number(e.target.value) } : x,
                        ),
                      )
                    }
                  />
                ))}
                <Input
                  className="col-span-2"
                  value={f.description}
                  placeholder="meaning"
                  onChange={(e) =>
                    setFields(draft.deal_fields.map((x, j) => (j === i ? { ...x, description: e.target.value } : x)))
                  }
                />
                <Button
                  variant="ghost"
                  className="col-span-1"
                  onClick={() => setFields(draft.deal_fields.filter((_, j) => j !== i))}
                >
                  ✕
                </Button>
              </div>
            ))}
            <Button
              variant="outline"
              size="sm"
              className="self-start"
              onClick={() => setFields([...draft.deal_fields, { name: "", type: "number", min: null, max: null, description: "" }])}
            >
              Add field
            </Button>
          </div>
        )}

        {s.kind === "surplus" && (
          <div className="grid gap-3 md:grid-cols-3">
            <div className="flex flex-col gap-2">
              <Label>Field that sets the payoff</Label>
              <SimpleSelect
                value={s.field}
                onChange={(field) => edit({ scoring: { ...s, field } })}
                options={draft.deal_fields.map((f) => ({ value: f.name }))}
              />
            </div>
            {roles.map((r) => (
              <div key={r} className="flex flex-col gap-2">
                <Label>{r} gains when it goes</Label>
                <SimpleSelect
                  value={s.direction[r] ?? "up"}
                  onChange={(d) => edit({ scoring: { ...s, direction: { ...s.direction, [r]: d as "up" | "down" } } })}
                  options={[
                    { value: "up", label: "up (payoff = value − reservation)" },
                    { value: "down", label: "down (payoff = reservation − value)" },
                  ]}
                />
              </div>
            ))}
            <p className="text-muted-foreground text-sm md:col-span-3">
              Give each role a <code>reservation</code> private value; an optional <code>no_deal</code> value is what
              they get without a deal.
            </p>
          </div>
        )}

        {s.kind === "valuations" && (
          <div className="grid gap-3 md:grid-cols-2">
            <div className="flex flex-col gap-2">
              <Label>Items to split (name = count)</Label>
              <ValuesBox
                key={resetKey}
                value={s.items}
                onChange={(items) =>
                  edit({
                    scoring: { ...s, items },
                    deal_fields: Object.entries(items).map(([name, n]) => ({
                      name,
                      type: "integer",
                      min: 0,
                      max: n,
                      description: `${name} ${s.allocation_role} receives`,
                    })),
                  })
                }
              />
            </div>
            <div className="flex flex-col gap-2">
              <Label>Offers say how many items this role receives</Label>
              <SimpleSelect
                value={s.allocation_role}
                onChange={(allocation_role) => edit({ scoring: { ...s, allocation_role } })}
                options={roles.map((r) => ({ value: r }))}
              />
              <p className="text-muted-foreground text-sm">
                Each role values items through its private values (item = points each).
              </p>
            </div>
          </div>
        )}

        {s.kind === "matrix" && (
          <pre className="bg-muted rounded p-3 text-xs">{JSON.stringify(s.payoffs, null, 1)}</pre>
        )}
      </CardContent>
    </Card>
  );
}

function ProtocolCard({ draft, edit }: { draft: GameSpec; edit: (p: Partial<GameSpec>) => void }) {
  const p = draft.protocol;
  const setP = (patch: Partial<Protocol>) => edit({ protocol: { ...p, ...patch } as Protocol });
  return (
    <Card>
      <CardHeader>
        <CardTitle>Turn rules</CardTitle>
        <CardDescription>
          {p.kind === "alternating"
            ? "Players take turns. Any message may carry an offer, accept, reject or walk away."
            : "Each round: a short talk phase, then everyone moves at once."}
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-wrap items-center gap-4">
        {p.kind === "alternating" ? (
          <>
            <Label>Max messages</Label>
            <Input
              className="w-24"
              type="number"
              min={1}
              value={p.max_messages}
              onChange={(e) => setP({ max_messages: Number(e.target.value) })}
            />
            <Label>First speaker</Label>
            <SimpleSelect
              className="w-40"
              value={String(p.first)}
              onChange={(v) => setP({ first: Number(v) })}
              options={draft.roles.map((r, i) => ({ value: String(i), label: r.name }))}
            />
            <Label className="flex items-center gap-2">
              <Checkbox checked={p.reject_ends} onCheckedChange={(c) => setP({ reject_ends: c })} />A rejection ends
              the game
            </Label>
          </>
        ) : (
          <>
            <Label>Rounds</Label>
            <Input className="w-24" type="number" min={1} value={p.rounds} onChange={(e) => setP({ rounds: Number(e.target.value) })} />
            <Label>Talk messages per round</Label>
            <Input
              className="w-24"
              type="number"
              min={0}
              value={p.talk_messages}
              onChange={(e) => setP({ talk_messages: Number(e.target.value) })}
            />
            <Label className="flex items-center gap-2">
              <Checkbox checked={p.show_horizon} onCheckedChange={(c) => setP({ show_horizon: c })} />
              Players know the number of rounds
            </Label>
          </>
        )}
      </CardContent>
    </Card>
  );
}
