#!/bin/bash

# Exit immediately if a command fails
set -e
export PYTHONPATH=$(pwd)/app/database

# How many latest migration files to keep
KEEP=5

# Step 0: ensure we are in the project root
cd "$(dirname "$0")"

# Step 1: create a baseline migration
current_date=$(date +"%Y%m%d_%H%M%S")
baseline_msg="[$current_date] baseline migration"

echo "Creating baseline migration..."
alembic revision --autogenerate -m "$baseline_msg"

# Step 2: apply it
echo "Applying baseline migration..."
alembic upgrade head

# Step 3: clean old migrations
echo "Cleaning old migrations (keeping last $KEEP)..."
cd alembic/versions

# List files oldest to newest, delete all except last $KEEP
ls -1tr | head -n -$KEEP | xargs -r rm -f

echo "Migration cleanup complete!"