#!/usr/bin/bash
set -euo pipefail

pushd "frontend" > /dev/null

bun run build:dev

popd > /dev/null
