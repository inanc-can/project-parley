"use client";

import { cn } from "cn";
import dynamic from "next/dynamic";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { FOCUS } from "@/components/landing/cta";
import { TRANSITION } from "@/components/landing/motion";

import { LEGEND, QUESTION_COLORS, nodeColor } from "./palette";
import type { GraphData, GraphNode } from "./types";
import { endId } from "./types";

const GraphCanvas = dynamic(() => import("./graph-canvas"), {
  ssr: false,
  loading: () => <p className="label-mono p-6">Laying out the map…</p>,
});

const REPO = "https://github.com/inanc-can/project-parley/blob/main/research/papers";

type Audience = "everyday" | "academic";
type Lens = "skills" | "topics" | "citations";

const LENSES: { id: Lens; label: string; hint: string }[] = [
  { id: "skills", label: "By social skill", hint: "Benchmarks grouped around the skills they measure" },
  { id: "topics", label: "By topic", hint: "Every paper grouped by the research topics it belongs to" },
  { id: "citations", label: "Citations", hint: "Only how the papers refer to each other" },
];

const READ_LABEL: Record<string, string> = {
  full: "Read in full",
  partial: "Partly read",
  abstract: "Abstract only",
  unverified: "Unverified",
};

const CHIP = cn(
  "rounded-sm border border-line px-3 py-1.5 text-sm font-medium text-muted-foreground hover:text-brand",
  "aria-pressed:border-brand aria-pressed:bg-accent aria-pressed:text-brand",
  TRANSITION,
  FOCUS,
);

const LINK = "text-brand underline-offset-4 hover:underline";

function useSize<T extends HTMLElement>() {
  const ref = useRef<T>(null);
  const [size, setSize] = useState({ width: 0, height: 0 });
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const ro = new ResizeObserver(([e]) =>
      setSize({ width: Math.round(e.contentRect.width), height: Math.round(e.contentRect.height) }),
    );
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return [ref, size] as const;
}

/** For each paper, the everyday questions it helps answer, with the plain-language line. */
function plainIndex(data: GraphData) {
  const byPaper = new Map<string, { question: GraphNode; plain: string }[]>();
  const byQuestion = new Map<string, { paper: GraphNode; plain: string }[]>();
  const nodes = new Map(data.nodes.map((n) => [n.id, n]));
  for (const l of data.links) {
    if (l.kind !== "question") continue;
    const q = nodes.get(endId(l.source));
    const p = nodes.get(endId(l.target));
    if (!q || !p) continue;
    byPaper.set(p.id, [...(byPaper.get(p.id) ?? []), { question: q, plain: l.plain ?? "" }]);
    byQuestion.set(q.id, [...(byQuestion.get(q.id) ?? []), { paper: p, plain: l.plain ?? "" }]);
  }
  return { byPaper, byQuestion };
}

