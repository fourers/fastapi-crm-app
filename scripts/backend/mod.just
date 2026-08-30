export REQUESTS_CA_BUNDLE := "/etc/ssl/certs/ca-certificates.crt"
export SSL_CERT_FILE := "/etc/ssl/certs/ca-certificates.crt"

[no-cd]
install:
    @scripts/backend/install.sh

[no-cd]
lint:
    @scripts/backend/lint.sh

[no-cd]
start:
    @scripts/backend/start.sh

[no-cd]
update:
    @scripts/backend/update.sh
