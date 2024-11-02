from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.modules.users.schema import UserResponse, UsersResponse, UserCreate
from app.modules.users.service import (
    get_users,
)
from app.db.database import get_db

router = APIRouter()


@router.get("/", response_model=UsersResponse)
def all(db: Session = Depends(get_db)):
    users = get_users(db=db)
    return users


# @router.post("/", response_model=UserResponse)
# def create_new_user(
#     user: UserCreate,
#     db: Session = Depends(get_db),
# ):
#     return create_user(db, user)
