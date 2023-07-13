from pathlib import Path

from fastapi_storages import FileSystemStorage, StorageFile, StorageImage
from tests.utils import NonOverwritingFileSystemStorage


def test_filesystem_storage_file_properties(tmp_path: Path) -> None:
    tmp_file = tmp_path / "example.txt"
    tmp_file.write_bytes(b"123")

    storage = FileSystemStorage(path=tmp_path)
    file = StorageFile(name="example.txt", storage=storage)

    assert file.name == "example.txt"
    assert file.size == 3
    assert file.path == str(tmp_file)
    assert str(file).endswith(file.name)


def test_filesystem_storage_image_properties(tmp_path: Path) -> None:
    tmp_file = tmp_path / "example.txt"
    tmp_file.write_bytes(b"123")

    storage = FileSystemStorage(path=tmp_path)
    image = StorageImage(name="example.txt", storage=storage, height=1, width=1)

    assert image.height == 1
    assert image.width == 1


def test_filesystem_storage_file_read_write(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_bytes(b"123")

    storage = FileSystemStorage(path=tmp_path)
    file = StorageFile(name="example.txt", storage=storage)
    file.write(file=input_file.open("rb"))

    byte_data = file.open().read()

    assert byte_data == b"123"


def test_filesystem_storage_rename_file_names(tmp_path: Path) -> None:
    filename = "duplicate.txt"
    tmp_file = tmp_path / filename
    tmp_file.touch()

    storage = NonOverwritingFileSystemStorage(path=tmp_path)
    file1 = StorageFile(name=filename, storage=storage)
    file1.write(file=tmp_file.open("rb"))

    file2 = StorageFile(name="duplicate.txt", storage=storage)
    file2.write(file=tmp_file.open("rb"))

    file3 = StorageFile(name="duplicate.txt", storage=storage)
    file3.write(file=tmp_file.open("rb"))

    assert file1.name == "duplicate_1.txt"
    assert file2.name == "duplicate_2.txt"
    assert file3.name == "duplicate_3.txt"

    assert Path(file1.path) == tmp_path / "duplicate_1.txt"
    assert Path(file2.path) == tmp_path / "duplicate_2.txt"
    assert Path(file3.path) == tmp_path / "duplicate_3.txt"

