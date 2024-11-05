from fastapi import APIRouter, Path, Depends, HTTPException
from app.modules.enrollments.service import (
    create_user_enrollment,
    validate_enrollment_details,
    find_existing_user_enrollment,
    update_user_enrollment,
    delete_user_enrollment,
)
from sqlalchemy.orm import Session
from .schema import EnrollmentResponse, EnrollmentCreate, EnrollmentUpdate
from app.db.database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.post("/", response_model=EnrollmentResponse)
def create(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
):
    promotion, level, time_slot = validate_enrollment_details(
        db=db,
        level_id=enrollment.level_id,
        promotion_id=enrollment.promotion_id,
        time_slot_id=enrollment.time_slot_id,
    )

    existing = find_existing_user_enrollment(
        db, promotion_id=promotion.id, user_id=enrollment.user_id, level_id=level.id
    )

    if existing:
        raise HTTPException(
            status_code=400, detail="User already enrolled in this promotion"
        )

    try:
        enrollment_data = {
            "user_id": enrollment.user_id,
            "promotion_id": promotion.id,
            "level_id": level.id,
            "time_slot_id": time_slot.id if time_slot else None,
        }
        return create_user_enrollment(db, enrollment_data, can_commit=True)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Unable to create enrollment. Please check if all referenced IDs (user, promotion, level, time_slot) are valid.",
        ) from e


@router.put("/{enrollment_id}", response_model=EnrollmentResponse)
def update(
    enrollment_id: str = Path(..., description="The ID of the enrollment to update."),
    enrollment_data: EnrollmentUpdate = None,
    db: Session = Depends(get_db),
):
    updated_enrollment = update_user_enrollment(
        db, enrollment_id=enrollment_id, enrollment_data=enrollment_data
    )
    return updated_enrollment


@router.delete("/{enrollment_id}", status_code=204)
def delete(
    enrollment_id: str = Path(..., description="The ID of the enrollment to delete."),
    db: Session = Depends(get_db),
):
    delete_user_enrollment(db, enrollment_id=enrollment_id)
    return None
