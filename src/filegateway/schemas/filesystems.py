from fs import osfs

from marshmallow import Schema, fields, post_load, INCLUDE

from .s3 import S3FsSchema

# We can open this at startup and reuse it.
LOCAL_FS: None | osfs.OSFS = None
def get_local_fs():
    global LOCAL_FS

    if LOCAL_FS is None:
        LOCAL_FS = osfs.OSFS('~/.filegateway', True, 0o755)

    return LOCAL_FS

class FsSchema(Schema):
    """Generic filesystem schema that maps itself to a specific schema.
    
    Implemented filesystems:
        - os: Local Filesystem
        - s3: Amazon AWS S3
    """
    class Meta:
        unknown = INCLUDE
    
    fs = fields.Str(required=True)
    
    @post_load
    def make_specific(self, data, **_kwargs):
        fs = data['fs']

        match fs:
            case 'os':
                return get_local_fs()
            case "s3":
                return S3FsSchema().load(data)
            case _:
                raise NotImplementedError(f"Filesystem {fs} does not exist!")
    
