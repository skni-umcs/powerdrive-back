import shutil
from datetime import datetime
from pydantic import ValidationError

from src.files.exceptions import FileNotFoundException, FileAlreadyExistsException, DirException, FileIsNotDirException
from src.files.schemas import FileMetadataCreate, FileMetadataUpdate, OnlyDirectory
from src.files.models import DbFileMetadata
from src.files.utilis import get_trash_dir_path, check_if_file_exists_in_db, \
    check_if_file_exists_in_disk, get_path_for_file, save_file_to_disk, get_and_creat_root_dir, \
    check_if_proper_dir_path, metadata_valid_with_extension, create_dirs_on_disk

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
    # print(dir_list)
    previous_dir = get_and_creat_root_dir(db, owner_id)
    path = ""

    for directory in dir_list:
        path += "/" + directory
        name = directory

        if name == "":
            name = "/"

        if check_if_file_exists_in_db(db, name, path, owner_id):
            previous_dir = db.query(DbFileMetadata).filter(
                DbFileMetadata.path == path,
                DbFileMetadata.is_deleted == False,
                DbFileMetadata.owner_id == owner_id).first()


        else:
            dir_metadata = DbFileMetadata(filename=name, path=path, type="DIR", owner_id=owner_id,
                                          size=0, is_dir=True,
                                          parent_id=previous_dir.id, last_modified=datetime.now())
            db.add(dir_metadata)
            db.commit()

            previous_dir = dir_metadata

    # print(previous_dir.path)
    return previous_dir


def save_file_to_db(db: Session, filename: str, path: str, is_dir: bool, owner_id: int,
                    file_type: str, size: int) -> DbFileMetadata:
    # print(path.rsplit("/", 1)[0])
    # parent_dir_name = path.rsplit("/", 1)[0]

    # if parent_dir_name == "":
    # parent_dir_name = "/"
    dir_name = path.rsplit("/", 1)[-1]

    parent_dir = db.query(DbFileMetadata).filter(
        DbFileMetadata.path == path,
        DbFileMetadata.is_dir == True,
        # TODO: Do weryfikacji
        # DbFileMetadata.filename == dir_name,
        DbFileMetadata.is_deleted == False,
        DbFileMetadata.owner_id == owner_id).first()

    print(parent_dir.path)

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

    ### VALIDATION
    if file_metadata_create.path == "/" and file_metadata_create.is_dir:
        raise HTTPException(status_code=409, detail="Cannot create root directory in this way")  # WORKS

    if file_data is not None and file_metadata_create.is_dir:
        raise HTTPException(status_code=409, detail="File data is not None")  # WORKS

    if file_data is None and not file_metadata_create.is_dir:
        raise HTTPException(status_code=409, detail="File data is None")  # WORKS

    ### END OF VALIDATION

    if file_metadata_create.is_dir:  # DIRERCTORY
        # check if dir exists in db
        if check_if_file_exists_in_db(db, file_metadata_create.path.split('/')[-1], file_metadata_create.path,
                                      owner_id):
            raise DirException("Directory already exists")  # TO CHECK

        create_dirs_on_disk(file_metadata_create.path, user_id=owner_id)
        return create_needed_dirs_in_db(db, file_metadata_create.path, owner_id)

    else:  # FILE
        file = check_if_file_exists_in_db(db, file_data.filename, file_metadata_create.path,
                                          owner_id)
        if file:
            raise FileAlreadyExistsException("File already exists in db")

        if check_if_file_exists_in_disk(file_metadata_create.path, owner_id=owner_id, filename=file_data.filename):
            raise FileAlreadyExistsException("File aready exists")

        ## TODO is this needed?
        # if not metadata_valid_with_extension(file_metadata_create.filename, file_data.content_type):
        #     raise HTTPException(status_code=409, detail="File extension not correspond to file type")

        # if file_metadata_create.size == file_data.file.__sizeof__(): TODO enable this
        #     raise ValueError("File size is not equal to file size in metadata")

        # if check_if_not_enough_space(file_metadata_create.size, user_id=owner_id):
        #     raise OSError("Not enough space")

        size = save_file_to_disk(file_data, file_metadata_create.path, owner_id=owner_id)

        create_needed_dirs_in_db(db, file_metadata_create.path, owner_id)

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
                                                    DbFileMetadata.is_deleted == False,
                                                    DbFileMetadata.owner_id == owner_id).first()

    if not file_metadata:
        raise FileNotFoundException(file_id)

    return file_metadata


