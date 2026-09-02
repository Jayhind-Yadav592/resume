#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install production dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files for WhiteNoise
python manage.py collectstatic --no-input

# Run database migrations (Neon PostgreSQL / default DB)
python manage.py migrate
