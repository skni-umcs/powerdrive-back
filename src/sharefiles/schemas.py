from pydantic import BaseModel

class ShareFileUserBase(BaseModel):
    file_id: int
    user_id: int
    read: bool
    write: bool
    delete: bool
    share: bool


class ShareFileUserCreate(ShareFileUserBase):
    pass


class ShareFileUserUpdate(ShareFileUserBase):
    id: int

class ShareFileUser(ShareFileUserBase):
    id: int


    class Config:
        orm_mode = True

