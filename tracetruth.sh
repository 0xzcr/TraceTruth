#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PY="$ROOT_DIR/tracer_venv/bin/python"

if [ -x "$VENV_PY" ]; then
  exec "$VENV_PY" "$ROOT_DIR/main.py"
else
  exec python3 "$ROOT_DIR/main.py"
fi
