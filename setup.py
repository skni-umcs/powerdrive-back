import logging
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from src.config import Settings
from src.database.core import create_db, check_all_tables

from src.user import service as user_service
from src.user.exceptions import UserNotFoundException

from src.dependencies import get_db

import src.user as user


settings = Settings()

# Import models here for table creation
from src.user.models import User

from src.calendar.models import Calendar, Event, ReoccurringEvent, eventIDSeq

from src.group.models import Group

from src.files.models import DbFileMetadata

from src.usersettings.models import DbUserSettings

from src.sharefiles.models import ShareFileUser
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def _create_test_database():
    if "test" not in settings.db_name:
        logging.error("You are not in test database, please set DB_NAME to *test* in docker_entrypoint.sh or .env")
        sys.exit(1)

    logger.info("Creating test database")
    try:
        conn = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cursor:
            cursor.execute(sql.SQL(f'DROP DATABASE IF EXISTS {settings.db_name}'))
            cursor.execute(sql.SQL(f'CREATE DATABASE {settings.db_name}'))

    finally:
        if conn:
            conn.close()


def _create_all_tables_if_needed():
    if not all(check_all_tables()):
        logger.info("Creating tables")
        create_db()
        logger.info("All tables created")
    else:
        logger.info("All tables exists. Nothing to do")


def _create_admin():
    logger.info("##### Creating admin user #####")
    # logger.info("Creating admin user")
    # check if admin exists

    logger.info("Checking if admin exists")
    admin = user_service.get_by_username(get_db().__next__(), "admin")
    if admin:
        logger.info("Admin already exists")
        return
    else:
        logger.info("Creating admin user")
        admin = user.add(get_db().__next__(),
                         user.UserCreate(username="admin", password="AdminAdmin1#", email="admin@example.com",
                                         first_name="admin",
                                         last_name="ADMIN"))
        session = get_db().__next__()
        admin.is_admin = True
        session.commit()


def _insert_initial_data():
    logger.info("##### Inserting initial data #####")
    logger.info("Inserting initial users for development")
    try:
        for i in range(10):
            new_user = user_service.get_by_username(get_db().__next__(), f"test{i}")
            if new_user:
                logger.info(f"User test{i} already exists")
                continue
            else:
                logger.info(f"Creating user test{i}")
                user.add(get_db().__next__(),
                         user.UserCreate(username=f"test{i}", password="TestTest1!", first_name="test",
                                         last_name="test",
                                         email=f"test{i}@example.com"))

    except Exception as e:
        logger.error(e)  # TODO check if users exists


# def _create_root_dir_for_files():
#     if settings.base_file_path:
#         logger.info(f"Creating root dir {settings.base_file_path}")
#         import os
#         os.makedirs(settings.base_file_path, exist_ok=True)
#
#     if settings.base_file_path_trash:
#         logger.info(f"Creating root dir {settings.base_file_path_trash}")
#         import os
#         os.makedirs(settings.base_file_path_trash, exist_ok=True)


def _run_migrations():
    logger.info("##### Running migrations #####")
    import alembic.config
    alembic_args = [
        "--raiseerr",
        "upgrade",
        "head"
    ]
    alembic.config.main(argv=alembic_args)


def _run_migrations():
    logger.info("##### Running migrations #####")
    import alembic.config
    alembic_args = [
        "--raiseerr",
        "upgrade",
        "head"
    ]
    alembic.config.main(argv=alembic_args)


def _run_migrations():
    logger.info("##### Running migrations #####")
    import alembic.config
    alembic_args = [
        "--raiseerr",
        "upgrade",
        "head"
    ]
    alembic.config.main(argv=alembic_args)


def setup_test():
    logger.info("##### Setting up test #####")
    # _create_test_database()
    # _create_all_tables_if_needed()
    # _create_root_dir_for_files()


def setup_dev():
    # _create_all_tables_if_needed()
    _run_migrations()
    _create_admin()
    _insert_initial_data()
    # _create_root_dir_for_files()


def setup_prod():
    # _create_all_tables_if_needed()
    _run_migrations()
    _create_admin()
    _insert_initial_data()
    logger.warning("setup_prod NOT IMPLEMENTED")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            setup_test()
        elif sys.argv[1] == "dev":
            setup_dev()
        elif sys.argv[1] == "prod":
            setup_prod()
        else:
            logger.error("Unknown argument")
            # print("Invalid argument")
    else:
        logger.error("No argument")
        # print("Missing argument")
        pass
