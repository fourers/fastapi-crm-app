#!/bin/bash
set -euo pipefail

source scripts/shared/admin_constants.sh
source scripts/shared/vault_helper.sh

database_info=("host" "${PGHOST}" "port" "${PGPORT}")

write_secret "myapp/admin" "$(format_json "${database_info[@]}" "database" "${PGDATABASE}" "username" "admin" "password" "${PGPASSWORD}")"

app_admin_password=$(random_password)
psql -v ON_ERROR_STOP=1 -c "CREATE USER app_admin PASSWORD '${app_admin_password}';"
write_secret "myapp/app_admin" "$(format_json "${database_info[@]}" "database" "myapp" "username" "app_admin" "password" "${app_admin_password}")"

app_user_password=$(random_password)
psql -v ON_ERROR_STOP=1 -c "CREATE USER app_user PASSWORD '${app_user_password}';"
write_secret "myapp/app_user" "$(format_json "${database_info[@]}" "database" "myapp" "username" "app_user" "password" "${app_user_password}")"

psql -v ON_ERROR_STOP=1 -f "scripts/init/init_db.sql"
