"use client";

import { useEffect, useState } from "react";

import { SimpleSelect } from "@/components/simple-select";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { api } from "@/lib/api";
import { attempt, notifyError, notifySuccess } from "@/lib/notify";
import type { MatchEvent, Outcome, RoomView, Turn } from "@/lib/types";

import { Transcript } from "./transcript";

type LiveEpisode = { assignment: Record<string, string>; turns: Turn[]; outcome?: Outcome };

export function MatchPanel({
  room,
  onChange,
  onShowResults,
}: {
  room: RoomView;
  onChange: () => void;
  onShowResults: () => void;
}) {
  const [runs, setRuns] = useState<number>(room.game.spec.runs);
  const [watching, setWatching] = useState<string | null>(null);

  // Adopt a running match (also when opening the page mid-match). Adjusting state during
  // render is React's pattern for reacting to a changed prop.
  const running = room.running[0] ?? null;
  if (running && running !== watching) setWatching(running);
  const busy = !!running;

  async function start() {
    await attempt(async () => {
      const { match_id } = await api.startMatch(room.id, runs);
      setWatching(match_id);
      onChange();
    }, `Match started: ${runs} runs`, "Couldn't start the match");
  }


  return (
    <div className="flex flex-col gap-4">
      <Card>
        <CardHeader>
          <CardTitle>Run a match</CardTitle>
          <CardDescription>
            The agents play the locked game {runs} times, swapping roles. Both of you watch live.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          <div className="flex items-center gap-3">
            <Label>Runs</Label>
            <Input className="w-24" type="number" min={1} value={runs} onChange={(e) => setRuns(Number(e.target.value))} />
            <Button onClick={start} disabled={!room.can_start || busy}>
              Start match
            </Button>
          </div>
          {!room.can_start && room.start_problems.length > 0 && (
            <p className="text-muted-foreground text-sm">Not yet: {room.start_problems.join("; ")}.</p>
          )}
        </CardContent>
      </Card>

      {watching && (
        <LiveMatch
          key={watching}
          roomId={room.id}
          matchId={watching}
          onDone={onChange}
          onError={(m) => notifyError(new Error(m), "The match failed")}
          onShowResults={onShowResults}
        />
      )}

      {room.me.is_host && <HostSettings room={room} onChange={onChange} />}
    </div>
  );
}

function LiveMatch({
  roomId,
  matchId,
  onDone,
  onError,
  onShowResults,
}: {
  roomId: string;
  matchId: string;
  onDone: () => void;
  onError: (m: string) => void;
  onShowResults: () => void;
}) {
  const [episodes, setEpisodes] = useState<Record<number, LiveEpisode>>({});
  const [finished, setFinished] = useState(false);
  const [selected, setSelected] = useState(0);

  useEffect(() => {
    const source = new EventSource(api.streamUrl(roomId, matchId));
    const handle = (raw: MessageEvent) => {
      const e = JSON.parse(raw.data) as MatchEvent;
      setEpisodes((prev) => {
        const next = { ...prev };
        if (e.type === "episode_start") next[e.index] = { assignment: e.assignment, turns: [] };
        if (e.type === "turn" && next[e.index])
          next[e.index] = { ...next[e.index], turns: [...next[e.index].turns, e.turn] };
        if (e.type === "episode_end" && next[e.index]) next[e.index] = { ...next[e.index], outcome: e.outcome };
        return next;
      });
      if (e.type === "match_end" || e.type === "error") {
        setFinished(true);
        if (e.type === "match_end") notifySuccess("Match finished", "Open Results for the full analysis.");
        if (e.type === "error") onError(e.message);
        source.close();
        onDone();
      }
    };
    // A finished match is no longer streamable; its results tab has everything.
    source.onerror = () => {
      source.close();
      setFinished(true);
    };
    for (const t of ["episode_start", "turn", "episode_end", "match_end", "error"]) source.addEventListener(t, handle);
    return () => source.close();
  }, [roomId, matchId, onDone, onError]);

  const indices = Object.keys(episodes).map(Number).sort((a, b) => a - b);
  const current = episodes[selected];

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>{finished ? "Match finished" : "Live"}</CardTitle>
          <CardDescription>
            {indices.filter((i) => episodes[i].outcome).length} of {indices.length} episodes done
          </CardDescription>
        </div>
        {finished && <Button onClick={onShowResults}>See results</Button>}
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="flex flex-wrap gap-2">
          {indices.map((i) => (
            <Button key={i} size="sm" variant={i === selected ? "default" : "outline"} onClick={() => setSelected(i)}>
              #{i + 1} {episodes[i].outcome ? "✓" : "…"}
            </Button>
          ))}
        </div>
        {current && <Transcript turns={current.turns} seatOf={current.assignment} />}
        {current?.outcome && (
          <p className="text-sm">
            <b>{current.outcome.end_reason}</b>
            {current.outcome.deal && ` · deal ${JSON.stringify(current.outcome.deal.terms)}`} · payoffs{" "}
            {JSON.stringify(current.outcome.payoffs)}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

function HostSettings({ room, onChange }: { room: RoomView; onChange: () => void }) {
  const [models, setModels] = useState(room.settings.allowed_models.join("\n"));
  const [judge, setJudge] = useState(room.settings.judge_model ?? "");
  const [parallel, setParallel] = useState(room.settings.parallel);
  const list = models.split("\n").map((m) => m.trim()).filter(Boolean);

  async function save() {
    const ok = await attempt(
      () => api.putSettings(room.id, { allowed_models: list, judge_model: judge || null, parallel }),
      "Settings saved",
      "Couldn't save settings",
    );
    if (ok) onChange();
  }


  return (
    <Card>
      <CardHeader>
        <CardTitle>Host settings</CardTitle>
        <CardDescription>
          All calls use your API key. Model names follow LiteLLM, e.g. featherless_ai/&lt;model id&gt;.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <Label>Models participants may pick (one per line)</Label>
        <Textarea rows={4} className="font-mono text-sm" value={models} onChange={(e) => setModels(e.target.value)} />
        <Label>Judge model</Label>
        <SimpleSelect
          value={judge || "none"}
          onChange={(v) => setJudge(v === "none" ? "" : v)}
          options={[{ value: "none", label: "No judge" }, ...list.map((m) => ({ value: m }))]}
        />
        <div className="flex items-center gap-3">
          <Label>Episodes played at once</Label>
          <Input className="w-24" type="number" min={1} value={parallel} onChange={(e) => setParallel(Number(e.target.value))} />
          <Button variant="outline" onClick={save}>
            Save settings
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
