import { startedHere } from "./room-events";
import type { GameSpec, MatchListItem, MatchResult, RoomSettings, RoomView, Seat } from "./types";

// Each room gets its own participant token, kept in this browser only.
const tokenKey = (roomId: string) => `parley:token:${roomId}`;

export function getToken(roomId: string): string | null {
  try {
    return localStorage.getItem(tokenKey(roomId));
  } catch {
    return null;
  }
}

export function setToken(roomId: string, token: string) {
  try {
    localStorage.setItem(tokenKey(roomId), token);
  } catch {
    /* private mode: the token lives only for this page */
  }
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

type ValidationIssue = { loc: (string | number)[]; msg: string };

// FastAPI sends a string, or a list of pydantic validation issues for bad input.
function formatDetail(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail))
    return (detail as ValidationIssue[])
      .map((d) => {
        const where = d.loc.filter((p) => p !== "body").join(" › ");
        return where ? `${where}: ${d.msg}` : d.msg;
      })
      .join("; ");
  return JSON.stringify(detail);
}

async function call<T>(path: string, init: RequestInit & { roomId?: string } = {}): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  const token = init.roomId ? getToken(init.roomId) : null;
  if (token) headers["X-Parley-Token"] = token;
  const res = await fetch(`/api${path}`, { ...init, headers });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = formatDetail(body.detail);
    } catch {
      /* not JSON */
    }
    throw new ApiError(res.status, detail);
  }
  return res.json() as Promise<T>;
}

const json = (body: unknown) => JSON.stringify(body);

export const api = {
  templates: () => call<Record<string, GameSpec>>("/templates"),
  reference: (spec: GameSpec) => call<Record<string, unknown>>("/reference", { method: "POST", body: json(spec) }),

  createRoom: (name: string) =>
    call<{ room_id: string; token: string }>("/rooms", { method: "POST", body: json({ name }) }),
  joinRoom: (roomId: string, name: string) =>
    call<{ token: string }>(`/rooms/${roomId}/join`, { method: "POST", body: json({ name }) }),
  room: (roomId: string) => call<RoomView>(`/rooms/${roomId}`, { roomId }),

  putGame: (roomId: string, spec: GameSpec) =>
    call(`/rooms/${roomId}/game`, { method: "PUT", body: json(spec), roomId }),
  agree: (roomId: string, version: number) =>
    call(`/rooms/${roomId}/game/agree`, { method: "POST", body: json({ version }), roomId }),
  unlock: (roomId: string) => call(`/rooms/${roomId}/game/unlock`, { method: "POST", roomId }),

  putSeat: (roomId: string, seat: Seat, reveal: boolean) =>
    call(`/rooms/${roomId}/seat`, { method: "PUT", body: json({ seat, reveal }), roomId }),
  ready: (roomId: string, ready: boolean) =>
    call(`/rooms/${roomId}/ready`, { method: "POST", body: json({ ready }), roomId }),
  putSettings: (roomId: string, settings: RoomSettings) =>
    call(`/rooms/${roomId}/settings`, { method: "PUT", body: json(settings), roomId }),

  startMatch: async (roomId: string, runs?: number) => {
    const r = await call<{ match_id: string }>(`/rooms/${roomId}/matches`, {
      method: "POST",
      body: json({ runs }),
      roomId,
    });
    startedHere.add(r.match_id);
    return r;
  },
  matches: (roomId: string) => call<MatchListItem[]>(`/rooms/${roomId}/matches`, { roomId }),
  match: (roomId: string, matchId: string) => call<MatchResult>(`/rooms/${roomId}/matches/${matchId}`, { roomId }),
  streamUrl: (roomId: string, matchId: string) =>
    `/api/rooms/${roomId}/matches/${matchId}/stream?token=${encodeURIComponent(getToken(roomId) ?? "")}`,
};
