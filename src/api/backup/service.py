import os
from datetime import datetime
from uuid import uuid4

import fastavro
from fastavro.schema import load_schema
from sqlmodel import select

from src.api.database.model import Deparment, HiredEmployee, Job
from src.api.database.operation import delete_all
from src.api.router.model import enum
from src.logger import logger

TABLE_TYPE_MAPPING = {
    enum.TableType.Department: Deparment,
    enum.TableType.Job: Job,
    enum.TableType.HiredEmployee: HiredEmployee,
}


class AvroBuckupClient:
    @staticmethod
    def create_backup(table_type, avro_file_path, avro_schema, session):
        try:
            q_rows = 0
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
            
            if os.path.exists(folder_path):
                for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)
                    os.remove(file_path)
                    
            file_path = folder_path + "/" + str(uuid4()) + ".avro"
            with open(file_path, "wb") as avro_file:
                all_records = [r.dict() for r in results.all()]
                fastavro.writer(avro_file, schema, all_records)

            q_rows = len(all_records)
            
            logger.info(
                f"Backup of table '{table_type}' created successfully at '{folder_path}'"
            )
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            
        return {"content_length": q_rows}

    @staticmethod
    def restore_backup(table_type, avro_file_path, date, session):
        try:
            q_rows = 0
            table_class = TABLE_TYPE_MAPPING.get(table_type)

            folder_path = os.path.join(
                avro_file_path,
                table_type,
                str(date.year),
                str(date.month).zfill(2),
                str(date.day).zfill(2),
            )
            file_name = os.listdir(folder_path)[0]
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "rb") as avro_file:
                records = list(fastavro.reader(avro_file))

            delete_all(table_type, session)

            q_rows = len(records)
            
            for record in records:
                table_instance = table_class(**record)
                session.add(table_instance)
                session.commit()
                session.refresh(table_instance)

            logger.info(
                f"Backup of table '{table_type}' restored successfully from '{file_path}'"
            )
            
        except Exception as e:
            logger.error(f"Error restoring backup: {str(e)}")
        
        return {"content_length": q_rows}
