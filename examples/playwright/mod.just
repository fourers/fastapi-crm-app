set default-list := true

test *ARGS:
    uv run pytest {{ARGS}}

[no-cd]
codegen:
    #!/usr/bin/env bash
    set -euo pipefail
    source .env
    uv run playwright codegen --ignore-https-errors "${CLICK_CLI_APP_ENDPOINT}"
