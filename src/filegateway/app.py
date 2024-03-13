import mimetypes
from flask import Flask, request, jsonify

from filegateway import Filesystem

class FileGatewayApp(Flask):
    """A Wrapper on a Flask App.
    Currently adds no functionality, but it's been added for future integration.
    """
    pass

def setup_app() -> FileGatewayApp:
    app = FileGatewayApp(__name__)

    # TODO: It'd be appropriate to Cache Filesystems, to make repeated use of the same filesystem more efficient.
    # The performance impact of this has not been investigated yet though, and it's likely not to be substantial.

    @app.route('/api/v1/add_document', methods=['JSON'])
    def add_document():
        """Adds a document to a flysystem Filesystem.
        
        Takes:
            A JSON HTTP request, with a correctly-formed JSON body.
            
        Returns:
            Respones: An HTTP response detailing the request result.
        """
        try:
            json: dict = request.json
            fs_json, path, content = json.get("fs"), json.get("path"), json.get("content")
            
            assert fs_json, "Filesystem is mandatory!"
            assert path, "Path is mandatory!"
            assert content, "Content is mandatory!"
            
            fs: Filesystem = Filesystem.from_json(fs_json)
            
            fs.write(path, content)
            
            return jsonify({"status": "ok"})
            
        except Exception as e:
            return jsonify({"status": "error", "error_message": str(e)}), 400

    @app.route('/api/v1/get_document', methods=['JSON'])
    def get_document():
        """Retrieves a document from a flysystem Filesystem.
        
        Takes:
            A JSON HTTP request, with a correctly-formed JSON body.
            
        Returns:
            Respones: An HTTP response detailing the request result.
        """
        try:
            json: dict = request.json
            fs_json, path, content = json.get("fs"), json.get("path"), json.get("content")
            
            assert fs_json, "Filesystem is mandatory!"
            assert path, "Path is mandatory!"
            
            fs: Filesystem = Filesystem.from_json(fs_json)
            
            content = fs.read(path)
            mime_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
            
            return content, 200, {'Content-Type': mime_type}
            
        except Exception as e:
            return jsonify({"status": "error", "error_message": str(e)}), 400
    
    return app