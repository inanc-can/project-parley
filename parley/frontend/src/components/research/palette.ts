import type { GraphNode, LinkKind } from "./types";

/** Node colours, in the site's editorial palette (navy brand, warm greys). */
export const COLORS = {
  skill: "#1f2d5c",
  topic: "#8a6d3b",
  person: "#2f6b4f",
  benchmark: "#5b6fa8",
  paper: "#a0a9c8",
  transfer: "#c2410c",
  dim: "#e5e2db",
} as const;

export const LINK_COLORS: Record<LinkKind, string> = {
  skill: "rgba(31,45,92,0.35)",
  topic: "rgba(138,109,59,0.28)",
  person: "rgba(47,107,79,0.45)",
  cites: "rgba(91,88,80,0.18)",
  question: "rgba(31,45,92,0.3)",
};

/** One colour per everyday question; its papers take the colour of their first question. */
export const QUESTION_COLORS = ["#1f2d5c", "#b45309", "#2f6b4f", "#8b3a62", "#3f6e9e", "#7a6a2f", "#c2410c"];

export function nodeColor(n: GraphNode): string {
  if (n.type === "question") return COLORS.skill;
  if (n.type !== "paper") return COLORS[n.type];
  if (n.transfer) return COLORS.transfer;
  return n.benchmark ? COLORS.benchmark : COLORS.paper;
}

export function nodeSize(n: GraphNode): number {
  if (n.type === "question") return 12;
  if (n.type === "skill") return 10;
  if (n.type === "topic") return 8;
  if (n.type === "person") return 5;
  return n.relevance === "high" ? 3 : n.relevance === "medium" ? 2 : 1.2;
}

export const LEGEND: { color: string; label: string }[] = [
  { color: COLORS.skill, label: "Social skill" },
  { color: COLORS.topic, label: "Topic" },
  { color: COLORS.person, label: "Researcher" },
  { color: COLORS.benchmark, label: "Benchmark" },
  { color: COLORS.paper, label: "Study" },
  { color: COLORS.transfer, label: "Measures transfer between skills" },
];
