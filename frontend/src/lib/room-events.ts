import type { RoomView } from "./types";

export type Notice = { title: string; description?: string; type: "success" | "info" };

// Match ids started from this browser, so we don't announce our own match back to us.
export const startedHere = new Set<string>();

// What the other people did between two polls of the room, phrased for the viewer.
export function roomNotices(prev: RoomView, next: RoomView): Notice[] {
  const me = next.me.name;
  const out: Notice[] = [];
  const before = new Map(prev.participants.map((p) => [p.name, p]));

  for (const p of next.participants) {
    if (p.name === me) continue;
    const was = before.get(p.name);
    if (!was) {
      out.push({ title: `${p.name} joined the room`, type: "info" });
      continue;
    }
    if (!was.agreed && p.agreed && next.game.version === prev.game.version)
      out.push({ title: `${p.name} agreed to version ${next.game.version}`, type: "info" });
    if (!was.ready && p.ready) out.push({ title: `${p.name} is ready`, type: "info" });
  }

  if (next.game.version > prev.game.version && next.game.edited_by && next.game.edited_by !== me)
    out.push({
      title: `${next.game.edited_by} edited the game`,
      description: `Now version ${next.game.version}. Review it before agreeing.`,
      type: "info",
    });

  if (!prev.game.locked && next.game.locked)
    out.push({ title: "Game locked", description: "Everyone agreed. Set up your agent next.", type: "success" });

  for (const id of next.running)
    if (!prev.running.includes(id) && !startedHere.has(id))
      out.push({ title: "A match started", description: "Watch it live in the Match tab.", type: "info" });

  return out;
}
