from typing import Any
from urllib.parse import urlparse

from sqlalchemy import types
from sqlalchemy.engine.interfaces import Dialect

from sqlalchemy_fields.exceptions import ValidationException


class URL(types.TypeDecorator):
    """
    URL type with validation.
    """

    impl = types.Unicode
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
