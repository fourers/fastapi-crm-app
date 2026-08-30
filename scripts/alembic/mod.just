export REQUESTS_CA_BUNDLE := "/etc/ssl/certs/ca-certificates.crt"
export SSL_CERT_FILE := "/etc/ssl/certs/ca-certificates.crt"

[no-cd]
generate MESSAGE:
    @scripts/alembic/generate_revision.sh {{MESSAGE}}

[no-cd]
upgrade:
    @scripts/alembic/upgrade_head.sh
