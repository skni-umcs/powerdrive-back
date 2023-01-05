from src.files.schemas import FileMetadataCreate, FileMetadataUpdate
from src.files.models import dbFileMetadata

from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.config import Settings


def save_file(file_data: bytes, file_name: str) -> str:
    settings = Settings()
    file_data = file_data.decode('utf-8')
    file_path = settings.base_file_path + file_name

    with open(file_path, "b") as file:
        file.write(file_data)
    return file_path


def add(db: Session, file_data: UploadFile, file_meta: FileMetadataCreate) -> dbFileMetadata:
    file_metadata_in_db: dbFileMetadata = dbFileMetadata(**file_meta.dict())

    file_metadata_in_db.path = save_file(file_data.file.read(), file_data.filename)
    db.add(file_metadata_in_db)
    db.commit()
    return file_metadata_in_db


def get_by_index(db: Session, file_id: int):
    return db.query(dbFileMetadata).filter(dbFileMetadata.id == file_id).first()


def update(db: Session, file_id: int, file_meta: FileMetadataUpdate) -> dbFileMetadata:
    file_metadata_in_db: dbFileMetadata = get_by_index(db, file_id)
    file_metadata_in_db.update(file_meta.dict())
    db.commit()
    db.refresh(file_metadata_in_db)
    return file_metadata_in_db


def delete_by_index(db: Session, file_id: int):
    file_metadata_in_db: dbFileMetadata = get_by_index(db, file_id)
    db.delete(file_metadata_in_db)
    db.commit()
