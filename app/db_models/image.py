import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db_models.item import Item


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    position = Column(Integer, default=1)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    owner = relationship("User", back_populates="images")
    item = relationship(Category, back_populates="images")
