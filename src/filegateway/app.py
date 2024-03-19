import mimetypes
import logging
from flask import Flask, request, jsonify

from filegateway.api import ListContentsApiSchema, WriteDocumentApiSchema, ReadDocumentApiSchema, Api

class FileGatewayApp(Flask):
    """A Wrapper on a Flask App.
    Currently adds no functionality, but it's been added for future integration.
    """
    pass

def setup_app() -> FileGatewayApp:
    """Sets up the FileGateway App.
    The app can then be run by a WSGI webserver or by the in-built Flask debug server.
    """
    app = FileGatewayApp(__name__)

    # TODO: It'd be appropriate to Cache Filesystems, to make repeated use of the same filesystem more efficient.
    # The performance impact of this has not been investigated yet though, and it's likely not to be substantial.

    if __name__ != '__main__':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        
    write_document_api_schema = WriteDocumentApiSchema()
    @app.route('/api/v1/write_document', methods=['JSON'])
    def write_document():
        """Adds a document to a flysystem Filesystem.
        
        Takes:
            A JSON HTTP request, with a correctly-formed JSON body according to
            `WriteDocumentApiSchema`
            
        Returns:
            Responds: JSON "Ok" or a JSON error.
        """
        try:
            api: Api = write_document_api_schema.load(request.json)
            
            api.fs.write(api.path, api.content)
            
            app.logger.info(f'Wrote file {api.path} on file system {api.fs.adapter.__str__()}.')
            return jsonify({"status": "ok"})
            
        except Exception as e:
            app.logger.error(f'Error processing request: {str(e)}')
            return jsonify({"status": "error", "error_message": str(e)}), 400


    read_document_api_schema = ReadDocumentApiSchema()
    @app.route('/api/v1/read_document', methods=['JSON'])
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
            
            content = api.fs.read(api.path)
            mime_type = mimetypes.guess_type(api.path)[0] or "application/octet-stream"
            
            app.logger.info(f'Serving file {api.path} from file system {api.fs.adapter.__str__()}.')
            return content, 200, {'Content-Type': mime_type}
            
        except Exception as e:
            app.logger.error(f'Error processing request: {str(e)}')
            return jsonify({"status": "error", "error_message": str(e)}), 400
    
    list_folders_api_schema = ListContentsApiSchema()
    @app.route('/api/v1/list_contents', methods=['JSON'])
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
            
            contents = api.fs.list_contents(api.path)
            
            app.logger.info(f'Listing directory {api.path} on file system {api.fs.adapter.__str__()}.')
            return jsonify({"status": "ok", "data": contents}), 200
            
        except Exception as e:
            app.logger.error(f'Error processing request: {str(e)}')
            return jsonify({"status": "error", "error_message": str(e)}), 400
    
    return app