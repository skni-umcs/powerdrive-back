from sqlalchemy.orm import Session
from src.user.models import User
from src.admin.exceptions import UserNotFoundException


def add_admin(session: Session, user_id: int) -> User:
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    user.is_admin = True
    session.commit()
    return user


def delete_admin(session: Session, user_id: int) -> User:
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    user.is_admin = False
    session.commit()
    return user


def get_all_admins(session: Session) -> list[User]:
    admins = session.query(User).filter(User.is_admin).all()
    return admins
