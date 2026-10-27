from sqlalchemy.orm import Session

from app.pets.pets_models import PetModel
from app.pets.pets_schemas import Pet


def _to_schema(model: PetModel) -> Pet:
    return Pet(
        id=model.id,
        studentId=model.student_id,
        name=model.name,
        species=model.species,
        age=model.age,
        createdAt=model.createdAt,
        updatedAt=model.updatedAt,
    )


class PetsRepository:
    def find_all_by_student(self, db: Session, student_id: str) -> list[Pet]:
        models = (
            db.query(PetModel)
            .filter(PetModel.student_id == student_id)
            .all()
        )
        return [_to_schema(model) for model in models]

    def find_by_id(self, db: Session, pet_id: str) -> Pet | None:
        model = db.get(PetModel, pet_id)
        return _to_schema(model) if model else None

    def find_by_student_and_name(
        self, db: Session, student_id: str, name: str
    ) -> Pet | None:
        model = (
            db.query(PetModel)
            .filter(
                PetModel.student_id == student_id,
                PetModel.name == name,
            )
            .first()
        )
        return _to_schema(model) if model else None

    def save(self, db: Session, pet: Pet) -> Pet:
        model = PetModel(
            id=pet.id,
            student_id=pet.studentId,
            name=pet.name,
            species=pet.species,
            age=pet.age,
            createdAt=pet.createdAt,
            updatedAt=pet.updatedAt,
        )
        saved = db.merge(model)
        db.flush()
        return _to_schema(saved)

    def delete(self, db: Session, pet_id: str) -> None:
        model = db.get(PetModel, pet_id)
        if model is not None:
            db.delete(model)
            db.flush()

    def delete_by_student(self, db: Session, student_id: str) -> None:
        models = (
            db.query(PetModel)
            .filter(PetModel.student_id == student_id)
            .all()
        )
        for model in models:
            db.delete(model)
        db.flush()


pets_repository = PetsRepository()