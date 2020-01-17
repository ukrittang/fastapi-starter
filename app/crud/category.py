from typing import List, Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE

from app.db_models.category import Category
from app.models.category import CategoryCreate, CategoryUpdate


def get(db: Session, *, obj_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == obj_id).first()


def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[Optional[Category]]:
    return db.query(Category).offset(skip).limit(limit).all()


def create(db: Session, *, obj_in: CategoryCreate) -> Category:
    obj_in_data = jsonable_encoder(obj_in)
    if obj_in_data['parent_id'] == 0:
        obj_in_data['parent_id'] = None
    obj = Category(**obj_in_data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, *, obj: Category, obj_in: CategoryUpdate) -> Category:
    obj_data = jsonable_encoder(obj)
    update_data = obj_in.dict(skip_defaults=True)
    for field in obj_data:
        if field in update_data:
            setattr(obj, field, update_data[field])
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, *, obj_id: int) -> bool:
    obj = db.query(Category).filter(Category.id == obj_id).first()
    if not obj:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Category not found!")
    if obj.children:
        raise HTTPException(status_code=HTTP_406_NOT_ACCEPTABLE, detail="Delete children first!")
    db.delete(obj)
    db.commit()
    return True
