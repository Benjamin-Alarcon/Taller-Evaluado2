from sqlalchemy.orm import Session
from app.students import students_repository
from app.students.students_schemas import StudentCreate

def get_all_students(db: Session):
    return students_repository.get_all_students(db)

def get_student_by_id(db: Session, student_id: int):
    return students_repository.get_student_by_id(db, student_id)

def create_student(db: Session, student: StudentCreate):
    db_student = students_repository.create_student(db, student)
    db.commit()
    db.refresh(db_student)
    return db_student