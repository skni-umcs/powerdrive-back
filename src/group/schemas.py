from pydantic import BaseModel


class GroupBase(BaseModel):
    group_name: str | None
    group_description: str | None
    group_owner_id: int | None


class GroupCreate(GroupBase):
    group_name: str


class GroupUpdate(GroupBase):
    group_id: int


class Group(GroupBase):
    group_id: int
    group_name: str
    group_description: str | None
    group_owner_id: int

    class Config:
        orm_mode = True


class GroupUser(BaseModel):
    group_user_id: int
    group_id: int
    user_id: int
    class Config:
        orm_mode = True
