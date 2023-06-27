## Working with storages

Often in projects, you want to get input file in the API and store it somewhere.
The `fastapi-storages` simplifies the process to store and retrieve the files
in a re-usable manner.

There are two  storages available:

- `FileSystemStorage`: To store files on the local file system.
- `S3Storage`: To store file objects in Amazon `S3` or any s3-compatible object storage.

### FileSystemStorage

A very minimal example to use `FileSystemStorage`:

```python
from fastapi import FastAPI, UploadFile
from fastapi_storages import FileSystemStorage


app = FastAPI()
storage = FileSystemStorage(path="/tmp")


@app.post("/upload/")
def create_upload_file(file: UploadFile):
    storage.write(file)
```

This will configure a `FileSystemStorage` to store files in the `/tmp` directory
and the request file is automatically saved into the destination.

### S3Storage

Now let's see a minimal example of using `S3Storage` in action:

```python
from fastapi import FastAPI, UploadFile
from fastapi_storages import S3Storage


class PublicAssetS3Storage(S3Storage):
    AWS_ACCESS_KEY_ID = "access"
    AWS_SECRET_ACCESS_KEY = "secret"
    AWS_S3_BUCKET_NAME = "test"
    AWS_S3_ENDPOINT_URL = "s3.amazonaws.com"
    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_USE_SSL = True


app = FastAPI()
storage = PublicAssetS3Storage()


@app.post("/upload/")
def create_upload_file(file: UploadFile):
    storage.write(file)
```

As you can see the code is not changed and `storage.write(file)` is called the same way
it was used in `FileSystemStorage`.

!!! warning
    You should never hard-code credentials like `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in the code.
    Instead, you can read values from environment variables or as a handy way, `fastapi-storages` will use the environment variables automatically, if they are defined.

## Working with ORM extensions

The example you saw was useful, but `fastapi-storages` has ORM integrations
which makes storing and serving the files easier.

Support ORM include:

- `SQLAlchemy`
- `SQLAdmin`

### SQLAlchemy

You can use custom `SQLAlchemy` types from `fastapi-storages` for this.

Supported types include:

- `FileType`
- `ImageType`

Let's see an example:

```python
from fastapi import FastAPI, UploadFile
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType

app = FastAPI()
Base = declarative_base()
engine = create_engine("sqlite:///test.db")


class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    file = Column(FileType(storage=FileSystemStorage(path="/tmp")))


# Create database and table
Base.metadata.create_all(engine)


@app.post("/upload/")
def create_upload_file(file: UploadFile):
    example = Example(file=file)
    with Session(engine) as session:
        session.add(example)
        session.commit()
        return {"filename": example.file.name}
```

As you can see the API `create_upload_file` has changed compared to using the storage directly.

You don't need the `storage.write(...)` call anymore.
With the custom SQLAlchemy types, before the model is saved in database,
the file is stored in the specified storage and then the record is saved.

You can just replace the storage with `S3Storage` and everything works without the change.
This will make your code cleaner and more readable.
