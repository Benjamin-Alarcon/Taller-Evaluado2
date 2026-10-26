from datetime import UTC

from sqlalchemy.orm import Session

from app.students.students_models import StudentModel
from app.students.students_schemas import Student


def _to_schema(model: StudentModel) -> Student:
    return Student(
        id=model.id,
        name=model.name,
        username=model.username,
        email=model.email,
        age=model.age,
        createdAt=model.createdAt.astimezone(UTC),
        updatedAt=model.updatedAt.astimezone(UTC),
    )


class StudentsRepository:
    def find_all(self, db: Session) -> list[Student]:
        models = db.query(StudentModel).order_by(StudentModel.createdAt.desc()).all()

        students: list[Student] = []
        for model in models:
            students.append(_to_schema(model))

        return students

    def find_by_id(self, db: Session, student_id: str) -> Student | None:
        model = db.get(StudentModel, student_id)

        if model is None:
            return None

        return _to_schema(model)

    def find_by_email(self, db: Session, email: str) -> Student | None:
        model = db.query(StudentModel).filter(StudentModel.email == email).first()

        if model is None:
            return None

        return _to_schema(model)

    def find_by_username(self, db: Session, username: str) -> Student | None:
        model = db.query(StudentModel).filter(StudentModel.username == username).first()

        if model is None:
            return None

        return _to_schema(model)

    def save(self, db: Session, student: Student) -> Student:
        model = StudentModel(
            id=student.id,
            name=student.name,
            username=student.username,
            email=student.email,
            age=student.age,
            createdAt=student.createdAt,
            updatedAt=student.updatedAt,
        )
        merged = db.merge(model)
        db.flush()

        return _to_schema(merged)

    def delete(self, db: Session, student_id: str) -> None:
        model = db.get(StudentModel, student_id)

        if model is not None:
            db.delete(model)
            db.flush()


students_repository = StudentsRepository()