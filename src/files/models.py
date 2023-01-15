from src.database.core import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class DbFileMetadata(Base):
    __tablename__ = 'pd_file'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=True)

    path = Column(String(1000), nullable=False)  # virtual_file_path with filename

    type = Column(String(255), nullable=False)  # file type (image, video, audio, etc) ?

    size = Column(Integer, nullable=False)  # file size in bytes

    is_deleted = Column(Boolean, default=False)  # is file deleted

    owner_id = Column(Integer, ForeignKey('pd_user.id'), nullable=False)

    is_root_dir = Column(Boolean, default=False)

    is_dir = Column(Boolean, default=False)

    parent_id = Column(Integer, ForeignKey('pd_file.id'))
