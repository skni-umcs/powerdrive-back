from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.files.service import add_new_file_and_save_od_disk

from src.files.exceptrions import FileNotFoundException, FileAlreadyExistsException
from src.files.schemas import FileMetadata, FileMetadataCreate, FileMetadataUpdate

from src.dependencies import get_db

from src.user.service import get_by_index as get_user_by_index
from src.user.schemas import User

api_router = APIRouter(prefix="/file", tags=["file"])


def get_current_user() -> User:
    db = get_db().__next__()
    return get_user_by_index(db, 1)


# @api_router.post("/", response_model=FileMetadata)
# def add_file(file_data: UploadFile,
#              current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     # def add_file(file_data: UploadFile, file_meta: FileMetadataCreate = Form(), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return add(db, file_data, file_meta, current_user)
@api_router.post("/", response_model=FileMetadata)
def add_file(file_data: UploadFile, file_meta: FileMetadataCreate = Form(),
             current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        file_ = add_new_file_and_save_od_disk(db, file_meta, file_data, current_user.id)
    except FileAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    # except ValueError as e:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    # except OSError as e:
    #     print(e)
    #     raise HTTPException(status_code=status.HTTP_507_INSUFFICIENT_STORAGE, detail=str(e))

    return file_
