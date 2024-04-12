# FileGateway

Filegateway is a Flask application for serving and uploading files from and to several targets, build upon PyFilesystem.
Interacting with Filegateway is done through simple RESTful APIs.

## Set-up
FileGateway can be run standalone (for testing usage) or with `gunicorn`. This repository provides a docker image complete with a `gunicorn` web server.
Simply run `make docker up` or `make podman up`.
