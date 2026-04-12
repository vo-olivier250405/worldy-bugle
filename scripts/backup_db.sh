#!/bin/bash

ENV_FILE="./worldy_bugle_api/.env"

if [ -f "$ENV_FILE" ]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
else
  echo "File .env not found: $ENV_FILE"
  exit 1
fi

# Create backups folder if it doesn't exist
BACKUP_DIR="./backups"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
FILENAME="dump_$TIMESTAMP.sql"
CONTAINER_NAME="${1:-worldy-bugle-postgres}"


docker exec "$CONTAINER_NAME" pg_dump -U "$POSTGRES_USER" -F p "$POSTGRES_DB" > "$BACKUP_DIR/$FILENAME"