import logging

from flask import Flask, request, jsonify, send_file
import marshmallow

from filegateway.schemas.request import RequestSchema
from filegateway.fs_target import FsTarget

class FileGatewayApp(Flask):
    """A Wrapper on a Flask App.
    Currently adds no functionality, but it's been added for future integration.
    """

api_schema = RequestSchema()
app = FileGatewayApp(__name__)

@app.route('/write', methods=['POST'])
def write_document():
    """Adds a document to a filesystem.
    
    Takes:
        A JSON body, formed according to
        :class:`filegateway.schemas.request.RequestSchema`.

        `content` key is mandatory and excepted to be a base64-encoded
        file.
        
    Returns:
        JSON-Encoded "Okay" or error.
    """
    file: FsTarget = api_schema.load(request.json)
    file.write()

    app.logger.info('Wrote file %s on file system %s.', file.path, file.get_fs_type())
    return jsonify({"status": "ok"})

@app.route('/read', methods=['POST'])
def read_document():
    """Retrieves a document from a filesystem.
    
    Takes:
        A JSON body, formed according to
        :class:`filegateway.schemas.request.RequestSchema`.
        
    Returns:
        JSON-Encoded "Okay" or error.
    """
    file: FsTarget = api_schema.load(request.json)
    content, mime = file.read(), file.guess_mime()

    app.logger.info('Serving file %s from file system %s.', file.path, file.get_fs_type())
    return send_file(content, as_attachment=True, download_name=file.path, mimetype=mime)

@app.route('/list', methods=['POST'])
def list_contents():
    """Lists the content in a filesystem path.

    Takes:
        A JSON body, formed according to
        :class:`filegateway.schemas.request.RequestSchema`.
        
    Returns:
        JSON-Encoded "Okay" or error.
    """
    folder: FsTarget = api_schema.load(request.json)
    contents = folder.list_contents()
    
    app.logger.info('Listing directory %s on file system %s.', folder.path, folder.get_fs_type())
    return jsonify({"status": "ok", "data": contents}), 200

@app.errorhandler(ValueError)
@app.errorhandler(marshmallow.ValidationError)
def handle_validation_errors(e: Exception):
    """Catches ValueErrors and Marshmallow schema validation
    errors and maps them to `Bad Request`s with a parseable JSON body.

    Args:
        Exception: e
            The caught exception.

    Returns:
        JSON-Encoded error.
    """
    error_type = e.__class__.__name__

    app.logger.error('Malformed request. %s: %s', error_type, str(e))
    return jsonify({"status": "error", "error_message": 'Malformed request. %s: %s' % (error_type, str(e))}), 400

@app.errorhandler(Exception)
def handle_errors(e):
    """Catches any uncaught error and maps `Internal Server Error`s with a parseable JSON body.

    Args:
        Exception: e
            The caught exception.

    Returns:
        JSON-Encoded error.
    """
    error_type = e.__class__.__name__

    app.logger.error('Error processing request: %s: %s', error_type, str(e))
    return jsonify({"status": "error", "error_message": 'Error processing request: %s: %s' % (error_type, str(e))}), 500

def setup_app() -> FileGatewayApp:
    """Returns the Flask App, attempting to bind gunicorn logger if existing.

    Returns:
        :class:`FileGatewayApp`: The Flask FileGateway App.
    """

    if __name__ != '__main__':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    return app
