# TODO: add privilege_id to function parameters and uncomment privilege in update function
# TODO: when constraints will start to work
from src.user.userExceptions import UserNotFoundException, UsernameTakenException
from sqlalchemy.orm import Session
from models import DBUser
from src.user.security_utils import get_password_hash


def add_user(session: Session, username: str, first_name: str, last_name: str,
             password: str, ) -> DBUser:
    if session.query(DBUser).filter(DBUser.username == username).first():
        raise UsernameTakenException()

    user = DBUser(user_name=username, first_name=first_name,
                  last_name=last_name, user_password=get_password_hash(password))
    session.add(user)
    session.commit()

    return user


def get_user_by_index(session: Session, user_id: int) -> DBUser:
    user = session.query(DBUser).filter(DBUser.user_id == user_id).first()
    if not user:
        raise UserNotFoundException()

    return user


def update_user_by_index(session: Session, user_id: int, username: str, first_name: str,
                         last_name: str, password: str, ) -> None:
    user = session.query(DBUser).filter(DBUser.user_id == user_id).first()

    if not user:
        raise UserNotFoundException()

    user_err = session.query(DBUser).filter(DBUser.user_name == username,
                                            DBUser.user_id != user_id).first()
    if user_err:
        raise UsernameTakenException()



    if username:
        user.user_name = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        user.hashed_password = get_password_hash(password)

    session.commit()


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
