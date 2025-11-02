#!/bin/bash
if [[ -z "${PORT}" ]]; then
    PORT=8000
fi

echo "Running FastAPI App..."
echo "Port: ${PORT}"

uvicorn config.asgi:fastapp --host 0.0.0.0 --port ${PORT} --reload
