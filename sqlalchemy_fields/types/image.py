from typing import Any, Optional

from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.types import TypeDecorator, Unicode

try:
    from PIL import Image, UnidentifiedImageError

    PIL = True
except ImportError:  # pragma: no cover
    PIL = False

from sqlalchemy_fields.exceptions import ValidationException
from sqlalchemy_fields.storages.base import BaseStorage, StorageImage


class ImageType(TypeDecorator):
    """
    Image type using `PIL` package to be used with Storage classes.
    Stores the image path in the column.

    ???+ usage
        ```python
        from sqlalchemy_fields.storages import FileSystemStorage
        from sqlalchemy_fields.types import ImageType

        class Example(Base):
            __tablename__ = "example"

            id = Column(Integer, primary_key=True)
            image = Column(ImageType(storage=FileSystemStorage(path="/tmp")))
        ```
    """

    impl = Unicode
    cache_ok = True

    def __init__(self, storage: BaseStorage, *args: Any, **kwargs: Any) -> None:
        assert PIL is True, "'Pillow' package is required."

        self.storage = storage
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if value is None:
            return value
        if len(value.file.read(1)) != 1:
            return None

        try:
            image_file = Image.open(value.file)
            image_file.verify()
        except UnidentifiedImageError:
            raise ValidationException("Invalid image file")

        image = StorageImage(
            name=value.filename,
            storage=self.storage,
            height=image_file.height,
            width=image_file.width,
        )
        image.write(file=value.file)

        image_file.close()
        value.file.close()
        return image.name

    def process_result_value(
        self, value: Any, dialect: Dialect
    ) -> Optional[StorageImage]:
        if value is None:
            return value

        image = Image.open(self.storage.get_path(value))
        return StorageImage(
            name=value, storage=self.storage, height=image.height, width=image.width
        )
