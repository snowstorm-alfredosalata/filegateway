from fs import osfs

from marshmallow import Schema, fields, post_load, INCLUDE

from .s3 import S3FsSchema

# We can open this at startup and reuse it.
LOCAL_FS = osfs.OSFS('~/.filegateway', True, 0o755)

class FsSchema(Schema):
    """Generic filesystem schema that maps itself to a specific schema.
    
    Implemented filesystems:
        - s3: Amazon AWS S3
    """
    class Meta:
        unknown = INCLUDE
    
    fs = fields.Str(required=True)
    
    @post_load
    def make_specific(self, data, **_kwargs):
        match data['fs']:
            case 'osfs':
                return LOCAL_FS
            case "s3":
                return S3FsSchema().load(data)
            case _:
                raise NotImplementedError
    
