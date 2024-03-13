from flysystem.filesystem import Filesystem as FlyFilesystem
from flysystem.adapters import s3

class Filesystem(FlyFilesystem):
    """
    A simple wrapper over the `flysystem` Filesystem interface.
    Contains helper methods to set up Filesystems with various adapter.
    """
    
    @staticmethod
    def from_json(json: dict) -> 'Filesystem':
        """
        Constructs a Filesystem object from JSON data.

        Args:
            json (dict): JSON data.

        Raises:
            NotImplementedError: When the supplied `json['fs']` is not a valid filesystem type.
                Currently only `s3` is accepted.
                
            AssertionError: When the supplied parameter do not match the requirements for the corresponding `fs`.

        Returns:
            Filesystem: The constructed Filesystem interface, wrapping over the underlying filesystem adapter.
        """
        fs = json.get("fs")
        
        assert fs, "Must specify a filesystem!"
        params: dict = json.get("params")
        
        match fs:
            case "s3":
                return Filesystem._s3_from_json(params)
            case _:
                raise NotImplementedError
    
    @staticmethod
    def _s3_from_json(json: dict) -> 'Filesystem':
        """
        Constructs a Filesystem with a Amazon AWS S3 Adapter.
        """
        assert json.get("endpoint_url"), "Filesystem S3 requires endpoint_url!"
        assert json.get("access_key_id"), "Filesystem S3 requires access_key_id!"
        assert json.get("secret_access_key"), "Filesystem S3 requires secret_access_key!"
        assert json.get("bucket_name"), "Filesystem S3 requires bucket_name!"
        assert json.get("region_name"), "Filesystem S3 requires region_name!"
        
        adapter = s3.S3FilesystemAdapter(**json)
        return Filesystem(adapter)
        