from sqlalchemy import delete

from src.api.database.model import Deparment, HiredEmployee, Job
from src.api.router.model import enum
from src.settings import CHUNK_SIZE

TABLE_TYPE_MAPPING = {
    enum.TableType.Department: Deparment,
    enum.TableType.Job: Job,
    enum.TableType.HiredEmployee: HiredEmployee,
}


def delete_all(table_type, session) -> int:
    table_class = TABLE_TYPE_MAPPING.get(table_type)
    statement = delete(table_class)
    results = session.exec(statement)
    session.commit()
    return results.rowcount


def insert(df, table_type, session):
    table_class = TABLE_TYPE_MAPPING.get(table_type)

    chunks = [df[i : i + int(CHUNK_SIZE)] for i in range(0, len(df), int(CHUNK_SIZE))]

    if table_class:
        for chunk in chunks:
            for _, row in chunk.iterrows():
                table_instance = table_class(**row.to_dict())
                session.add(table_instance)
                session.commit()
                session.refresh(table_instance)
