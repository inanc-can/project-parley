import type { Metadata } from "next";

import { ResearchMap } from "@/components/research/research-map";
import type { GraphData } from "@/components/research/types";
import graph from "@/data/research-graph.json";

export const metadata: Metadata = {
  title: "Research map",
  description:
    "What research says about AI agents that negotiate, persuade and cooperate for people: everyday questions with plain answers, and an interactive map of the literature for researchers.",
};

const data = graph as GraphData;
const TRAININGS = ["prompting", "SFT", "RL", "multi-agent"];

/** Per skill: how many benchmarks measure it, which training methods they evaluate, transfer. */
function coverage() {
  const papers = data.nodes.filter((n) => n.type === "paper" && n.eval);
  return data.nodes
    .filter((n) => n.type === "skill")
    .map((skill) => {
      const key = skill.id.replace("skill:", "");
      const hits = papers.filter((p) => p.skills?.includes(key));
      return {
        label: skill.label,
        total: hits.length,
        training: TRAININGS.map((t) => hits.filter((p) => p.training?.includes(t)).length),
        transfer: hits.filter((p) => p.transfer).length,
      };
    })
    .sort((a, b) => b.total - a.total);
}

export default function ResearchPage() {
  const rows = coverage();
  const max = Math.max(...rows.map((r) => r.total), 1);
  return (
    <div className="mx-auto max-w-7xl px-4 pt-32 pb-24">
      <div className="flex items-center gap-3 border-t border-line pt-4">
        <span className="label-mono text-brand">Research</span>
        <span className="label-mono">Literature map</span>
      </div>
      <h1 className="display-title mt-6 max-w-[820px] text-4xl md:text-6xl">
        What do we know about AI agents with social skills?
      </h1>
      <p className="mt-6 max-w-[680px] text-lg text-muted-foreground">
        AI agents are starting to negotiate, shop and make deals for people. This map gathers the
        research behind Parley. Start with an everyday question and get a plain answer, or switch to
        the researcher view to explore benchmarks, skills and citations. Every claim links back to a
        reading note with page references.
      </p>

      <div className="mt-12">
        <ResearchMap data={data} />
      </div>

      <section className="mt-24" aria-labelledby="coverage">
        <div className="flex items-center gap-3 border-t border-line pt-4">
          <span className="label-mono text-brand">For researchers</span>
          <span className="label-mono">Coverage</span>
        </div>
        <h2 id="coverage" className="display-title mt-6 max-w-[760px] text-3xl md:text-4xl">
          Many benchmarks measure skills. Few test whether training one helps another.
        </h2>
        <p className="mt-4 max-w-[640px] text-muted-foreground">
          For each social skill: how many of the {data.nodes.filter((n) => n.eval).length}{" "}
          benchmarks in the map measure it, how many evaluate each training method, and how many
          measure transfer between skills.
        </p>
        <div className="mt-8 overflow-x-auto">
          <table className="w-full min-w-[640px] border-collapse text-sm">
            <thead>
              <tr className="border-b border-line text-left">
                <th className="label-mono py-3 pr-4 font-medium">Skill</th>
                <th className="label-mono py-3 pr-4 font-medium">Benchmarks</th>
                {TRAININGS.map((t) => (
                  <th key={t} className="label-mono py-3 pr-4 text-right font-medium">
                    {t}
                  </th>
                ))}
                <th className="label-mono py-3 text-right font-medium text-[#c2410c]">Transfer</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.label} className="border-b border-line">
                  <td className="py-3 pr-4 font-medium">{r.label}</td>
                  <td className="py-3 pr-4">
                    <div className="flex items-center gap-3">
                      <span className="w-6 tabular-nums">{r.total}</span>
                      <span className="h-2 rounded-full bg-brand" style={{ width: `${(r.total / max) * 140}px` }} />
                    </div>
                  </td>
                  {r.training.map((n, i) => (
                    <td key={i} className={`py-3 pr-4 text-right tabular-nums ${n ? "" : "text-muted-foreground/50"}`}>
                      {n}
                    </td>
                  ))}
                  <td className={`py-3 text-right tabular-nums ${r.transfer ? "font-semibold text-[#c2410c]" : "text-muted-foreground/50"}`}>
                    {r.transfer}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-4 max-w-[640px] text-xs text-muted-foreground">
          Skill and training tags are read automatically from each note&apos;s summary fields, so a
          few may be loose; the linked notes are the source of truth. A benchmark can count under
          several skills.
        </p>
      </section>
    </div>
  );
}
