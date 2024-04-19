from marshmallow import Schema, fields, post_load

from .filesystems import FsSchema

from filegateway.fs_target import FsTarget

class RequestSchema(Schema):
    """ A Marshmallow schema, valid for all FileGateway API requests. 
    """
    fs = fields.Nested(FsSchema, required=True)

    path = fields.Str(required=True)
    content = fields.Str(required=False)

    @post_load
    def make_api_obj(self, data, **_kwargs):
        return FsTarget(**data)
