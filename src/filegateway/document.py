
from typing import Any, Dict

from dataclasses import dataclass
from datetime import datetime
import mimetypes
import uuid

class Document:
    def __init__(self,
        filename: str,
        content: str,
        
        mime_type: str | None = None,
        
        id: str | None = None,
        
        created_on: datetime | None = None,
        created_by: str | None = None,
        
        modified_on: datetime | None = None,
        modified_by: str | None = None      
    ):
        self.id = id or str(uuid.uuid4())
        self.filename = filename
        self.mime_type = mime_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"
        self.content = content
        
        self.created_on = created_on or datetime.now()
        self.created_by = created_by
        
        self.modified_on = modified_on or datetime.now()
        self.modified_by = modified_by or created_by
        
        
    def from_json(request: Any):
        assert request.get("filename"), "Missing filename!"
        assert request.get("content"), "Content empty!"
        
        return Document(**request)
    
    def get_metadata(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "mime_type": self.mime_type,
            "created_on": self.created_on,
            "created_by": self.created_by,
            "modified_on": self.modified_on,
            "modified_by": self.modified_by,
        }