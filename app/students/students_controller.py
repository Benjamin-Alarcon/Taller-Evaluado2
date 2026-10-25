from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.shared.database import get_db
from app.students import students_service
from app.students.students_schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return students_service.get_all_students(db)

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return students_service.create_student(db, student)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    db_student = students_service.get_student_by_id(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_student