from typing import BinaryIO


class BaseStorage:  # pragma: no cover
    def get_name(self, name: str) -> str:
        ...

    def get_path(self, name: str) -> str:
        ...

    def get_size(self, name: str) -> int:
        ...

    def open(self, name: str) -> BinaryIO:
        ...

    def write(self, file: BinaryIO, name: str) -> None:
        ...


class StorageFile:
    def __init__(self, *, name: str, storage: BaseStorage):
        self._name = name
        self._storage = storage

    @property
    def name(self) -> str:
        """File name including extension."""

        return self._storage.get_name(self._name)

    @property
    def path(self) -> str:
        """Complete file path."""

        return self._storage.get_path(self._name)

    @property
    def size(self) -> int:
        """File size in bytes."""

        return self._storage.get_size(self._name)

    def open(self) -> BinaryIO:
        """
        Open a file handle of the file.
        """

        return self._storage.open(self._name)

    def write(self, file: BinaryIO) -> None:
        """
        Write input file which is opened in binary mode to destination.
        """

        return self._storage.write(file=file, name=self._name)

    def __str__(self) -> str:
        return self.name
