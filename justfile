dev:
    scripts/start.sh

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
