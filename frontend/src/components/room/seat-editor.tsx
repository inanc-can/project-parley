"use client";

import { useState } from "react";

import { SimpleSelect } from "@/components/simple-select";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { api } from "@/lib/api";
import { attempt } from "@/lib/notify";
import type { RoomView, Seat } from "@/lib/types";

const SCRIPTED = ["tit_for_tat", "always_cooperate", "always_defect", "grim_trigger", "walk_away", "silent"];

function defaultSeat(kind: Seat["kind"], model: string, strategy = ""): Seat {
  if (kind === "team")
    return { kind, proposer_model: model, critic_model: model, decider_model: null, strategy, temperature: 0.7 };
  if (kind === "scripted") return { kind, name: "tit_for_tat", params: {} };
  return { kind: "llm", model, strategy, temperature: 0.7 };
}

export function SeatEditor({ room, onChange }: { room: RoomView; onChange: () => void }) {
  const models = room.settings.allowed_models;
  // Unsaved edits override what is saved on the server.
  const [localSeat, setLocalSeat] = useState<Seat | null>(null);
  const [localReveal, setLocalReveal] = useState<boolean | null>(null);
  const seat = localSeat ?? room.me.seat ?? defaultSeat("llm", models[0] ?? "");
  const reveal = localReveal ?? room.me.reveal;
  const dirty = localSeat !== null || localReveal !== null || !room.me.seat;
  const update = (s: Seat) => setLocalSeat(s);
  const strategy = "strategy" in seat ? seat.strategy : "";
  const modelOptions = models.map((m) => ({ value: m, label: m.replace(/^featherless_ai\//, "") }));

  async function run(fn: () => Promise<unknown>, success: string, errorTitle: string) {
    if (await attempt(fn, success, errorTitle)) onChange();
  }


  const others = room.participants.filter((p) => p.name !== room.me.name);

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Card className="md:col-span-2">
        <CardHeader>
          <CardTitle>Your agent</CardTitle>
          <CardDescription>
            Only you can see this. It plays every role in turn, since roles swap between runs.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <div className="flex flex-col gap-2">
            <Label>Type</Label>
            <SimpleSelect
              value={seat.kind}
              onChange={(k) => update(defaultSeat(k as Seat["kind"], models[0] ?? "", strategy))}
              options={[
                { value: "llm", label: "Single LLM" },
                { value: "team", label: "Team: proposer → critic → decider" },
                { value: "scripted", label: "Scripted baseline (no LLM)" },
              ]}
            />
          </div>

          {seat.kind === "llm" && (
            <div className="flex flex-col gap-2">
              <Label>Model</Label>
              <SimpleSelect value={seat.model} onChange={(model) => update({ ...seat, model })} options={modelOptions} />
            </div>
          )}

          {seat.kind === "team" && (
            <div className="grid gap-3 md:grid-cols-3">
              {(["proposer_model", "critic_model", "decider_model"] as const).map((k) => (
                <div key={k} className="flex flex-col gap-2">
                  <Label>{k.replace("_model", "")}</Label>
                  <SimpleSelect
                    value={seat[k] ?? "same"}
                    onChange={(m) => update({ ...seat, [k]: m === "same" ? null : m })}
                    options={k === "decider_model" ? [{ value: "same", label: "same as proposer" }, ...modelOptions] : modelOptions}
                  />
                </div>
              ))}
            </div>
          )}

          {seat.kind === "scripted" && (
            <div className="flex flex-col gap-2">
              <Label>Strategy</Label>
              <SimpleSelect
                value={seat.name}
                onChange={(name) => update({ ...seat, name })}
                options={SCRIPTED.map((s) => ({ value: s, label: s.replaceAll("_", " ") }))}
              />
              <p className="text-muted-foreground text-sm">
                Fixed strategies are useful as baselines. Tit for tat and friends fit the prisoner&apos;s dilemma.
              </p>
            </div>
          )}

          {seat.kind !== "scripted" && (
            <>
              <div className="flex flex-col gap-2">
                <Label>Strategy instructions</Label>
                <Textarea
                  rows={5}
                  value={seat.strategy}
                  onChange={(e) => update({ ...seat, strategy: e.target.value })}
                  placeholder="Anchor high, concede slowly, never reveal your minimum."
                />
              </div>
              <div className="flex items-center gap-3">
                <Label>Temperature</Label>
                <Input
                  className="w-24"
                  type="number"
                  step={0.1}
                  min={0}
                  max={2}
                  value={seat.temperature}
                  onChange={(e) => update({ ...seat, temperature: Number(e.target.value) })}
                />
              </div>
            </>
          )}

          <Label className="flex items-center gap-3">
            <Switch
              checked={reveal}
              onCheckedChange={(c) => setLocalReveal(c)}
            />
            Reveal my setup and reasoning to the others after a match
          </Label>


          <div className="flex gap-2">
            <Button
              variant="outline"
              disabled={!dirty}
              onClick={() =>
                run(
                  async () => {
                    await api.putSeat(room.id, seat, reveal);
                    setLocalSeat(null);
                    setLocalReveal(null);
                  },
                  "Agent saved",
                  "Couldn't save your agent",
                )
              }
            >
              Save agent
            </Button>
            <Button
              disabled={dirty || !room.me.seat || !room.game.locked}
              variant={room.me.ready ? "secondary" : "default"}
              onClick={() =>
                run(
                  () => api.ready(room.id, !room.me.ready),
                  room.me.ready ? "Marked as not ready" : "You're ready",
                  "Couldn't change readiness",
                )
              }
            >
              {room.me.ready ? "Undo ready" : "I'm ready"}
            </Button>
          </div>
          {!room.game.locked && <p className="text-muted-foreground text-sm">Agree on the game first to get ready.</p>}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Opponents</CardTitle>
          <CardDescription>You only see whether they are ready.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-2 text-sm">
          {others.length === 0 && <p className="text-muted-foreground">Nobody has joined yet.</p>}
          {others.map((p) => (
            <div key={p.name} className="flex justify-between">
              <span>{p.name}</span>
              <span className={p.ready ? "text-green-600" : "text-muted-foreground"}>
                {p.ready ? "ready" : p.has_seat ? "agent saved" : "setting up"}
              </span>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
