import os

import dotenv

dotenv.load_dotenv()


CHUNK_SIZE = os.getenv("CHUNK_SIZE")
