import os
import re
from pathlib import Path
from typing import BinaryIO

from sqlalchemy_fields.storages.base import BaseStorage

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")


class FileSystemStorage(BaseStorage):
    default_chunk_size = 64 * 1024

    def __init__(self, path: str):
        self._path = Path(path)
        if not self._path.exists():
            self._path.mkdir()

    def get_name(self, name: str) -> str:
        return secure_filename(name)

    def get_path(self, name: str) -> str:
        return str(self._path / Path(name))

    def get_size(self, name: str) -> int:
        return (self._path / name).stat().st_size

    def open(self, name: str) -> BinaryIO:
        path = self._path / Path(name)
        return open(path, "rb")

    def write(self, file: BinaryIO, name: str) -> None:
        path = self._path / Path(secure_filename(name))

        if path.is_dir():
            return

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