def move_file_to_trash(filename: str, path: str, owner_id: int) -> None:
    """
    Move file to trash
    :param filename: name of file
    :param path: path to file
    :param owner_id: id of user
    :param is_dir: is file directory
    :return: None
    """
    # if not check_if_file_exists_in_disk(path, owner_id=owner_id, filename=filename):
    #     raise FileNotFoundException(123)

    trash_path = get_trash_dir_path(owner_id)

    if not os.path.exists(trash_path):
        os.makedirs(trash_path)

    if os.path.exists(trash_path + filename):
        os.remove(trash_path + filename)

    # shutil.move(get_path_for_file(owner_id, path) + "/" + , trash_path)
    os.remove(get_path_for_file(owner_id, path) + "/" + filename)


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


def delete_file(db: Session, file_metadata: DbFileMetadata, owner_id: int):
    """
    Delete file from db and disk
    :param db: SQLAlchemy session
    :param file_metadata: DbFileMetadata object of file
    :param owner_id: id of user
    :return: None
    """
    file_metadata.is_deleted = True

    if not file_metadata.is_dir:
        move_file_to_trash(file_metadata.filename, file_metadata.path, owner_id)

    db.commit()


def delete_dir(db: Session, file_metadata: DbFileMetadata, owner_id: int):
    """
    Delete directory from db and disk
    :param db: SQLAlchemy session
    :param file_metadata: DbFileMetadata object of file
    :param owner_id: id of user
    :return: None
    """
    file_metadata.is_deleted = True

    children_files = get_children_files(db, file_metadata.id, owner_id)

    for child in children_files:
        if child.is_dir:
            delete_dir(db, child, owner_id)
        else:
            delete_file(db, child, owner_id)

    db.commit()
    os.rmdir(get_path_for_file(owner_id, file_metadata.path))


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
        delete_dir(db, file_metadata, owner_id)
    else:
        delete_file(db, file_metadata, owner_id)


def move_file_on_disk(old_path, new_path, owner_id):
    """
    Move file on disk
    :param old_path: old path to file with filename/dir name
    :param new_path: new path to file with filename/dir name
    :param owner_id: id of user
    :return: None
    """
    old_path = get_path_for_file(owner_id, old_path)
    new_path = get_path_for_file(owner_id, new_path)

    if os.path.exists(new_path):
        raise FileAlreadyExistsException(new_path)

    # check if need to create dirs
    if not os.path.exists(new_path.rsplit("/", 1)[0]):
        os.makedirs(new_path.rsplit("/", 1)[0])

    shutil.move(old_path, new_path)


def path_for_file(v_path: str, filename: str, owner_id: int) -> str:
    """
    Get path for file
    :param v_path: path to file
    :param filename: name of file
    :param owner_id: id of user
    :return: path to file
    """
    return get_path_for_file(owner_id, v_path) + "/" + filename


def path_for_dir(v_path: str, dir_name: str, owner_id: int) -> str:
    """
    Get path for dir /path contains dir name
    :param v_path: path to dir
    :param dir_name: name of dir
    :param owner_id: id of user
    :return: path to dir
    """
    return get_path_for_file(owner_id, v_path)


def move_dir_on_disk(old_path, new_path, owner_id):
    """
    Move dir on disk
    :param old_path: old path to dir with dir name
    :param new_path: new path to dir with dir name
    :param owner_id: id of user
    :return: None
    """
    old_path = get_path_for_file(owner_id, old_path)
    new_path = get_path_for_file(owner_id, new_path)

    print(old_path)
    print(new_path)

    if os.path.exists(new_path):
        raise FileAlreadyExistsException(new_path)

    # check if need to create dirs
    if not os.path.exists(new_path.rsplit("/", 1)[0]):
        os.makedirs(new_path.rsplit("/", 1)[0])

    shutil.move(old_path, new_path)


# def move_file(db: Session, file_metadata: DbFileMetadata, file_metadata_update: FileMetadataUpdate, owner_id: int):


