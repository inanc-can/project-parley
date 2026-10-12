"use client";

import { useEffect, useState } from "react";

import { SimpleSelect } from "@/components/simple-select";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { api } from "@/lib/api";
import type { MatchListItem, MatchResult, MatchSummary, RoomView } from "@/lib/types";

import { Transcript } from "./transcript";

const fmt = (n: number) => (Number.isInteger(n) ? String(n) : n.toFixed(2));

export function ResultsPanel({ room }: { room: RoomView }) {
  const [list, setList] = useState<MatchListItem[]>([]);
  const [matchId, setMatchId] = useState<string | null>(null);
  const [result, setResult] = useState<MatchResult | null>(null);
  const [episode, setEpisode] = useState(0);
  const doneCount = room.match_ids.length - room.running.length;

  useEffect(() => {
    api.matches(room.id).then((l) => {
      setList(l);
      setMatchId((cur) => cur ?? l.find((m) => m.status === "done")?.id ?? null);
    });
  }, [room.id, doneCount]);

  useEffect(() => {
    if (!matchId) return;
    api.match(room.id, matchId).then(setResult);
  }, [room.id, matchId]);

  if (!list.length) return <p className="text-muted-foreground">No matches yet.</p>;

  const summary = result && "episodes" in result.summary ? (result.summary as MatchSummary) : null;
  const ep = result?.episodes[episode];

  return (
    <div className="flex flex-col gap-4">
      <SimpleSelect
        value={matchId ?? ""}
        onChange={(id) => {
          setMatchId(id);
          setEpisode(0);
        }}
        options={list.map((m) => ({
          value: m.id,
          label: `${m.created_at.slice(0, 16).replace("T", " ")} · ${m.title} · ${m.runs} runs · ${m.status}`,
        }))}
      />

      {summary && (
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Summary</CardTitle>
              <CardDescription>{summary.episodes} episodes, averaged over the roles each person played.</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Person</TableHead>
                    <TableHead className="text-right">Mean payoff</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {Object.entries(summary.mean_payoff_by_seat).map(([seat, v]) => (
                    <TableRow key={seat}>
                      <TableCell>{seat}</TableCell>
                      <TableCell className="text-right">{fmt(v)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              <div className="mt-3 flex flex-wrap gap-2">
                {Object.entries(summary.end_reasons).map(([k, v]) => (
                  <Badge key={k} variant="secondary">
                    {k}: {v}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Metrics</CardTitle>
              <CardDescription>Means across episodes.</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableBody>
                  {Object.entries(summary.metrics).map(([k, v]) => (
                    <TableRow key={k}>
                      <TableCell className="font-mono text-xs">{k}</TableCell>
                      <TableCell className="text-right">{fmt(v)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
          {Object.keys(summary.reference).length > 0 && (
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>Theory baselines</CardTitle>
                <CardDescription>What game theory predicts for this game, to compare against.</CardDescription>
              </CardHeader>
              <CardContent>
                <pre className="bg-muted max-h-64 overflow-auto rounded p-3 text-xs">
                  {JSON.stringify(
                    Object.fromEntries(Object.entries(summary.reference).filter(([k]) => k !== "pareto_frontier")),
                    null,
                    2,
                  )}
                </pre>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {result && result.episodes.length > 0 && ep && (
        <Card>
          <CardHeader>
            <CardTitle>Episodes</CardTitle>
            <div className="flex flex-wrap gap-2 pt-2">
              {result.episodes.map((e, i) => (
                <Button key={i} size="sm" variant={i === episode ? "default" : "outline"} onClick={() => setEpisode(i)}>
                  #{i + 1}
                </Button>
              ))}
            </div>
          </CardHeader>
          <CardContent className="grid gap-6 md:grid-cols-3">
            <div className="md:col-span-2">
              <Transcript turns={ep.turns} seatOf={ep.assignment} />
            </div>
            <div className="flex flex-col gap-3 text-sm">
              <div>
                <p className="font-medium">Outcome</p>
                <p>{ep.outcome.end_reason}</p>
                {ep.outcome.deal && (
                  <p>
                    deal {JSON.stringify(ep.outcome.deal.terms)}
                    {ep.outcome.deal.source === "judge_extracted" && (
                      <Badge variant="outline" className="ml-2">
                        judge-extracted
                        {ep.outcome.deal.confidence != null && ` ${Math.round(ep.outcome.deal.confidence * 100)}%`}
                      </Badge>
                    )}
                  </p>
                )}
                <p>payoffs {JSON.stringify(ep.outcome.payoffs)}</p>
              </div>
              {ep.outcome.judge && (
                <div>
                  <p className="font-medium">Judge</p>
                  {ep.outcome.judge.error && <p className="text-destructive">{ep.outcome.judge.error}</p>}
                  {ep.outcome.judge.summary && <p className="text-muted-foreground">{ep.outcome.judge.summary}</p>}
                  {ep.outcome.judge.rubric &&
                    Object.entries(ep.outcome.judge.rubric).map(([role, scores]) => (
                      <p key={role} className="font-mono text-xs">
                        {role}: {Object.entries(scores).map(([k, v]) => `${k} ${v}`).join(", ")}
                      </p>
                    ))}
                </div>
              )}
              <div>
                <p className="font-medium">Agents</p>
                {Object.entries(ep.seats).map(([seat, cfg]) => (
                  <div key={seat} className="mt-1">
                    <p>{seat}</p>
                    {cfg ? (
                      <pre className="bg-muted overflow-auto rounded p-2 text-xs whitespace-pre-wrap">
                        {JSON.stringify(cfg, null, 1)}
                      </pre>
                    ) : (
                      <p className="text-muted-foreground text-xs">hidden by its owner</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
