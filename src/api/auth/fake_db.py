from src.api.auth.utils import get_password_hash

FAKE_DB = {
    "user1": {
        "username": "user1",
        "password": get_password_hash("password1"),
    },
}
