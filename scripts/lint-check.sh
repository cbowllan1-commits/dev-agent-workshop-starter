#!/usr/bin/env bash
set -e

echo "Running ruff format check..."
uv run ruff format --check src/ tests/

echo "Running ruff lint check..."
uv run ruff check src/ tests/

echo "All checks passed!"
