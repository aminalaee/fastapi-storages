from typing import Any, Optional

from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.types import TypeDecorator, Unicode

from sqlalchemy_fields.storages.base import BaseStorage, StorageFile


class FileType(TypeDecorator):
    """
    File type to be used with Storage classes. Stores the file path in the column.

    ???+ usage
        ```python
        from sqlalchemy_fields.storages import FileSystemStorage
        from sqlalchemy_fields.types import FileType

        class Example(Base):
            __tablename__ = "example"

            id = Column(Integer, primary_key=True)
            file = Column(FileType(storage=FileSystemStorage(path="/tmp")))
        ```
    """

    impl = Unicode
    cache_ok = True

    def __init__(self, storage: BaseStorage, *args: Any, **kwargs: Any) -> None:
        self.storage = storage
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if value is None:
            return value
        if len(value.file.read(1)) != 1:
            return None

        file = StorageFile(name=value.filename, storage=self.storage)
        file.write(file=value.file)

        value.file.close()
        return file.name

    def process_result_value(
        self, value: Any, dialect: Dialect
    ) -> Optional[StorageFile]:
        if value is None:
            return value

        return StorageFile(name=value, storage=self.storage)
