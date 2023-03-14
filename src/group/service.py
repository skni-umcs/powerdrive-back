from src.group.exceptions import GroupNotFoundException, OwnerNotFoundException, \
    GroupNameAlreadyExistsException, UserNotFoundException, NoGroupPermissionsException
from sqlalchemy.orm import Session
from src.group.models import Group, GroupUser
from src.group.schemas import GroupCreate, GroupUpdate
from src.user.service import get_by_index as get_user_by_index
from src.user.models import User
from fastapi import HTTPException



def if_current_can_manipulate_group(session: Session, group_id: int, current_user_id: int) -> bool:
    if get_user_by_index(session=session, user_id=current_user_id).if_admin:
        return True
    db_group = session.query(Group).filter(Group.group_id == group_id).first()
    if not db_group:
        return False
    if db_group.group_owner_id == current_user_id:
        print("bl")
        return True
    return False


def if_current_can_see_group(session: Session, group_id: int, current_user_id: int) -> bool:
    if get_user_by_index(session=session, user_id=current_user_id).if_admin:
        return True
    if session.query(GroupUser).filter(GroupUser.group_id == group_id and GroupUser.user_id == current_user_id).first()\
        or get_group_by_index(session=session, group_id=group_id).group_owner_id == current_user_id:
        return True
    return False


def get_group_by_index(session: Session, group_id: int) -> Group:
    group = session.query(Group).filter(Group.group_id == group_id).first()

    if not group:
        raise GroupNotFoundException()

    return group


def add_group(group: GroupCreate, session: Session, owner_id: int) -> Group:

    if get_group_by_name(session=session, group_name=group.group_name):
        raise GroupNameAlreadyExistsException()

    created_group = Group(group_name=group.group_name,
                          group_description=group.group_description,
                          group_owner_id=owner_id)
    session.add(created_group)
    session.commit()
    return created_group


# def get_all_groups(session: Session, current_user_id: int) -> list[Group]:
#     if if_current_can_manipulate_group(session=session, group_id=0, current_user_id=current_user_id):
#         groups = session.query(Group).all()
#         if not groups:
#             raise GroupNotFoundException()
#         return groups
#
#     db_group_for_user1 = session.query(GroupUser).filter(GroupUser.user_id == current_user_id).all()
#     db_group_for_user2 = session.query(Group).filter(Group.group_owner_id == current_user_id).all()
#
#     index1 = [g.user_id for g in db_group_for_user1]
#     index2 = [g.group_id for g in db_group_for_user2]
#     index = index1 + index2
#     unique_index = []
#     [unique_index.append(i) for i in index if i not in unique_index]
#     groups = [get_group_by_index(session, g, current_user_id) for g in unique_index]
#     if not groups:
#         raise GroupNotFoundException()
#     return groups
#
#
#
def get_by_index(session: Session, group_id: int, current_user_id: int) -> Group:
    if if_current_can_manipulate_group(session=session, group_id=group_id, current_user_id=current_user_id):
        group = session.query(Group).filter(Group.group_id == group_id).first()

        if not group:
            raise GroupNotFoundException()

        return group
    if if_current_can_see_group(session=session, group_id=group_id, current_user_id=current_user_id):
        group = session.query(Group).filter(Group.group_id == group_id).first()


        if not group:
            raise GroupNotFoundException()

        return group

    raise NoGroupPermissionsException()

#
#
# def get_group_users(session: Session, group_id: int, current_user_id: int) -> list[User]:
#     group = session.query(Group).filter(Group.group_id == group_id).first()
#
#     if not group:
#         raise GroupNotFoundException()
#
#     if group.group_owner_id != current_user_id \
#             or not get_user_by_index(session=session, user_id=current_user_id).if_admin:
#         raise HTTPException(status_code=401, detail=str("No group permission"))
#
#     users = []
#     group_users = session.query(GroupUser).filter(group_id == group_id).all()
#     for gu in group_users:
#         u = get_user_by_index(session=session, user_id=gu.user_id)
#         if not u:
#             raise UserNotFoundException()
#         users.append(u)
#     return users
#
#
def get_group_by_name(session: Session, group_name: str) -> Group:
    group = session.query(Group).filter(Group.group_name == group_name).first()
    return group


def update_group_by_index(session: Session, incoming_group: GroupUpdate, current_user_id: int) -> Group:
    if if_current_can_manipulate_group(session=session, group_id=incoming_group.group_id,
                                       current_user_id=current_user_id):
        db_group = get_group_by_index(session=session, group_id=incoming_group.group_id)

        if not db_group:
            raise GroupNotFoundException
        if incoming_group.group_description:
            db_group.group_description = incoming_group.group_description
        session.commit()
        return db_group

    raise NoGroupPermissionsException()



#
#
# def add_user_to_group(session: Session, group_id: int, new_user_id: int, current_user_id: int) -> GroupUser:
#     db_group = get_group_by_index(session=session, group_id=group_id, current_user_id=current_user_id)
#
#     if not db_group:
#         raise GroupNotFoundException
#
#     if db_group.group_owner_id != current_user_id \
#             or get_user_by_index(session=session, user_id=current_user_id).if_admin == False:
#         raise HTTPException(status_code=401, detail=str("No group permission"))
#
#     db_new_user = get_user_by_index(session=session, user_id=new_user_id)
#     if not db_new_user:
#         raise UserNotFoundException()
#     group_user = GroupUser(group_id=group_id, user_id=new_user_id)
#     session.add(group_user)
#     session.commit()
#     return group_user
#
#
# def delete_user_from_group(session: Session, group_id: int, user_id: int, current_user_id: int) -> None:
#     db_group = get_group_by_index(session=session, group_id=group_id, current_user_id=current_user_id)
#
#     if user_id == current_user_id:
#         db_group = session.query(GroupUser).filter(Group.group_id == group_id).first()
#
#     if not db_group:
#         raise GroupNotFoundException
#
#
#     group_user = session.query(GroupUser).filter(GroupUser.group_id == group_id
#                                                  and GroupUser.user_id == user_id).first()
#     session.delete(group_user)
#     session.commit()
#
#
def delete_group_by_index(session: Session, group_id: int, current_user_id: int) -> None:
    if if_current_can_manipulate_group(session=session, group_id=group_id, current_user_id=current_user_id):
        db_group = get_group_by_index(session=session, group_id=group_id)

        if not db_group:
            raise GroupNotFoundException

        session.delete(db_group)
        session.commit()
    else:
        raise HTTPException(status_code=401, detail=str("No group permission"))
