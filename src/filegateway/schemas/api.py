from fs.base import FS as baseFS
from marshmallow import Schema, fields, post_load

from .filesystems import FsSchema

class WriteDocumentApiSchema(Schema):
    """
    example api
    
    """
    path = fields.Str(required=True)
    content = fields.Str(required=True)
    fs = fields.Nested(FsSchema, required=True)

    @post_load
    def make_api_obj(self, data, **_kwargs):
        return Api(**data)

class ReadDocumentApiSchema(Schema):
    path = fields.Str(required=True)
    fs = fields.Nested(FsSchema, required=True)

    @post_load
    def make_api_obj(self, data, **_kwargs):
        return Api(**data)

class ListContentsApiSchema(Schema):
    path = fields.Str()
    fs = fields.Nested(FsSchema, required=True)

    @post_load
    def make_api_obj(self, data, **_kwargs):
        return Api(**data)

class Api():
    """Generic data object valid for all Api Calls.
    """
    path: str
    fs: baseFS
    content: None | str

    def __init__(self, fs: baseFS, path: str = "/", content = None):
        self.path = path
        self.fs = fs
        self.content = content
