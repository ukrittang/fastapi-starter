from typing import List, Optional

from pydantic import BaseModel

from app.models.item import Item


# Shared properties
class UserBase(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None


class UserBaseInDB(UserBase):
    pass


# Properties to receive via API on creation
class UserCreate(UserBaseInDB):
    email: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
    hashed_password: str
