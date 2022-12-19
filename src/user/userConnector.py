# TODO: add privilege_id to function parameters and uncomment privilege in update function
# TODO: when constraints will start to work
from src.user.userExceptions import UserNotFoundException, UsernameTakenException
from sqlalchemy.orm import Session
from src.user.models import DBUser
from src.user.schemas import UserCreate, UserUpdate
from src.user.security_utils import get_password_hash


def add_user(session: Session, user_in: UserCreate) -> DBUser:
    user = DBUser(**user_in.dict(exclude={"password"}))
    user.hash_password = get_password_hash(user_in.password)
    session.add(user)
    session.commit()

    return user


def get_user_by_index(session: Session, user_id: int) -> DBUser:
    user = session.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise UserNotFoundException()

    return user


def update_user(session: Session, user_update_in: UserUpdate) -> DBUser:
    user = session.query(DBUser).filter(DBUser.user_id == user_update_in.id).first()

    if not user:
        raise UserNotFoundException()

    user.user_name = user_update_in.username
    user.first_name = user_update_in.first_name
    user.last_name = user_update_in.last_name
    user.password = get_password_hash(user_update_in.password)
    user.email = user_update_in.email
    session.commit()
    return user


def delete_user_by_index(session: Session, user_id: int) -> None:
    user = session.query(DBUser).filter(DBUser.user_id == user_id).first()

    if not user:
        raise UserNotFoundException()

    session.delete(user)
    session.commit()


def get_all_users(session: Session, ) -> list[DBUser]:
    users = session.query(DBUser).all()
    return users


def get_user_by_username(session: Session, username: str) -> DBUser:
    user = session.query(DBUser).filter(DBUser.user_name == username).first()
    if not user:
        raise UserNotFoundException()

    return user
