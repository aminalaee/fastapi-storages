# SQLAlchemy Fields

[![PyPI - Version](https://img.shields.io/pypi/v/sqlalchemy-fields.svg)](https://pypi.org/project/sqlalchemy-fields)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sqlalchemy-fields.svg)](https://pypi.org/project/sqlalchemy-fields)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install sqlalchemy-fields
```

## Extra SQLAlchemy column types

- Email
- File
- IP
- URL
- UUID

```python
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy_fields.types import IPAddress

Base = declarative_base()
engine = create_engine("sqlite:///example.db")

class Example(Base):
    __tablename__ = "example"

    id = Column(Integer, primary_key=True)
    ip = Column(IPAddress)


example = Example(ip="127.0.0.1")
with Session(engine) as session:
    session.add(example)
    session.commit()
    print(example.ip)
"""
IPv4Address("127.0.0.1")
"""
```
