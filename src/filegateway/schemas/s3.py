from marshmallow import Schema, fields, post_load
from fs_s3fs import S3FS

class S3FsSchema(Schema):
    """Schema for accessing a S3 Filesystem

    Args:
        str: endpoint_url
        str: access_key_id
        str: secret_access_key
        str: bucket_name
        str: region_name
    """

    fs = fields.Str(required=True) # always "s3"
    
    endpoint_url = fields.Str(required=True)
    access_key_id = fields.Str(required=True)
    secret_access_key = fields.Str(required=True)
    bucket_name = fields.Str(required=True)
    region_name = fields.Str(required=True)
    
    @post_load
    def make_s3_fs(self, data, **_kwargs):
        return S3FS(
            data["bucket_name"], 
            aws_access_key_id=data["access_key_id"], 
            aws_secret_access_key=data["secret_access_key"], 
            region=data["region_name"], 
            endpoint_url=data["endpoint_url"])