from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Any, Optional, Union

from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy.types import CHAR, TypeDecorator

from sqlalchemy_fields.exceptions import ValidationException

IPAddress_TYPE = Union[IPv4Address, IPv6Address]


class IPAddressType(TypeDecorator):
    """
    IPAddress type supporting both IPv4 and IPv6
    using standard library's ipaddress module.
    Uses PostgreSQL's INET type, otherwise uses CHAR(39), storing as string values.

    ???+ usage
        ```python
        from sqlalchemy_fields.types import IPAddressType

        class Example(Base):
            __tablename__ = "example"

            id = Column(Integer, primary_key=True)
            ip = Column(IPAddressType())
        ```
    """

    def __init__(self, length: int = 39, *args: Any, **kwargs: Any) -> None:
        self.length = length
        super().__init__(*args, **kwargs)

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine:
        if dialect.name == "postgresql":
            return dialect.type_descriptor(postgresql.INET())
        else:
            return dialect.type_descriptor(CHAR(self.length))

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if value is None:
            return value

        try:
            return str(ip_address(value))
        except ValueError as exc:
            raise ValidationException(f"Invalid IPAddress: {value}") from exc

    def process_result_value(
        self, value: Any, dialect: Dialect
    ) -> Optional[IPAddress_TYPE]:
        if value is None:
            return value

        return ip_address(value)
