from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import src.files.service as service

from src.files.exceptions import FileNotFoundException, FileAlreadyExistsException, DirException
from src.files.schemas import FileMetadata, FileMetadataCreate, FileMetadataUpdate, OnlyDirectory, FileMetadataInDB
from src.files.utilis import get_base_path_for_user

from src.dependencies import get_db

from src.user.service import get_by_index as get_user_by_index
from src.user.schemas import User

from src.auth.security import get_current_user

api_router = APIRouter(prefix="/file", tags=["file"])


@api_router.get("/user_root_dir", response_model=FileMetadata)
async def get_user_root_dir(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get user's root directory
    """
    res = service.get_user_root_dir(db, current_user.id)
    # res = 1
    print(res)
    print(res.path)
    return res


@api_router.get("/dir_tree", response_model=OnlyDirectory)
# @api_router.get("/dir_tree/")
async def get_dir_tree(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get user's directory tree
    """
    res = service.get_dir_tree(db, current_user.id)
    return res


@api_router.post("", response_model=FileMetadata)
async def add_file(file_data: UploadFile | None = None, file_meta: FileMetadataCreate = Form(),
                   current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Add new file to database and save it on disk
    """
    try:
        # print(file_data.filename)
        file_ = service.add_new_file_and_save_on_disk(db, file_meta, file_data, current_user.id)
    except (FileAlreadyExistsException, DirException) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    # except ValueError as e:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    # except OSError as e:
    #     print(e)
    #     raise HTTPException(status_code=status.HTTP_507_INSUFFICIENT_STORAGE, detail=str(e))

    return file_


@api_router.put("", response_model=FileMetadata)
async def update_file(file_meta: FileMetadataUpdate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Update file metadata, may be used to rename file or move it to another directory

    can't change file content
    """
    try:
        file_ = service.update_file(db, file_meta, current_user.id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return file_


@api_router.get("/{file_id}", response_model=FileMetadata)
async def get_file_details(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get file metadata by id

    to get directory's children use `/file/{file_id}/list`

    to download file use `/file/{file_id}/download`

    to change file content use `/file/{file_id}/change_content`


    """
    try:
        file_ = service.get_file_metadata_by_id(db, file_id, current_user.id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    print(file_.path)
    return file_


@api_router.get("/{file_id}/download", response_class=FileResponse)
async def download_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Download file by id,

    if file is directory, download as zip <--- NOT IMPLEMENTED YET
    """
    try:
        file_ = service.get_file_metadata_by_id(db, file_id, current_user.id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    if file_.is_dir:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can't download directory (yet)")

    return FileResponse(get_base_path_for_user(current_user.id) + file_.path, filename=file_.filename,
                        media_type=file_.type)


@api_router.delete("/{file_id}", status_code=204)
async def delete_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete file by id
    """
    try:
        service.delete_file_by_id(db, file_id, current_user.id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



@api_router.put("/{file_id}/change_content", response_model=FileMetadata)
async def change_file_content(file_id: int, file_data: UploadFile, db: Session = Depends(get_db),
                              current_user: User = Depends(get_current_user)):
    """
    Change file content, may be used to update file content

    doesn't work for directories
    """
    try:
        file_ = service.change_file_content_on_disk(db, file_id, file_data, current_user.id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return file_


@api_router.get("/{file_id}/list", response_model=list[FileMetadata])
async def get_directory_children(file_id: int, db: Session = Depends(get_db),
                                 current_user: User = Depends(get_current_user)):
    """
    Get directory's children
    """
    return service.get_children(db, file_id, current_user.id)
