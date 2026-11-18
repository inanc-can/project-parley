"use client";

import { useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import type { Turn } from "@/lib/types";

function actionLabel(t: Turn) {
  if (!t.action) return null;
  const terms = Object.entries(t.action.terms ?? {});
  return terms.length ? `${t.action.type} ${terms.map(([k, v]) => `${k}=${v}`).join(", ")}` : t.action.type;
}

// Chat-style transcript. Private reasoning appears only where the API included it.
export function Transcript({ turns, seatOf }: { turns: Turn[]; seatOf?: Record<string, string> }) {
  const [showReasoning, setShowReasoning] = useState(false);
  const roles = [...new Set(turns.map((t) => t.role))];
  const hasPrivate = turns.some((t) => t.reasoning || t.deliberation);

  return (
    <div className="flex flex-col gap-2">
      {hasPrivate && (
        <Label className="flex items-center gap-2 self-end text-sm">
          <Switch checked={showReasoning} onCheckedChange={setShowReasoning} />
          Show private reasoning
        </Label>
      )}
      {turns.length === 0 && <p className="text-muted-foreground text-sm">No messages yet.</p>}
      {turns.map((t, i) => {
        const right = roles.indexOf(t.role) % 2 === 1;
        if (t.action?.type === "pass")
          return (
            <p key={i} className={`text-muted-foreground px-3 text-xs italic ${right ? "text-right" : ""}`}>
              {t.role}
              {seatOf?.[t.role] && ` (${seatOf[t.role]})`} stays silent
              {showReasoning && t.reasoning && <span className="block">{t.reasoning}</span>}
            </p>
          );
        return (
          <div key={i} className={`flex ${right ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-[80%] rounded-lg border px-3 py-2 ${right ? "bg-muted" : "bg-background"}`}>
              <div className="text-muted-foreground mb-1 flex flex-wrap items-center gap-2 text-xs">
                <span className="font-medium">
                  {t.role}
                  {seatOf?.[t.role] && ` (${seatOf[t.role]})`}
                </span>
                {t.round != null && (
                  <span>
                    round {t.round} · {t.phase}
                  </span>
                )}
                {!!t.retries && <span>{t.retries} retr{t.retries === 1 ? "y" : "ies"}</span>}
              </div>
              {t.message && <p className="text-sm whitespace-pre-wrap">{t.message}</p>}
              {t.action && (
                <Badge variant="outline" className="mt-1 font-mono">
                  {actionLabel(t)}
                </Badge>
              )}
              {showReasoning && t.reasoning && (
                <p className="text-muted-foreground mt-2 border-t pt-2 text-xs italic">{t.reasoning}</p>
              )}
              {showReasoning && t.deliberation && (
                <pre className="text-muted-foreground mt-2 border-t pt-2 text-xs whitespace-pre-wrap">
                  {JSON.stringify(t.deliberation, null, 1)}
                </pre>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
