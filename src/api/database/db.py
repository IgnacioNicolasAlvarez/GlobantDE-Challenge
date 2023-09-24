import logging

from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine, AsyncSession

from src.settings import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))


async def init_db():
    try:
        async with engine.begin() as conn:
            # await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        logger.error(e)


async def get_session() -> AsyncSession:
    try:
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session
    except Exception as e:
        logger.error(e)
