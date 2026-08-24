build:
    scripts/build.sh

build_dev:
    scripts/build_dev.sh

cli *ARGS:
    uv run examples/cli.py {{ARGS}}

dev:
    scripts/start.sh

format:
    scripts/format.sh

init:
    scripts/init.sh

init_data:
    cd examples && uv run init_data.py

install:
    scripts/install.sh

lint:
    scripts/lint.sh

start:
    docker compose up -d --wait

stop:
    docker compose down -v

test *ARGS:
    uv run pytest {{ARGS}}

update:
    scripts/update.sh

watch:
    scripts/watch.sh
