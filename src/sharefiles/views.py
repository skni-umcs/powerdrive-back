from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.auth.security import get_current_user
from src.dependencies import get_db
from src.sharefiles.schemas import ShareFileUser, ShareFileUserCreate, ShareFileUserUpdate
from src.user.schemas import User
from src.sharefiles import service
from src.sharefiles.exceptions import NotAuthorizedShareFileException, FileNotFoundException


api_router = APIRouter(prefix="/share/file", tags=["sharefile"])


@api_router.post("/", response_model=ShareFileUser)
def add_share(share: ShareFileUserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        new_group = service.add(current_user=current_user, share=share, db=db)
    except NotAuthorizedShareFileException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except FileNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return new_group


@api_router.put("/{share_id}/", response_model=ShareFileUser)
def update_share(share_id: int, share: ShareFileUserUpdate,
                 current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        updated_group = service.update(current_user=current_user, share=share, db=db)
    except NotAuthorizedShareFileException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except FileNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return updated_group


@api_router.get("/{share_id}/", response_model=ShareFileUser)
def get_share(share_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.get_by_id(current_user=current_user, share_id=share_id, db=db)

@api_router.get("/", response_model=[ShareFileUser])
def get_all_shares(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.get_all(current_user=current_user, db=db)


@api_router.delete("/{share_id}/", status_code=204)
def delete_share(share_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        service.delete(current_user=current_user, share_id=share_id, db=db)
    except NotAuthorizedShareFileException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except FileNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

