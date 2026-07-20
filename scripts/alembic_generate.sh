#!/usr/bin/bash
set -euo pipefail

message="${1:-}"

if [[ -z "${message}" ]]; then
    echo "Usage: ${0} <message>"
    exit 1
fi

alembic revision --autogenerate -m "${message}"
