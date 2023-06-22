from sqlalchemy.orm import Session

from src.files.models import DbFileMetadata
from src.sharefiles.models import ShareFileUser
from src.sharefiles.schemas import ShareFileUserCreate, ShareFileUserUpdate
from src.user.schemas import User
from src.sharefiles.exceptions import FileNotFoundException, NotAuthorizedShareFileException,\
ShareFileNotFoundException, ShareFileWrongPermissionException
from src.files import service as file_service

def check_if_permissions_correct(share: ShareFileUserCreate | ShareFileUserUpdate):
    if share.write and not share.read:
        return False
    if share.delete and not share.write:
        return False
    if share.share and not share.read:
        return False
    return True

def add(current_user: User, share: ShareFileUserCreate, db: Session) -> ShareFileUser:
    db_file = db.query(DbFileMetadata).filter(DbFileMetadata.id == share.file_id,
                                              DbFileMetadata.is_deleted == False).first()
    if not db_file:
        raise FileNotFoundException()
    if db_file.owner_id != current_user.id:
        raise NotAuthorizedShareFileException()

    if not check_if_permissions_correct(share):
        raise ShareFileWrongPermissionException()

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
        raise ShareFileNotFoundException()
    db_file = db.query(DbFileMetadata).filter(DbFileMetadata.id == db_share.file_id,
                                              DbFileMetadata.is_deleted == False).first()
    if not db_file:
        raise FileNotFoundException()
    if db_share.user_id != current_user.id and db_file.owner_id != current_user.id:
        raise NotAuthorizedShareFileException()
    return db_share



def get_all_for_user(current_user: User, db: Session) -> [ShareFileUser]:
    shares = db.query(ShareFileUser).filter(ShareFileUser.user_id == current_user.id).all()
    return [s for s in shares if db.query(DbFileMetadata).filter(DbFileMetadata.id == s.file_id,
                                                                 DbFileMetadata.is_deleted == False).first()]


def get_all_for_file(file_id: int, current_user: User, db: Session) -> [ShareFileUser]:
    db_file = db.query(DbFileMetadata).filter(DbFileMetadata.id == file_id,
                                              DbFileMetadata.is_deleted == False).first()

    if not db_file:
        raise FileNotFoundException()

    shares = db.query(ShareFileUser).filter(ShareFileUser.file_id == file_id).all()
    return shares


def update(current_user: User, share: ShareFileUserUpdate, db: Session) -> ShareFileUser:
    db_file = db.query(DbFileMetadata).filter(DbFileMetadata.id == share.file_id,
                                              DbFileMetadata.is_deleted == False
                                              ).first()
    if not db_file:
        raise FileNotFoundException()
    if db_file.owner_id != current_user.id:
        raise NotAuthorizedShareFileException()
    db_share = db.query(ShareFileUser).filter(ShareFileUser.id == share.id).first()
    if not db_share:
        raise ShareFileNotFoundException()

    if not check_if_permissions_correct(share):
        raise ShareFileWrongPermissionException()

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
        raise ShareFileNotFoundException()
    owner_id = db.query(DbFileMetadata).filter(DbFileMetadata.id == db_share.file_id).first().owner_id
    if db_share.user_id != current_user.id and owner_id != current_user.id:
        raise NotAuthorizedShareFileException()
    db.delete(db_share)
    db.commit()
    return db_share


def get_shared_files(current_user: User, db: Session) -> [DbFileMetadata]:
    shares = db.query(ShareFileUser).filter(ShareFileUser.user_id == current_user.id).all()
    files = []
    for share in shares:
        f = db.query(DbFileMetadata).filter(DbFileMetadata.id == share.file_id, DbFileMetadata.is_dir == False,
                                            DbFileMetadata.is_deleted == False).first()
        if f:
            files.append(f)
    return files


def get_shared_dir(current_user: User, db: Session) -> [DbFileMetadata]:
    shares = db.query(ShareFileUser).filter(ShareFileUser.user_id == current_user.id).all()
    files = []
    for share in shares:
        f = db.query(DbFileMetadata).filter(DbFileMetadata.id == share.file_id, DbFileMetadata.is_dir == True,
                                            DbFileMetadata.is_deleted == False).first()
        if f:
            files.append(f)
    return files


def get_shared_files_in_dir(current_user: User, dir_id: int,  db: Session) -> [DbFileMetadata]:
    share = db.query(ShareFileUser).filter(ShareFileUser.user_id == current_user.id, ShareFileUser.file_id == dir_id).first()
    files = []
    file = db.query(DbFileMetadata).filter(DbFileMetadata.id == share.file_id).first()
    if file.is_dir:
        files = db.query(DbFileMetadata).filter(DbFileMetadata.parent_id == file.id,
                                                DbFileMetadata.is_deleted == False).all()
    return [f for f in files if file_service.get_read_rights(db, f.id, current_user.id)]


def get_files_for_shares(current_user: User, db: Session) -> [DbFileMetadata]:
    shares = db.query(ShareFileUser).filter(ShareFileUser.user_id == current_user.id).all()
    files = []
    for share in shares:
        f = db.query(DbFileMetadata).filter(DbFileMetadata.id == share.file_id,
                                            DbFileMetadata.is_deleted == False).first()
        if f:
            files.append(f)
    return files


