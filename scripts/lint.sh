#!/usr/bin/bash
set -euo pipefail

uv run ty check .

uv run ruff check --fix .
uv run ruff format .
