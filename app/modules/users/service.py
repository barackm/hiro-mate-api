from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .model import User
from .schema import UserCreate
from datetime import datetime
from ..enrollments.service import create_user_enrollment, validate_enrollment_details


def get_users(db: Session):
    users = db.query(User).all()
    total = db.query(User).count()
    return {"total": total, "data": users}


# def create_user(
#     db: Session,
#     user_data: UserCreate,
# ) -> User:
#     promotion_id = user_data["promotion_id"]
#     level_id = user_data["level_id"]
#     time_slot_id = user_data["time_slot_id"]

#     validate_user_does_not_exist(
#         db, identifier=user_data["email"] if user_data["email"] else user_data["phone"]
#     )

#     if promotion_id and level_id:
#         promotion, level, time_slot = validate_enrollment_details(
#             db, promotion_id, level_id, time_slot_id
#         )
#     else:
#         promotion = level = time_slot = None

#     try:
#         new_user = create_new_user(db, user_data)
#         print(f"new_user {new_user}")
#         if promotion and level:
#             enrollment_data = {
#                 "user_id": new_user.id,
#                 "promotion_id": promotion.id,
#                 "level_id": level.id,
#                 "time_slot_id": time_slot.id if time_slot else None,
#             }
#             enrollment = create_user_enrollment(db=db, enrollment=enrollment_data)

#         db.commit()
#         db.refresh(new_user)
#         if promotion and level:
#             db.refresh(enrollment)

#         return new_user

#     except HTTPException:
#         raise
#     except Exception as e:
#         db.rollback()
#         print(e)
#         raise HTTPException(
#             status_code=500, detail=f"An unexpected error occurred. {e}"
#         )


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
    print("Creating user from Google", user_data)
    user = get_user_by_email(db, user_data["email"])
    if user:
        return user

    new_user = User(
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        email=user_data["email"],
        sub=user_data["sub"],
        account_confirmed_at=datetime.now(datetime.timezone.utc),
    )

    db.add(new_user)
    db.commit()

    return new_user
