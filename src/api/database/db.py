import logging

from sqlmodel import Session, SQLModel, create_engine

from src.settings import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        logger.error(e)


def get_session() -> Session:
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(e)
