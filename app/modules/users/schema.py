from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.modules.enrollments.schema import EnrollmentResponse


class User(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    surname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    photo: Optional[str] = None
    address: Optional[str] = None
    sub: Optional[str] = None
    provider: Optional[str] = None
    account_confirmed_at: Optional[datetime] = None
    profile_completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    enrollments: List[EnrollmentResponse]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    surname: Optional[str] = None
    email: Optional[str] = None
    sub: Optional[str] = None
    provider: Optional[str] = None


class UserResponse(User):
    id: UUID
    status: Optional[str] = "active"

    class Config:
        from_attributes = True


class UsersResponse(BaseModel):
    total: int
    data: List[UserResponse]

    class Config:
        from_attributes = True
