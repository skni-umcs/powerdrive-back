import logging
from src.database.core import create_db, check_all_tables
from src.user.models import DBUser
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Checking if all tables exists")
    logging.info(check_all_tables())
    if not all(check_all_tables()):
        logging.info("Creating database")
        create_db()
        logging.info("Database created")
    else:
        logging.info("All tables exists")
        logging.info("Nothing to do")

