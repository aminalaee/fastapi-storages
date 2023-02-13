import uuid
from typing import Any, Optional

from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy.types import CHAR, TypeDecorator


class UUIDType(TypeDecorator):
    """Platform-independent UUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(32),
    storing as stringified hex values.

    Accepts both string and UUID objects as input.

    ???+ usage
        ```python
        from sqlalchemy_fields.types import UUIDType

        class Example(Base):
            __tablename__ = "example"

            id = Column(Integer, primary_key=True)
            uuid = Column(UUIDType())
        ```
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine:
        if dialect.name == "postgresql":
            return dialect.type_descriptor(postgresql.UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if value is None:
            return value

        if dialect.name == "postgresql":
            return str(value)
        else:
            if isinstance(value, uuid.UUID):
                return value.hex
            else:
                return uuid.UUID(value).hex

    def process_result_value(self, value: Any, dialect: Dialect) -> Optional[uuid.UUID]:
        if value is None:
            return value

        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)
