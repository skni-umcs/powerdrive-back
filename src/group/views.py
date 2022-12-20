from sqlalchemy.orm import Session
from src.group.groupExceptions import GroupNotFoundException, OwnerNotFoundException
from fastapi import APIRouter, Depends, HTTPException

from src.group import groupConnector
from src.group.groupConnector import get_group_by_index, update_group_by_index, delete_group_by_index
from src.group.schemas import Group, GroupCreate, GroupUpdate, GroupUser
from src.user.schemas import User
from src.dependencies import get_db

from src.user.userConnector import get_user_by_index


api_router = APIRouter(prefix="/group", tags=["group"])


@api_router.post("/", response_model=Group)
async def add_group(group: GroupCreate,  current_user: User, db: Session = Depends(get_db)):
    try:
        db_current_user = get_user_by_index(session=db, user_id=current_user.id)
    except OwnerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        new_group = groupConnector.add_group(group=group, session=db, owner=db_current_user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return new_group


@api_router.post("/{group_id}/add_user", response_model=GroupUser)
async def add_user_to_group(group_id: int, user: User, current_user: User, db: Session = Depends(get_db)):
    try:
        db_current_user = get_user_by_index(session=db, user_id=current_user.id)
    except OwnerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        new_group_user = groupConnector.add_user_to_group(session=db,
                                                          group=get_group_by_index(session=db, group_id=group_id),
                                                          new_user=user, current_user=db_current_user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return new_group_user


@api_router.get("/", response_model=list[Group])
async def get_all_groups(db: Session = Depends(get_db)):
    return groupConnector.get_all_groups(db)


@api_router.get("/{group_id}", response_model=Group)
async def get_group(group_id: int, db: Session = Depends(get_db)):
    try:
        group = get_group_by_index(session=db, group_id=group_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return group


@api_router.get("/{group_id}/users", response_model=list[User])
async def get_group_users(group_id: int, db: Session = Depends(get_db)):
    return groupConnector.get_group_users(session=db, group_id=group_id)


@api_router.put("/{group_id}", response_model=Group)
async def update_group(incoming_group: GroupUpdate, current_user: User, db: Session = Depends(get_db)):
    db_current_user = get_user_by_index(session=db, user_id=current_user.id)
    try:
        updated_group = update_group_by_index(session=db, incoming_group=incoming_group, current_user=db_current_user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return updated_group


@api_router.delete("/{group_id}", status_code=204)
async def delete_group(group_id: int, current_user: User, db: Session = Depends(get_db)):
    db_current_user = get_user_by_index(session=db, user_id=current_user.id)
    try:
        delete_group_by_index(session=db, group_id=group_id, current_user=db_current_user)
    except GroupNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api_router.delete("/{group_id}/delete_user/{user_id}", status_code=204)
async def delete_user_from_group(group_id: int, user_id: int, current_user: User, db: Session = Depends(get_db)):
    db_current_user = get_user_by_index(session=db, user_id=current_user.id)
    try:
        groupConnector.delete_user_from_group(session=db, group_id=group_id, user_id=user_id,
                                              current_user=db_current_user)
    except GroupNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
