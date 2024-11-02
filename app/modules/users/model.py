from sqlalchemy import Column, String, DateTime, Text, text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from sqlalchemy.orm import relationship
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True, unique=True)
    phone = Column(String(20), nullable=True, unique=True)
    photo = Column(Text, nullable=True)
    account_confirmed_at = Column(DateTime, nullable=True)
    sub = Column(String(255), nullable=True)
    profile_completed_at = Column(DateTime, nullable=True)
    password = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
    promotions = relationship(
        "Promotion",
        secondary="user_enrollments",
        back_populates="users",
        overlaps="enrollments",
    )
    enrollments = relationship(
        "UserEnrollment", back_populates="user", overlaps="promotions"
    )
