import logging
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
from src.config import Settings
from src.database.core import create_db, check_all_tables, create_test_db

settings = Settings()

# FOR DATABASE CREATION
from src.user.models import User

logging.basicConfig(level=logging.INFO)


def setup_test():
    # create new database
    logging.info("Creating test database")
    conn = psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute(sql.SQL(f'DROP DATABASE IF EXISTS {settings.test_db_name}'))
    cursor.execute(sql.SQL(f'CREATE DATABASE {settings.test_db_name}'))
    # conn.commit()
    cursor.close()
    conn.close()

    logging.info("Test database created")

    # create tables
    # check_all_tables()
    logging.info("Creating tables")
    create_test_db()

    logging.info(settings.test_db_name)
    logging.info(settings.db_name)


def setup_dev():
    logging.info("Checking if all tables exists")
    logging.info(check_all_tables())

    if not all(check_all_tables()):
        logging.info("Creating tables")
        create_db()
        logging.info("All tables created")
    else:
        logging.info("All tables exists")
        logging.info("Nothing to do")


def setup_prod():
    logging.warning("NOT IMPLEMENTED")


if __name__ == "__main__":
    if sys.argv[1] == "test":
        setup_test()
    elif sys.argv[1] == "dev":
        setup_dev()
    elif sys.argv[1] == "prod":
        setup_prod()
    else:
        print("Invalid argument")
