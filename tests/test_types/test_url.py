from typing import Optional

import pytest
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session, declarative_base

from sqlalchemy_fields.types import URL
from tests.engine import database_uri

Base = declarative_base()
engine = create_engine(database_uri)


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    url = Column(URL)


@pytest.fixture(autouse=True)
def prepare_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.mark.parametrize(
    "url",
    [
        None,
        "http://aminalaee.dev",
        "https://aminalaee.dev",
        "ftp://aminalaee.dev",
        "ws://aminalaee.dev",
        "wss://aminalaee.dev",
        "wss://aminalaee.dev",
    ],
)
def test_valid_url(url: Optional[str]) -> None:
    model = Model(url=url)

    with Session(engine) as session:
        session.add(model)
        session.commit()

        assert model.url == url


@pytest.mark.parametrize(
    "url",
    [
        "",
        "me@aminalaee.dev",
        "aminalaee.dev",
        "file::aminalaee.dev",
        "mailto:me@aminalaee.dev",
        "aminalaee?.dev",
        "http:///aminalaee.dev",
        "http://[aminalaee.dev",
    ],
)
def test_invalid_url(url: str) -> None:
    model = Model(url=url)

    with Session(engine) as session:
        session.add(model)

        with pytest.raises(StatementError):
            session.commit()


@pytest.mark.parametrize(
    "url",
    [
        "http://aminalaee.dev/#",
        "HTTP://aminalaee.dev/",
    ],
)
def test_sanitize_url(url: str) -> None:
    model = Model(url=url)

    with Session(engine) as session:
        session.add(model)
        session.commit()

        assert model.url == "http://aminalaee.dev/"
