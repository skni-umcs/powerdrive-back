from src.database.core import Base

from sqlalchemy import Column, Integer, String


class GroupUser(Base):
    __tablename__ = 'pd_group_user'
    group_user_id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer)
    user_id = Column(Integer)


class Group(Base):
    __tablename__ = 'pd_group'
    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(100))
    group_description = Column(String(100))
    group_owner_id = Column(Integer)
