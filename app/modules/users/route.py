from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.modules.users.schema import UsersResponse
from app.modules.users.service import (
    get_users,
)
from app.db.database import get_db

router = APIRouter()


@router.get("/", response_model=UsersResponse)
def all(db: Session = Depends(get_db)):
    users = get_users(db=db)
    return users
