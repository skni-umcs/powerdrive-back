
from sqlalchemy.orm import Session
from src.group.groupExceptions import GroupNotFoundException, OwnerNotFoundException

from fastapi import APIRouter, Depends, HTTPException, status

from src.group import groupConnector
from src.group.groupConnector import  get_group_by_index, update_group_by_index, delete_group_by_index
from src.group.schemas import Group, GroupCreate, GroupUpdate
from src.user.schemas import User
from src.dependencies import get_db

from src.user.userConnector import get_user_by_index


api_router = APIRouter(prefix="/group", tags=["group"])


@api_router.post("/", response_model=Group)
async def add_group(group: GroupCreate, db: Session = Depends(get_db)):#, current_user: User = Depends(get_current_user)):
    try:
        current_user = get_user_by_index(session=db, user_id=1)
    except OwnerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        new_group = groupConnector.add_group(group=group, session=db, owner=current_user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return new_group

@api_router.post("/", response_model=Group)
async def add_group(group: GroupCreate, user: User, current_user: User, db: Session = Depends(get_db)):
    #, current_user: User = Depends(get_current_user)):
    try:
        current_user = get_user_by_index(session=db, user_id=1)
    except OwnerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        new_group = groupConnector.add_group(group=group, session=db, owner=current_user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return new_group


@api_router.get("/", response_model=list[Group])
async def get_all_groups(db: Session = Depends(get_db)):#, current_user: User = Depends(get_current_user)):
    return groupConnector.get_all_groups(db)


@api_router.get("/{group_id}", response_model=Group)
async def get_group(group_id: int, db: Session = Depends(get_db)):#, current_user: User = Depends(get_current_user)):
    try:
        group = get_group_by_index(session=db, group_id=group_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return group


@api_router.put("/{group_id}", response_model=Group)
async def update_group(incoming_group: GroupUpdate, db: Session = Depends(get_db)): #,
                       #current_user: User = Depends(get_current_user)):
    current_user = get_user_by_index(session=db, user_id=1)
    try:
        updated_group = update_group_by_index(session=db, incoming_group=incoming_group, current_user=current_user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return updated_group


@api_router.delete("/{group_id}", status_code=204)
async def delete_group(group_id: int, db: Session = Depends(get_db)):#, current_user: User = Depends(get_current_user)):
    current_user = get_user_by_index(session=db, user_id=1)
    try:
        delete_group_by_index(session=db, group_id=group_id, current_user=current_user)
    except GroupNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
