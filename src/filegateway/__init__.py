from importlib.metadata import PackageNotFoundError, version 

from .document import Document
from .filesystem import Filesystem

try:
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