export function ResearchMap({ data }: { data: GraphData }) {
  const [audience, setAudience] = useState<Audience>("everyday");
  const [mode, setMode] = useState<"3d" | "2d">("3d");
  const [lens, setLens] = useState<Lens>("skills");
  const [fullOnly, setFullOnly] = useState(false);
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<string | null>(null);
  const [boxRef, size] = useSize<HTMLDivElement>();

  // Node objects stay the same across filters so the layout keeps its positions.
  const byId = useMemo(() => new Map(data.nodes.map((n) => [n.id, n])), [data]);
  const plain = useMemo(() => plainIndex(data), [data]);
  const questions = useMemo(() => data.nodes.filter((n) => n.type === "question"), [data]);

  // A link like /research?q=loyal opens that everyday question (used by the home page).
  useEffect(() => {
    const q = new URLSearchParams(window.location.search).get("q");
    if (!q || !byId.has(`question:${q}`)) return;
    queueMicrotask(() => setSelected(`question:${q}`));
    boxRef.current?.scrollIntoView({ block: "center" });
  }, [byId, boxRef]);

  const colorOf = useCallback(
    (n: GraphNode) => {
      if (audience === "academic") return nodeColor(n);
      if (n.type === "question") return QUESTION_COLORS[questions.indexOf(n) % QUESTION_COLORS.length];
      const first = plain.byPaper.get(n.id)?.[0]?.question;
      return first ? QUESTION_COLORS[questions.indexOf(first) % QUESTION_COLORS.length] : nodeColor(n);
    },
    [audience, plain, questions],
  );

  const view: GraphData = useMemo(() => {
    if (audience === "everyday") {
      const asked = data.links.filter((l) => l.kind === "question");
      const ids = new Set(asked.flatMap((l) => [endId(l.source), endId(l.target)]));
      // Faint citation lines between these studies show how the questions connect.
      const cites = data.links.filter(
        (l) => l.kind === "cites" && ids.has(endId(l.source)) && ids.has(endId(l.target)),
      );
      return { nodes: data.nodes.filter((n) => ids.has(n.id)), links: [...asked, ...cites] };
    }
    const keepPaper = (n: GraphNode) =>
      (!fullOnly || n.read === "full") && (lens !== "skills" || (n.skills?.length ?? 0) > 0);
    const hubType = lens === "skills" ? "skill" : lens === "topics" ? "topic" : null;
    const nodes = data.nodes.filter((n) =>
      n.type === "paper" ? keepPaper(n) : n.type === hubType || n.type === "person",
    );
    const ids = new Set(nodes.map((n) => n.id));
    const kinds = new Set(["cites", "person", ...(hubType ? [hubType] : [])]);
    const links = data.links.filter(
      (l) => kinds.has(l.kind) && ids.has(endId(l.source)) && ids.has(endId(l.target)),
    );
    // Drop people left without a paper.
    const linked = new Set(links.flatMap((l) => [endId(l.source), endId(l.target)]));
    return { nodes: nodes.filter((n) => n.type !== "person" || linked.has(n.id)), links };
  }, [data, audience, lens, fullOnly]);

  const neighbours = useMemo(() => {
    const set = new Set<string>();
    if (!selected) return set;
    for (const l of view.links) {
      const [s, t] = [endId(l.source), endId(l.target)];
      if (s === selected) set.add(t);
      if (t === selected) set.add(s);
    }
    return set;
  }, [selected, view]);

  const matches = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (q.length < 2) return [];
    return view.nodes
      .filter((n) =>
        [n.label, n.id, n.answer ?? "", ...(n.authors ?? [])].some((s) => s.toLowerCase().includes(q)),
      )
      .slice(0, 8);
  }, [query, view]);

  const switchAudience = (a: Audience) => {
    setAudience(a);
    setSelected(null);
  };

  const node = selected ? byId.get(selected) ?? null : null;
  const papersShown = view.nodes.filter((n) => n.type === "paper").length;
  const hint =
    audience === "everyday"
      ? `Each large dot is a question; the small dots around it are studies that help answer it. ${papersShown} studies.`
      : `${LENSES.find((l) => l.id === lens)?.hint}. ${papersShown} papers shown.`;

  return (
    <div>
      <div role="tablist" aria-label="Who is reading" className="inline-flex rounded-sm border border-line p-1">
        {(
          [
            ["everyday", "Everyday questions"],
            ["academic", "For researchers"],
          ] as const
        ).map(([id, label]) => (
          <button
            key={id}
            type="button"
            role="tab"
            aria-selected={audience === id}
            onClick={() => switchAudience(id)}
            className={cn(
              "rounded-[3px] px-4 py-2 text-sm font-medium text-muted-foreground",
              "aria-selected:bg-brand aria-selected:text-white",
              TRANSITION,
              FOCUS,
            )}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_380px]">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            {audience === "academic" && (
              <>
                {LENSES.map((l) => (
                  <button key={l.id} type="button" aria-pressed={lens === l.id} onClick={() => setLens(l.id)} className={CHIP}>
                    {l.label}
                  </button>
                ))}
                <span className="mx-1 h-5 w-px bg-line" aria-hidden />
                <button type="button" aria-pressed={fullOnly} onClick={() => setFullOnly((v) => !v)} className={CHIP}>
                  Read in full only
                </button>
              </>
            )}
            <div className="ml-auto flex rounded-sm border border-line p-0.5" role="group" aria-label="View">
              {(["3d", "2d"] as const).map((m) => (
                <button
                  key={m}
                  type="button"
                  aria-pressed={mode === m}
                  onClick={() => setMode(m)}
                  className={cn(
                    "label-mono rounded-[3px] px-3 py-1 aria-pressed:bg-brand aria-pressed:text-white",
                    TRANSITION,
                    FOCUS,
                  )}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>
          <p className="mt-3 text-sm text-muted-foreground">
            {hint} {mode === "3d" ? "Drag to rotate, scroll to zoom," : "Drag to pan, scroll to zoom,"} click a
            dot for details.
          </p>

          <div
            ref={boxRef}
            className="relative mt-4 h-[62vh] min-h-[420px] overflow-hidden rounded-sm border border-line bg-[#fbfaf8]"
          >
            {size.width > 0 && (
              <GraphCanvas
                key={audience}
                data={view}
                mode={mode}
                width={size.width}
                height={size.height}
                selected={selected}
                neighbours={neighbours}
                onSelect={setSelected}
                colorOf={colorOf}
                tight={audience === "everyday"}
              />
            )}
            {audience === "academic" && (
              <ul className="pointer-events-none absolute bottom-3 left-3 flex max-w-[calc(100%-24px)] flex-wrap gap-x-4 gap-y-1 rounded-sm bg-white/85 px-3 py-2 backdrop-blur">
                {LEGEND.map((l) => (
                  <li key={l.label} className="flex items-center gap-1.5 text-xs text-muted-foreground">
                    <span className="size-2.5 rounded-full" style={{ background: l.color }} aria-hidden />
                    {l.label}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <aside className="flex min-w-0 flex-col gap-4">
          <div className="relative">
            <label htmlFor="map-search" className="label-mono">
              {audience === "everyday" ? "Search questions and studies" : "Find a paper, author or skill"}
            </label>
            <input
              id="map-search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={audience === "everyday" ? "e.g. budget, lie, persuade" : "e.g. SPIRAL, Zou, persuading"}
              className={cn("mt-2 w-full rounded-sm border border-line bg-background px-3 py-2 text-sm", FOCUS)}
            />
            {matches.length > 0 && (
              <ul className="absolute inset-x-0 top-full z-10 mt-1 rounded-sm border border-line bg-background shadow-lg">
                {matches.map((m) => (
                  <li key={m.id}>
                    <button
                      type="button"
                      onClick={() => {
                        setSelected(m.id);
                        setQuery("");
                      }}
                      className={cn("flex w-full items-start gap-2 px-3 py-2 text-left text-sm hover:bg-accent", FOCUS)}
                    >
                      <span className="mt-1.5 size-2 shrink-0 rounded-full" style={{ background: colorOf(m) }} />
                      <span className="line-clamp-2">{m.label}</span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="rounded-sm border border-line p-5 lg:max-h-[62vh] lg:overflow-y-auto">
            {audience === "everyday" ? (
              node?.type === "question" ? (
                <QuestionDetails node={node} items={plain.byQuestion.get(node.id) ?? []} colorOf={colorOf} onSelect={setSelected} />
              ) : node ? (
                <PlainPaper node={node} items={plain.byPaper.get(node.id) ?? []} colorOf={colorOf} onSelect={setSelected} />
              ) : (
                <QuestionList questions={questions} colorOf={colorOf} counts={plain.byQuestion} onSelect={setSelected} />
              )
            ) : node ? (
              <Details node={node} data={data} byId={byId} onSelect={setSelected} />
            ) : (
              <Intro data={data} />
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}

/* ---------- everyday view ---------- */

function QuestionList({
  questions,
  counts,
  colorOf,
  onSelect,
}: {
  questions: GraphNode[];
  counts: Map<string, unknown[]>;
  colorOf: (n: GraphNode) => string;
  onSelect: (id: string) => void;
}) {
  return (
    <div>
      <p className="label-mono">Start with a question</p>
      <p className="mt-2 text-sm text-muted-foreground">
        AI agents are starting to bargain, shop and negotiate for people. Pick a question to see what
        research has found so far, in plain words.
      </p>
      <ul className="mt-4 flex flex-col">
        {questions.map((q) => (
          <li key={q.id} className="border-t border-line">
            <button
              type="button"
              onClick={() => onSelect(q.id)}
              className={cn("group flex w-full items-start gap-3 py-3 text-left", FOCUS)}
            >
              <span className="mt-1.5 size-2.5 shrink-0 rounded-full" style={{ background: colorOf(q) }} />
              <span className="flex-1">
                <span className="block font-medium group-hover:text-brand">{q.label}</span>
                <span className="text-xs text-muted-foreground">{counts.get(q.id)?.length ?? 0} studies</span>
              </span>
              <span aria-hidden className="text-muted-foreground group-hover:text-brand">
                →
              </span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

function QuestionDetails({
  node,
  items,
  colorOf,
  onSelect,
}: {
  node: GraphNode;
  items: { paper: GraphNode; plain: string }[];
  colorOf: (n: GraphNode) => string;
  onSelect: (id: string | null) => void;
}) {
  return (
    <div>
      <BackRow label="All questions" onBack={() => onSelect(null)} />
      <h3 className="display-title mt-3 text-2xl" style={{ color: colorOf(node) }}>
        {node.label}
      </h3>
      <p className="label-mono mt-5">Short answer</p>
      <p className="mt-2 text-[15px] leading-relaxed">{node.answer}</p>
      <p className="label-mono mt-6">What the studies found</p>
      <ul className="mt-2 flex flex-col">
        {items.map(({ paper, plain }) => (
          <li key={paper.id} className="border-t border-line py-3">
            <p className="text-sm leading-relaxed">{plain}</p>
            <button
              type="button"
              onClick={() => onSelect(paper.id)}
              className={cn("mt-1 text-left text-xs text-muted-foreground hover:text-brand", FOCUS)}
            >
              {shortCite(paper)} →
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

function PlainPaper({
  node,
  items,
  colorOf,
  onSelect,
}: {
  node: GraphNode;
  items: { question: GraphNode; plain: string }[];
  colorOf: (n: GraphNode) => string;
  onSelect: (id: string | null) => void;
}) {
  return (
    <div>
      <BackRow label="All questions" onBack={() => onSelect(null)} />
      <p className="label-mono mt-3">A study · {shortCite(node)}</p>
      <h3 className="display-title mt-2 text-xl">{node.label}</h3>
      {items.map(({ question, plain }) => (
        <div key={question.id} className="mt-5 border-t border-line pt-3">
          <button
            type="button"
            onClick={() => onSelect(question.id)}
            className={cn("text-left text-sm font-medium hover:underline", FOCUS)}
            style={{ color: colorOf(question) }}
          >
            {question.label}
          </button>
          <p className="mt-2 text-sm leading-relaxed">{plain}</p>
        </div>
      ))}
      <details className="mt-5 border-t border-line pt-3 text-sm">
        <summary className={cn("label-mono cursor-pointer hover:text-brand", FOCUS)}>Technical summary</summary>
        {node.question && <p className="mt-3 text-muted-foreground">{node.question}</p>}
        <PaperLinks node={node} />
      </details>
    </div>
  );
}

function BackRow({ label, onBack }: { label: string; onBack: () => void }) {
  return (
    <button type="button" onClick={onBack} className={cn("label-mono hover:text-brand", FOCUS)}>
      ← {label}
    </button>
  );
}

function shortCite(p: GraphNode) {
  const first = p.authors?.[0]?.split(" ").at(-1) ?? "";
  return `${first}${(p.authors?.length ?? 0) > 1 ? " et al." : ""}, ${p.year}`;
}

/* ---------- researcher view ---------- */

function Intro({ data }: { data: GraphData }) {
  const papers = data.nodes.filter((n) => n.type === "paper");
  const full = papers.filter((n) => n.read === "full").length;
  const benchmarks = papers.filter((n) => n.benchmark).length;
  const transfer = papers.filter((n) => n.transfer).length;
  return (
    <div>
      <p className="label-mono">How to read the map</p>
      <p className="mt-3 text-sm text-muted-foreground">
        Each dot is a paper on LLM agents in social and strategic settings. Large labelled dots are
        the social skills, topics and researchers they connect to. Lines between papers are
        references in the reading notes.
      </p>
      <dl className="mt-5 grid grid-cols-2 gap-4">
        {[
          [papers.length, "papers"],
          [full, "read in full"],
          [benchmarks, "benchmarks"],
          [transfer, "measure transfer"],
        ].map(([n, label]) => (
          <div key={label} className="border-t border-line pt-2">
            <dt className="label-mono">{label}</dt>
            <dd className="display-title mt-1 text-3xl">{n}</dd>
          </div>
        ))}
      </dl>
      <p className="mt-5 text-sm text-muted-foreground">
        The orange dots are the few studies that test whether training one social skill carries
        over to others, the open question this map was built around.
      </p>
    </div>
  );
}

function Details({
  node,
  data,
  byId,
  onSelect,
}: {
  node: GraphNode;
  data: GraphData;
  byId: Map<string, GraphNode>;
  onSelect: (id: string | null) => void;
}) {
  const related = data.links
    .filter((l) => l.kind !== "question" && (endId(l.source) === node.id || endId(l.target) === node.id))
    .map((l) => byId.get(endId(l.source) === node.id ? endId(l.target) : endId(l.source)))
    .filter((n): n is GraphNode => !!n && (node.type === "paper" ? n.type === "paper" : true))
    .sort((a, b) => (b.year ?? 0) - (a.year ?? 0));

  const kind = node.type === "paper" ? (node.benchmark ? "Benchmark" : "Study") : node.type;

  return (
    <div>
      <div className="flex items-center justify-between gap-2">
        <p className="label-mono" style={{ color: nodeColor(node) }}>
          {kind}
          {node.year ? ` · ${node.year}` : ""}
        </p>
        <button type="button" onClick={() => onSelect(null)} className={cn("label-mono hover:text-brand", FOCUS)}>
          Close
        </button>
      </div>
      <h3 className="display-title mt-2 text-xl">{node.label}</h3>
      {node.place && <p className="mt-1 text-sm text-muted-foreground">{node.place}</p>}

      {node.type === "paper" && (
        <>
          <p className="mt-2 text-sm text-muted-foreground">
            {node.authors?.slice(0, 4).join(", ")}
            {(node.authors?.length ?? 0) > 4 ? " et al." : ""}
          </p>
          <div className="mt-3 flex flex-wrap gap-1.5">
            <Tag strong={node.read === "full"}>{READ_LABEL[node.read ?? "unverified"]}</Tag>
            {node.skills?.map((s) => (
              <Tag key={s}>{byId.get(`skill:${s}`)?.label ?? s}</Tag>
            ))}
            {node.training?.map((t) => (
              <Tag key={t}>trains: {t}</Tag>
            ))}
            {node.transfer && <Tag accent>measures transfer</Tag>}
          </div>
          {node.question && (
            <Block label="Question">
              <p>{node.question}</p>
            </Block>
          )}
          {node.findings && node.findings.length > 0 && (
            <Block label="Key findings">
              <ul className="flex list-disc flex-col gap-2 pl-4">
                {node.findings.map((f, i) => (
                  <li key={i}>{f}</li>
                ))}
              </ul>
            </Block>
          )}
          {node.map?.["Scoring"] && (
            <Block label="Scoring">
              <p>{node.map["Scoring"]}</p>
            </Block>
          )}
          <PaperLinks node={node} />
        </>
      )}

      {related.length > 0 && (
        <Block label={node.type === "paper" ? "Connected papers" : `${related.length} papers`}>
          <ul className="flex flex-col">
            {related.map((r) => (
              <li key={r.id}>
                <button
                  type="button"
                  onClick={() => onSelect(r.id)}
                  className={cn("flex w-full items-start gap-2 rounded-sm py-1.5 text-left hover:text-brand", FOCUS)}
                >
                  <span className="mt-1.5 size-2 shrink-0 rounded-full" style={{ background: nodeColor(r) }} />
                  <span className="line-clamp-2">{r.label}</span>
                </button>
              </li>
            ))}
          </ul>
        </Block>
      )}
    </div>
  );
}

function PaperLinks({ node }: { node: GraphNode }) {
  return (
    <div className="mt-4 flex flex-wrap gap-x-4 gap-y-1 text-sm">
      <a href={`${REPO}/${node.id}.md`} target="_blank" rel="noreferrer" className={LINK}>
        Full note
      </a>
      {node.arxiv && (
        <a href={`https://arxiv.org/abs/${node.arxiv}`} target="_blank" rel="noreferrer" className={LINK}>
          Paper (arXiv)
        </a>
      )}
      {node.code?.startsWith("http") && (
        <a href={node.code.split(" ")[0]} target="_blank" rel="noreferrer" className={LINK}>
          Code
        </a>
      )}
    </div>
  );
}

function Block({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="mt-5 border-t border-line pt-3 text-sm">
      <p className="label-mono mb-2">{label}</p>
      {children}
    </div>
  );
}

function Tag({ children, strong, accent }: { children: React.ReactNode; strong?: boolean; accent?: boolean }) {
  return (
    <span
      className={cn(
        "rounded-sm border px-2 py-0.5 text-xs",
        accent ? "border-[#c2410c] text-[#c2410c]" : strong ? "border-brand text-brand" : "border-line text-muted-foreground",
      )}
    >
      {children}
    </span>
  );
}
