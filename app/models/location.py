from typing import List, Optional

from pydantic import BaseModel

from app.models.item import Item


# Shared properties
class LocationBase(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive via API on create
class LocationCreate(LocationBase):
    parent_id: int = None


# Properties to receive via API on update
class LocationUpdate(LocationBase):
    parent_id: int = None


class LocationBaseInDB(LocationBase):
    id: int


class LocationParent(LocationBaseInDB):

    class Config:
        orm_mode = True


# Additional properties to return via API
class Location(LocationBaseInDB):
    parent: LocationParent = None
    items: List[Item] = []

    class Config:
        orm_mode = True


# Additional properties stored in DB
class LocationInDB(LocationBaseInDB):
    pass
