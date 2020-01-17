from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser
from app.crud import category as crud_category
from app.db_models.user import User as DBUser
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.models.msg import Msg

router = APIRouter()


@router.post("", response_model=Category)
def create_category(
    *,
    db: Session = Depends(get_db),
    obj_in: CategoryCreate,
    # pylint: disable=unused-argument
    current_user: DBUser = Depends(get_current_active_superuser)
):
    """
    Create new category.
    """
    item = crud_category.create(db=db, obj_in=obj_in)
    return item


@router.put("/{category_id}", response_model=Category)
def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    name: str = Body(None),
    slug: str = Body(None),
    parent_id: int = Body(None),
    is_active: bool = Body(None),
    # pylint: disable=unused-argument
    current_user: DBUser = Depends(get_current_active_superuser),
):
    """
    Update category.
    """
    current_obj = crud_category.get(db=db, obj_id=category_id)
    current_category_data = jsonable_encoder(current_obj)
    obj_in = CategoryUpdate(**current_category_data)
    if name is not None:
        obj_in.name = name
    if slug is not None:
        obj_in.slug = slug
    if parent_id is not None:
        if parent_id != 0:
            obj_in.parent_id = parent_id
    if is_active is not None:
        obj_in.is_active = is_active
    obj = crud_category.update(db, obj=current_obj, obj_in=obj_in)
    return obj


@router.delete("/{category_id}", response_model=Msg)
def delete_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    # pylint: disable=unused-argument
    current_user: DBUser = Depends(get_current_active_superuser)
):
    """
    Delete category.
    """
    obj = crud_category.delete(db=db, obj_id=category_id)
    if obj:
        return {"msg": "Success"}
    return {"msg": "Failed"}


@router.get("", response_model=List[Category])
def read_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000
):
    """
    Retrieve items.
    """
    obj_list = crud_category.get_multi(db, skip=skip, limit=limit)
    return obj_list


@router.get("/{category_id}", response_model=Category)
def read_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    # current_user: DBUser = Depends(get_current_active_user),
):
    """
    Get category by ID.
    """
    obj = crud_category.get(db=db, obj_id=category_id)
    if not obj:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Category not found")
    return obj
