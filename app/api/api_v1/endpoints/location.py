from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser
from app.crud import location as crud_location
from app.db_models.user import User as DBUser
from app.models.location import Location, LocationCreate, LocationUpdate
from app.models.msg import Msg

router = APIRouter()


@router.post("", response_model=Location)
def create_location(
    *,
    db: Session = Depends(get_db),
    obj_in: LocationCreate,
    # pylint: disable=unused-argument
    current_user: DBUser = Depends(get_current_active_superuser)
):
    """
    Create new location.
    """
    item = crud_location.create(db=db, obj_in=obj_in)
    return item


@router.put("/{location_id}", response_model=Location)
def update_location(
    *,
    db: Session = Depends(get_db),
    location_id: int,
    name: str = Body(None),
    slug: str = Body(None),
    parent_id: int = Body(None),
    is_active: bool = Body(None),
    # pylint: disable=unused-argument
    current_user: DBUser = Depends(get_current_active_superuser),
):
    """
    Update location.
    """
    current_obj = crud_location.get(db=db, obj_id=location_id)
    current_location_data = jsonable_encoder(current_obj)
    obj_in = LocationUpdate(**current_location_data)
    if name is not None:
        obj_in.name = name
    if slug is not None:
        obj_in.slug = slug
    if parent_id is not None:
        if parent_id != 0:
            obj_in.parent_id = parent_id
    if is_active is not None:
        obj_in.is_active = is_active
    obj = crud_location.update(db, obj=current_obj, obj_in=obj_in)
    return obj


@router.delete("/{location_id}", response_model=Msg)
def delete_location(
    *,
    db: Session = Depends(get_db),
    location_id: int,
    # pylint: disable=unused-argument
    current_user: DBUser = Depends(get_current_active_superuser)
):
    """
    Delete location.
    """
    obj = crud_location.delete(db=db, obj_id=location_id)
    if obj:
        return {"msg": "Success"}
    return {"msg": "Failed"}


@router.get("", response_model=List[Location])
def read_locations(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000
):
    """
    Retrieve items.
    """
    obj_list = crud_location.get_multi(db, skip=skip, limit=limit)
    return obj_list


@router.get("/{location_id}", response_model=Location)
def read_location(
    *,
    db: Session = Depends(get_db),
    location_id: int,
    # current_user: DBUser = Depends(get_current_active_user),
):
    """
    Get location by ID.
    """
    obj = crud_location.get(db=db, obj_id=location_id)
    if not obj:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Location not found")
    return obj
