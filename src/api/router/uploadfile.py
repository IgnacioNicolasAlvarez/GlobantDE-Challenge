from io import StringIO
from typing import List

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from src.api.database.db import get_session
from src.api.database.operation import delete_all, insert
from src.api.router.model import enum
from src.logger import logger

router = APIRouter(
    prefix="/uploadfile",
    tags=["uploadfile"],
    responses={404: {"description": "Not found"}},
)

null_values = ["nan", "null", "none"]


@router.post("/upload/")
async def upload(
    file: UploadFile,
    column_names: List[str],
    sep: str = ",",
    is_full_load: bool = True,
    table_type: enum.TableType = enum.TableType.Department,
    session=Depends(get_session),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=406, detail="The only allowed file extension is .csv"
        )

    if table_type not in enum.TableType:
        raise HTTPException(status_code=400, detail=f"Invalid table_type: {table_type}")

    try:
        contents = await file.read()
        data = contents.decode("utf-8")

        df = pd.read_csv(
            StringIO(data),
            names=column_names[0].split(","),
            sep=sep,
            header=None,
        )

        df.replace(null_values, None, inplace=True)

        if is_full_load:
            delete_all(table_type=table_type, session=session)
        insert(df=df, table_type=table_type, session=session)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    return {"filename": file.filename, "content_length": len(contents)}
