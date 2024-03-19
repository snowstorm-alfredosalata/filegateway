FROM python:3.12-alpine
LABEL AUTHOR="as@salata.ovh"

ENV \
    GUNICORN_WORKERS 4 \
    GUNICORN_ACCESS_LOG_FILE - \
    GUNICORN_LOG_FILE - \
    GUNICORN_LOG_LEVEL info \
    LANG C.UTF-8

RUN apk add git

RUN pip install gunicorn --break-system-packages \
    git+https://github.com/snowstorm-alfredosalata/filegateway.git

EXPOSE 8000

COPY entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]