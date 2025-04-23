#!/bin/bash

pid=$(lsof -ti :8000)
if [ -n "$pid" ]; then
  echo "Stopping running server..."
  kill "$pid"
  sleep 1
fi

echo "Starting Lorcana Workshop..."
source venv/bin/activate
uvicorn app:app --reload
