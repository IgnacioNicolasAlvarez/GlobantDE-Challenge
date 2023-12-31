from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from src.api.backup.service import AvroBuckupClient
from src.api.database.db import get_session
from src.api.router.model import enum
from src.logger import logger
from src.settings import BACKUP_BASE_PATH

router = APIRouter(
    prefix="/backup",
    tags=["backup"],
    responses={404: {"description": "Not found"}},
)


@router.post("/write/")
async def create_backup(
    table_type: enum.TableType = enum.TableType.Department, session=Depends(get_session)
):
    if table_type not in enum.TableType:
        raise HTTPException(status_code=400, detail=f"Invalid table_type: {table_type}")

    try:
        result = AvroBuckupClient.create_backup(
            table_type=table_type,
            session=session,
            avro_file_path=f"{BACKUP_BASE_PATH}/",
            avro_schema=f"{BACKUP_BASE_PATH}/schema/{table_type.value}.avsc",
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    return {"content_length": result["content_length"]}


@router.post("/restore/")
async def restore_backup(
    table_type: enum.TableType = enum.TableType.Department,
    session=Depends(get_session),
    date: date = date.today(),
):
    if table_type not in enum.TableType:
        raise HTTPException(status_code=400, detail=f"Invalid table_type: {table_type}")

    try:
        result = AvroBuckupClient.restore_backup(
            avro_file_path=f"{BACKUP_BASE_PATH}/",
            table_type=table_type,
            session=session,
            date=date,
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    return {"content_length": result["content_length"]}
