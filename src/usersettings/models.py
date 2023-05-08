from src.database.core import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Text


class DbUserSettings(Base):
    __tablename__ = 'pd_user_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('pd_user.id'), nullable=False, unique=True)
    values = Column(Text(), nullable=False)
