## Working with custom types

In order to use the custom types you can easily include them in your
models the same way you use SQLAlchemy types.

For example:

```python
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy_fields.types import UUIDType

Base = declarative_base()
engine = create_engine("sqlite:///test.db")


class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType())
```

Each custom type will have a different storage,
even different based on database backend you are using.

So for example if you are using `UUIDType` with PostgreSQL then
it is already stored as UUID since this is supported by PostgreSQL,
and in other databases like SQLite and MySQL it is stored as `CHAR(32)`.

Some custom types like `EmailType` require third-party packages
for valdiation and you need to check that type's documentation at [API Reference](api_reference/types.md).

## Working with storages

If you're working with `FileType` or `ImageType` then you probably want to use a storage.
The storage backend determines how and where the file is stored, and only the path
of the file is stored in the database column.

There are two types of storages available:

- `FileSystemStorage`: To store files on the local file system.
- `S3Storage`: To store file objects in Amazon `S3` or any s3-compatible object storage.

### FileSystemStorage

An example to use `FileSystemStorage`:

```python
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy_fields.storages import FileSystemStorage
from sqlalchemy_fields.types import FileType

Base = declarative_base()
engine = create_engine("sqlite:///test.db")


class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    file = Column(FileType(storage=FileSystemStorage(path="/tmp")))
```

This will configure a `FileSystemStorage` to store files in the `/tmp` directory
and store the file path in `Example.file` column.

Now let's store some files, if you are already using `FastAPI` or `Starlette` you can
make use of `UploadFile`, otherwise you can just create a dataclass to have two attributes
called `file` and `filename`.

```python
import io
from typing import BinaryIO

from sqlalchemy.orm import Session

# from fastapi import UploadFile
# from starlette.datastructures import UploadFile
# Otherwise we can define it simply
class UploadFile:
    def __init__(self, file: BinaryIO, filename: str) -> None:
        self.file = file
        self.filename = filename


data = io.BytesIO(b"abc") # Or open a file in binary mode
upload_file = UploadFile(file=data, filename="example.txt")
example = Example(file=upload_file)

with Session(engine) as session:
    session.add(example)
    session.commit()
    print(example.file, type(example.file))

"""
/tmp/example.txt, <class 'sqlalchemy_fields.storages.StorageFile'>
"""
```

### S3Storage

For example let's say we have a bucket called `test` that we want to store all the files in:

```python
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy_fields.storages import S3Storage
from sqlalchemy_fields.types import FileType

Base = declarative_base()
engine = create_engine("sqlite:///test.db")


class AssetS3Storage(S3Storage):
    AWS_ACCESS_KEY_ID = "access"
    AWS_SECRET_ACCESS_KEY = "secret"
    AWS_S3_BUCKET_NAME = "test"
    AWS_S3_ENDPOINT_URL = "s3.amazonaws.com"
    AWS_S3_USE_SSL = False


class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    file = Column(FileType(storage=AssetS3Storage()))
```

You probably don't want to hard-code `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
in your code. Instead you have two options:

- Either set the same keys as environment variables
- Handle reading and setting them from any source on the `S3Storage` class

And that's it, the same examples of `FileSystemStorage` work with the difference that
the files will actually will be stored on the S3 bucket instead of the local filesystem.
