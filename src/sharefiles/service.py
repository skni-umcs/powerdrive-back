from sqlalchemy.orm import Session

from src.files.models import DbFileMetadata
from src.sharefiles.models import ShareFileUser
from src.sharefiles.schemas import ShareFileUserCreate, ShareFileUserUpdate
from src.user.schemas import User
from src.sharefiles.exceptions import FileNotFoundException, NotAuthorizedShareFileException


def add(current_user: User, share: ShareFileUserCreate, db: Session) -> ShareFileUser:
    db_file = db.query(DbFileMetadata).filter(DbFileMetadata.id == share.file_id).first()
    if not db_file:
        raise FileNotFoundException()
    if db_file.owner_id != current_user.id:
        raise FileNotFoundException

    db_share = ShareFileUser(
        file_id=share.file_id,
        user_id=share.user_id,
        read=share.read,
        write=share.write,
        delete=share.delete,
        share=share.share,
    )
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share


def get_by_id(current_user: User, share_id: int, db: Session) -> ShareFileUser:
    db_share = db.query(ShareFileUser).filter(ShareFileUser.id == share_id).first()
    if not db_share:
        raise FileNotFoundException()
    return db_share


def get_all(current_user: User, db: Session) -> [ShareFileUser]:
    return db.query(ShareFileUser).all()

def get_all_for_user(current_user: User, db: Session) -> [ShareFileUser]:
    return db.query(ShareFileUser).filter(ShareFileUser.user_id == current_user.id).all()


def get_for_user(current_user: User, file_id: int,  db: Session) -> ShareFileUser:
    db_file = db.query(ShareFileUser).filter(ShareFileUser.user_id == current_user.id
                                             and ShareFileUser.file_id == file_id).all()

    if not db_file:
        raise FileNotFoundException
    return db_file


def update(current_user: User, share: ShareFileUserUpdate, db: Session) -> ShareFileUser:
    db_file = db.query(DbFileMetadata).filter(DbFileMetadata.id == share.file_id).first()
    if not db_file:
        print('file not found')
        raise FileNotFoundException()
    if db_file.owner_id != current_user.id:
        raise NotAuthorizedShareFileException()
    db_share = db.query(ShareFileUser).filter(ShareFileUser.id == share.id).first()
    if not db_share:
        raise FileNotFoundException()

    db_share.read = share.read
    db_share.write = share.write
    db_share.delete = share.delete
    db_share.share = share.share
    db.commit()
    db.refresh(db_share)
    return db_share


def delete(current_user: User, share_id: int, db: Session):
    db_share = db.query(ShareFileUser).filter(ShareFileUser.id == share_id).first()
    if not db_share:
        raise FileNotFoundException()
    owner_id = db.query(DbFileMetadata).filter(DbFileMetadata.id == db_share.file_id).first().owner_id
    if db_share.user_id != current_user.id and owner_id != current_user.id:
        raise NotAuthorizedShareFileException()
    db.delete(db_share)
    db.commit()
    return db_share

