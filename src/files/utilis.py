import os

from sqlalchemy.orm import Session

from src.config import Settings
from src.files.models import DbFileMetadata
import mimetypes

from datetime import datetime

settings = Settings()


def get_base_path_for_user(user_id: id) -> str:
    """
    Compose base(physical) file path for user
    :param user_id: id of user
    :return: base files path
    """
    # print(os.path.join(settings.base_file_path, str(user_id)))
    return os.path.join(settings.base_file_path, str(user_id))


def get_trash_dir_path(user_id: id) -> str:
    """
    Compose trash dir path for user
    :param user_id: id of user
    :return: trash dir path
    """
    return os.path.join(get_base_path_for_user(user_id), settings.trash_dir_name)


# def get_main_dir_path(user_id: id) -> str:
#     """
#     Compose main dir path for user
#     :param user_id: id of user
#     :return: main dir path
#     """
#     return os.path.join(get_base_path_for_user(user_id), settings.main_dir_name)
def check_if_file_exists_in_db(db: Session, filename: str, virtual_path: str, owner_id: int) -> bool:
    """
    Check if file exists in db
    :param db: SQLAlchemy session
    :param virtual_path: path to file from db
    :param owner_id: file owner id
    :return: True if file exists, False otherwise
    """
    return db.query(DbFileMetadata).filter(DbFileMetadata.path == virtual_path,
                                           DbFileMetadata.filename == filename,
                                           DbFileMetadata.owner_id == owner_id).first() is not None


def check_if_file_exists_in_disk(virtual_path: str, owner_id: int, filename: str = None) -> bool:
    """
    Check if file exists in disk
    :param virtual_path: path to file from db
    :param owner_id: file owner id
    :param filename: name of file
    :return: True if file exists, False otherwise
    """
    if filename:
        if virtual_path == '/':
            virtual_path = ''
        path = get_base_path_for_user(owner_id) + virtual_path + '/' + filename
        return os.path.exists(os.path.join(path, filename))
    else:
        return os.path.exists(os.path.join(get_base_path_for_user(owner_id), virtual_path))


def check_if_not_enough_space(size, user_id):
    return os.statvfs(get_base_path_for_user(user_id)).f_bavail > size


def get_path_for_file(user_id: int, virtual_path: str) -> str:
    """
    Compose physical path from virtual path(path store in db) ended with /
    :param user_id: id of user
    :param virtual_path: path from db
    :param is_dir: if path is directory
    :return: physical path
    """

    return get_base_path_for_user(user_id) + virtual_path + '/'


def save_file_to_disk(file_data, virtual_path: str, owner_id: id) -> int:
    """
    Save file to diskaq
    :param file_data: file data to save
    :param virtual_path: path to compose full path
    :param owner_id: id of user
    :return: bytes written to disk
    """
    os.makedirs(os.path.dirname(get_path_for_file(owner_id, virtual_path) + '/'), exist_ok=True)

    with open(get_path_for_file(owner_id, virtual_path) + '/' + file_data.filename, "a+b") as buffer:
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
        root_dir = DbFileMetadata(path="/", filename="/", type="DIR", owner_id=owner_id, size=0, is_dir=True,
                                  is_root_dir=True, last_modified=datetime.now())
        db.add(root_dir)
        db.commit()
    print(root_dir.id)
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


def metadata_valid_with_extension(filename: str, content_type: str) -> bool:
    """
    Check if file metadata is valid with extension
    :param filename: filename with extension
    :param content_type: content type of file, from http stream
    :return: True if extension corresponds to content type, False otherwise
    """
    mimetypes.init()
    return content_type in mimetypes.guess_type(filename)


def create_dirs_on_disk(path: str, user_id: int) -> None:
    """
    Create directories on disk
    :param path: path to create
    :param user_id: id of user
    :return: None
    """
    os.makedirs(get_path_for_file(user_id, path), exist_ok=True)
