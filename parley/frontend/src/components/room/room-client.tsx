"use client";

import { useParams, useSearchParams } from "next/navigation";
import { Sparkles } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "@/components/ui/toast";
import { ApiError, api, getToken, setToken } from "@/lib/api";
import { notifyError, notifyInfo, notifySuccess } from "@/lib/notify";
import { roomNotices } from "@/lib/room-events";
import { parseTab, publishRoom, setRoomTab } from "@/lib/room-store";
import type { RoomView } from "@/lib/types";

import { AgentMap } from "./agent-map";
import { GameEditor } from "./game-editor";
import { MatchPanel } from "./match-panel";
import { RoomAssistant, useAssistantOpen } from "./room-assistant";
import { ResultsPanel } from "./results-panel";
import { SeatEditor } from "./seat-editor";

const POLL_MS = 2000;

export function RoomClient() {
  const { id: roomId } = useParams<{ id: string }>();
  const [room, setRoom] = useState<RoomView | null>(null);
  const [needsJoin, setNeedsJoin] = useState(false);
  const [error, setError] = useState<string | null>(null); // only shown before the room first loads
  // The tab lives in `?tab=` so the sidebar can link to it; switching rewrites the URL in place.
  const tab = parseTab(useSearchParams().get("tab"));
  const [assistantOpen, setAssistantOpen] = useAssistantOpen();
  const prev = useRef<RoomView | null>(null);
  const offline = useRef(false);

  const refresh = useCallback(async () => {
    // A watch link from `parley mcp` carries the token in the fragment: keep it, then drop it
    // from the address bar so "Copy invite link" doesn't hand it on.
    const fromLink = new URLSearchParams(window.location.hash.slice(1)).get("token");
    if (fromLink) {
      setToken(roomId, fromLink);
      window.history.replaceState(null, "", window.location.pathname + window.location.search);
    }
    if (!getToken(roomId)) {
      setNeedsJoin(true);
      return;
    }
    try {
      const next = await api.room(roomId);
      if (prev.current) for (const n of roomNotices(prev.current, next)) toast.add(n);
      prev.current = next;
      publishRoom(next);
      if (offline.current) notifySuccess("Reconnected");
      offline.current = false;
      setRoom(next);
      setNeedsJoin(false);
      setError(null);
    } catch (e) {
      if (e instanceof ApiError && e.status === 403) setNeedsJoin(true);
      else if (!prev.current) setError((e as Error).message);
      else if (!offline.current) {
        // Toast once per outage, not on every poll.
        offline.current = true;
        notifyError(e, "Lost connection to the server. Retrying…");
      }
    }
  }, [roomId]);

  useEffect(() => {
    const first = setTimeout(refresh, 0);
    const t = setInterval(refresh, POLL_MS);
    return () => {
      clearTimeout(first);
      clearInterval(t);
    };
  }, [refresh]);

  if (needsJoin) return <JoinForm roomId={roomId} onJoined={refresh} />;
  if (!room) return <p className="text-muted-foreground p-8">{error ?? "Loading room…"}</p>;

  return (
    <div className="flex min-w-0 flex-1">
      <div className="mx-auto flex w-full min-w-0 max-w-5xl flex-col gap-8 px-4 py-10">
        <header className="flex flex-col gap-4 border-b border-line pb-6 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="label-mono">Room {room.id}</p>
            <h1 className="display-title mt-2 text-3xl sm:text-4xl">{room.game.spec.title}</h1>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            {room.participants.map((p) => (
              <Badge key={p.name} variant={p.name === room.me.name || p.owner === room.me.name ? "default" : "secondary"}>
                {p.name}
                {p.is_host && " · host"}
                {room.game.locked ? (p.ready ? " · ready" : " · setting up") : p.agreed ? " · agreed" : ""}
              </Badge>
            ))}
            {room.participants.length < room.capacity && (
              <Badge variant="outline">waiting for {room.capacity - room.participants.length} more</Badge>
            )}
            <Button size="sm" variant={assistantOpen ? "secondary" : "outline"} onClick={() => setAssistantOpen(!assistantOpen)}>
              <Sparkles /> Assistant
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={() =>
                navigator.clipboard
                  ?.writeText(window.location.href)
                  .then(() => notifyInfo("Invite link copied", "Send it to the other player."))
                  .catch((e) => notifyError(e, "Couldn't copy the link"))
              }
            >
              Copy invite link
            </Button>
          </div>
        </header>
  
        <Tabs value={tab} onValueChange={(v) => setRoomTab(parseTab(String(v)))}>
          <TabsList variant="line" className="h-10 w-full justify-start gap-6 rounded-none border-b border-line p-0">
            <TabsTrigger className="flex-none px-0" value="map">Map</TabsTrigger>
            <TabsTrigger className="flex-none px-0" value="game">1 · Game{room.game.locked ? " ✓" : ""}</TabsTrigger>
            <TabsTrigger className="flex-none px-0" value="seat">2 · My agent{room.me.ready ? " ✓" : ""}</TabsTrigger>
            <TabsTrigger className="flex-none px-0" value="match">3 · Match{room.running.length ? " ●" : ""}</TabsTrigger>
            <TabsTrigger className="flex-none px-0" value="results">Results</TabsTrigger>
          </TabsList>
          <TabsContent value="map" className="mt-6">
            <AgentMap room={room} onChange={refresh} />
          </TabsContent>
          <TabsContent value="game" className="@container mt-6">
            <GameEditor room={room} onChange={refresh} />
          </TabsContent>
          <TabsContent value="seat" className="@container mt-6">
            <div className="flex flex-col gap-8">
              <SeatEditor room={room} onChange={refresh} />
              {room.controlled.map((c) => (
                <SeatEditor key={c.name} room={room} onChange={refresh} seatOf={c.name} />
              ))}
            </div>
          </TabsContent>
          <TabsContent value="match" className="mt-6">
            <MatchPanel room={room} onChange={refresh} onShowResults={() => setRoomTab("results")} />
          </TabsContent>
          <TabsContent value="results" className="mt-6">
            <ResultsPanel room={room} />
          </TabsContent>
        </Tabs>
      </div>
      <RoomAssistant
        room={room}
        onChange={refresh}
        open={assistantOpen}
        onClose={() => setAssistantOpen(false)}
      />
    </div>
  );
}

function JoinForm({ roomId, onJoined }: { roomId: string; onJoined: () => void }) {
  const [name, setName] = useState("");

  async function join() {
    try {
      const { token } = await api.joinRoom(roomId, name);
      setToken(roomId, token);
      onJoined();
    } catch (e) {
      notifyError(e, "Couldn't join");
    }
  }

  return (
    <div className="mx-auto flex w-full max-w-md flex-1 flex-col justify-center px-4 py-16">
      <Card>
        <CardHeader>
          <CardTitle>Join room {roomId}</CardTitle>
          <CardDescription>Pick a display name. No account needed.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Your name" />
          <Button onClick={join} disabled={!name.trim()}>
            Join
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
