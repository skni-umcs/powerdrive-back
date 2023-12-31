from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, ValidationError, validator, root_validator
import json


class FileMetadataBase(BaseModel):
    # filename: str
    path: str
    is_dir: bool = False

    @validator('path')
    # @classmethod
    def check_path(cls, v):
        if len(v) > 2500:
            raise ValueError('Path is too long')

        if v == '/':
            return v

        if v[0] != '/':
            raise ValueError('Path must start with /')

        if v[-1] == '/':
            raise ValueError('Path must not end with /')

        if '//' in v:
            raise ValueError('Path must not contain multiple slashes')

        if '..' in v:
            raise ValueError('Path must not contain ..')

        return v

    # chcek if path contains filename and if it is directory
    # @root_validator()
    # def check_path_and_filename(cls, values):
    #     path: str = values.get('path')
    #     filename = values.get('filename')
    #     is_dir = values.get('is_dir')
    #     if is_dir and not path.endswith(filename):
    #         raise ValueError('Path for dir must end with dirname')
    #     # if not is_dir and path.endswith(filename):
    #     # raise ValueError('Path must not end with filename')
    #     return values

    # replace multiple slashes with one


class FileMetadataCreate(FileMetadataBase):
    pass

    # don try change this:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    # don try change this:
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class FileMetadataUpdate(FileMetadataBase):
    filename: str
    id: int


class FileMetadataInDB(FileMetadataBase):
    id: int
    filename: str
    path: str
    type: str
    is_deleted: bool
    user_id: int

    class Config:
        orm_mode = True


class FileMetadata(FileMetadataBase):
    id: int
    filename: str
    type: str
    size: int
    last_modified: datetime
    # is_deleted: bool = False

    class Config:
        orm_mode = True


class OnlyDirectory(FileMetadata):
    # TODO fix in swagger
    children: list[OnlyDirectory] = []

    class Config:
        orm_mode = True
