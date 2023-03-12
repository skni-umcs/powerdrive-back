import shutil
from datetime import datetime
from pydantic import ValidationError

from src.files.exceptions import FileNotFoundException, FileAlreadyExistsException, DirException
from src.files.schemas import FileMetadataCreate, FileMetadataUpdate
from src.files.models import DbFileMetadata
from src.files.utilis import get_trash_dir_path, check_if_file_exists_in_db, \
    check_if_file_exists_in_disk, get_path_for_file, save_file_to_disk, get_and_creat_root_dir, \
    check_if_proper_dir_path, metadata_valid_with_extension

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from src.config import Settings

import os

import logging

logger = logging.getLogger(__name__)

settings = Settings()


def create_needed_dirs_in_db(db: Session, path: str, owner_id: int):
    """
    Create needed directories in db
    :param db: SQLAlchemy session
    :param path: path to file
    :param owner_id: id of user
    :return: None
    """
    # print(path)
    dir_list = path.split("/")[1:]

    previous_dir = get_and_creat_root_dir(db, owner_id)
    path = ""

    for directory in dir_list:
        path += "/" + directory
        name = directory

        if check_if_file_exists_in_db(db, path, owner_id):
            continue

        dir_metadata = DbFileMetadata(filename=name, path=path, type="DIR", owner_id=owner_id,
                                      size=0, is_dir=True,
                                      parent_id=previous_dir.id, last_modified=datetime.now())
        db.add(dir_metadata)
        db.commit()

        previous_dir = dir_metadata


def save_file_to_db(db: Session, filename: str, path: str, is_dir: bool, owner_id: int,
                    file_type: str, size: int) -> DbFileMetadata:
    # print(file_metadata_create.path.rsplit("/", 1)[0])
    parent_dir_name = path.rsplit("/", 1)[0]
    if parent_dir_name == "":
        parent_dir_name = "/"

    parent_dir = db.query(DbFileMetadata).filter(
        DbFileMetadata.path == parent_dir_name,
        DbFileMetadata.owner_id == owner_id).first()
    db_file = DbFileMetadata(filename=filename, path=path, is_dir=is_dir, type=file_type, size=size, owner_id=owner_id,
                             parent_id=parent_dir.id, last_modified=datetime.now())

    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def add_new_file_and_save_on_disk(db: Session, file_metadata_create: FileMetadataCreate, file_data: UploadFile | None,
                                  owner_id: int) -> DbFileMetadata:
    """
    Add new file to db and save
     it to disk
    :param db: SQLAlchemy session
    :param file_metadata_create: FileMetadataCreate object comes from request
    :param file_data: file data comes from request
    :param owner_id: id of user from JWT
    :return: DbFileMetadata object of new file
    """
    if file_data is None and not file_metadata_create.is_dir:
        raise HTTPException(status_code=409, detail="File data is None")

    if file_metadata_create.is_dir:
        create_needed_dirs_in_db(db, file_metadata_create.path, owner_id)
        return save_file_to_db(db, file_metadata_create, owner_id, "directory", 0)

    else:
        if check_if_file_exists_in_db(db, file_metadata_create.path, owner_id) or check_if_file_exists_in_disk(
                file_metadata_create.path, owner_id=owner_id):
            raise FileAlreadyExistsException("File already exists")

        if check_if_file_exists_in_disk(file_metadata_create.path, owner_id=owner_id):
            raise FileAlreadyExistsException(file_metadata_create.path)

        ## TODO is this needed?
        # if not metadata_valid_with_extension(file_metadata_create.filename, file_data.content_type):
        #     raise HTTPException(status_code=409, detail="File extension not correspond to file type")

        # if file_metadata_create.size == file_data.file.__sizeof__(): TODO enable this
        #     raise ValueError("File size is not equal to file size in metadata")

        # if check_if_not_enough_space(file_metadata_create.size, user_id=owner_id):
        #     raise OSError("Not enough space")

        size = save_file_to_disk(file_data, file_metadata_create.path, owner_id=owner_id)

        create_needed_dirs_in_db(db, file_metadata_create.path.rsplit('/', 1)[0], owner_id)

        db_file = save_file_to_db(db, filename=file_data.filename, path=file_metadata_create.path, owner_id=owner_id,
                                  file_type=file_data.content_type, size=size, is_dir=file_metadata_create.is_dir)

        return db_file


def get_file_metadata_by_id(db: Session, file_id: int, owner_id: int) -> DbFileMetadata:
    """
    Get file metadata from db
    :param db: SQLAlchemy session
    :param file_id: file id
    :param owner_id: id of user
    :return: DbFileMetadata object of file
    """
    file_metadata = db.query(DbFileMetadata).filter(DbFileMetadata.id == file_id,
                                                    DbFileMetadata.owner_id == owner_id).first()

    if not file_metadata:
        raise FileNotFoundException(file_id)

    return file_metadata


