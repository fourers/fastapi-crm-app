#!/usr/bin/bash
set -euo pipefail

pushd "frontend" > /dev/null

bun update --lockfile-only

popd > /dev/null
