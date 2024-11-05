from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from ..time_slots.schema import TimeSlotResponse


class EnrollmentBase(BaseModel):
    user_id: UUID
    promotion_id: UUID
    level_id: UUID
    time_slot_id: Optional[UUID] = None
    end_date: Optional[datetime] = None
    status: str = "active"


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentResponse(EnrollmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    promotion: Optional["PromotionResponse"]
    time_slot: Optional[TimeSlotResponse] = None

    class Config:
        from_attributes = True


class EnrollmentUpdate(BaseModel):
    end_date: Optional[datetime] = None
    status: Optional[str] = None


class EnrollmentUpdate(BaseModel):
    promotion_id: Optional[UUID]
    level_id: Optional[UUID]
    time_slot_id: Optional[UUID] = None
    end_date: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True


from ..promotions.schema import PromotionResponse
