# SQLAlchemy Fields

<p align="center">
<a href="https://github.com/aminalaee/sqlalchemy-fields/actions">
    <img src="https://github.com/aminalaee/sqlalchemy-fields/workflows/Tests/badge.svg" alt="Build Status">
</a>
<a href="https://github.com/aminalaee/sqlalchemy-fields/actions">
    <img src="https://github.com/aminalaee/sqlalchemy-fields/workflows/Publish/badge.svg" alt="Publish Status">
</a>
<a href="https://codecov.io/gh/aminalaee/sqlalchemy-fields">
    <img src="https://codecov.io/gh/aminalaee/sqlalchemy-fields/branch/main/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/sqlalchemy-fields/">
    <img src="https://badge.fury.io/py/sqlalchemy-fields.svg" alt="Package version">
</a>
<a href="https://pypi.org/project/sqlalchemy-fields" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/sqlalchemy-fields.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://aminalaee.dev/sqlalchemy-fields](https://aminalaee.dev/sqlalchemy-fields)

**Source Code**: [https://github.com/aminalaee/sqlalchemy-fields](https://github.com/aminalaee/sqlalchemy-fields)

---

**Table of Contents**

- [Installation](#installation)
- [Custom Types](#custom-types)

## Installation

```console
pip install sqlalchemy-fields
pip install 'sqlalchemy-fields[full]'
```

## Custom Types

- `EmailType`
- `FileType`
- `ImageType`
- `IPAddressType`
- `URLType`
- `UUIDType`

```python
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy_fields.types import IPAddressType


Base = declarative_base()
engine = create_engine("sqlite:///example.db")


class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    ip = Column(IPAddressType)


example = Example(ip="127.0.0.1")
with Session(engine) as session:
    session.add(example)
    session.commit()
    print(example.ip)
"""
IPv4Address("127.0.0.1")
"""
```

## Storages

- `FileSystemStorage`
- `S3Storage`
