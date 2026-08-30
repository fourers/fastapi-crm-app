#!/usr/bin/bash
set -euo pipefail

pushd "frontend" > /dev/null

bun run lint:fix
bun run format
bun run typecheck

popd > /dev/null
