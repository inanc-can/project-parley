# Parley — notes for Claude

Research platform where LLM agents negotiate and play games; the goal is publishable
findings on how models, prompts and techniques change behaviour. Setup, usage and the code
layout are in `README.md`; the original design plan is
`~/.claude/plans/i-want-to-build-hashed-toucan.md`.

## Commands

- `make test` — pytest + frontend lint + `tsc` (all must pass before committing)
- `make dev` — API on :8000 + web app on :3000. The API does **not** auto-reload: restart
  it after backend changes. Next serves `/api/*` by proxying to the API.
- `uv run parley sim` — interactive terminal simulation (needs a TTY; the user runs it).
  `uv run parley run <config.json> --show-turns` is the scriptable equivalent.
- `uv run ruff check src tests && uv run ruff format src tests` — line length 100.

## Working conventions

- Ask design-shaping questions **one at a time**, state assumptions, and recommend an option.
  Use visual-explainer pages for non-trivial plans.
- Keep reproducibility first-class: every episode stores spec, seats, seeds, version.
- `litellm` is a slow import: import it lazily inside functions (see `llm/client.py`,
  `matches/runner.py`), never at module level.
- `frontend/AGENTS.md`: this Next.js version differs from training data; read its bundled
  docs before Next-specific changes. UI uses shadcn on Base UI (not Radix).
- Styling follows the user's "editorial" style: serif display titles (Butler → Fraunces),
  Schibsted Grotesk body, IBM Plex Mono uppercase labels, navy `#1f2d5c` accent, warm-grey
  `#e5e2db` hairlines, 0.25rem radius. Tokens live in `frontend/src/app/globals.css`.

## How the match pipeline handles failure (keep these properties)

- LLM client (`llm/client.py`) retries transient provider errors with backoff (2/5/10/20 s).
- Runner retries a failed episode (`MatchConfig.episode_attempts`, default 3), then records it
  with `end_reason="error"` and `EpisodeRecord.error`; other episodes continue. Setup errors
  (auth, unknown/gated model) stop the match. Episodes are saved as each one ends.
- Bad agent replies are re-prompted 3 times; the attempt number is in the feedback so a
  cached bad reply isn't replayed. Forfeits keep the rejected replies in
  `outcome.forfeit_attempts`.
- The SSE stream must send `Cache-Control: no-transform` (else Next gzips and buffers it).
- `Store` shares one SQLite connection across threads behind a lock.

## Known provider behaviour (Featherless, the provider until 2026-10-17)

Overload → HTTP 200 with an error object appended ("Extra data"); retry fixes it.
Qwen2.5-14B sometimes emits degenerate `{"!!!!…` (counts as the agent's forfeit — a
provider artefact) and often closes its JSON early (the parser repairs this). Models
regularly ignore their own reservation price (e.g. buyers accepting above their limit).

## Testing the web app

The Claude in Chrome extension has been unreliable. Fallback that works: headless Chrome
with `--remote-debugging-port` driven over CDP from a small Node script, one browser context
per player (separate localStorage tokens). Shell commands use zsh: no `timeout` binary.

## Status (2026-10-17)

Done: all 8 plan steps; editorial styling; full two-person match verified in the UI (live
view, results, toasts); the reliability fixes above; `parley sim` CLI mode. Then: shadcn app
sidebar; room **Map** tab (React Flow: agents as nodes, the game as the edge, an inspector panel
for seats/game, a start bar); **Assign me** (one person takes the open seat, `Participant.owner`,
`seat_of` on seat/ready); the room **assistant** (`api/assistant.py`): a chat column built on
assistant-ui that acts with the person's token through JSON actions, streamed as NDJSON.

Inference moved to OpenRouter (`OPENROUTER_API_KEY`) on 2026-10-17; Llama-3.1-8B and Qwen2.5-7B
replace Hermes-3-8B and Qwen2.5-14B, which OpenRouter lacks. Stored rooms were migrated (backup:
`.parley/parley.before-openrouter.sqlite`); Featherless still works via `PARLEY_MODELS`.

Assistant notes: Qwen2.5-72B with JSON mode; falls back to phi-4 when rate limited
(`PARLEY_ASSISTANT_MODEL` / `_FALLBACK_MODEL`). Its replies are not cached; unusable replies are
logged. `edit_game` refuses surplus games whose roles lost their `reservation`.
`next.config.ts` raises `proxyTimeout` because answers take over a minute. Vendored
`src/components/assistant-ui/` is excluded from lint; update it with `assistant-ui add`.
Run the API with `PYTHONPATH=src` (as the Makefile does) if `No module named 'parley'`.

Redesign (2026-10-18, stage 1 of 6 done): the `alternating` protocol became `Conversation`
(`kind: "conversation"`). Natural turn-taking is the default: agents may pass (`{"type": "pass"}`
or an empty reply), follow up (`"follow_up": true`, at most `max_follow_ups` in a row) or walk
away; it ends on a deal, a walk-away, `silence` (everyone passes in a row), or a hidden safety cap
(`limit`, with `show_limit` false). `strict_alternation()` is the old setup and every template
uses it; specs saved as `alternating` load as strict. Later stages: seat memory/history and cost,
richer scenes, briefings, reruns, a harness builder (decisions in Claude's project memory).

Open / ideas, roughly in order:
1. Flag degenerate provider output separately from genuine forfeits.
2. Metric for offers/acceptances beyond the agent's own reservation value.
3. Match tab: while a match runs, the start form shows the viewer's own runs value.
4. Rooms with more than two agents and a game per connection (the map is ready for it).
5. Human playing a seat (needed for human baselines); study view comparing matches.
6. Persist map positions, the assistant chat and the sidebar's collapsed state.
7. Butler font files aren't in the repo; titles fall back to Fraunces.
