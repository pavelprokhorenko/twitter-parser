from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

postgres = settings.postgres

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    postgres.user,
    postgres.password,
    postgres.host,
    postgres.port,
    postgres.database,
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=settings.service.debug,
    pool_pre_ping=True,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
