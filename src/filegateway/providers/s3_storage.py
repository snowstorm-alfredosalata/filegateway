from typing import Dict

from flysystem.adapters import s3

from filegateway import Document
from filegateway.providers import Storage

class S3Storage(Storage):
    db : Dict[str, Document] = dict()
    
    def __init__(self):
        self.adapter = s3.S3FilesystemAdapter('https://s3.amazonaws.com', )
        
    
    def get(self, id: str) -> Document | None:
        return self.db.get(id, None)
    
    def add_or_edit(self, document: Document) -> str:
        current_document = self.db.get(document.id, None)
        
        if current_document != None:
            document.modified_by = document.created_by
            
            document.created_on = current_document.created_on
            document.created_by = current_document.created_by
        
        self.db[document.id] = document
        
        return document.id
        