from src.database.core import Base

from sqlalchemy import Column, Integer, String


class DBGroupUser(Base):
    __tablename__ = 'GroupUser'
    group_user_id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer)
    user_id = Column(Integer)


class DBGroup(Base):
    __tablename__ = 'Group'

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(100))
    group_description = Column(String(100))
    group_owner_id = Column(Integer)
    #group_owner = relationship('DBUser')
    #group_users = relationship('DBUser', secondary=DBGroupUser.__table__)
