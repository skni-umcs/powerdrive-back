# TODO: add privilege_id to function parameters and uncomment privilege in update function
# TODO: when constraints will start to work
from src.user.exceptions import UserNotFoundException, UsernameTakenException
from sqlalchemy.orm import Session
from src.user.models import User
from src.user.schemas import UserCreate, UserUpdate
from src.auth.security import get_password_hash


def add_user(session: Session, user_in: UserCreate) -> User:
    user = User(**user_in.dict(exclude={"password"}))
    user.password = get_password_hash(user_in.password)
    session.add(user)
    session.commit()

    return user


def get_user_by_index(session: Session, user_id: int) -> User:
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise UserNotFoundException()

    return user


def update_user(session: Session, user_update_in: UserUpdate) -> User:
    user = session.query(User).filter(User.user_id == user_update_in.id).first()

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
    user = session.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise UserNotFoundException()

    session.delete(user)
    session.commit()


def get_all_users(session: Session, ) -> list[User]:
    users = session.query(User).all()
    return users


def get_user_by_username(session: Session, username: str) -> User:
    user = session.query(User).filter(User.user_name == username).first()
    if not user:
        raise UserNotFoundException()

    return user
