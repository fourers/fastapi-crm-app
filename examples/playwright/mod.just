set default-list := true

test *ARGS:
    uv run pytest {{ARGS}}
