import os
from pathlib import Path
from typing import BinaryIO

try:
    import boto3
except ImportError:
    boto3 = None

from sqlalchemy_fields.storages.base import BaseStorage
from sqlalchemy_fields.storages.utils import secure_filename


class S3Storage(BaseStorage):
    """
    Amazon S3 or any S3 compatible storage backend.
    You might want to use this with the `FileType` type.
    """

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    AWS_S3_BUCKET_NAME = ""
    AWS_S3_ENDPOINT_URL = ""
    AWS_S3_USE_SSL = True

    def __init__(self) -> None:
        assert boto3 is not None, "'boto3' is not installed"

        self._s3 = boto3.resource(
            "s3", endpoint_url=self.AWS_S3_ENDPOINT_URL, use_ssl=self.AWS_S3_USE_SSL
        )
        self._bucket = self._s3.create_bucket(Bucket=self.AWS_S3_BUCKET_NAME)

    def get_name(self, name: str) -> str:
        """
        Get the normalized name of the file.
        """

        return secure_filename(Path(name).name)

    def get_path(self, name: str) -> str:
        """
        Get full URL to the file.
        """

        url = f"{self.AWS_S3_ENDPOINT_URL}/{self.AWS_S3_BUCKET_NAME}"
        path = Path(name)
        if len(path.parents) > 1:
            url += f"/{path.parent}"

        url += f"/{secure_filename(path.name)}"
        return url

    def get_size(self, name: str) -> int:
        """
        Get file size in bytes.
        """

        key = secure_filename(Path(name).name)
        return self._bucket.Object(key).content_length

    def write(self, file: BinaryIO, name: str) -> None:
        """
        Write input file which is opened in binary mode to destination.
        """

        file.seek(0, 0)
        key = secure_filename(Path(name).name)
        self._bucket.upload_fileobj(file, key)
