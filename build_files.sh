#!/usr/bin/env bash
# Vercel Build Script for Django
echo "--> Installing dependencies from requirements.txt..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "--> Collecting static assets for WhiteNoise..."
python3 manage.py collectstatic --no-input --clear

echo "--> Vercel Build Completed Successfully."
