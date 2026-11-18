import { useSyncExternalStore } from "react";

import { TOKENS_CHANGED, api, listTokenRooms } from "./api";
import type { RoomView } from "./types";

// Shared between the room page (which polls the room) and the app sidebar (which shows the
// rooms this browser has joined and the current room's step status).

export type RoomSummary = { id: string; title: string; locked: boolean; ready: boolean; running: boolean };

export const ROOM_TABS = ["map", "game", "seat", "match", "results"] as const;
export type RoomTab = (typeof ROOM_TABS)[number];

export function parseTab(value: string | null): RoomTab {
  return (ROOM_TABS as readonly string[]).includes(value ?? "") ? (value as RoomTab) : "map";
}

/** Switch the room tab by rewriting `?tab=`; Next syncs `useSearchParams` with history calls. */
export function setRoomTab(tab: RoomTab) {
  const params = new URLSearchParams(window.location.search);
  params.set("tab", tab);
  window.history.replaceState(null, "", `?${params.toString()}`);
}

// Replaced (never mutated) on change, so the map itself is a valid external-store snapshot.
let summaries: ReadonlyMap<string, RoomSummary> = new Map();
const summaryListeners = new Set<() => void>();
const requested = new Set<string>();

export function publishRoom(view: RoomView) {
  const next: RoomSummary = {
    id: view.id,
    title: view.game.spec.title,
    locked: view.game.locked,
    ready: view.me.ready,
    running: view.running.length > 0,
  };
  const prev = summaries.get(view.id);
  if (
    prev &&
    prev.title === next.title &&
    prev.locked === next.locked &&
    prev.ready === next.ready &&
    prev.running === next.running
  )
    return;
  summaries = new Map(summaries).set(view.id, next);
  for (const l of summaryListeners) l();
}

/** Fetch a room once so the sidebar can show its title; failures just leave the id showing. */
export function loadRoomSummary(roomId: string) {
  if (requested.has(roomId) || summaries.has(roomId)) return;
  requested.add(roomId);
  api.room(roomId).then(publishRoom, () => {});
}

function subscribeSummaries(listener: () => void) {
  summaryListeners.add(listener);
  return () => {
    summaryListeners.delete(listener);
  };
}

const NO_SUMMARIES: ReadonlyMap<string, RoomSummary> = new Map();

export function useRoomSummaries(): ReadonlyMap<string, RoomSummary> {
  return useSyncExternalStore(subscribeSummaries, () => summaries, () => NO_SUMMARIES);
}

// Rooms with a token in localStorage, kept as a stable array snapshot.
const NO_ROOMS: string[] = [];
let knownRooms: string[] = NO_ROOMS;

function readKnownRooms() {
  const ids = listTokenRooms();
  if (ids.join() !== knownRooms.join()) knownRooms = ids;
  return knownRooms;
}

function subscribeKnownRooms(listener: () => void) {
  const onChange = () => {
    const before = knownRooms;
    if (readKnownRooms() !== before) listener();
  };
  window.addEventListener(TOKENS_CHANGED, onChange);
  window.addEventListener("storage", onChange);
  return () => {
    window.removeEventListener(TOKENS_CHANGED, onChange);
    window.removeEventListener("storage", onChange);
  };
}

export function useKnownRooms(): string[] {
  return useSyncExternalStore(subscribeKnownRooms, readKnownRooms, () => NO_ROOMS);
}
