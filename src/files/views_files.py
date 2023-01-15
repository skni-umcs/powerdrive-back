from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.files.service import add_new_file_and_save_od_disk, get_file_metadata_by_id, delete_file_by_id, \
    get_file_chidlren, change_file_content_on_diks
from src.files.exceptions import FileNotFoundException, FileAlreadyExistsException
from src.files.schemas import FileMetadata, FileMetadataCreate, FileMetadataUpdate
from src.files.utilis import get_base_path_for_user

from src.dependencies import get_db

from src.user.service import get_by_index as get_user_by_index, update
from src.user.schemas import User

api_router = APIRouter(prefix="/file", tags=["file"])


def get_current_user() -> User:
    db = get_db().__next__()
    return get_user_by_index(db, 1)


@api_router.post("", response_model=FileMetadata)
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


@api_router.get("/{file_id}", response_model=FileMetadata)
def get_file_details(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        file_ = get_file_metadata_by_id(db, file_id, current_user.id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return file_


@api_router.get("/{file_id}/download", response_class=FileResponse)
def download_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        file_ = get_file_metadata_by_id(db, file_id, current_user.id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return FileResponse(get_base_path_for_user(current_user.id) + file_.path, filename=file_.filename,
                        media_type=file_.type)


@api_router.delete("/{file_id}", status_code=204)
def delete_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        file_ = delete_file_by_id(db, file_id, current_user.id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    # return file_


@api_router.put("", response_model=FileMetadata)
def update_file(file_meta: FileMetadataUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    try:
        file_ = update(db, file_meta, current_user.id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return file_


@api_router.put("/{file_id}/change_content", response_model=FileMetadata)
def change_file_content(file_id: int, file_data: UploadFile, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    try:
        file_ = change_file_content_on_diks(db, file_id, file_data, current_user.id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return file_


# @api_router.get("/zip/{dir_id}")
# def get_dir_content_as_zip(dir_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")

@api_router.get("/{file_id}/list", response_model=list[FileMetadata])
def get_directory_children(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_file_chidlren(db, file_id, current_user.id)

# @api_router.get("/{dir_id/list", response_model=list[FileMetadata])
# def list_files(dir_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     pass
