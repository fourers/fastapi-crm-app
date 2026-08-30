[no-cd]
[arg('FLAG', pattern='|--dev')]
build FLAG='':
    @scripts/frontend/build.sh {{ if FLAG == "--dev" { "true" } else { "false" } }}

[no-cd]
install:
    @scripts/frontend/install.sh

[no-cd]
lint:
    @scripts/frontend/lint.sh

[no-cd]
update:
    @scripts/frontend/update.sh

[no-cd]
watch:
    @scripts/frontend/watch.sh
