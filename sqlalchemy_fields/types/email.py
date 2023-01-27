from typing import Any

from email_validator import validate_email, EmailNotValidError
from sqlalchemy import types
from sqlalchemy.engine.interfaces import Dialect

from sqlalchemy_fields.exceptions import ValidationException


class Email(types.TypeDecorator):
    """
    Email type with validation using email-validator package.
    """

    impl = types.Unicode
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Dialect) -> None:
        if value is None:
            return value

        try:
            return validate_email(value).email
        except EmailNotValidError as exc:
            raise ValidationException(f"Invalid Email: {value}") from exc
