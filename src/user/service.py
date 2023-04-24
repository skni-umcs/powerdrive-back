# TODO: add privilege_id to function parameters and uncomment privilege in update function
# TODO: when constraints will start to work
from src.user.exceptions import UserNotFoundException, UsernameTakenException, UserEmailTakenException
from sqlalchemy.orm import Session
from src.user.models import User
from src.user.schemas import UserCreate, UserUpdate
from src.user.models import get_password_hash


def add(session: Session, user_in: UserCreate) -> User:
    if get_by_username(session, user_in.username):
        raise UsernameTakenException()

    if get_by_email(session, user_in.email):
        raise UserEmailTakenException()

    user = User(**user_in.dict(exclude={"password"}))
    user.password = get_password_hash(user_in.password)
    session.add(user)
    session.commit()

    return user


def get_by_index(session: Session, user_id: int) -> User:
    return session.query(User).filter(User.id == user_id).first()


def update(session: Session, user_update_in: UserUpdate) -> User:
    user = get_by_index(session, user_update_in.id)

    if not user:
        raise UserNotFoundException()

    existing_user = get_by_username(session, user_update_in.username)
    if existing_user and existing_user.id != user.id:
        raise UsernameTakenException()

    existing_user = get_by_email(session, user_update_in.email)
    if existing_user and existing_user.id != user.id:
        raise UserEmailTakenException()

    user.username = user_update_in.username
    user.first_name = user_update_in.first_name
    user.last_name = user_update_in.last_name
    user.password = get_password_hash(user_update_in.password)
    user.email = user_update_in.email
    session.commit()
    return user


def delete_by_index(session: Session, user_id: int) -> None:
    user = get_by_index(session, user_id)

    if not user:
        raise UserNotFoundException()

    session.delete(user)
    session.commit()


def get_all(session: Session, ) -> list[User]:
    return session.query(User).all()


def get_by_username(session: Session, username: str) -> User:
    return session.query(User).filter(User.username == username).first()


def get_by_email(session: Session, email: str) -> User:
    return session.query(User).filter(User.email == email).first()
