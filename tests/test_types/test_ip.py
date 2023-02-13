from ipaddress import IPv4Address, IPv6Address
from typing import Optional, Union

import pytest
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session, declarative_base

from sqlalchemy_fields.types import IPAddressType
from tests.engine import database_uri

Base = declarative_base()
engine = create_engine(database_uri)


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    ip = Column(IPAddressType)


@pytest.fixture(autouse=True)
def prepare_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_nullable_ip() -> None:
    model = Model(ip=None)

    with Session(engine) as session:
        session.add(model)
        session.commit()

        assert model.ip is None


@pytest.mark.parametrize(
    "ip",
    [
        "127.0.0.1",
        "2001:db8:3333:4444:5555:6666:7777:8888",
        IPv4Address("127.0.0.1"),
        IPv6Address("2001:db8:3333:4444:5555:6666:7777:8888"),
    ],
)
def test_valid_ip(ip: Optional[Union[str, IPv4Address, IPv6Address]]) -> None:
    model = Model(ip=ip)

    with Session(engine) as session:
        session.add(model)
        session.commit()

        assert str(model.ip) == str(ip)


@pytest.mark.parametrize(
    "ip",
    [
        "",
        "12345678",
        "255.255.255.256",
    ],
)
def test_invalid_ip(ip: str) -> None:
    model = Model(ip=ip)

    with Session(engine) as session:
        session.add(model)

        with pytest.raises(StatementError):
            session.commit()
