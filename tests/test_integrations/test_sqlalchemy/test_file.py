import io
from pathlib import Path
from typing import BinaryIO

import pytest
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from tests.engine import database_uri

Base = declarative_base()
engine = create_engine(database_uri)


class UploadFile:
    """
    Dummy UploadFile like the one in Starlette.
    """

    def __init__(self, file: BinaryIO, filename: str) -> None:
        self.file = file
        self.filename = filename


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    file = Column(FileType(storage=FileSystemStorage(path="/tmp")))


@pytest.fixture(autouse=True)
def prepare_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_valid_file(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_bytes(b"123")

    upload_file = UploadFile(file=input_file.open("rb"), filename="example.txt")
    model = Model(file=upload_file)

    with Session(engine) as session:
        session.add(model)
        session.commit()

        assert model.file.name == "example.txt"
        assert model.file.size == 3
        assert Path(model.file.path) == Path("/tmp/example.txt")


def test_nullable_file() -> None:
    model = Model(file=None)

    with Session(engine) as session:
        session.add(model)
        session.commit()

        assert model.file is None


def test_clear_empty_file() -> None:
    upload_file = UploadFile(file=io.BytesIO(b""), filename="")
    model = Model(file=upload_file)

    with Session(engine) as session:
        session.add(model)
        session.commit()

        assert model.file is None
