from flysystem.filesystem import Filesystem
from flysystem.adapters import s3

from marshmallow import Schema, fields, post_load, INCLUDE, EXCLUDE

class S3FsSchema(Schema):
    """Schema for accessing a S3 Filesystem

    Args:
        str: endpoint_url
        str: access_key_id
        str: secret_access_key
        str: bucket_name
        str: region_name
    """
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
    """Generic filesystem schema that maps itself to a specific schema.
    
    Implemented filesystems:
        - s3: Amazon AWS S3
    """
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

class ListContentsApiSchema(Schema):
    path = fields.Str()
    fs = fields.Nested(FsSchema, required=True)
    
    @post_load
    def make_api_obj(self, data, **kwargs):
        return Api(**data)

class Api():
    """Generic data object valid for all Api Calls.
    """
    def __init__(self, fs: Filesystem, path: str = "/", content = None):
        self.path = path
        self.fs = fs
        self.content = content