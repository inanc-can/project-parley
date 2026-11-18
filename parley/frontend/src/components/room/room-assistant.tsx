"use client";

import {
  AssistantRuntimeProvider,
  AuiConfig,
  Suggestions,
  useLocalRuntime,
  type ChatModelAdapter,
  type ThreadMessage,
} from "@assistant-ui/react";
import { Sparkles, X } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { Thread } from "@/components/assistant-ui/elements/thread.aui";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import type { ChatMessage, RoomView } from "@/lib/types";

// A chat in a column on the right of the room, built on assistant-ui. The assistant acts as you:
// it can edit the game, take seats, set up your agents, start matches and read results (see
// api/assistant.py). Each of its steps shows as text plus the actions it ran, as tool calls.

const SUGGESTIONS = [
  "Set up a used-car sale where I play both sides and run it 4 times",
  "Make my agent anchor high and my second agent friendly",
  "How did the last match go?",
];

/** A thread message as the assistant's history sees it; its actions become a short note. */
function toChatMessage(m: ThreadMessage): ChatMessage | null {
  if (m.role !== "user" && m.role !== "assistant") return null;
  const text = m.content.flatMap((p) => (p.type === "text" ? [p.text] : [])).join("\n");
  const did = m.content.flatMap((p) => (p.type === "tool-call" ? [`${p.toolName}${p.isError ? " (failed)" : ""}`] : []));
  const content = did.length ? `${text}\n[did: ${did.join(", ")}]` : text;
  return content.trim() ? { role: m.role, content } : null;
}

type Part =
  | { type: "text"; text: string }
  | { type: "reasoning"; text: string }
  | {
      type: "tool-call";
      toolCallId: string;
      toolName: string;
      args: Record<string, never>;
      argsText: string;
      result?: unknown;
      isError?: boolean;
    };

function roomAdapter(roomId: string, onChange: () => void): ChatModelAdapter {
  return {
    // Yields the growing answer after every event, so the trace shows while the assistant works:
    // a running action appears at once and gets its result when it finishes.
    async *run({ messages, abortSignal }) {
      const history = messages.map(toChatMessage).filter((m): m is ChatMessage => m !== null);
      const parts: Part[] = [];
      let rounds = 0;
      try {
        for await (const e of api.assistantStream(roomId, history, abortSignal)) {
          if (e.type === "thinking") {
            // The model is working (often tens of seconds): show that until its reply arrives.
            const text = rounds++ === 0 ? "Thinking…" : "Reading the results and planning the next step…";
            yield { content: [...parts, { type: "reasoning" as const, text }] };
            continue;
          }
          if (e.type === "error") throw new Error(e.message);
          if (e.type === "message") parts.push({ type: "text", text: e.text });
          else if (e.type === "action")
            parts.push({
              type: "tool-call",
              toolCallId: `call-${e.id}`,
              toolName: e.tool,
              args: e.args as Record<string, never>,
              argsText: JSON.stringify(e.args),
            });
          else {
            const i = parts.findIndex((p) => p.type === "tool-call" && p.toolCallId === `call-${e.id}`);
            if (i >= 0) parts[i] = { ...(parts[i] as Extract<Part, { type: "tool-call" }>), result: e.result, isError: !e.ok };
            onChange(); // an action finished: show its effect on the map right away
          }
          yield { content: [...parts] };
        }
      } finally {
        onChange();
      }
    },
  };
}

const OPEN_KEY = "parley:assistant-open";
const WIDE = "(min-width: 1024px)";

/** Whether the assistant column is open: remembered per browser, open by default on wide screens. */
export function useAssistantOpen(): [boolean, (open: boolean) => void] {
  const [open, setOpen] = useState(() => {
    try {
      const saved = localStorage.getItem(OPEN_KEY);
      if (saved !== null) return saved === "1";
    } catch {
      /* storage unavailable */
    }
    return typeof window !== "undefined" && window.matchMedia(WIDE).matches;
  });
  const set = (next: boolean) => {
    setOpen(next);
    try {
      localStorage.setItem(OPEN_KEY, next ? "1" : "0");
    } catch {
      /* storage unavailable */
    }
  };
  return [open, set];
}

export function RoomAssistant({
  room,
  onChange,
  open,
  onClose,
}: {
  room: RoomView;
  onChange: () => void;
  open: boolean;
  onClose: () => void;
}) {
  const adapter = useMemo(() => roomAdapter(room.id, onChange), [room.id, onChange]);
  const runtime = useLocalRuntime(adapter);
  const config = useMemo(() => AuiConfig({ suggestions: Suggestions(SUGGESTIONS) }), []);

  // Tell page-level overlays (the map inspector) how much room the column takes on the right.
  useEffect(() => {
    const root = document.documentElement;
    const apply = () => root.style.setProperty("--assistant-w", open && window.matchMedia(WIDE).matches ? "26rem" : "0px");
    apply();
    const mq = window.matchMedia(WIDE);
    mq.addEventListener("change", apply);
    return () => {
      mq.removeEventListener("change", apply);
      root.style.removeProperty("--assistant-w");
    };
  }, [open]);

  return (
    <AssistantRuntimeProvider runtime={runtime} config={config}>
      {/* A column beside the room content on wide screens, full screen on narrow ones. Kept
          mounted while closed so the conversation survives closing it. */}
      <aside
        className={`${open ? "flex" : "hidden"} fixed inset-0 z-50 flex-col bg-background lg:sticky lg:top-14 lg:z-10 lg:h-[calc(100svh-3.5rem)] lg:w-[26rem] lg:shrink-0 lg:border-l lg:border-line`}
        aria-label="Assistant"
      >
        <div className="flex h-14 shrink-0 items-center gap-2 border-b border-line px-4">
          <Sparkles className="size-4 text-brand" />
          <span className="label-mono text-foreground">Assistant</span>
          <span className="truncate text-xs text-muted-foreground">acts as you in this room</span>
          <Button size="icon" variant="ghost" className="ml-auto" aria-label="Close assistant" onClick={onClose}>
            <X />
          </Button>
        </div>
        <div className="min-h-0 flex-1">
          <Thread autoFocus={false} components={{ Welcome }} />
        </div>
      </aside>
    </AssistantRuntimeProvider>
  );
}

function Welcome() {
  return (
    <div className="mb-4 flex flex-col gap-1 px-2">
      <p className="display-title text-2xl">What should we set up?</p>
      <p className="text-sm text-muted-foreground">
        The assistant acts as you in this room: it edits the game, sets up your agents, takes the
        open seat and starts matches.
      </p>
    </div>
  );
}
