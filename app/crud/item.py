from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db_models.item import Item
from app.models.item import ItemCreate


def get(db: Session, *, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()


def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[Optional[Item]]:
    return db.query(Item).offset(skip).limit(limit).all()


def get_multi_by_owner(
    db: Session, *, owner_id: int, skip=0, limit=100
) -> List[Optional[Item]]:
    return (
        db.query(Item)
        .filter(Item.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(db: Session, *, item_in: ItemCreate, owner_id: int) -> Item:
    item_in_data = jsonable_encoder(item_in)
    item = Item(**item_in_data, owner_id=owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
