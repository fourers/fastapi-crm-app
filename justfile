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

install:
    scripts/install.sh

lint:
    scripts/lint.sh

start:
    docker compose up -d --wait

stop:
    docker compose down -v

update:
    scripts/update.sh

watch:
    scripts/watch.sh
