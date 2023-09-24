import os

import dotenv

dotenv.load_dotenv()


CHUNK_SIZE = os.getenv("CHUNK_SIZE")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
