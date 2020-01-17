# Import all the models, so that Base has them before being
# imported by Alembic
# pylint: disable=unused-import
from app.db.base_class import Base
from app.db_models.category import Category
from app.db_models.item import Item
from app.db_models.location import Location
from app.db_models.user import User
