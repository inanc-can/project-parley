/** Shape of research/generated/graph.json (built by research/scripts/build.py). */

export type NodeType = "paper" | "topic" | "skill" | "person" | "question";

export type GraphNode = {
  id: string;
  type: NodeType;
  label: string;
  // papers only
  authors?: string[];
  year?: number;
  venue?: string | null;
  arxiv?: string | null;
  url?: string | null;
  code?: string | null;
  read?: "full" | "partial" | "abstract" | "unverified";
  relevance?: "high" | "medium" | "low";
  topics?: string[];
  benchmark?: boolean;
  skills?: string[];
  training?: string[];
  transfer?: boolean;
  question?: string;
  findings?: string[];
  map?: Record<string, string>;
  /** benchmarks only: coarse classification from the Map fields */
  eval?: EvalClass | null;
  // people only
  place?: string;
  // everyday questions only
  short?: string;
  answer?: string;
  // set by the force layout
  x?: number;
  y?: number;
  z?: number;
};

export type EvalClass = {
  scoring: "rules" | "mixed" | "judge" | "other";
  opponents: string[];
  agents: "1" | "2" | "many";
  tests: "capability" | "propensity" | "both" | "not recorded";
  code: string | null;
};

export type LinkKind = "topic" | "skill" | "cites" | "person" | "question";

export type GraphLink = {
  source: string | GraphNode;
  target: string | GraphNode;
  kind: LinkKind;
  /** question links: what this paper found, in plain words */
  plain?: string;
};

export type GraphData = { nodes: GraphNode[]; links: GraphLink[] };

export const endId = (end: string | GraphNode) => (typeof end === "string" ? end : end.id);
