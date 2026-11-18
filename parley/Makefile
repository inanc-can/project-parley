# macOS can flag .venv files "hidden", and Python then skips the editable-install .pth;
# putting src on the path directly makes that irrelevant.
export PYTHONPATH := src

# Start the API (port 8000) and the web app (port 3000) together. Ctrl-C stops both.
dev:
	trap "kill 0" EXIT; uv run parley serve & (cd frontend && pnpm dev) & wait

test:
	uv run pytest -q
	cd frontend && pnpm lint && pnpm exec tsc --noEmit

.PHONY: dev test
