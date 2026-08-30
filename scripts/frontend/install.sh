#!/usr/bin/bash
set -euo pipefail

pushd "frontend" > /dev/null

bun install

popd > /dev/null
