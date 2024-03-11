from typing import Dict

from filegateway import Document
from filegateway.providers import Storage

class InMemoryStorage(Storage):
    db : Dict[str, Document] = dict()
    
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
        