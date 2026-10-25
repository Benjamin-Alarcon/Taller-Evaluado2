from pydantic import BaseModel, ConfigDict, EmailStr

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)