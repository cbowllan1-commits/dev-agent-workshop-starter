#!/usr/bin/env bash
set -e

echo "=== Dev Agent Workshop Setup ==="
echo ""

# Check required tools
errors=0

check_tool() {
    if command -v "$1" &> /dev/null; then
        echo "  [OK] $1 $(command $1 --version 2>/dev/null | head -1)"
    else
        echo "  [MISSING] $1 — $2"
        errors=$((errors + 1))
    fi
}

echo "Checking prerequisites..."
check_tool python3 "Install from https://python.org"
check_tool uv "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
check_tool node "Install from https://nodejs.org"

if ! command -v pnpm &> /dev/null; then
    echo "  [INSTALLING] pnpm..."
    npm install -g pnpm 2>/dev/null && echo "  [OK] pnpm installed" || {
        echo "  [MISSING] pnpm — Install with: npm install -g pnpm"
        errors=$((errors + 1))
    }
else
    echo "  [OK] pnpm $(pnpm --version 2>/dev/null)"
fi

check_tool claude "Install from https://docs.anthropic.com/en/docs/claude-code"

echo ""

if [ $errors -gt 0 ]; then
    echo "ERROR: $errors missing tool(s). Install them and re-run this script."
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
uv sync --all-extras
echo ""

echo "Installing frontend dependencies..."
cd frontend && pnpm install && cd ..
echo ""

echo "Running tests..."
uv run pytest -q
echo ""

echo "=== Setup complete! ==="
echo ""
echo "To start the app:"
echo "  ./scripts/run-dev.sh"
echo ""
echo "To start Claude Code:"
echo "  claude"
