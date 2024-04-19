import logging

from flask import Flask, request, jsonify, send_file
import marshmallow

from filegateway.schemas.api import RequestSchema
from filegateway.fs_target import FsTarget

class FileGatewayApp(Flask):
    """A Wrapper on a Flask App.
    Currently adds no functionality, but it's been added for future integration.
    """

api_schema = RequestSchema()
app = FileGatewayApp(__name__)

@app.route('/write', methods=['POST'])
def write_document():
    """Adds a document to a flysystem Filesystem.
    
    Takes:
        A JSON HTTP request, with a correctly-formed JSON body according to
        :class:`WriteDocumentApiSchema`
        
    Returns:
        Responds: JSON "Ok" or a JSON error.
    """
    file: FsTarget = api_schema.load(request.json)
    file.write()

    app.logger.info('Wrote file %s on file system %s.', file.path, file.get_fs_type())
    return jsonify({"status": "ok"})

@app.route('/delete', methods=['POST'])
def delete_document():
    """Adds a document to a flysystem Filesystem.
    
    Takes:
        A JSON HTTP request, with a correctly-formed JSON body according to
        :class:`WriteDocumentApiSchema`
        
    Returns:
        Responds: JSON "Ok" or a JSON error.
    """
    file: FsTarget = api_schema.load(request.json)
    file.delete()

    app.logger.info('Deleted file or folder %s on file system %s.', file.path, file.get_fs_type())
    return jsonify({"status": "ok"})

@app.route('/read', methods=['POST'])
def read_document():
    """Retrieves a document from a flysystem Filesystem.
    
    Takes:
        A JSON HTTP request, with a correctly-formed JSON body according to
        `ReadDocumentApiSchema`
        
    Returns: The requested document or a JSON-encoded error.
    """
    file: FsTarget = api_schema.load(request.json)
    content, mime = file.read(), file.guess_mime()

    app.logger.info('Serving file %s from file system %s.', file.path, file.get_fs_type())
    return send_file(content, as_attachment=True, download_name=file.path, mimetype=mime)

@app.route('/list', methods=['POST'])
def list_contents():
    """
    
        
    Returns: The requested document or a JSON-encoded error.
    """
    folder: FsTarget = api_schema.load(request.json)
    contents = folder.list_contents()
    
    app.logger.info('Listing directory %s on file system %s.', folder.path, folder.get_fs_type())
    return jsonify({"status": "ok", "data": contents}), 200


def setup_app() -> FileGatewayApp:
    """Returns the Flask App, attempting to bind gunicorn logger if existing.

    Returns:
        FileGatewayApp: The Flask FileGateway App.
    """

    if __name__ != '__main__':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    return app


@app.errorhandler(ValueError)
@app.errorhandler(marshmallow.ValidationError)
def handle_validation_errors(e: Exception):
    app.logger.error('Malformed request. %s: %s', e.__class__, str(e))
    return jsonify({"status": "error", "error_message": str(e)}), 400



@app.errorhandler(Exception)
def handle_errors(e):
    app.logger.error('Error processing request: %s: %s', e.__class__, str(e))
    return jsonify({"status": "error", "error_message": str(e)}), 500
