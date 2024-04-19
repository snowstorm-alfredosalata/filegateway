from io import BytesIO
import mimetypes
from fs import base
import base64

class FsTarget():
    """Main helper and executor class on Filegateway. May target a directory or a 
    file to any local o remote filesystem.

    Raises:
        ValueError: When performing an invalid target/operation 
        combinations (such as `list_contents` on a file, or `read` on a directory.)
    """

    fs: base.FS
    path: str
    content: bytes | None

    def __init__(self, fs: base.FS, path: str = "/", content: str | None = None):
        self.fs = fs
        self.path = self.fs.validatepath(path)

        if content is not None:
            self.content = base64.b64decode(content)

    def write(self):
        """Saves the file, overwriting existing items."""    
        if self.content is None:
            raise ValueError("Cannot write an empty content!")

        self.fs.writebytes(self.content)

    def read(self) -> BytesIO:
        """Reads the file and returns a :class:`BytesIO` stream."""
        if not self.is_file():
            raise ValueError(f"{self.path} is not a file!")
        
        return BytesIO(self.fs.readbytes(self.path))
    
    def guess_mime(self) -> str:
        """Attempts to guess mime from the filename."""
        return mimetypes.guess_type(self.path)[0] or "application/octet-stream"

    def get_fs_type(self) -> str:
        """Returns the underlying filesystem name."""
        return self.fs.__class__
    
    def is_dir(self) -> bool:
        return self.fs.isdir(self.path)
    
    def is_file(self) -> bool:
        return self.fs.isfile(self.path)

    def list_contents(self) -> str:
        """Lists the directory contents."""
        if not self.is_dir():
            raise ValueError(f"{self.path} is not a directory!")

        return self.fs.listdir(self.path)
 