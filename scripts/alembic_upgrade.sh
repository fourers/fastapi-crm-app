#!/usr/bin/bash
set -euo pipefail

export REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"
export SSL_CERT_FILE="/etc/ssl/certs/ca-certificates.crt"

uv run alembic upgrade head
