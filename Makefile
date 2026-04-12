include worldy_bugle_api/.env
export

CONTAINER_NAME ?= worldy-bugle-postgres
API_CONTAINER_NAME ?= worldy-bugle-api
BACKUP_DIR     := ./backups
DB_NAME        := $(POSTGRES_DB)

.PHONY: help backup_db clean_load_db load_sources makemigrations migrate

help:
	@echo "Available commands:"
	@echo ""
	@echo "  make backup_db [CONTAINER_NAME=container]                        - Backup the database"
	@echo "  make clean_load_db DUMP_FILE=path/to/dump.sql [CONTAINER_NAME=x] - Clean and load the database"
	@echo "  make load_sources                                                   - Load source data into the database"
	@echo "  make makemigrations                                                   - Create new migrations based on model changes"
	@echo "  make migrate                                                   - Apply database migrations"
	@echo ""
	@echo "Examples:"
	@echo "  make backup_db"
	@echo "  make backup_db CONTAINER_NAME=my-postgres-container"
	@echo "  make clean_load_db DUMP_FILE=backups/dump_2026-04-12.sql"

backup_db:
	@mkdir -p "$(BACKUP_DIR)"
	@TIMESTAMP=$$(date +"%Y-%m-%d_%H-%M-%S") && \
	docker exec "$(CONTAINER_NAME)" pg_dump -U "$(POSTGRES_USER)" -F p "$(DB_NAME)" > "$(BACKUP_DIR)/dump_$$TIMESTAMP.sql" && \
	echo "Backup saved to $(BACKUP_DIR)/dump_$$TIMESTAMP.sql"

clean_load_db:
	@if [ -z "$(DUMP_FILE)" ]; then echo "Usage: make clean_load_db DUMP_FILE=path/to/dump.sql"; exit 1; fi
	@if [ ! -f "$(DUMP_FILE)" ]; then echo "File not found: $(DUMP_FILE)"; exit 1; fi
	@echo "Dropping and recreating database '$(DB_NAME)'..."
	docker exec -i "$(CONTAINER_NAME)" psql -U "$(POSTGRES_USER)" -d postgres -c "DROP DATABASE IF EXISTS \"$(DB_NAME)\";"
	docker exec -i "$(CONTAINER_NAME)" psql -U "$(POSTGRES_USER)" -d postgres -c "CREATE DATABASE \"$(DB_NAME)\";"
	@echo "Loading $(DUMP_FILE)..."
	docker exec -i "$(CONTAINER_NAME)" psql -U "$(POSTGRES_USER)" -d "$(DB_NAME)" < "$(DUMP_FILE)"
	@echo "Done."

load_sources:
	@echo "Loading source data..."
	docker exec -it "$(API_CONTAINER_NAME)" python3 manage.py loaddata fixtures/sources.json
	@echo "Done."

makemigrations:
	docker exec -it "$(API_CONTAINER_NAME)" python3 manage.py makemigrations

migrate:
	docker exec -it "$(API_CONTAINER_NAME)" python3 manage.py migrate