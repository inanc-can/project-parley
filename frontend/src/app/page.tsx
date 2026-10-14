"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api, setToken } from "@/lib/api";
import { notifyError } from "@/lib/notify";

export default function Home() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [busy, setBusy] = useState(false);

  async function create() {
    setBusy(true);
    try {
      const { room_id, token } = await api.createRoom(name);
      setToken(room_id, token);
      router.push(`/room/${room_id}`);
    } catch (e) {
      notifyError(e, "Couldn't create the room");
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto flex w-full max-w-xl flex-1 flex-col justify-center gap-8 px-4 py-20">
      <div>
        <p className="label-mono text-brand">Research</p>
        <h1 className="display-title mt-3 text-4xl sm:text-5xl">Parley</h1>
        <p className="text-muted-foreground mt-4 max-w-[34rem] text-base leading-relaxed">
          Agree on a game together, build your agent in private, and watch the agents negotiate.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Start a room</CardTitle>
          <CardDescription>You become the host. Share the room link with the other player.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          <Label htmlFor="name">Your name</Label>
          <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Ada" />
          <Button onClick={create} disabled={!name.trim() || busy}>
            Create room
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Join a room</CardTitle>
          <CardDescription>Paste the room code (or just open the link you were sent).</CardDescription>
        </CardHeader>
        <CardContent className="flex gap-2">
          <Input value={code} onChange={(e) => setCode(e.target.value.trim())} placeholder="room code" />
          <Button variant="secondary" disabled={!code} onClick={() => router.push(`/room/${code}`)}>
            Open
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}
