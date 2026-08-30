#!/usr/bin/bash
set -euo pipefail

uv run ruff check --fix .
uv run ruff format .
uv run ty check .
