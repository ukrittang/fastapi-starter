from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    title: str
    description: str
    category_id: int
    location_id: int


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemBaseInDB(ItemBase):
    id: int
    owner_id: int


# Properties to return to client
class Item(ItemBaseInDB):
    class Config:
        orm_mode = True


# Properties properties stored in DB
class ItemInDB(ItemBaseInDB):
    pass
