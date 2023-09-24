from io import StringIO
from typing import List

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from src.api.database.db import AsyncSession, get_session
from src.api.database.model import Deparment
from src.api.router.model import enum
from src.logger import logger
from src.settings import CHUNK_SIZE

router = APIRouter(
    prefix="/uploadfile",
    tags=["uploadfile"],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload/")
async def upload(
    file: UploadFile,
    column_names: List[str] = [],
    sep: str = ",",
    has_header: bool = False,
    is_full_load: bool = True,
    table_type: enum.TableType = enum.TableType.Department,
    session: AsyncSession = Depends(get_session),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=406, detail="The only allowed file extension is .csv"
        )

    try:
        contents = await file.read()
        data = contents.decode("utf-8")

        df = pd.read_csv(
            StringIO(data),
            names=column_names[0].split(","),
            sep=sep,
            header=int(has_header),
        )

        chunks = [
            df[i : i + int(CHUNK_SIZE)] for i in range(0, len(df), int(CHUNK_SIZE))
        ]

        for chunk in chunks:
            for _, row in chunk.iterrows():
                department = Deparment(**row.to_dict())
                session.add(department)
                await session.commit()
                await session.refresh(department)

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    return {"filename": file.filename, "content_length": len(contents)}
