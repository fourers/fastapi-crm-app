#!/usr/bin/bash
set -euo pipefail

source scripts/shared/admin_constants.sh
source scripts/shared/vault_helper.sh

write_creds "${KC_USERNAME}" "${KC_PASSWORD}" "keycloak_admin"
