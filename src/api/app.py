from fastapi import Depends, FastAPI, Request
from fastapi.security import OAuth2PasswordBearer

from src.logger import logger

from .router.auth import router as auth_router
from .router.uploadfile import router as uploadfile_router

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(
        f"Request received: {request.method} {request.url} {request.query_params}"
    )
    response = await call_next(request)
    logger.info(f"Response sent: {response.status_code}")
    return response


app.include_router(auth_router)
app.include_router(uploadfile_router, dependencies=[Depends(oauth2_scheme)])
