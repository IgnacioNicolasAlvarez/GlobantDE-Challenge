from src.api.database.model import Deparment, HiredEmployee, Job
from src.api.router.model import enum

TABLE_TYPE_MAPPING = {
    enum.TableType.Department: Deparment,
    enum.TableType.Job: Job,
    enum.TableType.HiredEmployee: HiredEmployee,
}
