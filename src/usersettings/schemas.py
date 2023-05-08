from pydantic import BaseModel


class UserSettings(BaseModel):
    values: str

    class Config:
        orm_mode = True
