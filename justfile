mod alembic 'scripts/alembic'
mod backend 'scripts/backend'
mod frontend 'scripts/frontend'
mod init_commands 'scripts/init'

build: frontend::build

dev: backend::start

init: stop start init_commands::database init_commands::vault alembic::upgrade

install: backend::install frontend::install

lint: backend::lint frontend::lint

start:
    docker compose up -d --wait

stop:
    docker compose down -v

update: backend::update frontend::update
