from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.api.auth.model import Token
from src.api.auth.utils import create_access_token, get_password_hash, verify_password
from src.logger import logger
from src.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

fake_users_db = {
    "user1": {
        "username": "user1",
        "password": get_password_hash("password1"),
    },
}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    
    if user and verify_password(form_data.password, user["password"]):
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            subject=form_data.username,
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}

    logger.error(f"User {form_data.username} not found")

    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
