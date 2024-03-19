#!/bin/sh

gunicorn -b "0.0.0.0:8000" -w ${GUNICORN_WORKERS} "filegateway.app:setup_app()"