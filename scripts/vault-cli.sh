#!/bin/bash
set -euo pipefail

docker compose exec -it vault vault "${@}"
