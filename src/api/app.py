import os

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from src.api.database.db import init_db
from src.logger import logger

from .router.auth import router as auth_router
from .router.backup import router as backup_router
from .router.uploadfile import router as uploadfile_router


def initialize_app():
    state_dir = "app_state"
    state_file = os.path.join(state_dir, "initialized.txt")

    if not os.path.exists(state_file):
        init_db()
        os.makedirs(state_dir, exist_ok=True)
        with open(state_file, "w") as f:
            f.write("initialized")


initialize_app()

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


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(uploadfile_router, dependencies=[Depends(oauth2_scheme)])
app.include_router(backup_router, dependencies=[Depends(oauth2_scheme)])
