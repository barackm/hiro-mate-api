from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .model import User
from .schema import UserCreate
from datetime import datetime, timezone


def get_users(db: Session):
    users = db.query(User).all()
    total = db.query(User).count()
    return {"total": total, "data": users}


def validate_user_does_not_exist(db: Session, identifier: str):
    if get_user_by_email(db, identifier):
        raise HTTPException(
            status_code=400, detail="User with this email already exists."
        )


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, identifier: str):

    return (
        db.query(User)
        .filter(or_(User.email == identifier, User.phone == identifier))
        .first()
    )


def get_user_by_email_or_phone_number(db: Session, identifier: str):
    user = (
        db.query(User)
        .filter(or_(User.phone == identifier, User.email == identifier))
        .first()
    )

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    return user


def create_user_from_google(db: Session, user_data: UserCreate):
    user = get_user_by_email(db, user_data["email"])
    if user:
        return user

    new_user = User(
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        email=user_data["email"],
        sub=user_data["sub"],
        account_confirmed_at=datetime.now(timezone.utc),
        provider="google",
    )

    db.add(new_user)
    db.commit()

    return new_user
