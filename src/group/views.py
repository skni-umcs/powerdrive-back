from sqlalchemy.orm import Session
from src.group.exceptions import GroupNotFoundException, OwnerNotFoundException
from fastapi import APIRouter, Depends, HTTPException
from src.group import service
from src.group.schemas import Group, GroupCreate, GroupUpdate, GroupUser
from src.user.schemas import User
from src.dependencies import get_db
from src.auth.security import get_current_user

api_router = APIRouter(prefix="/group", tags=["group"])


@api_router.post("/", response_model=Group)
async def add_group(group: GroupCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        new_group = service.add_group(group=group, session=db, owner_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return new_group


@api_router.delete("/{group_id}", status_code=204)
async def delete_group(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        service.delete_group_by_index(session=db, group_id=group_id, current_user_id=current_user.id)
    except GroupNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


# @api_router.post("/{group_id}/add_user", response_model=GroupUser)
# async def add_user_to_group(group_id: int, user: User,
#                             current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     try:
#         new_group_user = service.add_user_to_group(session=db,
#                                                    group_id=group_id,
#                                                    new_user_id=user.id, current_user_id=current_user.id)
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     return new_group_user
#
#
# @api_router.get("/", response_model=list[Group])
# async def get_all_groups(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return service.get_all_groups(db, current_user.id)
#
#
@api_router.get("/{group_id}", response_model=Group)
async def get_group(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    try:
        group = service.get_by_index(session=db, group_id=group_id, current_user_id=current_user.id)

    except Exception as e:
        raise HTTPException(status_code=404, detail=str("Group not found"))
    return group
#
#
# @api_router.get("/{group_id}/users", response_model=list[User])
# async def get_group_users(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return service.get_group_users(session=db, group_id=group_id, current_user_id=current_user.id)
#
#
# @api_router.put("/{group_id}", response_model=Group)
# async def update_group(incoming_group: GroupUpdate, current_user: User = Depends(get_current_user),
#                        db: Session = Depends(get_db)):
#     try:
#         updated_group = service.update_group_by_index(session=db, incoming_group=incoming_group,
#                                                       current_user_id=current_user.id)
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))
#
#     return updated_group
#
#

#
#
# @api_router.delete("/{group_id}/delete_user/{user_id}", status_code=204)
# async def delete_user_from_group(group_id: int, user_id: int, current_user: User = Depends(get_current_user),
#                                  db: Session = Depends(get_db)):
#     try:
#         service.delete_user_from_group(session=db, group_id=group_id, user_id=user_id,
#                                        current_user_id=current_user.id)
#     except GroupNotFoundException as e:
#         raise HTTPException(status_code=404, detail=str(e))
