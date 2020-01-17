from typing import List, Optional

from pydantic import BaseModel

from app.models.item import Item


# Shared properties
class CategoryBase(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive via API on create
class CategoryCreate(CategoryBase):
    parent_id: int = None


# Properties to receive via API on update
class CategoryUpdate(CategoryBase):
    parent_id: int = None


class CategoryBaseInDB(CategoryBase):
    id: int


class CategoryParent(CategoryBaseInDB):

    class Config:
        orm_mode = True


# Additional properties to return via API
class Category(CategoryBaseInDB):
    parent: CategoryParent = None
    items: List[Item] = []

    class Config:
        orm_mode = True


# Additional properties stored in DB
class CategoryInDB(CategoryBaseInDB):
    pass
