#!/usr/bin/bash
set -euo pipefail

echo "Setting up docker..."
just stop
just start

echo "Setting up database..."
scripts/init_db.sh

echo "Setting up login server..."
scripts/init_keycloak.sh

echo "Setting up database schema..."
scripts/alembic_upgrade.sh
