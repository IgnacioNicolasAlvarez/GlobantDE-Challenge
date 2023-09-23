from io import StringIO
from typing import List

import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile

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
    delimiter: str = None,
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
            names=column_names,
            sep=sep,
            delimiter=delimiter,
        )

        chunks = [df[i : i + int(CHUNK_SIZE)] for i in range(0, len(df), int(CHUNK_SIZE))]

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    return {"filename": file.filename, "content_length": len(contents)}
