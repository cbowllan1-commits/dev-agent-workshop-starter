#!/usr/bin/env bash
set -e

# Start backend and frontend in parallel
# Ctrl+C kills both processes

cleanup() {
    echo ""
    echo "Shutting down..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "Starting backend on :8000 and frontend on :5173..."
echo "Press Ctrl+C to stop both."
echo ""

# Start backend
uv run uvicorn src.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
cd frontend && pnpm dev &
FRONTEND_PID=$!

# Wait for either to exit
wait $BACKEND_PID $FRONTEND_PID
