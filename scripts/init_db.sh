#!/bin/bash
set -euo pipefail

source scripts/shared/admin_constants.sh
source scripts/shared/vault_helper.sh

function random_password() {
  openssl rand -base64 24
}

write_creds admin "${PGPASSWORD}"

app_admin_password=$(random_password)
psql -v ON_ERROR_STOP=1 -c "CREATE USER app_admin PASSWORD '${app_admin_password}';"
write_creds app_admin "${app_admin_password}"

app_user_password=$(random_password)
psql -v ON_ERROR_STOP=1 -c "CREATE USER app_user PASSWORD '${app_user_password}';"
write_creds app_user "${app_user_password}"

psql -v ON_ERROR_STOP=1 -f "sql/init_db.sql"
