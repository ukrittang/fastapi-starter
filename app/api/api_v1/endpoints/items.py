from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_user
from app.crud import item as crud_item
from app.db_models.user import User as DBUser
from app.models.item import Item, ItemCreate

router = APIRouter()


@router.post("", response_model=Item)
def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: ItemCreate,
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Create new item.
    """
    item = crud_item.create(db=db, item_in=item_in, owner_id=current_user.id)
    return item


@router.get("", response_model=List[Item])
def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve items.
    """
    items = crud_item.get_multi(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=Item)
def read_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    # current_user: DBUser = Depends(get_current_active_user),
):
    """
    Get item by ID.
    """
    item = crud_item.get(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Item not found")
    return item
