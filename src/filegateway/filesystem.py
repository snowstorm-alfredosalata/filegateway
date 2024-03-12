from flysystem.filesystem import Filesystem as FlyFilesystem, FilesystemAdapter
from flysystem.adapters import s3

class Filesystem(FlyFilesystem):
    def from_json(json: dict) -> Filesystem:
        fs = json.get("fs")
        
        assert fs, "Must specify a filesystem!"
        
        match fs:
            case "s3":
                return Filesystem._s3_from_json(json)
            case _:
                raise NotImplementedError
    
    def _s3_from_json(json: dict) -> this:
        assert json.get("endpoint_url"), "Filesystem S3 requires endpoint_url!"
        assert json.get("access_key_id"), "Filesystem S3 requires access_key_id!"
        assert json.get("secret_access_key"), "Filesystem S3 requires secret_access_key!"
        assert json.get("bucket_name"), "Filesystem S3 requires bucket_name!"
        assert json.get("region_name"), "Filesystem S3 requires region_name!"
        
        adapter = s3.S3FilesystemAdapter(**json)
        return Filesystem(adapter)
        