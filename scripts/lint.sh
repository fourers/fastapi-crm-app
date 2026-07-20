#!/usr/bin/bash
set -euo pipefail

ty check .

ruff check --fix .
ruff format .
