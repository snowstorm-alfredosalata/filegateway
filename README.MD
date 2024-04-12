# FileGateway

Filegateway is a Flask application for serving and uploading files from and to several targets, build upon PyFilesystem.
Interacting with Filegateway is done through simple RESTful APIs.

Currently only supports Amazon AWS S3.

**Not yet suitable for production use.**

## Available APIs

- `/write, methods=['POST']`: Write a document to a filesystem
- `/read, methods=['POST']`: Read a document from a filesystem
- `/list, methods=['POST']`: List content in a folder from a filesystem

For API Json schemas, please check `src/filegateway/api`

## Docker

Filegateway includes a Docker image Dockerfile.

To build:

```sh
# Gunicorn workers should tipically be 2 * CPU
cd ./docker && \
docker build -t local/filegateway . && \
docker run -p 8000:8000 -v ~/.filegateway:/mnt/logs:z -e GUNICORN_WORKERS=4 -e GUNICORN_ACCESS_LOG_FILE=/mnt/logs/access.log -e GUNICORN_LOG_FILE=/mnt/logs/error.log -e GUNICORN_LOG_LEVEL=info -d local/filegateway
```

**Warning:** building python package is mandatory before building the docker image, or it will fail.

## Testing requests
Run `example-request.js` with npm or `example-request.sh` with bash.

## Running unit tests
Simply run:
```
    pip3 install tox && tox
```
