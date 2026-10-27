from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.pets.pets_repository import pets_repository
from app.pets.pets_schemas import Pet
from app.shared.datetimes import utc_now
from app.shared.exceptions import conflict
from app.shared.types import FieldErrors
from app.students.students_repository import StudentsRepository, students_repository
from app.students.students_schemas import (
    CreateStudentDto,
    Student,
    StudentList,
    UpdateStudentDto,
)


class StudentsService:
    def __init__(self, repository: StudentsRepository) -> None:
        self.repository = repository

    def find_all(self, db: Session) -> StudentList:
        students = self.repository.find_all(db)

        return StudentList(total=len(students), items=students)

    def find_by_id(self, db: Session, student_id: str) -> Student:
        student = self.repository.find_by_id(db, student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado",
            )

        return student

    def create(self, db: Session, data: CreateStudentDto) -> Student:
        self.assert_no_conflicts(db, data)

        now = utc_now()
        student = Student(
            id=str(uuid4()),
            name=data.name,
            username=data.username,
            email=data.email,
            age=data.age,
            createdAt=now,
            updatedAt=now,
        )

        try:
            saved = self.repository.save(db, student)

            for pet_data in data.pets:
                existing = pets_repository.find_by_student_and_name(
                    db, student.id, pet_data.name
                )
                if existing:
                    raise conflict({
                        "pets": {
                            "message": f"Ya existe una mascota llamada {pet_data.name}"
                        }
                    })

                pet = Pet(
                    id=str(uuid4()),
                    studentId=student.id,
                    name=pet_data.name,
                    species=pet_data.species,
                    age=pet_data.age,
                    createdAt=now,
                    updatedAt=now,
                )
                pets_repository.save(db, pet)

            db.commit()
            return saved
        except Exception:
            db.rollback()
            raise

    def update(self, db: Session, student_id: str, data: UpdateStudentDto) -> Student:
        existing = self.find_by_id(db, student_id)
        self.assert_no_conflicts(db, data, except_id=student_id)

        updated = existing.model_copy(
            update={
                **data.model_dump(exclude_none=True),
                "updatedAt": utc_now(),
            }
        )

        try:
            saved = self.repository.save(db, updated)
            db.commit()
            return saved
        except Exception:
            db.rollback()
            raise

    def delete(self, db: Session, student_id: str) -> Student:
        existing = self.find_by_id(db, student_id)

        try:
            self.repository.delete(db, student_id)
            db.commit()
            return existing
        except Exception:
            db.rollback()
            raise

    def assert_no_conflicts(
        self,
        db: Session,
        data: CreateStudentDto | UpdateStudentDto,
        except_id: str | None = None,
    ) -> None:
        errors: FieldErrors = {}

        if data.email:
            existing = self.repository.find_by_email(db, data.email)
            if existing and existing.id != except_id:
                errors["email"] = {"message": "El correo electrónico ya está en uso"}

        if data.username:
            existing = self.repository.find_by_username(db, data.username)
            if existing and existing.id != except_id:
                errors["username"] = {"message": "El nombre de usuario ya está en uso"}

        if errors:
            raise conflict(errors)


students_service = StudentsService(students_repository)