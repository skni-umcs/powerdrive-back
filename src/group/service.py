from src.group.exceptions import GroupNotFoundException, OwnerNotFoundException, \
    GroupNameAlreadyExistsException, UserNotFoundException, NoGroupPermissionsException
from sqlalchemy.orm import Session
from src.group.models import DBGroup, DBGroupUser
from src.group.schemas import GroupCreate, GroupUpdate, Group
from src.user.service import get_by_index
# from src.user.schemas import User
from src.user.models import User


def add_group(group: GroupCreate, session: Session, owner_id: int) -> DBGroup:

    if get_group_by_name(session=session, group_name=group.group_name):
        raise GroupNameAlreadyExistsException()
    db_owner = get_by_index(session=session, user_id=owner_id)
    if not db_owner:
        raise OwnerNotFoundException()

    created_group = DBGroup(group_name=group.group_name,
                            group_description=group.group_description,
                            group_owner_id=db_owner.id)
    session.add(created_group)
    session.commit()
    return created_group


def get_all_groups(session: Session,) -> list[DBGroup]:
    groups = session.query(DBGroup).all()
    return groups


def get_group_by_index(session: Session, group_id: int) -> DBGroup:
    group = session.query(DBGroup).filter(DBGroup.group_id == group_id).first()

    if not group:
        raise GroupNotFoundException()

    return group


def get_group_users(session: Session, group_id: int) -> list[User]:
    group = session.query(DBGroup).filter(DBGroup.group_id == group_id).first()

    if not group:
        raise GroupNotFoundException()

    users = []
    group_users = session.query(DBGroupUser).filter(group_id == group_id).all()
    for gu in group_users:
        u = get_by_index(session=session, user_id=gu.user_id)
        if not u:
            raise UserNotFoundException()
        users.append(u)
    return users


def get_group_by_name(session: Session, group_name: str) -> DBGroup:
    group = session.query(DBGroup).filter(DBGroup.group_name == group_name).first()
    return group


def update_group_by_index(session: Session, incoming_group: GroupUpdate, current_user_id: int) -> DBGroup:
    db_group = get_group_by_index(session=session, group_id=incoming_group.group_id)
    if not db_group:
        raise GroupNotFoundException
    if db_group.group_owner_id != current_user_id:
        raise NoGroupPermissionsException()
    if incoming_group.group_description:
        db_group.group_description = incoming_group.group_description

    session.commit()
    return db_group


def add_user_to_group(session: Session, group: Group, new_user_id: int, current_user_id: int) -> DBGroupUser:
    if get_by_index(session=session, user_id=group.group_owner_id) != get_by_index(session=session,
                                                                                             user_id=current_user_id):
        raise NoGroupPermissionsException()

    db_new_user = get_by_index(session=session, user_id=new_user_id)
    if not db_new_user:
        raise UserNotFoundException()
    group_user = DBGroupUser(group_id=group.group_id, user_id=db_new_user.id)
    session.add(group_user)
    session.commit()
    return group_user


def delete_user_from_group(session: Session, group_id: int, user_id: int, current_user_id: int) -> None:
    group = get_group_by_index(session=session, group_id=group_id)
    if not group:
        raise GroupNotFoundException
    if get_by_index(session=session, user_id=group.group_owner_id) != get_by_index(session=session,
                                                                                   user_id=current_user_id):
        raise NoGroupPermissionsException()
    group_user = session.query(DBGroupUser).filter(DBGroupUser.group_id == group_id
                                                   and DBGroupUser.user_id == user_id).first()
    session.delete(group_user)
    session.commit()


def delete_group_by_index(session: Session, group_id: int, current_user_id: int) -> None:
    group = session.query(DBGroup).filter(DBGroup.group_id == group_id).first()
    if get_by_index(session=session, user_id=group.group_owner_id) != get_by_index(session=session,
                                                                                       user_id=current_user_id):
        raise NoGroupPermissionsException()

    if not group:
        raise GroupNotFoundException()

    session.delete(group)
    session.commit()
