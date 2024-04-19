from marshmallow import Schema, fields, post_load

from .filesystems import FsSchema

from filegateway.fs_target import FsTarget

class RequestSchema(Schema):
    """Unified schema for filesystem.

    Args:
        :class:`FsSchema`: fs
            A filesystem definition according to any of the implemented schemas.
        str: path
            The target path. Might represent a file or a directory.
        str: content
            A file encoded as a base64 string. Only required for Write requests.
    """
    fs = fields.Nested(FsSchema, required=True)

    path = fields.Str(required=True)
    content = fields.Str(required=True)

    @post_load
    def make_api_obj(self, data, **_kwargs):
        return FsTarget(**data)
