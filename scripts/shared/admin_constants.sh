#!/bin/bash

# Vault
export VAULT_ADDR="http://localhost:8200"
export VAULT_TOKEN="root"

# Database
export PGHOST="localhost"
export PGPORT="5432"
export PGDATABASE="postgres"
export PGUSER="admin"
export PGPASSWORD="secret"

# Keycloak
export KC_USERNAME="admin"
export KC_PASSWORD="admin"
export KC_CLIENT_ID="fastapi"
export KC_CLIENT_SECRET="VERY_SECRET_CLIENT_SECRET"

# Redis
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_PASSWORD="SecurePassword"
