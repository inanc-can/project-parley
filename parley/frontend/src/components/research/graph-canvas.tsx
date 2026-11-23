"use client";

/**
 * The force layout itself, in 3D (three.js) or 2D (canvas). Loaded only in the browser:
 * both libraries touch `window` at import time.
 */
import { useEffect, useRef } from "react";
import ForceGraph2D from "react-force-graph-2d";
import ForceGraph3D from "react-force-graph-3d";
import SpriteText from "three-spritetext";

import { LINK_COLORS, COLORS, nodeSize } from "./palette";
import type { GraphData, GraphLink, GraphNode } from "./types";
import { endId } from "./types";

type Props = {
  data: GraphData;
  mode: "3d" | "2d";
  width: number;
  height: number;
  selected: string | null;
  neighbours: Set<string>;
  onSelect: (id: string | null) => void;
  colorOf: (n: GraphNode) => string;
  /** fewer, larger clusters (everyday view): pull them closer */
  tight?: boolean;
};

const isHub = (n: GraphNode) => n.type !== "paper";

function tooltip(n: GraphNode) {
  const kind = n.type === "paper" ? (n.benchmark ? "Benchmark" : "Study") : n.type;
  const extra = n.type === "paper" ? ` · ${n.year} · ${n.authors?.[0] ?? ""}${(n.authors?.length ?? 0) > 1 ? " et al." : ""}` : "";
  return `<div style="font:12px/1.4 var(--font-sans,system-ui);max-width:280px;padding:6px 8px;background:#fff;color:#1c1b1a;border:1px solid #e5e2db;border-radius:4px"><div style="font:500 10px var(--font-mono,monospace);text-transform:uppercase;letter-spacing:.12em;color:#5b5850">${kind}${extra}</div>${n.label}</div>`;
}

export default function GraphCanvas({ data, mode, width, height, selected, neighbours, onSelect, colorOf, tight = false }: Props) {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const ref = useRef<any>(undefined);
  const fitted = useRef(false);
  const fitOnce = () => {
    if (fitted.current || selected) return;
    fitted.current = true;
    ref.current?.zoomToFit(600, 40);
  };

  const faded = (id: string) => selected !== null && id !== selected && !neighbours.has(id);
  const color = (n: GraphNode) => (faded(n.id) ? COLORS.dim : colorOf(n));
  const linkColor = (l: GraphLink) => {
    if (selected === null) return LINK_COLORS[l.kind];
    const touches = endId(l.source) === selected || endId(l.target) === selected;
    return touches ? "rgba(31,45,92,0.7)" : "rgba(229,226,219,0.25)";
  };

  // Spread the layout a little: hubs repel more so their paper clouds separate.
  useEffect(() => {
    const fg = ref.current;
    if (!fg) return;
    fg.d3Force("charge")?.strength((n: GraphNode) => (isHub(n) ? (tight ? -160 : -600) : tight ? -30 : -70));
    fg.d3Force("link")?.distance((l: GraphLink) => (l.kind === "cites" ? 90 : tight ? 30 : 70));
    fitted.current = false;
    fg.d3ReheatSimulation?.();
    // Frame the layout once it has mostly settled, in case the engine keeps ticking.
    const t = setTimeout(() => {
      fitted.current = false;
      fitOnce();
    }, 2500);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode, data]);

  // Fly to the selected node.
  useEffect(() => {
    const fg = ref.current;
    if (!fg || !selected) return;
    const n = data.nodes.find((x) => x.id === selected);
    if (!n || n.x === undefined) return;
    if (mode === "3d") {
      const dist = 140;
      const r = Math.hypot(n.x, n.y ?? 0, n.z ?? 0) || 1;
      const k = 1 + dist / r;
      fg.cameraPosition({ x: n.x * k, y: (n.y ?? 0) * k, z: (n.z ?? 0) * k }, n, 1200);
    } else {
      fg.centerAt(n.x, n.y, 800);
      fg.zoom(3, 800);
    }
  }, [selected, mode, data.nodes]);

  const common = {
    graphData: data,
    width,
    height,
    nodeId: "id",
    nodeVal: (n: object) => nodeSize(n as GraphNode),
    nodeLabel: (n: object) => tooltip(n as GraphNode),
    linkColor: (l: object) => linkColor(l as GraphLink),
    onNodeClick: (n: object) => onSelect((n as GraphNode).id),
    onBackgroundClick: () => onSelect(null),
    cooldownTicks: 200,
    warmupTicks: 40,
  };

  if (mode === "3d") {
    return (
      <ForceGraph3D
        ref={ref}
        {...common}
        backgroundColor="#fbfaf8"
        showNavInfo={false}
        nodeColor={(n: object) => color(n as GraphNode)}
        nodeOpacity={0.95}
        nodeResolution={12}
        linkWidth={(l: object) => ((l as GraphLink).kind === "cites" ? 0 : 0.6)}
        linkOpacity={0.5}
        nodeThreeObjectExtend
        nodeThreeObject={(o: object) => {
          const n = o as GraphNode;
          if (!isHub(n)) return undefined as unknown as never;
          const s = new SpriteText(n.short ?? n.label);
          s.color = faded(n.id) ? "#c9c5bc" : colorOf(n);
          s.textHeight = n.type === "person" ? 4 : n.type === "question" ? 7 : 5.5;
          s.fontFace = "IBM Plex Mono, ui-monospace, monospace";
          s.fontWeight = "500";
          s.position.y = nodeSize(n) + 6;
          return s;
        }}
        onEngineStop={fitOnce}
      />
    );
  }

  return (
    <ForceGraph2D
      ref={ref}
      {...common}
      backgroundColor="#fbfaf8"
      linkWidth={(l: object) => ((l as GraphLink).kind === "cites" ? 0.4 : 0.8)}
      nodeRelSize={3}
      nodeCanvasObjectMode={() => "after"}
      nodeColor={(n: object) => color(n as GraphNode)}
      nodeCanvasObject={(o: object, ctx: CanvasRenderingContext2D, scale: number) => {
        const n = o as GraphNode;
        const show = isHub(n) || n.id === selected || (scale > 2.5 && neighbours.has(n.id));
        if (!show || n.x === undefined || n.y === undefined) return;
        const text = isHub(n) ? (n.short ?? n.label) : n.id;
        const size = (isHub(n) ? 13 : 10) / scale;
        ctx.font = `500 ${size}px "IBM Plex Mono", ui-monospace, monospace`;
        ctx.textAlign = "center";
        ctx.textBaseline = "top";
        ctx.fillStyle = faded(n.id) ? "#c9c5bc" : n.type === "paper" ? "#1c1b1a" : colorOf(n);
        ctx.fillText(text, n.x, n.y + Math.sqrt(nodeSize(n)) * 3 + 2 / scale);
      }}
      onEngineStop={fitOnce}
    />
  );
}
