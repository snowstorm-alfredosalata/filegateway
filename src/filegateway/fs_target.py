from io import BytesIO
import mimetypes
from fs import base
import base64

class FsTarget():
    """Generic data object valid for all Api Calls.
    """
    fs: base.FS
    path: str
    content: bytes | None

    def __init__(self, fs: base.FS, path: str = "/", content: str | None = None):
        self.path = path
        self.fs = fs

        if content is not None:
            self.content = base64.b64decode(content)

    def write(self):
        if self.content is None:
            raise ValueError("Cannot write an empty content!")

        self.fs.writebytes(self.content)

    def read(self) -> BytesIO:
        if not self.is_file():
            raise ValueError(f"{self.path} is not a file!")
        
        return BytesIO(self.fs.readbytes(self.path))
    
    def guess_mime(self) -> str:
        return mimetypes.guess_type(self.path)[0] or "application/octet-stream"

    def get_fs_type(self) -> str:
        return self.fs.__class__
    
    def is_dir(self) -> bool:
        return self.fs.isdir(self.path)
    
    def is_file(self) -> bool:
        return self.fs.isfile(self.path)

    def list_contents(self) -> str:
        if not self.is_dir():
            raise ValueError(f"{self.path} is not a directory!")

        return self.fs.listdir(self.path)
 