<p align="center">
<a href="https://github.com/aminalaee/fastapi-storages">
    <img width="500px" src="https://raw.githubusercontent.com/aminalaee/fastapi-storages/main/docs/assets/images/banner.png" alt"FastAPI_Storages">
</a>
</p>

<p align="center">
<a href="https://github.com/aminalaee/fastapi-storages/actions">
    <img src="https://github.com/aminalaee/fastapi-storages/workflows/Tests/badge.svg" alt="Build Status">
</a>
<a href="https://github.com/aminalaee/fastapi-storages/actions">
    <img src="https://github.com/aminalaee/fastapi-storages/workflows/Publish/badge.svg" alt="Publish Status">
</a>
<a href="https://codecov.io/gh/aminalaee/fastapi-storages">
    <img src="https://codecov.io/gh/aminalaee/fastapi-storages/branch/main/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi-storages/">
    <img src="https://badge.fury.io/py/fastapi-storages.svg" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi-storages" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi-storages.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

# FastAPI Storages

A collection of backend storages and ORM extensions to simplify file management in FastAPI and Starlette projects.

Similar to `django-storages` project, but aiming to work with a wider range of database ORMs and backends.

---

**Documentation**: [https://aminalaee.dev/fastapi-storages](https://aminalaee.dev/fastapi-storages)

**Source Code**: [https://github.com/aminalaee/fastapi-storages](https://github.com/aminalaee/fastapi-storages)

---

## Installation

```console
pip install fastapi-storages
pip install 'fastapi-storages[full]'
```

## Supported integrations

- `SQLAlchemy`
- `SQLModel`
- `SQLAdmin`

## Supported storage backends

- `FileSystemStorage`
- `S3Storage`

## Example

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

## Integration with Alembic

By default, these new types are not registered in Alembic's migrations. To integrate these new types with Alembic, one needs to follow:

### 1. Create new "type" on top of these types

Let's say, we create the following snippet in `custom_types.py`

```python
from fastapi_storages.integrations.sqlalchemy import FileType as _FileType
from fastapi_storages import FileSystemStorage

class FileType(_FileType):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(storage=FileSystemStorage(path='/tmp'), *args, **kwargs)
```

### 2. Add files path to `script.py.mako`

After using this type in any model's field, adding the following line to `alembic/script.py.mako` is enough to make migrations work.

```
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
import sqlalchemy as sa
from alembic import op
import path_to_custom_types_py_file
${imports if imports else ""}

# THE REST OF SCRIPT
```