def move_dir(db: Session, file_metadata: DbFileMetadata, file_metadata_update: FileMetadataUpdate, owner_id: int):
    """
    Move file on disk and update metadata
    :param db: SQLAlchemy session
    :param file_metadata: DbFileMetadata object of file
    :param file_metadata_update: FileMetadataUpdate object comes from request
    :param owner_id: id of user
    :return: None
    """
    old_path = file_metadata.path
    new_path = file_metadata_update.path

    # change name if need
    if file_metadata.filename != file_metadata_update.filename:
        file_metadata.filename = file_metadata_update.filename

    ## change path in metadata
    file_metadata.path = file_metadata_update.path

    # create directories in db if need

    parent_id = create_needed_dirs_in_db(db, file_metadata_update.path, owner_id)

    file_metadata.parent_id = parent_id

    db.commit()
    db.refresh(file_metadata)

    for child in get_children_files(db, file_metadata.id, owner_id):
        if child.is_dir:
            move_dir(db, child, FileMetadataUpdate(path=child.path.replace(old_path, new_path)), owner_id)
        else:
            child.path = child.path.replace(old_path, new_path)
            child.parent_id = db.query(DbFileMetadata.id).filter(DbFileMetadata.path == file_metadata_update.path,
                                                                 DbFileMetadata.is_dir == True,
                                                                 DbFileMetadata.owner_id == owner_id
                                                                 ).first().id
            child.parent_id = db
    db.commit()

    move_dir_on_disk(old_path, new_path, owner_id)


def update_file(db: Session, file_metadata_update: FileMetadataUpdate, owner_id: int) -> DbFileMetadata:
    """
    Update file metadata
    :param db: SQLAlchemy session
    :param file_metadata_update: FileMetadataUpdate object comes from request
    :param owner_id: id of user
    :return: DbFileMetadata object of updated file
    """
    file_metadata = get_file_metadata_by_id(db, file_metadata_update.id, owner_id)

    ### CHECK IF NEW NAME

    if file_metadata_update.filename != file_metadata.filename or file_metadata_update.path != file_metadata.path:
        if check_if_file_exists_in_db(db, file_metadata_update.path, file_metadata_update.filename, owner_id):
            raise FileAlreadyExistsException(file_metadata_update.filename)

        if file_metadata.is_dir:

            move_dir(db, file_metadata, file_metadata_update, owner_id)
            # create_needed_dirs_in_db(db, file_metadata_update.path, owner_id)

            # move_dir_on_disk(file_metadata.path, file_metadata_update.path, owner_id)

        else:
            create_needed_dirs_in_db(db, file_metadata_update.path, owner_id)

            # move file on disk

            move_file_on_disk(file_metadata.path + "/" + file_metadata.filename,
                              file_metadata_update.path + "/" + file_metadata_update.filename, owner_id)

            parent_id = db.query(DbFileMetadata.id).filter(DbFileMetadata.path == file_metadata_update.path,
                                                           DbFileMetadata.is_dir == True,
                                                           DbFileMetadata.owner_id == owner_id
                                                           ).first().id

            file_metadata.parent_id = parent_id
            file_metadata.path = file_metadata_update.path
            file_metadata.filename = file_metadata_update.filename




    else:
        return file_metadata

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
                                           DbFileMetadata.owner_id == owner_id,
                                           DbFileMetadata.is_deleted == False).all()


def get_user_root_dir(db: Session, user_id: int) -> DbFileMetadata:
    """
    Get user root dir
    :param db: SQLAlchemy session
    :param user_id: id of user
    :return: DbFileMetadata object of root dir
    """
    return get_and_creat_root_dir(db, user_id)


def filter_children_by_is_dir(db: Session, file_id: int, owner_id: int, is_dir: bool) -> list[DbFileMetadata]:
    """
    Get children files of file
    :param db: SQLAlchemy session
    :param file_id: id of file
    :param owner_id: id of user
    :param is_dir: is dir
    :return: List of DbFileMetadata objects
    """

    return db.query(DbFileMetadata).filter(DbFileMetadata.parent_id == file_id,
                                           DbFileMetadata.owner_id == owner_id,
                                           DbFileMetadata.is_deleted == False,
                                           DbFileMetadata.is_dir == is_dir).all()


def pom2(db: Session, dir_in: DbFileMetadata, owner_id: int, is_dir: bool) -> OnlyDirectory:
    children = filter_children_by_is_dir(db, dir_in.id, owner_id, is_dir)
    result = []

    for child in children:
        result.append(pom2(db, child, owner_id, is_dir))

    res = OnlyDirectory(**dir_in.__dict__, children=result)
    return res


def get_dir_tree(db: Session, owner_id: int) -> OnlyDirectory:
    """
    Get dir tree
    :param db: SQLAlchemy session
    :param owner_id: id of user
    :return: List of DbFileMetadata objects
    """

    root_dir = get_user_root_dir(db, owner_id)
    dir_tree = [root_dir]

    children = pom2(db, root_dir, owner_id, True)

    return children
