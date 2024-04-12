from fs import osfs, base
from fs_s3fs import S3FS

from marshmallow import Schema, fields, post_load, INCLUDE, EXCLUDE

# We can open this at startup and reuse it.
LOCAL_FS = osfs.OSFS('~/.filegateway', True, 0o755)

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
        return S3FS(
            data["bucket_name"], 
            aws_access_key_id=data["access_key_id"], 
            aws_secret_access_key=data["secret_access_key"], 
            region=data["region_name"], 
            endpoint_url=data["endpoint_url"])

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
            case 'osfs':
                return LOCAL_FS
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
    path: str
    fs: base.FS
    content: None | str

    def __init__(self, fs: base.FS, path: str = "/", content = None):
        self.path = path
        self.fs = fs
        self.content = content