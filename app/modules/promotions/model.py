from sqlalchemy import Column, Date, Numeric, ForeignKey, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from sqlalchemy.orm import relationship
import uuid


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(
        UUID(as_uuid=True),
        ForeignKey("programs.id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String(255), nullable=False)
    promotion_start_date = Column(Date, nullable=False)
    promotion_end_date = Column(Date, nullable=False)
    general_fee = Column(Numeric(10, 2), nullable=False)
    installments = Column(Numeric(10, 2), nullable=True, default=1)
    discount = Column(Numeric(10, 2), nullable=True, default=0)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    program = relationship("Program", back_populates="promotions")
    users = relationship(
        "User",
        secondary="user_enrollments",
        back_populates="promotions",
        overlaps="enrollments,user,promotion",
    )
    enrollments = relationship(
        "UserEnrollment", back_populates="promotion", overlaps="users"
    )
