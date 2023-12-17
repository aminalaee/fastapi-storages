import io
from pathlib import Path

import pytest
from peewee import AutoField, Model, SqliteDatabase

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.peewee import FileType
from tests.engine import database_name
from tests.test_integrations.utils import UploadFile

db = SqliteDatabase(database_name)


class Model(Model):
    id = AutoField(primary_key=True)
    file = FileType(storage=FileSystemStorage(path="/tmp"), null=True)

    class Meta:
        database = db


@pytest.fixture(autouse=True)
def prepare_database():
    db.create_tables([Model])
    yield
    db.drop_tables([Model])


def test_valid_file(tmp_path: Path) -> None:
    Model.file.storage = FileSystemStorage(path=str(tmp_path))

    input_file = tmp_path / "input.txt"
    input_file.write_bytes(b"123")

    upload_file = UploadFile(file=input_file.open("rb"), filename="example.txt")
    Model.create(file=upload_file)
    model = Model.get()

    assert model.file.name == "example.txt"
    assert model.file.size == 3
    assert model.file.path == str(tmp_path / "example.txt")


def test_nullable_file() -> None:
    model = Model(file=None)
    model.save()

    assert model.file is None


def test_clear_empty_file() -> None:
    upload_file = UploadFile(file=io.BytesIO(b""), filename="")
    Model.create(file=upload_file)

    model = Model.get()
    assert model.file is None
