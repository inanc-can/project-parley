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

## Known provider behaviour (Featherless)

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
view, results, toasts); the reliability fixes above; `parley sim` CLI mode.

Open / ideas, roughly in order:
1. Flag degenerate provider output separately from genuine forfeits.
2. Metric for offers/acceptances beyond the agent's own reservation value.
3. Match tab: while a match runs, the start form shows the viewer's own runs value.
4. Human playing a seat (needed for human baselines); study view comparing matches.
5. Butler font files aren't in the repo; titles fall back to Fraunces.
