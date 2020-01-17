from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from app.db.base_class import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", cascade='delete', back_populates="category")
    # parent = relationship("Category", cascade='delete', remote_side=[id])
    children = relationship("Category", backref=backref('parent', remote_side=id))
