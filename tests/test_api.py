import pytest
from marshmallow import ValidationError

from flysystem.adapters import s3
from filegateway.api import ReadDocumentApiSchema, WriteDocumentApiSchema, FsSchema, Api

__author__ = "snowstorm-alfredosalata"
__copyright__ = "snowstorm-alfredosalata"
__license__ = "MIT"


def test_from_valid_json_succeeds():
    """API Tests"""
    valid_api = {
        "path": "some/path.txt",
        "content": "some_content",
        "fs": {
            "fs": "s3",
            "endpoint_url": "https://s3-eu-north-1.amazonaws.com",
            "access_key_id": "some key",
            "secret_access_key": "some access secret",
            "bucket_name": "some-bucket",
            "region_name": "eu-north-1"
        }
    }
    api: Api = WriteDocumentApiSchema().load(valid_api)
    assert api.fs.adapter.__class__ == s3.S3FilesystemAdapter
    
    valid_api = {
        "path": "some/path.txt",
        "fs": {
            "fs": "s3",
            "endpoint_url": "https://s3-eu-north-1.amazonaws.com",
            "access_key_id": "some key",
            "secret_access_key": "some access secret",
            "bucket_name": "some-bucket",
            "region_name": "eu-north-1"
        }
    }
    api: Api = ReadDocumentApiSchema().load(valid_api)
    assert api.fs.adapter.__class__ == s3.S3FilesystemAdapter

def test_from_invalid_json_fails():
    invalid_json = {
        "fs": "s3",
        "endpoint_url": "https://someurl.com",
        "access_key_id": "some_key"
    }
    
    with pytest.raises(ValidationError):
        FsSchema().load(invalid_json)
    
    invalid_json = {
        "fs": "non-existing-fs",
        "endpoint_url": "https://s3-eu-north-1.amazonaws.com",
        "access_key_id": "some key",
        "secret_access_key": "some access secret",
        "bucket_name": "some-bucket",
        "region_name": "eu-north-1"
    }
    
    with pytest.raises(NotImplementedError):
        FsSchema().load(invalid_json)