from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone


class StudentEnrollment(Base):
    __tablename__ = "student_enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    promotion_id = Column(
        UUID(as_uuid=True), ForeignKey("promotions.id"), nullable=False
    )
    level_id = Column(UUID(as_uuid=True), ForeignKey("levels.id"), nullable=False)
    time_slot_id = Column(
        UUID(as_uuid=True), ForeignKey("time_slots.id"), nullable=True
    )
    enrollment_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="active")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    student = relationship(
        "Student", back_populates="enrollments", overlaps="students,promotions"
    )
    promotion = relationship(
        "Promotion", back_populates="enrollments", overlaps="students,promotions"
    )
    time_slot = relationship(
        "TimeSlot", back_populates="enrollments", overlaps="time_slots"
    )
