from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone


class UserEnrollment(Base):
    __tablename__ = "user_enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    promotion_id = Column(
        UUID(as_uuid=True),
        ForeignKey("promotions.id", ondelete="CASCADE"),
        nullable=False,
    )
    level_id = Column(
        UUID(as_uuid=True), ForeignKey("levels.id", ondelete="CASCADE"), nullable=False
    )
    time_slot_id = Column(
        UUID(as_uuid=True),
        ForeignKey("time_slots.id", ondelete="CASCADE"),
        nullable=True,
    )

    end_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="active")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User", back_populates="enrollments", overlaps="promotions")
    promotion = relationship(
        "Promotion", back_populates="enrollments", overlaps="promotions"
    )
    time_slot = relationship(
        "TimeSlot", back_populates="enrollments", overlaps="time_slots"
    )