def move_file_to_trash(path, owner_id) -> None:
    """
    Move file to trash
    :param path: path to file
    :param owner_id: id of user
    :return: None
    """
    trash_dir = get_trash_dir_path(owner_id)

    if not os.path.exists(trash_dir):
        os.mkdir(trash_dir)

    full_trash_path = trash_dir + path.rsplit("/", 1)[1]

    shutil.move(get_path_for_file(owner_id, path), full_trash_path)


def get_children_files(db: Session, file_id: int, owner_id: int) -> list[DbFileMetadata]:
    """
    Get children files of file
    :param db: SQLAlchemy session
    :param file_id: id of file
    :param owner_id: id of user
    :return: List of DbFileMetadata objects
    """

    return db.query(DbFileMetadata).filter(DbFileMetadata.parent_id == file_id,
                                           DbFileMetadata.owner_id == owner_id,
                                           DbFileMetadata.is_deleted == False).all()


# def get_ch


def delete_file_by_id(db: Session, file_id: int, owner_id: int):
    """
    Delete file from db and disk
    :param db: SQLAlchemy session
    :param file_id: file id
    :param owner_id: id of user
    :return: None
    """
    file_metadata = get_file_metadata_by_id(db, file_id, owner_id)

    if file_metadata.is_dir:
        children = get_children_files(db, file_id, owner_id)
        for child in children:
            delete_file_by_id(db, child.id, owner_id)

    if not file_metadata.is_root_dir:
        move_file_to_trash(file_metadata.path, owner_id=owner_id)
        file_metadata.is_deleted = True
        file_metadata.last_modified = datetime.now()
        db.commit()

    # db.refresh(file_metadata)
    # return file_metadata


def move_file_on_disk(old_path, new_path, owner_id):
    """
    Move file on disk
    :param old_path: old path to file
    :param new_path: new path to file
    :param owner_id: id of user
    :return: None
    """
    old_path = get_path_for_file(owner_id, old_path)
    new_path = get_path_for_file(owner_id, new_path)

    shutil.move(old_path, new_path)


def update_file(db: Session, file_metadata_update: FileMetadataUpdate, owner_id: int) -> DbFileMetadata:
    """
    Update file metadata
    :param db: SQLAlchemy session
    :param file_metadata_update: FileMetadataUpdate object comes from request
    :param owner_id: id of user
    :return: DbFileMetadata object of updated file
    """
    file_metadata = get_file_metadata_by_id(db, file_metadata_update.id, owner_id)

    if file_metadata.is_dir:
        children = get_children_files(db, file_metadata.id, owner_id)
        for ch in children:
            update_file(db, FileMetadataUpdate(id=ch.id,
                                               path=file_metadata_update.path + ch.path[len(file_metadata.path):]),
                        owner_id)
        # TODO check if works correctly

    if file_metadata_update.path:
        if check_if_file_exists_in_db(db, file_metadata_update.path, owner_id):
            raise FileAlreadyExistsException(file_metadata_update.path)

        if check_if_file_exists_in_disk(file_metadata_update.path, owner_id=owner_id):
            raise FileAlreadyExistsException(file_metadata_update.path)

        move_file_on_disk(file_metadata.path, file_metadata_update.path, owner_id=owner_id)

        file_metadata.path = file_metadata_update.path

    if file_metadata_update.filename:
        file_metadata.filename = file_metadata_update.filename

    file_metadata.last_modified = datetime.now()
    db.commit()
    db.refresh(file_metadata)
    return file_metadata


def change_file_content_on_disk(db: Session, file_id: int, file_data: UploadFile, owner_id: int) -> DbFileMetadata:
    """
    Change file content

    In future file data will be versioned

    :param db: SQLAlchemy session
    :param file_id: id of file
    :param file_data: file data
    :param owner_id: id of user
    :return: DbFileMetadata object of file
    """

    file_metadata = get_file_metadata_by_id(db, file_id, owner_id)

    if file_metadata.is_dir:
        raise DirException(file_metadata.path)

    size = save_file_to_disk(file_data, file_metadata.path, owner_id=owner_id)

    file_metadata.size = size
    file_metadata.content_type = file_data.content_type

    db.commit()
    db.refresh(file_metadata)
    return file_metadata


def get_children(db: Session, file_id: int, owner_id: int) -> list[DbFileMetadata]:
    """
    Get children files of file
    :param db: SQLAlchemy session
    :param file_id: id of file
    :param owner_id: id of user
    :return: List of DbFileMetadata objects
    """

    return db.query(DbFileMetadata).filter(DbFileMetadata.parent_id == file_id,
                                           DbFileMetadata.owner_id == owner_id).all()
