#!/usr/bin/bash
set -euo pipefail

source scripts/shared/admin_constants.sh
source scripts/shared/vault_helper.sh

write_creds "${KC_USERNAME}" "${KC_PASSWORD}" "keycloak_admin"

write_creds "${KC_CLIENT_ID}" "${KC_CLIENT_SECRET}" "keycloak_client"

write_creds "redis" "${REDIS_PASSWORD}"
