// Mirrors the pydantic models in src/parley (core/spec.py, core/types.py, matches/, api/rooms.py).

export type Role = { name: string; private_brief: string; private_values: Record<string, number> };
export type DealField = {
  name: string;
  type: "number" | "integer";
  min: number | null;
  max: number | null;
  description: string;
};

export type Scoring =
  | { kind: "surplus"; field: string; direction: Record<string, "up" | "down"> }
  | { kind: "valuations"; items: Record<string, number>; allocation_role: string }
  | { kind: "matrix"; payoffs: Record<string, number[]> }
  | { kind: "judge_only" };

export type Protocol =
  | { kind: "alternating"; max_messages: number; first: number; reject_ends: boolean }
  | {
      kind: "simultaneous_rounds";
      rounds: number;
      talk_messages: number;
      moves: string[];
      show_horizon: boolean;
    };

export type GameSpec = {
  title: string;
  shared_context: string;
  roles: Role[];
  deal_fields: DealField[];
  scoring: Scoring;
  protocol: Protocol;
  allowed_actions: Record<string, string[]> | null;
  runs: number;
  judge_rubric: string | null;
};

export type Seat =
  | { kind: "llm"; model: string; strategy: string; temperature: number }
  | {
      kind: "team";
      proposer_model: string;
      critic_model: string;
      decider_model: string | null;
      strategy: string;
      temperature: number;
    }
  | { kind: "scripted"; name: string; params: Record<string, unknown> };

export type RoomSettings = { allowed_models: string[]; judge_model: string | null; parallel: number };

export type RoomView = {
  id: string;
  me: { name: string; is_host: boolean; seat: Seat | null; ready: boolean; reveal: boolean };
  // Seats this person took with "Assign me"; they edit these like their own.
  controlled: { name: string; seat: Seat | null; ready: boolean; reveal: boolean }[];
  participants: {
    name: string;
    ready: boolean;
    has_seat: boolean;
    agreed: boolean;
    is_host: boolean;
    owner: string | null; // who controls this seat, when it was taken with "Assign me"
  }[];
  capacity: number;
  game: { version: number; spec: GameSpec; locked: boolean; edited_by: string | null };
  settings: RoomSettings;
  can_start: boolean;
  start_problems: string[];
  match_ids: string[];
  running: string[];
};

// The room assistant's chat history, as its endpoints take it.
export type ChatMessage = { role: "user" | "assistant"; content: string };
// What the assistant's stream sends while it works (see api/assistant.py `chat_events`).
export type AssistantEvent =
  | { type: "thinking" }
  | { type: "message"; text: string }
  | { type: "action"; id: number; tool: string; args: Record<string, unknown> }
  | { type: "result"; id: number; ok: boolean; result: unknown }
  | { type: "error"; message: string };

export type Action = { type: string; terms: Record<string, number> };
export type Turn = {
  role: string;
  message: string;
  action: Action | null;
  reasoning?: string | null;
  deliberation?: Record<string, unknown>[] | null;
  retries?: number;
  round: number | null;
  phase: "talk" | "move" | null;
};

export type Outcome = {
  end_reason: string;
  deal: { terms: Record<string, number>; source: "formal" | "judge_extracted"; confidence: number | null } | null;
  payoffs: Record<string, number>;
  forfeited_by: string | null;
  forfeit_attempts: { error: string; output: string }[];
  metrics: Record<string, number>;
  judge: {
    summary?: string;
    rubric?: Record<string, Record<string, number>>;
    evidence?: string[];
    error?: string;
  } | null;
};

export type Episode = {
  index: number;
  seed: number;
  assignment: Record<string, string>; // role -> seat (person)
  seats: Record<string, (Seat & { strategy_sha256?: string }) | null>;
  turns: Turn[];
  outcome: Outcome;
  attempts: number;
  error: string | null; // every attempt failed; outcome.end_reason is "error"
};

export type MatchSummary = {
  episodes: number;
  failed: number;
  mean_payoff_by_seat: Record<string, number>;
  end_reasons: Record<string, number>;
  metrics: Record<string, number>;
  reference: Record<string, unknown>;
};

export type MatchResult = { status: string | null; summary: MatchSummary | Record<string, never>; episodes: Episode[] };
export type MatchListItem = { id: string; status: string; created_at: string; title: string; runs: number };

export type MatchEvent =
  | { type: "match_start"; match_id: string; runs: number }
  | { type: "episode_start"; index: number; assignment: Record<string, string>; attempt: number }
  | { type: "turn"; index: number; turn: Turn }
  | { type: "episode_retry"; index: number; attempt: number; error: string }
  | { type: "episode_end"; index: number; outcome: Outcome; error: string | null }
  | { type: "match_end"; match_id: string }
  | { type: "error"; message: string };
