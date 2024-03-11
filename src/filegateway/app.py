import base64
from flask import Flask, request, jsonify

from filegateway import Document, Filesystem


class FileGatewayApp(Flask):
    pass

def setup_app() -> FileGatewayApp:
    app = FileGatewayApp(__name__)

    @app.route('/api/v1/add_document', methods=['POST'])
    def add_document():
        try:
            json = request.json
            fs_json, document_json = json["fs"], json["document"]
            
            fs = Filesystem.from_json(fs_json)
            document = Document.from_json(request.json)
            
            fs.
            app.storage.add_or_edit(document)
            
            return jsonify({"status": "ok", "document_id": document.id})
            
        except Exception as e:
            return jsonify({"status": "error", "error_message": str(e)}), 400

    @app.route('/api/v1/get_document', methods=['GET'])
    def get_document():
        document_id = request.args.get('id')
        
        if (document_id == None):
            return jsonify({"error": "missing mandatory parameter document_id"}), 400
        
        document = app.storage.get(document_id)
        if (document == None):
            return jsonify({"error": "document not present in database"}), 404
        
        return base64.b64decode(document.content), 200, {'Content-Type': document.mime_type}

    @app.route('/api/v1/get_document_metadata', methods=['GET'])
    def get_document_metadata():
        document_id = request.args.get('id')
        
        if (document_id == None):
            return jsonify({"error": "missing mandatory parameter document_id"}), 400
        
        document = app.storage.get(document_id)
        if (document == None):
            return jsonify({"error": "document not present in database"}), 404
        
        return jsonify(document.get_metadata()), 200, {'Content-Type': document.mime_type}
    
    return app