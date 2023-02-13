import os
import re
from pathlib import Path
from typing import BinaryIO

from sqlalchemy_fields.storages.base import BaseStorage

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")


class FileSystemStorage(BaseStorage):
    """
    File system storage which stores files in the local filesystem.
    You might want to use this with the `FileType` type.
    """

    default_chunk_size = 64 * 1024

    def __init__(self, path: str):
        self._path = Path(path)
        if not self._path.exists():
            self._path.mkdir()

    def get_name(self, name: str) -> str:
        """
        Get the normalized name of the file.
        """
        return secure_filename(name)

    def get_path(self, name: str) -> str:
        """
        Get full path to the file.
        """
        return str(self._path / Path(name))

    def get_size(self, name: str) -> int:
        """
        Get file size in bytes.
        """
        return (self._path / name).stat().st_size

    def open(self, name: str) -> BinaryIO:
        """
        Open a file handle of the file object in binary mode.
        """
        path = self._path / Path(name)
        return open(path, "rb")

    def write(self, file: BinaryIO, name: str) -> None:
        """
        Write input file which is opened in binary mode to destination.
        """
        filename = secure_filename(name)
        path = self._path / Path(filename)

        file.seek(0, 0)
        with open(path, "wb") as output:
            while True:
                chunk = file.read(self.default_chunk_size)
                if not chunk:
                    break
                output.write(chunk)


def secure_filename(filename: str) -> str:
    """
    From Werkzeug secure_filename.
    """
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")

    normalized_filename = _filename_ascii_strip_re.sub("", "_".join(filename.split()))
    filename = str(normalized_filename).strip("._")
    return filename
