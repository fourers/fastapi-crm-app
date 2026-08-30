export REQUESTS_CA_BUNDLE := "/etc/ssl/certs/ca-certificates.crt"
export SSL_CERT_FILE := "/etc/ssl/certs/ca-certificates.crt"

[no-cd]
install:
    @echo "Installing backend..."
    @scripts/backend/install.sh

[no-cd]
lint:
    @echo "Linting backend..."
    @scripts/backend/lint.sh

[no-cd]
start:
    @scripts/backend/start.sh

[no-cd]
update:
    @echo "Updating backend..."
    @scripts/backend/update.sh
