import os
from pathlib import Path
from typing import BinaryIO

try:
    import boto3
except ImportError:  # pragma: no cover
    boto3 = None

from sqlalchemy_fields.storages.base import BaseStorage
from sqlalchemy_fields.storages.utils import secure_filename


class S3Storage(BaseStorage):
    """
    Amazon S3 or any S3 compatible storage backend.
    You might want to use this with the `FileType` type.
    Requires `boto3` to be installed.
    """

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    """AWS access key ID. Either set here or as an environment variable."""

    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    """AWS secret access key. Either set here or as an environment variable."""

    AWS_S3_BUCKET_NAME = ""
    """AWS S3 bucket name to use."""

    AWS_S3_ENDPOINT_URL = ""
    """AWS S3 endpoint URL."""

    AWS_S3_USE_SSL = True
    """Indicate if SSL should be used."""

    AWS_DEFAULT_ACL = ""
    """Optional ACL set on the object like `public-read`.
    By default file will be private."""

    def __init__(self) -> None:
        assert boto3 is not None, "'boto3' is not installed"
        assert not self.AWS_S3_ENDPOINT_URL.startswith(
            "http"
        ), "URL should not contain protocol"

        self._http_scheme = "https" if self.AWS_S3_USE_SSL else "http"
        self._url = f"{self._http_scheme}://{self.AWS_S3_ENDPOINT_URL}"
        self._s3 = boto3.resource(
            "s3",
            endpoint_url=self._url,
            use_ssl=self.AWS_S3_USE_SSL,
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
        )
        self._bucket = self._s3.Bucket(name=self.AWS_S3_BUCKET_NAME)

    def get_name(self, name: str) -> str:
        """
        Get the normalized name of the file.
        """

        filename = secure_filename(Path(name).name)
        return str(Path(name).with_name(filename))

    def get_path(self, name: str) -> str:
        """
        Get full URL to the file.
        """

        key = self.get_name(name)
        url = f"{self._url}/{self.AWS_S3_BUCKET_NAME}/{key}"
        return url

    def get_size(self, name: str) -> int:
        """
        Get file size in bytes.
        """

        key = self.get_name(name)
        return self._bucket.Object(key).content_length

    def write(self, file: BinaryIO, name: str) -> str:
        """
        Write input file which is opened in binary mode to destination.
        """

        file.seek(0, 0)
        key = self.get_name(name)
        self._bucket.upload_fileobj(file, key, ExtraArgs={"ACL": self.AWS_DEFAULT_ACL})
        return key
