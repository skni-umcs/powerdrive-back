import logging
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from src.config import Settings
from src.database.core import create_db, check_all_tables


settings = Settings()

# Import models here for table creation
from src.user.models import User
from src.calendar.models import Calendar, Event, ReoccurringEvent, eventIDSeq

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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


def setup_test():
    _create_test_database()
    _create_all_tables_if_needed()


def _create_admin():
    logger.warning("_create_admin NOT IMPLEMENTED")


def setup_dev():
    _create_all_tables_if_needed()
    _create_admin()


def setup_prod():
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
            print("Invalid argument")
    else:
        print("Missing argument")
