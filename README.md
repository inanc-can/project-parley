# Parley

A research platform for AI agents that negotiate and play games: zero-sum, positive-sum,
negative-sum and mixed-motive. Two people agree on a game together, each privately builds
an agent (one LLM or a team), and the agents negotiate in free dialogue. Every episode is
logged with what's needed to reproduce it, scored from the deal and a judge LLM, and
compared with game-theory baselines.

## Setup

```sh
uv sync --extra analysis          # Python 3.12
cd frontend && pnpm install && cd ..
cp .env.example .env              # add FEATHERLESS_AI_API_KEY (or another provider's key)
```

## Run the web app

```sh
make dev        # API on :8000, web app on http://localhost:3000
```

Create a room and send the link to the other person. On your network, start the API with
`uv run parley serve --host 0.0.0.0` and share `http://<your-ip>:3000/room/<id>`.

1. **Game**: write the scenario (or start from a template). Both press *Agree* to lock it.
2. **My agent**: pick a model (from the host's list), write a strategy, optionally a team.
3. **Match**: run N episodes with roles swapped and watch them live.
4. **Results**: payoffs, judge ratings, theory baselines, transcripts. Each person decides
   whether their setup and reasoning are revealed.

Model names follow LiteLLM: `openrouter/<org>/<model>` (the default provider),
`featherless_ai/<model id>`, `anthropic/<model>`, `ollama/<model>`.
The host sets the allowed list in the Match tab, or with `PARLEY_MODELS` (comma-separated).

## Simulations in the terminal

```sh
uv run parley sim          # pick a game, set up both seats, choose runs; then watch it live
```

It ends with a summary (payoffs per seat, endings, metrics, theory baselines). The match is
stored like any other, and the setup is saved to `.parley/last_sim.json`, so
`uv run parley run .parley/last_sim.json --show-turns` reruns it exactly.

## Scripted studies (no UI)

```sh
uv run parley template buy_sell > match.json   # edit seats, runs, models
uv run parley run match.json
uv run parley matches
uv run parley export <match_id> --out analysis/<match_id>.jsonl
uv run parley baselines buy_sell
```

Then open `analysis/explore.ipynb` (payoffs by model and role with bootstrap CIs, metrics).

## Layout

| Path | What |
|---|---|
| `src/parley/core/` | `GameSpec`, conversation engine, protocols, scoring, theory baselines |
| `src/parley/agents/` | LLM agent (JSON turns + retries), team per seat, scripted baselines |
| `src/parley/judge.py` | judge LLM: rubric scores, extracts deals agreed only in words |
| `src/parley/matches/` | seats and the match runner (role swap, seeds, parallel episodes) |
| `src/parley/api/` | FastAPI: rooms, shared game, private seats, live stream (SSE) |
| `frontend/` | Next.js + shadcn/ui web app |
| `../research/` | separate repo: literature notes, papers, related code; never imported |

## Tests

```sh
make test       # pytest + frontend lint and type check
```

On macOS, if `uv run parley` says `No module named 'parley'`, macOS has flagged the venv's
`.pth` file as hidden: run `chflags -R nohidden .venv` (the Makefile works around it).
