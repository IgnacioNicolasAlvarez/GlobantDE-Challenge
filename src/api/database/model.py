from sqlmodel import Field, SQLModel


class HiredEmployeeBase(SQLModel):
    id: int
    name: str
    datetime: str
    deparment_id: int
    job_id: int


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
