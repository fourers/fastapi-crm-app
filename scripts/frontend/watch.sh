#!/usr/bin/bash
set -euo pipefail

pushd "frontend" > /dev/null

bun run build:watch

popd > /dev/null
