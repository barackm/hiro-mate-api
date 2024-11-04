from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .model import UserEnrollment
from .schema import EnrollmentUpdate
from ..levels.service import get_level_by_id
from ..promotions.service import get_promotion_by_id
from ..time_slots.service import get_time_slot_by_id


def create_user_enrollment(
    db: Session,
    enrollment: dict,
    can_commit: bool = False,
) -> UserEnrollment:
    user_enrollment = UserEnrollment(
        **enrollment,
        end_date=None,
        status="active",
    )
    db.add(user_enrollment)
    if can_commit:
        db.commit()
        db.refresh(user_enrollment)

    return user_enrollment


def find_existing_user_enrollment(
    db: Session,
    user_id: str,
    promotion_id: str,
    level_id: str,
    exclude_enrollment_id: Optional[str] = None,
) -> Optional[UserEnrollment]:
    query = db.query(UserEnrollment).filter(
        UserEnrollment.user_id == user_id,
        UserEnrollment.promotion_id == promotion_id,
        UserEnrollment.level_id == level_id,
    )
    if exclude_enrollment_id:
        query = query.filter(UserEnrollment.id != exclude_enrollment_id)
    return query.first()


def update_user_enrollment(
    db: Session, enrollment_id: str, enrollment_data: EnrollmentUpdate
) -> UserEnrollment:
    enrollment = (
        db.query(UserEnrollment).filter(UserEnrollment.id == enrollment_id).first()
    )
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found.")

    user_id = enrollment.user_id

    if enrollment_data.promotion_id and enrollment_data.level_id:
        promotion, level, time_slot = validate_enrollment_details(
            db,
            promotion_id=enrollment_data.promotion_id,
            level_id=enrollment_data.level_id,
            time_slot_id=enrollment_data.time_slot_id,
        )

        existing_enrollment = find_existing_user_enrollment(
            db,
            user_id=user_id,
            promotion_id=promotion.id,
            level_id=level.id,
            exclude_enrollment_id=enrollment_id,
        )
        if existing_enrollment:
            raise HTTPException(
                status_code=400,
                detail="User is already enrolled in the specified promotion and level.",
            )

        enrollment.promotion_id = promotion.id
        enrollment.level_id = level.id
        enrollment.time_slot_id = time_slot.id if time_slot else None

    if enrollment_data.status is not None:
        enrollment.status = enrollment_data.status
    if enrollment_data.end_date is not None:
        enrollment.end_date = enrollment_data.end_date

    try:
        db.commit()
        db.refresh(enrollment)
        return enrollment
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to update enrollment."
        ) from e


def delete_user_enrollment(db: Session, enrollment_id: str) -> UserEnrollment:
    enrollment = (
        db.query(UserEnrollment).filter(UserEnrollment.id == enrollment_id).first()
    )
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found.")

    try:
        db.delete(enrollment)
        db.commit()
        return enrollment
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to delete enrollment."
        ) from e


def validate_enrollment_details(
    db: Session, promotion_id: str, level_id: str, time_slot_id: Optional[str]
):
    promotion = get_promotion_by_id(db, promotion_id)
    if not promotion:
        raise HTTPException(
            status_code=404, detail=f"Promotion with id {promotion_id} not found."
        )

    level = get_level_by_id(db, level_id)
    if not level:
        raise HTTPException(
            status_code=404, detail=f"Level with id {level_id} not found."
        )

    if level.program_id != promotion.program_id:
        raise HTTPException(
            status_code=400,
            detail="Level and promotion do not belong to the same program.",
        )

    time_slot = None
    if time_slot_id:
        time_slot = get_time_slot_by_id(db, time_slot_id)
        if not time_slot:
            raise HTTPException(
                status_code=404, detail=f"Time slot with id {time_slot_id} not found."
            )
        if time_slot.program_id != promotion.program_id:
            raise HTTPException(
                status_code=400,
                detail="Time slot does not belong to the same program as the promotion.",
            )

    return promotion, level, time_slot
