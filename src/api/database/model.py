from datetime import datetime

from pydantic import validator
from sqlmodel import Field, SQLModel

from src.logger import logger
from src.settings import DATE_FORMAT


class HiredEmployeeBase(SQLModel):
    id: int
    name: str
    datetime: str
    deparment_id: int
    job_id: int

    @validator("datetime")
    def validate_datetime(cls, value):
        try:
            datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            logger.info(
                f"The datetime field must be a valid date in the specified format"
            )
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
