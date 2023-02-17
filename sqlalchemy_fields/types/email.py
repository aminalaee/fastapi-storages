from typing import Any

try:
    import email_validator
except ImportError:
    email_validator = None
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.types import TypeDecorator, Unicode

from sqlalchemy_fields.exceptions import ValidationException


class EmailType(TypeDecorator):
    """
    Email type with validation using `email-validator` package.

    ???+ usage
        ```python
        from sqlalchemy_fields.types import EmailType

        class Example(Base):
            __tablename__ = "example"

            id = Column(Integer, primary_key=True)
            email = Column(EmailType())
            billing_email = Column(EmailType(length=128))
        ```
    """

    impl = Unicode
    cache_ok = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        assert email_validator is not None, "'email_validator' package is required."
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: Any, dialect: Dialect) -> None:
        if value is None:
            return value

        try:
            return email_validator.validate_email(value).email
        except email_validator.EmailNotValidError as exc:
            raise ValidationException(f"Invalid Email: {value}") from exc
