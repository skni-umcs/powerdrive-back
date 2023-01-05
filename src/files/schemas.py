from pydantic import BaseModel, EmailStr, ValidationError, validator
import json


class FileMetadataBase(BaseModel):
    name: str
    # path: str
    type: str
    size: int
    is_deleted: bool
    user_id: int


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

    class Config:
        orm_mode = True


class FileMetadata(FileMetadataBase):
    id: int

    class Config:
        orm_mode = True
