default: install

[no-cd]
[arg('FLAG', pattern='|--dev')]
build FLAG='':
    @echo "Building frontend..."
    @scripts/frontend/build.sh {{ if FLAG == "--dev" { "true" } else { "false" } }}

[no-cd]
install:
    @echo "Installing frontend..."
    @scripts/frontend/install.sh

[no-cd]
lint:
    @echo "Linting frontend..."
    @scripts/frontend/lint.sh

[no-cd]
update:
    @echo "Updating frontend..."
    @scripts/frontend/update.sh

[no-cd]
watch:
    @scripts/frontend/watch.sh
