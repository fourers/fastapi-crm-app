#!/bin/bash
set -euo pipefail

function random_password() {
  openssl rand -base64 24
}

function write_creds() {
  local -r username="${1:-}"
  local -r password="${2:-}"
  secret_path="myapp/${username}"
  echo "Writing secret: ${secret_path}"
  curl -fsS -X POST "${VAULT_ADDR}/v1/secret/data/${secret_path}" \
    -H "X-Vault-Token: ${VAULT_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"data\":{\"username\":\"${username}\",\"password\":\"${password}\"}}"
}

apt-get update && apt-get install -y --no-install-recommends curl

write_creds admin "${PGPASSWORD}"

app_admin_password=$(random_password)
psql -v ON_ERROR_STOP=1 -c "CREATE USER app_admin PASSWORD '${app_admin_password}';"
write_creds app_admin "${app_admin_password}"

app_user_password=$(random_password)
psql -v ON_ERROR_STOP=1 -c "CREATE USER app_user PASSWORD '${app_user_password}';"
write_creds app_user "${app_user_password}"

psql -v ON_ERROR_STOP=1 -f "sql/init_db.sql"
