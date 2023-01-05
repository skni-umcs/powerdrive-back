from src.database.core import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class dbFileMetadata(Base):
    __tablename__ = 'File'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    path = Column(String(1000), nullable=False)
    type = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, default=False)
    # is_dir = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    # parent_id = Column(Integer, ForeignKey('File.id'))
