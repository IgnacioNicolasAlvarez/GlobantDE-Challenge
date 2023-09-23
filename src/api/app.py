from fastapi import FastAPI, Request, Response

from src.logger import logger

from .router.uploadfile import router as uploadfile_router

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(
        f"Request received: {request.method} {request.url} {request.query_params}"
    )
    response = await call_next(request)
    logger.info(f"Response sent: {response.status_code}")
    return response


app.include_router(uploadfile_router)
