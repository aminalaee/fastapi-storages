from typing import Optional

import pytest
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session, declarative_base

from sqlalchemy_fields.types import EmailType
from tests.engine import database_uri

Base = declarative_base()
engine = create_engine(database_uri)


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    email = Column(EmailType())


@pytest.fixture(autouse=True)
def prepare_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.mark.parametrize("email", [None, "me@aminalaee.dev"])
def test_valid_email(email: Optional[str]) -> None:
    model = Model(email=email)

    with Session(engine) as session:
        session.add(model)
        session.commit()

        assert model.email == email


@pytest.mark.parametrize("email", ["", "me@domain.fake", "aminalaee.dev"])
def test_invalid_email(email: str) -> None:
    model = Model(email=email)

    with Session(engine) as session:
        session.add(model)

        with pytest.raises(StatementError):
            session.commit()
