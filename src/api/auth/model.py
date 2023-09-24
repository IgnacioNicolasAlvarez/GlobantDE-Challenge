from pydantic import BaseModel


class User(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str
    password: str
