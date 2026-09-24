#!/usr/bin/env bash
# One-shot setup for macOS and Linux (also usable on CI machines).
#
# Usage:
#     bash scripts/bootstrap.sh
#     bash scripts/bootstrap.sh --reset      # rebuild the sample data
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

if [ ! -x ".venv/bin/python" ]; then
    echo "Creating the virtual environment (.venv) ..."
    python3 -m venv .venv
fi

echo "Installing dependencies ..."
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example - adjust SECRET_KEY before sharing this machine."
fi

echo "Seeding the database ..."
./.venv/bin/python scripts/seed_data.py "$@"

echo
echo "Setup complete. Start the app with: .venv/bin/python run.py"
