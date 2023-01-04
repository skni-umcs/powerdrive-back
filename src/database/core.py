from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from src.config import Settings
# from database.models import *

sett = Settings()
# engine = create_engine(sett.db_url, connect_args={"check_same_thread": False})
engine = create_engine(sett.db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def _check_if_table_exists(table_name: str):
    return engine.has_table(table_name)


def check_all_tables():
    return [_check_if_table_exists(table_name) for table_name in Base.metadata.tables.keys()]


def create_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    session.commit()
    session.close()


def create_test_db():
    test_engine = create_engine(sett.test_db_url, echo=True)
    Base.metadata.create_all(bind=test_engine)
    testmaker = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = testmaker()
    session.commit()
    session.close()