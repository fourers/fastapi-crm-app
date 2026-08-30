mod alembic 'scripts/alembic'
mod backend 'scripts/backend'
mod frontend 'scripts/frontend'

build: frontend::build

cli *ARGS:
    uv run examples/cli.py {{ARGS}}

dev: backend::start

init:
    scripts/init.sh

init_data:
    cd examples && uv run init_data.py

install: backend::install frontend::install

lint: backend::lint frontend::lint

start:
    docker compose up -d --wait

stop:
    docker compose down -v

test *ARGS:
    uv run pytest {{ARGS}}

update: backend::update frontend::update
