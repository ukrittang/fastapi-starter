from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from app.api.utils.db import get_db
from app.api.utils.security import (get_current_active_superuser,
                                    get_current_active_user)
from app.core import config
from app.crud import user as crud_user
from app.db_models.user import User as DBUser
from app.models.user import User, UserCreate, UserInDB, UserUpdate
from app.utils import send_new_account_email

router = APIRouter()


@router.get("", response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve users.
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("", response_model=User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
):
    """
    Create new user.
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = crud_user.create(db=db, user_in=user_in)
    if config.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud_user.update(db, user=current_user, user_in=user_in)
    return user


@router.get("/me", response_model=User)
def read_user_me(
    # db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user),
):
    """
    Get current user.
    """
    return current_user


@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific user by id.
    """
    user = crud_user.get(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    # pylint: disable=unused-argument
    current_user: UserInDB = Depends(get_current_active_superuser),
):
    """
    Update a user.
    """
    user = crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    user = crud_user.update(db, user=user, user_in=user_in)
    return user
