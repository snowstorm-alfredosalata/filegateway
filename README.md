# Filegateway

Filegateway is a simple microservice leveraging Flysystem to provide API-based
access to various file storages.

Currently only supports Amazon AWS S3.

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