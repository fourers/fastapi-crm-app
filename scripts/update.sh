#!/usr/bin/bash
set -euo pipefail

uv sync --upgrade

pushd "frontend" > /dev/null

bun update

popd > /dev/null
