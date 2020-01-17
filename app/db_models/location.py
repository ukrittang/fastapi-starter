from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from app.db.base_class import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("locations.id"))
    is_active = Column(Boolean(), default=True, index=True)

    items = relationship("Item", cascade='delete', back_populates="location")
    # parent = relationship("Location", cascade='delete', remote_side=[id])
    children = relationship("Location", backref=backref('parent', remote_side=id))
