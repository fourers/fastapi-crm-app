function write_creds() {
  local -r username="${1:-}"
  local -r password="${2:-}"
  local -r path="${3:-"${username}"}"
  secret_path="myapp/${path}"
  echo "Writing secret: ${secret_path}"
  curl -fsS -X POST "${VAULT_ADDR}/v1/secret/data/${secret_path}" \
    -H "X-Vault-Token: ${VAULT_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"data\":{\"username\":\"${username}\",\"password\":\"${password}\"}}"
}
