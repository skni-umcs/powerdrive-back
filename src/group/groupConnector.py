from src.group.groupExceptions import GroupNotFoundException, OwnerNotFoundException, \
    GroupNameAlreadyExistsException, UserNotFoundException, NoGroupPermissionsException
from sqlalchemy.orm import Session
from src.group.models import DBGroup, DBGroupUser
from src.group.schemas import GroupCreate, GroupUpdate, Group
from src.user.userConnector import get_user_by_index
from src.user.schemas import User


def add_group(group: GroupCreate, session: Session, owner: User) -> DBGroup:

    if get_group_by_name(session=session, group_name=group.group_name):
        raise GroupNameAlreadyExistsException()
    db_owner = get_user_by_index(session=session, user_id=1)
    if not owner:
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


def get_group_by_name(session: Session, group_name: str) -> DBGroup:
    group = session.query(DBGroup).filter(DBGroup.group_name == group_name).first()
    return group


def update_group_by_index(session: Session, incoming_group: GroupUpdate, current_user: User) -> DBGroup:
    db_group = get_group_by_index(session=session, group_id=incoming_group.group_id)
    if not db_group:
        raise GroupNotFoundException
    if db_group.group_owner_id != current_user.id:
        raise NoGroupPermissionsException()
    if incoming_group.group_description:
        db_group.group_description = incoming_group.group_description

    session.commit()
    return db_group


def add_user_to_group(session: Session, group: Group, new_user: User, current_user: User) -> DBGroupUser:
    if get_user_by_index(session=session, user_id=group.group_owner_id) != get_user_by_index(session=session,
                                                                                             user_id=current_user.id):
        raise NoGroupPermissionsException()

    db_new_user = get_user_by_index(session=session, user_id=new_user.id)
    if not db_new_user:
        raise UserNotFoundException()
    group_user = DBGroupUser(group_id=group.group_id, user_id=db_new_user.id)
    session.commit()
    return group_user


def delete_group_by_index(session: Session, group_id: int, current_user: User) -> None:
    group = session.query(DBGroup).filter(DBGroup.group_id == group_id).first()

    if not group:
        raise GroupNotFoundException()

    session.delete(group)
    session.commit()
