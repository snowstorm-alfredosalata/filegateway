#!/bin/sh

gunicorn -b "0.0.0.0:8000" -w ${GUNICORN_WORKERS} "filegateway.app:setup_app()" \
    --access-logfile ${GUNICORN_ACCESS_LOG_FILE} \
    --log-file ${GUNICORN_LOG_FILE} \
    --log-level ${GUNICORN_LOG_LEVEL} 