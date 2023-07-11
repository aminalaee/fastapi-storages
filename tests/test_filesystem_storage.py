from pathlib import Path

from fastapi_storages import FileSystemStorage, StorageFile, StorageImage


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


def test_filesystem_storage_duplicate_file_names(tmp_path: Path) -> None:
    import os
    filename = "duplicate.txt"
    base_file = filename.split('.')[0]

    tmp_file = tmp_path / filename
    tmp_file.write_bytes(b"123")
    
    base_path, ext = os.path.splitext(tmp_file)

    storage = FileSystemStorage(path=tmp_path, overwrite_existing_files=False)
    file1 = StorageFile(name=filename, storage=storage)
    file1.write(file=tmp_file.open("rb"))

    file2 = StorageFile(name=filename, storage=storage)
    file2.write(file=tmp_file.open("rb"))

    file3 = StorageFile(name=filename, storage=storage)
    file3.write(file=tmp_file.open("rb"))

    assert file1.name == f"{base_file}_1{ext}"
    assert file2.name == f"{base_file}_2{ext}"
    assert file3.name == f"{base_file}_3{ext}"

    assert file1.path == f"{str(base_path)}_1{ext}"
    assert file2.path == f"{str(base_path)}_2{ext}"
    assert file3.path == f"{str(base_path)}_3{ext}"

