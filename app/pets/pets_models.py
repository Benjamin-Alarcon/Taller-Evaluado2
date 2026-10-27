from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.shared.database import Base


class PetModel(Base):
    __tablename__ = "pets"

    id = Column(String(36), primary_key=True)
    student_id = Column(
        String(36),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String(50), nullable=False)
    species = Column(String(50), nullable=False)
    age = Column(Integer, nullable=True)
    createdAt = Column("created_at", DateTime(timezone=True), nullable=False)
    updatedAt = Column("updated_at", DateTime(timezone=True), nullable=False)

    student = relationship("StudentModel", back_populates="pets")