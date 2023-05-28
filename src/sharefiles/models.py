from src.database.core import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class ShareFileUser(Base):
    __tablename__ = 'pd_share_file_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey('pd_file.id'))
    user_id = Column(Integer, ForeignKey('pd_user.id'))
    read = Column(Boolean, default=False)
    write = Column(Boolean, default=False)
    delete = Column(Boolean, default=False)
    share = Column(Boolean, default=False)

    # read, write, delete, share,  owner

