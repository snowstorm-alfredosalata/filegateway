import mimetypes
import logging
from flask import Flask, request, jsonify

from filegateway.schemas.api import Api
from filegateway.schemas.api import WriteDocumentApiSchema
from filegateway.schemas.api import ReadDocumentApiSchema
from filegateway.schemas.api import ListContentsApiSchema


class FileGatewayApp(Flask):
    """A Wrapper on a Flask App.
    Currently adds no functionality, but it's been added for future integration.
    """

app = FileGatewayApp(__name__)

write_document_api_schema = WriteDocumentApiSchema()
@app.route('/write', methods=['POST'])
def write_document():
    """Adds a document to a flysystem Filesystem.
    
    Takes:
        A JSON HTTP request, with a correctly-formed JSON body according to
        :class:`WriteDocumentApiSchema`
        
    Returns:
        Responds: JSON "Ok" or a JSON error.
    """
    try:
        api: Api = write_document_api_schema.load(request.json)

        with api.fs.open(api.path, 'wt') as file:
            file.write(api.content)

        app.logger.info('Wrote file %s on file system %s.', api.path, api.fs.__class__)
        return jsonify({"status": "ok"})

    except Exception as e:
        app.logger.error('Error processing request: %s', str(e))
        return jsonify({"status": "error", "error_message": str(e)}), 400


read_document_api_schema = ReadDocumentApiSchema()
@app.route('/read', methods=['POST'])
def read_document():
    """Retrieves a document from a flysystem Filesystem.
    
    Takes:
        A JSON HTTP request, with a correctly-formed JSON body according to
        `ReadDocumentApiSchema`
        
    Returns:
        Responds: The requested document or a JSON error.
    """
    try:
        api: Api = read_document_api_schema.load(request.json)

        with api.fs.open(api.path, 'rt') as file:
            content = file.read(api.content)

        mime_type = mimetypes.guess_type(api.path)[0] or "application/octet-stream"

        app.logger.info('Serving file %s from file system %s.', api.path, api.fs.__class__)
        return content, 200, {'Content-Type': mime_type}

    except Exception as e:
        app.logger.error('Error processing request: %s', str(e))
        return jsonify({"status": "error", "error_message": str(e)}), 400

list_folders_api_schema = ListContentsApiSchema()
@app.route('/list', methods=['POST'])
def list_contents():
    """Retrieves a document from a flysystem Filesystem.
    
    Takes:
        A JSON HTTP request, with a correctly-formed JSON body according to
        `ListContentsApiSchema`
        
    Returns:
        Responds: JSON-encoded list of folder contents or a JSON error.
    """
    try:
        api: Api = list_folders_api_schema.load(request.json)

        contents = api.fs.listdir(api.path)

        app.logger.info('Listing directory %s on file system %s.', api.path, api.fs.__class__)
        return jsonify({"status": "ok", "data": contents}), 200

    except Exception as e:
        app.logger.error('Error processing request: %s', str(e))
        return jsonify({"status": "error", "error_message": str(e)}), 400


def setup_app() -> FileGatewayApp:
    """Sets up the FileGateway App.
    The app can then be run by a WSGI webserver or by the in-built Flask debug server.
    """

    # TODO: It'd be appropriate to Cache Filesystems, to make repeated
    # use of the same filesystem more efficient.
    # The performance impact of this has not been investigated yet though,
    # and it's likely not to be substantial.

    if __name__ != '__main__':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    return app
