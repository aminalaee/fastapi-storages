from typing import Any, Optional

from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.types import TypeDecorator, Unicode

from sqlalchemy_fields.storages.base import BaseStorage, StorageFile


class File(TypeDecorator):
    """
    File type to be used with FileSystemStorage.
    Stores the file path in the column.
    """

    impl = Unicode
    cache_ok = True

    def __init__(self, storage: BaseStorage, *args: Any, **kwargs: Any) -> None:
        self.storage = storage
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if value is None:
            return value

        file = StorageFile(name=value.filename, storage=self.storage)
        file.write(file=value.file)
        return file.name

    def process_result_value(
        self, value: Any, dialect: Dialect
    ) -> Optional[StorageFile]:
        if value is None:
            return value

        return StorageFile(name=value, storage=self.storage)
