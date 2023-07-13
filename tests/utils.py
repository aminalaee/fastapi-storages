from fastapi_storages import FileSystemStorage


class NonOverwritingFileSystemStorage(FileSystemStorage):
        OVERWRITE_EXISTING_FILES = False