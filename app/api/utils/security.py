import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import (HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND)

from app import crud
from app.api.utils.db import get_db
from app.core import config
from app.core.jwt import ALGORITHM
from app.db_models.user import User
from app.models.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=config.API_LOGIN_URL)


def get_current_user(
    db: Session = Depends(get_db), token: str = Security(reusable_oauth2)
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = crud.user.get(db, user_id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_current_active_user(current_user: User = Security(get_current_user)):
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="The user doesn't have enough privileges"
        )
    return current_user
