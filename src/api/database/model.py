from sqlmodel import Field, SQLModel
from pydantic import validator
from datetime import datetime


class HiredEmployeeBase(SQLModel):
    id: int
    name: str
    datetime: str
    deparment_id: int
    job_id: int
    
    @validator("datetime")
    def validate_datetime(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ") 
        except ValueError:
            raise ValueError("El campo 'datetime' debe ser una fecha válida en el formato especificado")
        return value


class HiredEmployee(HiredEmployeeBase, table=True):
    pk: int = Field(default=None, nullable=False, primary_key=True)


class HiredEmployeeCreate(HiredEmployeeBase):
    pass


class DeparmentBase(SQLModel):
    id: int
    deparment: str


class Deparment(DeparmentBase, table=True):
    pk: int = Field(default=None, nullable=False, primary_key=True)


class DeparmentCreate(DeparmentBase):
    pass


class JobBase(SQLModel):
    id: int
    job: str


class Job(JobBase, table=True):
    pk: int = Field(default=None, nullable=False, primary_key=True)


class JobCreate(JobBase):
    pass
