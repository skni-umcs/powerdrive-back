# TODO: add privilege_id to function parameters and uncomment privilege in update function
# TODO: when constraints will start to work
from ..exceptions.userExceptions import UserNotFoundException, UsernameTakenException
from sqlalchemy.orm import Session
from ..models import dbUser
from rest.user.security_utils import get_password_hash


def add_user(session: Session, username: str, first_name: str, last_name: str,
             password: str, ) -> dbUser:
    if session.query(dbUser).filter(dbUser.username == username).first():
        raise UsernameTakenException()

    user = dbUser(username=username, first_name=first_name,
                  last_name=last_name, hashed_password=get_password_hash(password))
    session.add(user)
    session.commit()

    return user


def get_user_by_index(session: Session, user_id: int) -> dbUser:
    user = session.query(dbUser).filter(dbUser.user_id == user_id).first()
    if not user:
        raise UserNotFoundException()

    return user


def update_user_by_index(session: Session, user_id: int, username: str, first_name: str,
                         last_name: str, password: str, ) -> None:
    user = session.query(dbUser).filter(dbUser.user_id == user_id).first()

    if not user:
        raise UserNotFoundException()

    user_err = session.query(dbUser).filter(dbUser.username == username,
                                            dbUser.user_id != user_id).first()
    if user_err:
        raise UsernameTakenException()



    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    # if privilege_id:
    #     user.privilege_id = privilege_id
    if password:
        user.hashed_password = get_password_hash(password)

    session.commit()


def delete_user_by_index(session: Session, user_id: int) -> None:
    user = session.query(dbUser).filter(dbUser.user_id == user_id).first()

    if not user:
        raise UserNotFoundException()

    session.delete(user)
    session.commit()


def get_all_users(session: Session, ) -> list[dbUser]:
    users = session.query(dbUser).all()
    return users


def get_user_by_username(session: Session, username: str) -> dbUser:
    user = session.query(dbUser).filter(dbUser.username == username).first()
    if not user:
        raise UserNotFoundException()

    return user
