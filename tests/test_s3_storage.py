import os
from pathlib import Path

import boto3
from moto import mock_s3

from fastapi_storages import S3Storage

os.environ["MOTO_S3_CUSTOM_ENDPOINTS"] = "http://custom.s3.endpoint"


class PrivateS3Storage(S3Storage):
    AWS_ACCESS_KEY_ID = "access"
    AWS_SECRET_ACCESS_KEY = "secret"
    AWS_S3_BUCKET_NAME = "bucket"
    AWS_S3_ENDPOINT_URL = "custom.s3.endpoint"
    AWS_S3_USE_SSL = False


@mock_s3
def test_s3_storage_methods(tmp_path: Path) -> None:
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="bucket")

    tmp_file = tmp_path / "example.txt"
    tmp_file.write_bytes(b"123")

    storage = PrivateS3Storage()

    assert storage.get_name("test (1).txt") == "test_1.txt"
    assert (
        storage.get_path("test (1).txt")
        == "http://custom.s3.endpoint/bucket/test_1.txt"
    )
    assert (
        storage.get_path("a/test.txt") == "http://custom.s3.endpoint/bucket/a/test.txt"
    )
    assert (
        storage.get_path("a/b/c/test.txt")
        == "http://custom.s3.endpoint/bucket/a/b/c/test.txt"
    )

    storage.write(tmp_file.open("rb"), "example.txt")
    assert storage.get_size("example.txt") == 3


@mock_s3
def test_s3_storage_querystring_auth(tmp_path: Path) -> None:
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="bucket")

    tmp_file = tmp_path / "example.txt"
    tmp_file.write_bytes(b"123")

    class TestStorage(PrivateS3Storage):
        AWS_QUERYSTRING_AUTH = True

    storage = TestStorage()

    assert storage.get_path("test.txt").startswith(
        "http://custom.s3.endpoint/bucket/test.txt?"
    )
    assert storage.get_path("test.txt").count("AWSAccessKeyId=access") == 1
    assert storage.get_path("test.txt").count("Signature=") == 1
    assert storage.get_path("test.txt").count("Expires=") == 1


@mock_s3
def test_s3_storage_custom_domain(tmp_path: Path) -> None:
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="bucket")

    tmp_file = tmp_path / "example.txt"
    tmp_file.write_bytes(b"123")

    class TestStorage(PrivateS3Storage):
        AWS_S3_CUSTOM_DOMAIN = "s3.fastapi.storages"

    storage = TestStorage()

    assert storage.get_path("test.txt") == "http://s3.fastapi.storages/test.txt"


@mock_s3
def test_s3_storage_duplicate_file_names(tmp_path: Path) -> None:
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket="bucket")

    tmp_file = tmp_path / "duplicate.txt"
    tmp_file.write_bytes(b"123")

    class TestStorage(PrivateS3Storage):
        AWS_S3_CUSTOM_DOMAIN = "s3.fastapi.storages"

    storage = TestStorage(overwrite_existing_files=False)

    key1 = storage.write(tmp_file.open("rb"), "duplicate.txt")
    key2 = storage.write(tmp_file.open("rb"), "duplicate.txt")
    key3 = storage.write(tmp_file.open("rb"), "duplicate.txt")

    assert key1 == "duplicate.txt"
    assert key2 == "duplicate_1.txt"
    assert key3 == "duplicate_2.txt"

    assert Path(storage.get_path("duplicate_2.txt")) == Path("http://s3.fastapi.storages/duplicate_2.txt")
