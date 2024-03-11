from filegateway.document import Document

class Storage():
    def get(self, id: str) -> Document | None:
        raise NotImplementedError
    
    def add_or_edit(self, document: Document) -> str:
        raise NotImplementedError


from .in_memory_storage import InMemoryStorage 