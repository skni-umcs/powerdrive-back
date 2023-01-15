import shutil

from src.files.exceptions import FileNotFoundException, FileAlreadyExistsException, DirDeleteException, DirException
from src.files.schemas import FileMetadataCreate, FileMetadataUpdate
from src.files.models import DbFileMetadata
from src.files.utilis import get_base_path_for_user, get_trash_dir_path

from fastapi import UploadFile
from sqlalchemy.orm import Session
from src.config import Settings

import os

import logging

logger = logging.getLogger(__name__)

settings = Settings()


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
    return os.path.exists(os.path.join(get_base_path_for_user(owner_id), virtual_path))


def check_if_not_enough_space(size, user_id):
    return os.statvfs(get_base_path_for_user(user_id)).f_bavail > size


def get_path_for_file(user_id: int, virtual_path: str) -> str:
    """
    Compose physical path from virtual path(path store in db)
    :param user_id: id of user
    :param virtual_path: path from db
    :return: physical path
    """
    return get_base_path_for_user(user_id) + virtual_path


def save_file_to_disk(file_data, virtual_path: str, owner_id: id) -> int:
    """
    Save file to diskaq
    :param file_data: file data to save
    :param virtual_path: path to compose full path
    :param owner_id: id of user
    :return: bytes written to disk
    """
    os.makedirs(os.path.dirname(get_path_for_file(owner_id, virtual_path)), exist_ok=True)

    with open(get_path_for_file(owner_id, virtual_path), "wb") as buffer:
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

    # TODO remove this function, directory isnt needed
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


def move_file_to_trash(path, owner_id):
    """
    Move file to trash
    :param path: path to file
    :param owner_id: id of user
    :return: None
    """
    trash_dir = get_trash_dir_path(owner_id)

    if not os.path.exists(trash_dir):
        os.mkdir(trash_dir)

    shutil.move(get_path_for_file(owner_id, path), trash_dir)


def get_children_files(db: Session, file_id: int, owner_id: int) -> list[DbFileMetadata]:
    """
    Get children files of file
    :param db: SQLAlchemy session
    :param file_id: id of file
    :param owner_id: id of user
    :return: List of DbFileMetadata objects
    """

    return db.query(DbFileMetadata).filter(DbFileMetadata.parent_id == file_id,
                                           DbFileMetadata.owner_id == owner_id).all()


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

    move_file_to_trash(file_metadata.path, owner_id=owner_id)

    file_metadata.is_deleted = True

    db.commit()
    db.refresh(file_metadata)
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

    db.commit()
    db.refresh(file_metadata)
    return file_metadata


def change_file_content_on_diks(db: Session, file_id: int, file_data: UploadFile, owner_id: int) -> DbFileMetadata:
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


def get_file_chidlren(db: Session, file_id: int, owner_id: int) -> list[DbFileMetadata]:
    """
    Get children files of file
    :param db: SQLAlchemy session
    :param file_id: id of file
    :param owner_id: id of user
    :return: List of DbFileMetadata objects
    """

    return db.query(DbFileMetadata).filter(DbFileMetadata.parent_id == file_id,
                                           DbFileMetadata.owner_id == owner_id).all()
