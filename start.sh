#!/bin/bash

# Check for existing uvicorn process
PID=$(ps aux | grep "uvicorn app:app" | grep -v grep | awk '{print $2}')

if [ -n "$PID" ]; then
  echo "Stopping existing uvicorn process (PID $PID)..."
  kill "$PID"
  sleep 1
fi

echo "Starting uvicorn..."
source venv/bin/activate
uvicorn app:app --reload
