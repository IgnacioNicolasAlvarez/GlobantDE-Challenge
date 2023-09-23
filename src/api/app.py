from fastapi import FastAPI

from .router.uploadfile import router as uploadfile_router

app = FastAPI()

app.include_router(uploadfile_router)
