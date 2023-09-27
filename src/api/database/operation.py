from sqlalchemy import delete

from src.api.utils.mapping import TABLE_TYPE_MAPPING
from src.logger import logger
from src.settings import CHUNK_SIZE


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
                try:
                    table_instance = table_class(**row.to_dict())
                    session.add(table_instance)
                    session.commit()
                    session.refresh(table_instance)
                except Exception as e:
                    session.rollback()
                    logger.error(e)
