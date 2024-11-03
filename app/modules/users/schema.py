from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from app.modules.enrollments.schema import EnrollmentResponse


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    surname: Optional[str] = None
    email: Optional[str] = None
    sub: Optional[str] = None
    provider: Optional[str] = None


class UserResponse(UserCreate):
    id: UUID
    status: Optional[str] = "active"

    class Config:
        from_attributes = True


class UsersResponse(BaseModel):
    total: int
    data: List[UserResponse]

    class Config:
        from_attributes = True
