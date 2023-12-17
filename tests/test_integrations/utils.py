from typing import BinaryIO


class UploadFile:
    """
    Dummy UploadFile like the one in Starlette.
    """

    def __init__(self, file: BinaryIO, filename: str) -> None:
        self.file = file
        self.filename = filename
