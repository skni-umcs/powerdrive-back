from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Body
from sqlalchemy.orm import Session

from src.files.service import add  # ,  get_by_index, update, delete_by_index, get_all

from src.files.exceptrions import FileNotFoundException
from src.files.schemas import FileMetadata, FileMetadataCreate, FileMetadataUpdate

from src.dependencies import get_db

api_router = APIRouter(prefix="/file", tags=["file"])


# @api_router.get("/{file_id}", response_model=File)
# def get_file(file_id: int, db: Session = Depends(get_db)):
#     try:
#         file = get_by_index(db, file_id)
#     except FileNotFoundException as e:
#         raise HTTPException(status_code=404, detail=str(e))
#
#     return file

# @api_router.get("/", response_model=list[File])
# def get_all_files(db: Session = Depends(get_db)):
#     return get_all(db)

@api_router.post("/", response_model=FileMetadata)
def add_file(file_data: UploadFile, file_meta: FileMetadataCreate = Form(), db: Session = Depends(get_db)):
    return add(db, file_data, file_meta)
