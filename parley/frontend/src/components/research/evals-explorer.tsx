"use client";

import { useMemo, useState } from "react";

import type { EvalClass, GraphNode } from "./types";

const REPO = "https://github.com/inanc-can/project-parley/blob/main/research/papers";

export type EvalRow = GraphNode & { eval: EvalClass; name: string };
type Option = { key: string; label: string };

const SCORING: Record<string, { label: string; hint: string }> = {
  rules: { label: "Rules", hint: "Outcome computed from the game's rules" },
  mixed: { label: "Mixed", hint: "Rules plus an LLM or human judge for part of the score" },
  judge: { label: "LLM judge", hint: "An LLM decides the score" },
  other: { label: "Other", hint: "" },
};
const TESTS: Record<string, string> = {
  capability: "Capability",
  propensity: "Propensity",
  both: "Capability + propensity",
  "not recorded": "Not recorded",
};
const AGENTS: Record<string, string> = { "1": "1 agent", "2": "2 agents", many: "3+ agents" };
const COUNTERPARTS = ["scripted", "LLM", "human", "solver", "trained agents"];
const TRAININGS = ["prompting", "SFT", "RL", "multi-agent"];

function Chips({
  label,
  options,
  value,
  onChange,
}: {
  label: string;
  options: Option[];
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="label-mono mr-1 w-28 shrink-0">{label}</span>
      {[{ key: "", label: "All" }, ...options].map((o) => (
        <button
          key={o.key || "all"}
          type="button"
          aria-pressed={value === o.key}
          onClick={() => onChange(o.key)}
          className={`rounded-full border px-3 py-1 text-xs transition-colors ${
            value === o.key
              ? "border-brand bg-brand text-white"
              : "border-line bg-background text-foreground hover:border-brand/50"
          }`}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

function Bar({ title, parts, total }: { title: string; parts: { label: string; n: number }[]; total: number }) {
  const shades = ["#1f2d5c", "#5b6fa8", "#a0a9c8", "#d6dae8", "#e5e2db"];
  return (
    <div className="border-t border-line pt-4">
      <p className="label-mono">{title}</p>
      <div className="mt-3 flex h-2 overflow-hidden rounded-full bg-secondary">
        {parts.map((p, i) => (
          <span key={p.label} style={{ width: `${(p.n / total) * 100}%`, background: shades[i] }} />
        ))}
      </div>
      <ul className="mt-3 space-y-1 text-sm">
        {parts.map((p, i) => (
          <li key={p.label} className="flex items-center gap-2">
            <span className="size-2 shrink-0 rounded-full" style={{ background: shades[i] }} />
            <span className="flex-1">{p.label}</span>
            <span className="tabular-nums text-muted-foreground">{p.n}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function EvalsExplorer({ rows, skills }: { rows: EvalRow[]; skills: Option[] }) {
  const [skill, setSkill] = useState("");
  const [scoring, setScoring] = useState("");
  const [counterpart, setCounterpart] = useState("");
  const [training, setTraining] = useState("");
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState<string | null>(null);

  const skillLabel = useMemo(() => Object.fromEntries(skills.map((s) => [s.key, s.label])), [skills]);

  const shown = useMemo(() => {
    const q = query.trim().toLowerCase();
    return rows.filter(
      (r) =>
        (!skill || r.skills?.includes(skill)) &&
        (!scoring || r.eval.scoring === scoring) &&
        (!counterpart || r.eval.opponents.includes(counterpart)) &&
        (!training ||
          (training === "none" ? !r.training?.length : training === "transfer" ? r.transfer : r.training?.includes(training))) &&
        (!q || `${r.name} ${r.label} ${r.authors?.join(" ")} ${r.map?.["Skills measured"]}`.toLowerCase().includes(q)),
    );
  }, [rows, skill, scoring, counterpart, training, query]);

  const total = rows.length;
  const count = (f: (r: EvalRow) => boolean) => rows.filter(f).length;
  const filtered = skill || scoring || counterpart || training || query;

  return (
    <div>
      <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
        <Bar
          title="How it's scored"
          total={total}
          parts={["rules", "mixed", "judge"].map((k) => ({ label: SCORING[k].label, n: count((r) => r.eval.scoring === k) }))}
        />
        <Bar
          title="Who the agent faces"
          total={total}
          parts={[
            { label: "Other LLMs only", n: count((r) => r.eval.opponents.join() === "LLM") },
            { label: "Includes scripted or solver", n: count((r) => r.eval.opponents.some((o) => o === "scripted" || o === "solver")) },
            { label: "Includes humans", n: count((r) => r.eval.opponents.includes("human")) },
          ]}
        />
        <Bar
          title="What it tests"
          total={total}
          parts={["capability", "both", "propensity", "not recorded"].map((k) => ({ label: TESTS[k], n: count((r) => r.eval.tests === k) }))}
        />
        <Bar
          title="Training"
          total={total}
          parts={[
            { label: "No training evaluated", n: count((r) => !r.training?.length) },
            { label: "Prompting only", n: count((r) => r.training?.join() === "prompting") },
            { label: "Fine-tuning or RL", n: count((r) => !!r.training?.some((t) => t !== "prompting")) },
            { label: "Measures transfer", n: count((r) => !!r.transfer) },
          ]}
        />
      </div>

      <div className="mt-12 space-y-3 rounded-lg border border-line bg-secondary p-4 md:p-6">
        <Chips label="Skill" options={skills} value={skill} onChange={setSkill} />
        <Chips
          label="Scoring"
          options={["rules", "mixed", "judge"].map((k) => ({ key: k, label: SCORING[k].label }))}
          value={scoring}
          onChange={setScoring}
        />
        <Chips
          label="Counterpart"
          options={COUNTERPARTS.map((c) => ({ key: c, label: c === "LLM" ? "LLM" : c[0].toUpperCase() + c.slice(1) }))}
          value={counterpart}
          onChange={setCounterpart}
        />
        <Chips
          label="Training"
          options={[
            ...TRAININGS.map((t) => ({ key: t, label: t })),
            { key: "none", label: "None" },
            { key: "transfer", label: "Measures transfer" },
          ]}
          value={training}
          onChange={setTraining}
        />
        <div className="flex flex-wrap items-center gap-3 pt-1">
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by name, author or skill"
            aria-label="Search evals"
            className="h-9 w-full max-w-xs rounded-md border border-line bg-background px-3 text-sm outline-none focus:border-brand"
          />
          <span className="text-sm text-muted-foreground">
            {shown.length} of {total} evals
          </span>
          {filtered && (
            <button
              type="button"
              onClick={() => {
                setSkill("");
                setScoring("");
                setCounterpart("");
                setTraining("");
                setQuery("");
              }}
              className="text-sm text-brand underline-offset-4 hover:underline"
            >
              Clear filters
            </button>
          )}
        </div>
      </div>

      <div className="mt-8 hidden grid-cols-12 gap-4 border-b border-line pb-3 md:grid">
        <span className="label-mono col-span-4">Eval</span>
        <span className="label-mono col-span-3">Skills</span>
        <span className="label-mono col-span-2">Setup</span>
        <span className="label-mono col-span-2">Scoring</span>
        <span className="label-mono col-span-1 text-right">Training</span>
      </div>
      <ul className="max-md:mt-6">
        {shown.map((r) => {
          const expanded = open === r.id;
          return (
            <li key={r.id} className="border-b border-line">
              <button
                type="button"
                onClick={() => setOpen(expanded ? null : r.id)}
                aria-expanded={expanded}
                className="grid w-full gap-3 py-5 text-left md:grid-cols-12 md:gap-4"
              >
                <div className="md:col-span-4">
                  <p className="display-title text-xl leading-tight">{r.name}</p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {r.authors?.[0]?.split(" ").slice(-1)[0]}
                    {(r.authors?.length ?? 0) > 1 ? " et al." : ""} · {r.year}
                    {r.read !== "full" && <span className="ml-2 text-[#b45309]">read: {r.read}</span>}
                  </p>
                </div>
                <div className="flex flex-wrap content-start gap-1.5 md:col-span-3">
                  {(r.skills ?? []).map((s) => (
                    <span key={s} className="rounded-full bg-secondary px-2 py-0.5 text-xs">
                      {skillLabel[s] ?? s}
                    </span>
                  ))}
                  {!r.skills?.length && <span className="text-xs text-muted-foreground">Other skills</span>}
                </div>
                <div className="text-sm md:col-span-2">
                  <p>{AGENTS[r.eval.agents]}</p>
                  <p className="text-muted-foreground">vs {r.eval.opponents.join(", ") || "none"}</p>
                </div>
                <div className="text-sm md:col-span-2">
                  <p title={SCORING[r.eval.scoring].hint}>{SCORING[r.eval.scoring].label}</p>
                  <p className="text-muted-foreground">{TESTS[r.eval.tests]}</p>
                </div>
                <div className="text-sm md:col-span-1 md:text-right">
                  <p>
                    <span className="text-muted-foreground md:hidden">Training: </span>
                    {r.training?.length ? r.training.join(", ") : "—"}
                  </p>
                  {r.transfer && <p className="font-semibold text-[#c2410c]">transfer</p>}
                </div>
              </button>
              {expanded && (
                <div className="grid gap-6 pb-8 md:grid-cols-12 md:gap-4">
                  <div className="space-y-4 text-sm md:col-span-8">
                    <p className="text-muted-foreground">{r.label}</p>
                    {r.question && (
                      <div>
                        <p className="label-mono">Question</p>
                        <p className="mt-1">{r.question}</p>
                      </div>
                    )}
                    {["Skills measured", "Scoring", "Opponents", "Training evaluated", "Transfer between skills measured", "Models tested"].map(
                      (k) =>
                        r.map?.[k] && (
                          <div key={k}>
                            <p className="label-mono">{k}</p>
                            <p className="mt-1">{r.map[k]}</p>
                          </div>
                        ),
                    )}
                  </div>
                  <div className="flex flex-col items-start gap-2 text-sm md:col-span-4">
                    <a href={`${REPO}/${r.id}.md`} target="_blank" rel="noreferrer" className="text-brand underline-offset-4 hover:underline">
                      Reading note with page references ↗
                    </a>
                    {r.arxiv && (
                      <a href={`https://arxiv.org/abs/${r.arxiv}`} target="_blank" rel="noreferrer" className="text-brand underline-offset-4 hover:underline">
                        Paper on arXiv ↗
                      </a>
                    )}
                    {r.eval.code && (
                      <a href={r.eval.code} target="_blank" rel="noreferrer" className="text-brand underline-offset-4 hover:underline">
                        Code or project page ↗
                      </a>
                    )}
                  </div>
                </div>
              )}
            </li>
          );
        })}
      </ul>
      {!shown.length && <p className="py-12 text-center text-muted-foreground">No eval matches these filters.</p>}
    </div>
  );
}
