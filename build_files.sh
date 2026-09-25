#!/usr/bin/env bash
# Vercel Build Script for Django with PEP 668 compatibility
set -e

echo "--> Installing dependencies from requirements.txt..."
python3 -m pip install --upgrade pip --break-system-packages 2>/dev/null || pip install --upgrade pip
python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt

echo "--> Collecting static assets for WhiteNoise..."
python3 manage.py collectstatic --no-input --clear || python manage.py collectstatic --no-input --clear

echo "--> Vercel Build Completed Successfully."
