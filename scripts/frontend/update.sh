#!/usr/bin/bash
set -euo pipefail

pushd "frontend" > /dev/null

bun update

popd > /dev/null
