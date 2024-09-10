from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.modules.users.schema import UserResponse, UsersResponse, UserCreate
from app.modules.users.service import get_users, create_user
from app.db.database import get_db

router = APIRouter()


@router.get("/", response_model=UsersResponse)
def all(db: Session = Depends(get_db)):
    users = get_users(db=db)
    return users


@router.post("/", response_model=UserResponse)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    program_id: str = Query(None),
    level_id: str = Query(None),
    time_slot_id: str = Query(None),
):
    print("program_id", program_id)
    print("level_id", level_id)
    print("time_slot_id", time_slot_id)
    return create_user(db, user, program_id, level_id, time_slot_id)
