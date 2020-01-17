from fastapi import APIRouter

from app.api.api_v1.endpoints import (auth, category, items, location, users,
                                      utils)
from app.core import config

api_router = APIRouter()
api_router.include_router(auth.router, prefix=config.API_AUTH_PREFIX, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(location.router, prefix="/locations", tags=["locations"])
