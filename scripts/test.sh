#!/usr/bin/bash
set -euo pipefail

uv run pytest "${@}"
