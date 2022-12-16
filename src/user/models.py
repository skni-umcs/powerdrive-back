from src.database.core import Base

from sqlalchemy import Column, Integer, String


class DBUser(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100))
    user_password = Column(String(100))
    user_email = Column(String(100))
    user_first_name = Column(String(100))
    user_last_name = Column(String(100))

    user_description = Column(String(100))
