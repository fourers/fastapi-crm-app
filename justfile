mod alembic 'scripts/alembic'
mod backend 'scripts/backend'
mod docker 'scripts/docker.just'
mod examples 'examples'
mod frontend 'scripts/frontend'
mod init_commands 'scripts/init'

default: install

build: frontend::build

build_docker: docker::build

dev: backend::start

init: stop start init_commands::database init_commands::vault alembic::upgrade

install: backend::install frontend::install

lint: backend::lint frontend::lint

shellcheck:
    @docker run --rm -v ".:/mnt" koalaman/shellcheck:stable $(find scripts -type f -name '*.sh' -printf '/mnt/%p\n')

start:
    docker compose up -d --wait

stop:
    docker compose down -v

update: backend::update frontend::update
