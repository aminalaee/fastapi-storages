import os

database_name = os.environ.get("TEST_DATABASE_NAME", "test.sqlite")
database_uri = os.environ.get("TEST_DATABASE_URI", "sqlite://")
