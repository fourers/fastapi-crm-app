set default-list := true

[no-cd]
database:
	@echo "Setting up database..."
	@scripts/init/init_db.sh

[no-cd]
vault:
	@echo "Setting up vault..."
	@scripts/init/init_vault.sh
