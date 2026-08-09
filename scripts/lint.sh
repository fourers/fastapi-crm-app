#!/usr/bin/bash
set -euo pipefail

uv run ty check .

uv run ruff check --fix .
uv run ruff format .

pushd "frontend" > /dev/null

bun run lint:fix
bun run format
bun run typecheck

popd > /dev/null
