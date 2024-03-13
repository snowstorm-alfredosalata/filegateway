import pytest

from flysystem.adapters import s3
from filegateway.filesystem import Filesystem

__author__ = "snowstorm-alfredosalata"
__copyright__ = "snowstorm-alfredosalata"
__license__ = "MIT"


def test_from_valid_json_succeeds():
    """API Tests"""
    valid_json = {
        "fs": "s3",
        "params": {
            "endpoint_url": "https://s3-eu-north-1.amazonaws.com",
            "access_key_id": "some key",
            "secret_access_key": "some access secret",
            "bucket_name": "some-bucket",
            "region_name": "eu-north-1"
        }
    }
    
    fs = Filesystem.from_json(valid_json)
    
    assert fs.adapter.__class__ == s3.S3FilesystemAdapter

def test_from_invalid_json_fails():
    invalid_json = {
        "fs": "s3",
        "params": {
            "endpoint_url": "https://someurl.com",
            "access_key_id": "some_key",
        }
    }
    
    with pytest.raises(AssertionError):
        Filesystem.from_json(invalid_json)
    
    invalid_json = {
        "fs": "bogus_fs",
        "params": {
            "endpoint_url": "https://someurl.com",
            "access_key_id": "some_key",
        }
    }
    
    with pytest.raises(NotImplementedError):
        Filesystem.from_json(invalid_json)