from pathlib import Path

from sqlalchemy_fields.storages import FileSystemStorage, StorageFile


def test_filesystem_storage_file_properties(tmp_path: Path) -> None:
    tmp_file = tmp_path / "example.txt"
    tmp_file.write_bytes(b"123")

    storage = FileSystemStorage(path=tmp_path)
    file = StorageFile(name="example.txt", storage=storage)

    assert file.name == "example.txt"
    assert file.size == 3
    assert file.path == str(tmp_file)
    assert str(file) == file.name


def test_filesystem_storage_file_read_write(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_bytes(b"123")

    storage = FileSystemStorage(path=tmp_path)
    file = StorageFile(name="example.txt", storage=storage)
    file.write(file=input_file.open("rb"))

    byte_data = file.open().read()

    assert byte_data == b"123"
