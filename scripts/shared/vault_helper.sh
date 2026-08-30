function write_secret() {
  local -r secret_path="${1}"
  local -r payload="${2}"
  echo "Writing secret: ${secret_path}"
  curl -fsS -X POST "${VAULT_ADDR}/v1/secret/data/${secret_path}" \
    -H "X-Vault-Token: ${VAULT_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$(json_set "data" "${payload}")"
}

function random_password() {
  openssl rand -base64 24
}

function format_json() {
    if (( $# % 2 != 0 )); then
        echo "Error: arguments must be key-value pairs" >&2
        return 1
    fi

    local json="{}"

    while (($#)); do
        json=$(jq --arg key "$1" --arg value "$2" '.[$key] = $value' <<< "$json")
        shift 2
    done

    printf '%s\n' "$json"
}

function json_set() {
    local key="${1}"
    local value="${2}"

    jq -cn --arg key "$key" --argjson value "$value" \
        '{($key): $value}'
}
