# import tempfile
# from typing import BinaryIO

# import boto3

# from sqlalchemy_fields.storages.base import BaseStorage


# class S3Storage(BaseStorage):
#     default_chunk_size = 64 * 1024
#     default_spool_size = 1024 * 1024

#     access_key_id = ""
#     secret_access_key_id = ""
#     bucket_name = ""
#     region_name = ""
#     url_protocol = "https"
#     endpoint_url = ""

#     def __init__(self, bucket: str):
#         self._bucket = bucket
#         self._client = boto3.client("s3")

#     def get_name(self, name: str) -> str:
#         return ""

#     def get_path(self, name: str) -> str:
#         url = f"{self.url_protocol}://{self.custom_domain}/{name}"
#         return url

#     def get_size(self, name: str) -> int:
#         response = self._client.head_object(Bucket=self._bucket, Key=name)
#         return response["ContentLength"]

#     def open(self, name: str) -> BinaryIO:
#         file = tempfile.SpooledTemporaryFile(max_size=self.default_spool_size)
#         return self._client.download_fileobj(self._bucket, name, file)

#     def write(self, file: BinaryIO, name: str) -> str:
#         file.seek(0, 0)
#         self._client.upload_fileobj(file, self._bucket, name)

#         return self.get_path(name)
