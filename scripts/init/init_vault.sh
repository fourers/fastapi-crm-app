#!/usr/bin/bash
set -euo pipefail

source scripts/shared/admin_constants.sh
source scripts/shared/vault_helper.sh

write_secret "myapp/keycloak_admin" "$(format_json "username" "${KC_USERNAME}" "password" "${KC_PASSWORD}")"
write_secret "myapp/keycloak_client" "$(format_json "client_id" "${KC_CLIENT_ID}" "client_secret" "${KC_CLIENT_SECRET}")"

write_secret "myapp/redis" "$(format_json "host" "${REDIS_HOST}" "port" "${REDIS_PORT}" "password" "${REDIS_PASSWORD}")"
