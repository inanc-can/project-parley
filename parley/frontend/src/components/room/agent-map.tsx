"use client";

import {
  Background,
  BackgroundVariant,
  BaseEdge,
  Controls,
  EdgeLabelRenderer,
  Handle,
  Panel,
  Position,
  ReactFlow,
  applyNodeChanges,
  getStraightPath,
  type Edge,
  type EdgeProps,
  type Node,
  type NodeChange,
  type NodeProps,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { Bot, Lock, Play, UserRound, UserRoundPlus, X } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { createPortal } from "react-dom";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import { attempt } from "@/lib/notify";
import { setRoomTab } from "@/lib/room-store";
import type { RoomView, Seat } from "@/lib/types";

import { GameEditor } from "./game-editor";
import { SeatEditor } from "./seat-editor";

// The room as a map: one node per agent (yours, your guests', and open seats), and an edge per
// pair of agents carrying the game they play. Clicking a node or an edge opens the inspector.

type AgentData = {
  name: string;
  you: boolean; // you control it: your own seat, or one you took with "Assign me"
  seatOf?: string; // set for a seat you took with "Assign me"
  host: boolean;
  open: boolean; // an empty seat waiting for a player
  model: string | null; // null when private (someone else's agent)
  status: string;
};
type AgentNode = Node<AgentData, "agent">;
type GameData = { title: string; locked: boolean; running: boolean; onSelect?: (id: string) => void };
type GameEdge = Edge<GameData, "game">;

type Selection = { kind: "agent"; id: string } | { kind: "game"; id: string } | null;

const RADIUS = 220;

function seatModel(seat: Seat | null): string | null {
  if (!seat) return null;
  if (seat.kind === "live") return `live · ${seat.client || "agent"}`;
  const m = seat.kind === "llm" ? seat.model : seat.kind === "team" ? seat.proposer_model : `scripted · ${seat.name}`;
  return m.split("/").pop() ?? m; // drop provider/org prefixes so it fits the node
}

function buildGraph(room: RoomView): { nodes: AgentNode[]; edges: GameEdge[] } {
  const agents: AgentData[] = room.participants.map((p) => {
    const taken = room.controlled.find((c) => c.name === p.name);
    const you = p.name === room.me.name || !!taken;
    const seat = taken ? taken.seat : room.me.seat;
    return {
      name: p.name,
      you,
      seatOf: taken?.name,
      host: p.is_host,
      open: false,
      model: you ? (seatModel(seat) ?? "no agent yet") : null,
      status: !p.has_seat ? "no agent yet" : p.ready ? "ready" : "setting up",
    };
  });
  for (let i = agents.length; i < room.capacity; i++)
    agents.push({ name: "Open seat", you: false, host: false, open: true, model: null, status: "waiting for a player" });

  const n = agents.length;
  const nodes: AgentNode[] = agents.map((a, i) => {
    // Lay agents out on a circle (left/right for two), starting with you.
    const angle = Math.PI + (2 * Math.PI * i) / n;
    return {
      id: a.open ? `open-${i}` : `agent-${a.name}`,
      type: "agent",
      position: { x: RADIUS * Math.cos(angle), y: RADIUS * Math.sin(angle) * (n > 2 ? 1 : 0) },
      data: a,
    };
  });

  const edges: GameEdge[] = [];
  for (let i = 0; i < n; i++)
    for (let j = i + 1; j < n; j++)
      edges.push({
        id: `game-${nodes[i].id}-${nodes[j].id}`,
        source: nodes[i].id,
        target: nodes[j].id,
        type: "game",
        data: { title: room.game.spec.title, locked: room.game.locked, running: room.running.length > 0 },
      });
  return { nodes, edges };
}

function AgentNodeView({ data, selected }: NodeProps<AgentNode>) {
  return (
    <div
      className={`w-48 rounded-(--radius) border bg-background px-3 py-2.5 text-left transition-colors ${
        data.open ? "border-dashed text-muted-foreground" : ""
      } ${selected ? "border-brand ring-2 ring-brand/20" : "border-line hover:border-foreground/30"}`}
    >
      {/* Hidden handles: edges attach to the node centre-ish, nodes aren't wired by hand yet. */}
      <Handle type="source" position={Position.Right} className="!opacity-0" isConnectable={false} />
      <Handle type="target" position={Position.Left} className="!opacity-0" isConnectable={false} />
      <div className="flex items-center gap-2">
        {data.open ? <UserRound className="size-4" /> : <Bot className="size-4 text-brand" />}
        <span className="truncate font-medium">{data.name}</span>
      </div>
      <p className="label-mono mt-1.5 text-[0.65rem]">
        {[data.seatOf ? "yours" : data.you && "you", data.host && "host", data.status].filter(Boolean).join(" · ")}
      </p>
      {!data.open && (
        <p className="mt-1 flex items-center gap-1 truncate font-mono text-xs text-muted-foreground">
          {data.model ?? (
            <>
              <Lock className="size-3" /> private
            </>
          )}
        </p>
      )}
    </div>
  );
}

function GameEdgeView({ id, sourceX, sourceY, targetX, targetY, data, selected }: EdgeProps<GameEdge>) {
  const [path, labelX, labelY] = getStraightPath({ sourceX, sourceY, targetX, targetY });
  return (
    <>
      <BaseEdge
        id={id}
        path={path}
        interactionWidth={24}
        style={{
          stroke: selected ? "var(--brand)" : "var(--muted-foreground)",
          strokeWidth: selected ? 2 : 1.25,
          strokeDasharray: data?.locked ? undefined : "5 4",
        }}
      />
      <EdgeLabelRenderer>
        <div
          className={`nodrag nopan pointer-events-auto absolute cursor-pointer rounded-(--radius) border bg-background px-2 py-1 text-xs ${
            selected ? "border-brand text-brand" : "border-line"
          }`}
          style={{ transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)` }}
          onClick={() => data?.onSelect?.(id)}
        >
          <span className="label-mono mr-1.5 text-[0.6rem]">
            {data?.running ? "● playing" : data?.locked ? "game ✓" : "game"}
          </span>
          {data?.title}
        </div>
      </EdgeLabelRenderer>
    </>
  );
}

const nodeTypes = { agent: AgentNodeView };
const edgeTypes = { game: GameEdgeView };

export function AgentMap({ room, onChange }: { room: RoomView; onChange: () => void }) {
  const graph = useMemo(() => buildGraph(room), [room]);
  // Where each node was dragged to and its measured size; React Flow needs both back.
  const [layout, setLayout] = useState<Record<string, Pick<AgentNode, "position" | "measured">>>({});
  const [selection, setSelection] = useState<Selection>(null);

  const nodes = graph.nodes.map((n) => ({
    ...n,
    ...layout[n.id],
    selected: selection?.kind === "agent" && selection.id === n.id,
  }));
  // The edge label sits outside React Flow's hit testing, so it selects through the edge data.
  const selectGame = (id: string) => setSelection({ kind: "game", id });
  const edges = graph.edges.map((e) => ({
    ...e,
    data: { ...e.data!, onSelect: selectGame },
    selected: selection?.kind === "game" && selection.id === e.id,
  }));

  function onNodesChange(changes: NodeChange<AgentNode>[]) {
    // Keep drags and measurements; selection is driven by clicks below, and nodes come from the room.
    const next = applyNodeChanges(
      changes.filter((c) => c.type === "position" || c.type === "dimensions"),
      nodes,
    );
    setLayout(Object.fromEntries(next.map((n) => [n.id, { position: n.position, measured: n.measured }])));
  }

  useEffect(() => {
    if (!selection) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setSelection(null);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selection]);

  const selectedAgent = selection?.kind === "agent" ? nodes.find((n) => n.id === selection.id)?.data : undefined;
  const selectedGame = selection?.kind === "game" ? edges.find((e) => e.id === selection.id) : undefined;

  return (
    <div className="relative h-[70svh] min-h-[28rem] overflow-hidden rounded-(--radius) border border-line bg-muted/30">
      <ReactFlow<AgentNode, GameEdge>
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        onNodesChange={onNodesChange}
        onNodeClick={(_, n) => setSelection({ kind: "agent", id: n.id })}
        onEdgeClick={(_, e) => selectGame(e.id)}
        onPaneClick={() => setSelection(null)}
        nodesConnectable={false}
        fitView
        fitViewOptions={{ padding: 0.4, maxZoom: 1.1 }}
        proOptions={{ hideAttribution: true }}
      >
        <Background variant={BackgroundVariant.Lines} gap={24} lineWidth={1} color="var(--line)" />
        <Controls showInteractive={false} position="bottom-left" />
        <Panel position="top-left">
          {/* Keyed on the game version so a changed game resets the runs to its default. */}
          <StartBar key={room.game.version} room={room} onChange={onChange} />
        </Panel>
      </ReactFlow>

      {/* The inspector spans the page height below the top bar, beside the assistant column. */}
      {(selectedAgent || selectedGame) &&
        createPortal(
          <aside className="@container fixed top-14 bottom-0 right-(--assistant-w,0px) z-40 flex w-full max-w-[34rem] flex-col border-l border-line bg-background shadow-[-8px_0_24px_-16px_rgb(0_0_0/0.15)]">
            <div className="flex items-center justify-between gap-2 border-b border-line px-4 py-3">
              <div className="min-w-0">
                <p className="label-mono">{selectedAgent ? "Agent" : "Game between agents"}</p>
                <p className="display-title truncate text-xl">
                  {selectedAgent?.name ?? selectedGame?.data?.title ?? ""}
                </p>
              </div>
              <Button size="icon" variant="ghost" aria-label="Close" onClick={() => setSelection(null)}>
                <X />
              </Button>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              {selectedAgent?.you && (
                <SeatEditor key={selectedAgent.name} room={room} onChange={onChange} seatOf={selectedAgent.seatOf} />
              )}
              {selectedAgent && !selectedAgent.you && (
                <AgentProperties
                  agent={selectedAgent}
                  onAssign={async () => {
                    let name = "";
                    const ok = await attempt(
                      async () => ({ name } = await api.assignSelf(room.id)),
                      "Seat taken",
                      "Couldn't take the seat",
                    );
                    if (!ok) return;
                    setSelection({ kind: "agent", id: `agent-${name}` }); // open its editor next
                    onChange();
                  }}
                />
              )}
              {selectedGame && <GameEditor room={room} onChange={onChange} />}
            </div>
          </aside>,
          document.body,
        )}
    </div>
  );
}

/** Start a match from the map; then switch to the Match tab to watch it live. */
function StartBar({ room, onChange }: { room: RoomView; onChange: () => void }) {
  const [runs, setRuns] = useState(room.game.spec.runs);
  const running = room.running.length > 0;

  async function start() {
    const ok = await attempt(() => api.startMatch(room.id, runs), `Match started: ${runs} runs`, "Couldn't start the match");
    if (!ok) return;
    onChange();
    setRoomTab("match");
  }

  return (
    <div className="flex max-w-md flex-col gap-1.5 rounded-(--radius) border border-line bg-background p-2">
      <div className="flex items-center gap-2">
        <span className="label-mono pl-1">Runs</span>
        <Input
          className="h-8 w-16"
          type="number"
          min={1}
          value={runs}
          onChange={(e) => setRuns(Number(e.target.value))}
          aria-label="Runs"
        />
        <Button size="sm" onClick={start} disabled={!room.can_start || running}>
          <Play /> {running ? "Match running" : "Start match"}
        </Button>
        {running && (
          <Button size="sm" variant="ghost" onClick={() => setRoomTab("match")}>
            Watch
          </Button>
        )}
      </div>
      {!room.can_start && !running && room.start_problems.length > 0 && (
        <p className="px-1 text-xs text-muted-foreground">Not yet: {room.start_problems.join("; ")}.</p>
      )}
    </div>
  );
}

function AgentProperties({ agent, onAssign }: { agent: AgentData; onAssign: () => void }) {
  const rows: [string, string][] = agent.open
    ? [["Status", "Waiting for a player. Share the invite link, or take the seat yourself."]]
    : [
        ["Player", agent.name + (agent.host ? " (host)" : "")],
        ["Status", agent.status],
        ["Model", "private"],
        ["Strategy", "private"],
      ];
  return (
    <div className="flex flex-col gap-4">
      <dl className="divide-y divide-line border-y border-line">
        {rows.map(([k, v]) => (
          <div key={k} className="grid grid-cols-[7rem_1fr] gap-3 py-2.5">
            <dt className="label-mono">{k}</dt>
            <dd className="text-sm">{v}</dd>
          </div>
        ))}
      </dl>
      {agent.open && (
        <div className="flex flex-col items-start gap-2">
          <Button onClick={onAssign}>
            <UserRoundPlus /> Assign me
          </Button>
          <p className="text-sm text-muted-foreground">
            You&apos;ll set up this agent too and can run your agents against each other. Release the
            seat later to let someone else join.
          </p>
        </div>
      )}
      {!agent.open && (
        <p className="text-sm text-muted-foreground">
          Other players build their agents in private. Their model and strategy show up in the results
          if they choose to reveal them after a match.
        </p>
      )}
    </div>
  );
}
