from flysystem.filesystem import Filesystem
from flysystem.adapters import s3

from marshmallow import Schema, fields, post_load, INCLUDE, EXCLUDE

class S3FsSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    endpoint_url = fields.Str(required=True)
    access_key_id = fields.Str(required=True)
    secret_access_key = fields.Str(required=True)
    bucket_name = fields.Str(required=True)
    region_name = fields.Str(required=True)
    
    @post_load
    def make_s3_fs(self, data, **kwargs):
        adapter = s3.S3FilesystemAdapter(**data)
        return Filesystem(adapter)

class FsSchema(Schema):
    class Meta:
        unknown = INCLUDE
    
    fs = fields.Str(required=True)
    
    @post_load
    def make_specific(self, data, **kwargs):
        match data['fs']:
            case "s3":
                return S3FsSchema().load(data)
            case _:
                raise NotImplementedError
    
class WriteDocumentApiSchema(Schema):
    path = fields.Str(required=True)
    content = fields.Str(required=True)
    fs = fields.Nested(FsSchema, required=True)
    
    @post_load
    def make_api_obj(self, data, **kwargs):
        return Api(**data)
    
class ReadDocumentApiSchema(Schema):
    path = fields.Str(required=True)
    fs = fields.Nested(FsSchema, required=True)
    
    @post_load
    def make_api_obj(self, data, **kwargs):
        return Api(**data)

class Api():
    def __init__(self, path: str, fs: Filesystem, content = None):
        self.path = path
        self.fs = fs
        self.content = content