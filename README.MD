# Filegateway

A simple Microservice to store files on various filesystems with consistent RESTful APIs. 
Powered by Flask & Flysystem.

Currently only supports Amazon AWS S3.

**Not yet suitable for production use.**

## Available APIs

- `/api/v1/write_document, methods=['JSON']`: Write a document to a filesystem
- `/api/v1/read_document, methods=['JSON']`: Read a document from a filesystem
- `/api/v1/list_contents, methods=['JSON']`: List content in a folder from a filesystem

For API Json schemas, please check `src/filegateway/api`

## Docker

Filegateway includes a Docker image Dockerfile.

To build:

```
    python3 -m build && docker build -t local/filegateway . && docker run local/filegateway -p 5000:5000
```

**Warning:** building python package is mandatory before building the docker image, or it will fail.

## Testing requests
Run `example-request.js` with npm or `example-request.sh` with bash.

## Running unit tests
Simply run:
```
    pip3 install tox && tox
```
