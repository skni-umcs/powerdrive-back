from pydantic import BaseModel, EmailStr, ValidationError, validator, root_validator
import json


class FileMetadataBase(BaseModel):
    filename: str
    path: str

    # type: str
    # size: int
    # is_dir: bool | None = None

    # is_deleted: bool

    @validator('path')
    # @classmethod
    def check_path(cls, v):
        if v[0] != '/':
            raise ValueError('Path must start with /')
        return v

    @validator('path')
    # @classmethod
    def check_path_and_filename(cls, v, values, **kwargs):
        if not v.endswith(values['filename']):
            raise ValueError('Filename must be in path')
        return v
    #
    # @validator('size')
    # # @classmethod
    # def check_size(cls, v):
    #     if v < 0:
    #         raise ValueError('Size must be positive')
    #     return v


class FileMetadataCreate(FileMetadataBase):
    pass

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class FileMetadataUpdate(FileMetadataCreate):
    id: int


class FileMetadataInDB(FileMetadataBase):
    id: int
    path: str
    type: str
    # is_deleted: bool
    user_id: int

    class Config:
        orm_mode = True


class FileMetadata(FileMetadataBase):
    id: int
    type: str

    class Config:
        orm_mode = True
