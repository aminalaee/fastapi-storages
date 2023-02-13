from typing import Any
from urllib.parse import urlparse

from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.types import TypeDecorator, Unicode

from sqlalchemy_fields.exceptions import ValidationException


class URLType(TypeDecorator):
    """
    URL type with validation using Python standard library.

    ???+ usage
        ```python
        from sqlalchemy_fields.types import URLType

        class Example(Base):
            __tablename__ = "example"

            id = Column(Integer, primary_key=True)
            url = Column(URLType())
            website = Column(URLType(length=1024))
        ```
    """

    impl = Unicode
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Dialect) -> None:
        if value is None:
            return value

        try:
            parsed_result = urlparse(value)
        except ValueError:
            raise ValidationException(f"Invalid URL: {value}")

        if parsed_result.scheme and parsed_result.netloc:
            return parsed_result.geturl()

        raise ValidationException(f"Invalid URL: {value}")
