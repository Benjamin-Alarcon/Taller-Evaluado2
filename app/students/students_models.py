from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint

from app.shared.database import Base


class StudentModel(Base):
    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint("email", name="uq_students_email"),
        UniqueConstraint("username", name="uq_students_username"),
    )

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(30), nullable=False)
    email = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    createdAt = Column("created_at", DateTime(timezone=True), nullable=False)
    updatedAt = Column("updated_at", DateTime(timezone=True), nullable=False)