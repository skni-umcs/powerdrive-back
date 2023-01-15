import os

from src.config import Settings

settings = Settings()


def get_base_path_for_user(user_id: id) -> str:
    """
    Compose base(physical) file path for user
    :param user_id: id of user
    :return: base files path
    """
    print(os.path.join(settings.base_file_path, str(user_id)))
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
