import type { Metadata } from "next";
import Link from "next/link";

import { EvalsExplorer, type EvalRow } from "@/components/research/evals-explorer";
import type { GraphData } from "@/components/research/types";
import graph from "@/data/research-graph.json";

export const metadata: Metadata = {
  title: "Evals for social AI agents",
  description:
    "Every benchmark we have read for AI agents that negotiate, cooperate, persuade and deceive, classified by skill, scoring, counterpart and training.",
};

const data = graph as GraphData;

/** Short, recognisable names where the paper title is long or the benchmark has its own name. */
const NAMES: Record<string, string> = {
  bianchi2024negotiationarena: "NegotiationArena",
  bozdag2025persuade: "PMIYC (Persuade Me if You Can)",
  chen2023your: "Auction Arena",
  davidson2024evaluating: "LM agency through negotiations",
  gajewska2026benchmarking: "Defences against character attacks",
  hua2026passive: "SocialRL",
  huang2024gamabench: "GAMA-Bench",
  leibo2021meltingpot: "Melting Pot",
  lewis2017deal: "Deal or No Deal",
  li2026whose: "PrincipalBench",
  lupu2025decrypto: "Decrypto",
  oh2026merit: "MERIT",
  sarkar2025training: "Social deduction RL (Among Us)",
  smith2025evaluating: "Concordia contest",
  wu2026measuring: "Collaborative Intelligence",
  zhu2025automated: "A2A-NT (The Automated but Risky Game)",
};

export default function EvalsPage() {
  const rows: EvalRow[] = data.nodes
    .filter((n): n is EvalRow => n.type === "paper" && !!n.eval)
    .map((n) => ({ ...n, eval: n.eval!, name: NAMES[n.id] ?? n.label.split(":")[0] }))
    .sort((a, b) => (b.year ?? 0) - (a.year ?? 0) || a.name.localeCompare(b.name));
  const skills = data.nodes
    .filter((n) => n.type === "skill")
    .map((n) => ({ key: n.id.replace("skill:", ""), label: n.label }));

  return (
    <div className="mx-auto max-w-7xl px-4 pt-32 pb-24">
      <div className="flex items-center gap-3 border-t border-line pt-4">
        <span className="label-mono text-brand">Research</span>
        <span className="label-mono">Evals</span>
      </div>
      <h1 className="display-title mt-6 max-w-[860px] text-4xl md:text-6xl">
        How do people test AI agents with social skills?
      </h1>
      <p className="mt-6 max-w-[680px] text-lg text-muted-foreground">
        {rows.length} benchmarks we have read, from bargaining and teamwork to persuasion and hidden-role
        games, classified by the skill they measure, how they score it, who the agent faces and
        whether they test training. Open any row for details and the reading note.
      </p>
      <p className="mt-4 text-sm text-muted-foreground">
        Prefer the big picture?{" "}
        <Link href="/research" className="text-brand underline-offset-4 hover:underline">
          Explore the research map
        </Link>
      </p>

      <div className="mt-16">
        <EvalsExplorer rows={rows} skills={skills} />
      </div>

      <p className="mt-8 max-w-[680px] text-xs text-muted-foreground">
        Classes are read automatically from each note&apos;s summary fields, so a few may be loose;
        the linked notes are the source of truth. &ldquo;Propensity&rdquo; means what an agent tends to
        do when not told, &ldquo;capability&rdquo; what it can do when asked. Notes marked
        &ldquo;read: partial&rdquo; are not yet read in full.
      </p>
    </div>
  );
}
