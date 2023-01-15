from src.files.exceptrions import FileNotFoundException, FileAlreadyExistsException
from src.files.schemas import FileMetadataCreate, FileMetadataUpdate
from src.files.models import DbFileMetadata

from src.user.schemas import User

from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.config import Settings

import os

import logging

logger = logging.getLogger(__name__)

settings = Settings()


def compose_base_files_path(user_id: id) -> str:
    """
    Compose base(physical) file path for user
    :param user_id: id of user
    :return: base files path
    """
    return os.path.join(settings.base_file_path, str(user_id))


def check_if_file_exists_in_db(db: Session, virtual_path: str, owner_id: int) -> bool:
    """
    Check if file exists in db
    :param db: SQLAlchemy session
    :param virtual_path: path to file from db
    :param owner_id: file owner id
    :return: True if file exists, False otherwise
    """
    return db.query(DbFileMetadata).filter(DbFileMetadata.path == virtual_path,
                                           DbFileMetadata.owner_id == owner_id).first() is not None


def check_if_file_exists_in_disk(virtual_path: str, owner_id: int) -> bool:
    """
    Check if file exists in disk
    :param virtual_path: path to file from db
    :param owner_id: file owner id
    :return: True if file exists, False otherwise
    """
    return os.path.exists(os.path.join(compose_base_files_path(owner_id), virtual_path))


def check_if_not_enough_space(size, user_id):
    return os.statvfs(compose_base_files_path(user_id)).f_bavail > size


def compose_physical_path(user_id: int, virtual_path: str) -> str:
    """
    Compose physical path from virtual path(path store in db)
    :param user_id: id of user
    :param virtual_path: path from db
    :return: physical path
    """
    return compose_base_files_path(user_id) + virtual_path


def save_file_to_disk(file_data, virtual_path: str, owner_id: id) -> int:
    """
    Save file to diskaq
    :param file_data: file data to save
    :param virtual_path: path to compose full path
    :param owner_id: id of user
    :return: bytes written to disk
    """
    os.makedirs(os.path.dirname(compose_physical_path(owner_id, virtual_path)), exist_ok=True)

    with open(compose_physical_path(owner_id, virtual_path), "wb") as buffer:
        by = buffer.write(file_data.file.read())

    return by


def get_and_creat_root_dir(db: Session, owner_id: int) -> DbFileMetadata:
    """
    Get root directory for user. If root directory does not exist, create it.
    :param db: SQLAlchemy session
    :param owner_id: id of user
    :return: root directory of user as DBFileMetadata object
    """
    root_dir = db.query(DbFileMetadata).filter(DbFileMetadata.path == "/", DbFileMetadata.owner_id == owner_id,
                                               DbFileMetadata.is_root_dir == True).first()

    if not root_dir:
        root_dir = DbFileMetadata(path="/", filename="/", type="directory", owner_id=owner_id, size=0, is_dir=True,
                                  is_root_dir=True)
        db.add(root_dir)
        db.commit()

    return root_dir


def check_if_proper_dir_path(path: str) -> bool:
    """
    Check if path is proper directory path(ends with "/")
    :param path: path to check
    :return: True if path is proper directory path, False otherwise

    >>> check_if_proper_dir_path("/home/user/")
    True
    >>> check_if_proper_dir_path("/home/user/file.txt")
    False

    """
    return path.endswith("/")


def check_if_proper_file_path(path: str) -> bool:
    """
    Check if path is proper file path(ends with "/")
    :param path: path to check
    :return: True if path is proper file path, False otherwise

    >>> check_if_proper_file_path("/home/user/")
    False
    >>> check_if_proper_file_path("/home/user/file.txt")
    True
    """
    return not path.endswith("/")


def create_needed_dirs_in_db(db: Session, path: str, owner_id: int):
    """
    Create needed directories in db
    :param db: SQLAlchemy session
    :param path: path to file
    :param owner_id: id of user
    :return: None
    """
    dir_list = path.split("/")[1:-1]

    previous_dir = get_and_creat_root_dir(db, owner_id)
    path = "/"

    for directory in dir_list:
        path += directory + "/"
        if check_if_file_exists_in_db(db, path, owner_id) and check_if_proper_dir_path(path):
            continue
        print(path.rsplit("/", 1))
        dir_metadata = DbFileMetadata(filename=path, path=path, type="directory", owner_id=owner_id,
                                      size=0, is_dir=True,
                                      parent_id=previous_dir.id)
        db.add(dir_metadata)
        db.commit()

        previous_dir = dir_metadata


def save_file_to_db(db: Session, file_metadata_create: FileMetadataCreate, owner_id: int,
                    file_type: str, size: int) -> DbFileMetadata:
    """
    Save file metadata to db
    :param db:
    :param file_metadata_create:
    :param owner_id:
    :return:
    """

    print(file_metadata_create.path.rsplit("/", 1)[0])
    parent_dir = db.query(DbFileMetadata).filter(
        DbFileMetadata.path == file_metadata_create.path.rsplit("/", 1)[0] + '/',
        DbFileMetadata.owner_id == owner_id).first()
    db_file = DbFileMetadata(**file_metadata_create.dict(), type=file_type, size=size, owner_id=owner_id,
                             parent_id=parent_dir.id)

    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def add_new_file_and_save_od_disk(db: Session, file_metadata_create: FileMetadataCreate, file_data: UploadFile | None,
                                  owner_id: int) -> DbFileMetadata:
    """
    Add new file to db and save it to disk
    :param db: SQLAlchemy session
    :param file_metadata_create: FileMetadataCreate object comes from request
    :param file_data: file data comes from request
    :param owner_id: id of user from JWT
    :return: DbFileMetadata object of new file
    """
    if check_if_file_exists_in_db(db, file_metadata_create.path, owner_id) or check_if_file_exists_in_disk(
            file_metadata_create.path, owner_id=owner_id):
        raise FileAlreadyExistsException("File already exists")

    if check_if_file_exists_in_disk(file_metadata_create.path, owner_id=owner_id):
        raise FileAlreadyExistsException(file_metadata_create.path)

    # if file_metadata_create.size == file_data.file.__sizeof__(): TODO enable this
    #     raise ValueError("File size is not equal to file size in metadata")

    # if check_if_not_enough_space(file_metadata_create.size, user_id=owner_id):
    #     raise OSError("Not enough space")

    size = save_file_to_disk(file_data, file_metadata_create.path, owner_id=owner_id)

    create_needed_dirs_in_db(db, file_metadata_create.path, owner_id)

    db_file = save_file_to_db(db, file_metadata_create, owner_id, file_data.content_type, size)
    # TODO check file type

    return db_file
