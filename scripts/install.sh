#!/usr/bin/bash
set -euo pipefail

uv sync

pushd "frontend" > /dev/null

bun install

popd > /dev/null
