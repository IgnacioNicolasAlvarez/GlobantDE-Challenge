from fastapi import APIRouter, Depends, HTTPException

from src.api.database.db import get_session
from src.api.utils.template import QueryTemplate, execute_template_query
from src.logger import logger
from src.settings import TEMPLATE_PATH

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    responses={404: {"description": "Not found"}},
)


@router.post("/execute_query/")
async def execute_query(
    select_year: int, template: QueryTemplate, session=Depends(get_session)
):
    try:
        results = execute_template_query(
            session=session,
            template_dir=TEMPLATE_PATH,
            template_name=template.value,
            context={"select_year": select_year},
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    return {"results": results}
