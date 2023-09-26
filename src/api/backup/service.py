import os
from datetime import datetime
from uuid import uuid4

import fastavro
from fastavro.schema import load_schema
from sqlmodel import select

from src.api.database.model import Deparment, HiredEmployee, Job
from src.api.router.model import enum
from src.logger import logger

TABLE_TYPE_MAPPING = {
    enum.TableType.Department: Deparment,
    enum.TableType.Job: Job,
    enum.TableType.HiredEmployee: HiredEmployee,
}


class AvroBuckupClient:
    def create_backup(self, table_type, avro_file_path, avro_schema, session):
        try:
            table_class = TABLE_TYPE_MAPPING.get(table_type)
            statement = select(table_class)
            results = session.exec(statement)

            schema = load_schema(avro_schema)

            current_date = datetime.now()
            folder_path = os.path.join(
                avro_file_path,
                table_type,
                str(current_date.year),
                str(current_date.month).zfill(2),
                str(current_date.day).zfill(2),
            )
            os.makedirs(folder_path, exist_ok=True)
            file_path = folder_path + "/" + str(uuid4()) + ".avro"
            with open(file_path, "wb") as avro_file:
                all_records = [r.dict() for r in results.all()]
                fastavro.writer(avro_file, schema, all_records)

            logger.info(
                f"Backup of table '{table_type}' created successfully at '{folder_path}'"
            )
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
