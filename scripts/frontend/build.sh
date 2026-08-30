#!/usr/bin/bash
set -euo pipefail

is_dev="${1:-false}"

pushd "frontend" > /dev/null

if [[ "${is_dev}" == "true" ]]; then
  bun run build:dev
else
  bun run build
fi

popd > /dev/null
