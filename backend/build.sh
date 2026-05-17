#!/usr/bin/env bash
# Render Build Script
# This script runs during Render's build phase

set -o errexit  # Exit on error

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Training ML model..."
cd api && python train_model.py && cd ..

echo "==> Build complete!"
