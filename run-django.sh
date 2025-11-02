#!/bin/bash
if [[ -z "${PORT}" ]]; then
    PORT=8000
fi

if [[ -z "${WORKERS}" ]]; then
    WORKERS=4
fi

APPLICATION_ASGI=config.asgi:application
APPLICATION_TIMEOUT=30

echo "Running Django App..."
echo "APPLICATION_ASGI: ${APPLICATION_ASGI}"
echo "APPLICATION_TIMEOUT: ${APPLICATION_TIMEOUT}"
echo "APPLICATION_PORT: ${PORT}"
echo "APPLICATION_WORKERS: ${WORKERS}"

gunicorn ${APPLICATION_ASGI} \
    --timeout ${APPLICATION_TIMEOUT} \
    --graceful-timeout 30 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --worker-class=uvicorn.workers.UvicornWorker \
    --workers=${WORKERS} \
    --bind=0.0.0.0:${PORT}
