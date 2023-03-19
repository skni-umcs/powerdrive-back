from src.config import Settings
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# from psycopg2.errors import
import psycopg2

import sys

settings = Settings()


def _drop_db():
    print("Dropping database")
    try:
        conn = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            user=settings.db_user,
            password=settings.db_password,
        )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        #         with conn.cursor() as cursor:
        #             cursor.execute(sql.SQL(f"""SELECT pg_terminate_backend(pg_stat_activity.pid)
        # FROM pg_stat_activity
        # WHERE pg_stat_activity.datname = '{settings.db_name} '
        #   AND pid <> pg_backend_pid();"""))

        with conn.cursor() as cursor:
            cursor.execute(sql.SQL(f'DROP DATABASE {settings.db_name} WITH (FORCE)'))

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "drop_db":
            try:
                _drop_db()
            except psycopg2.errors.ObjectInUse as e:
                print("Database is in use. Close all connections and try again /Stop docker containers and try again/ ")

        else:
            print("Unknown command")
    else:
        print("No command provided")
