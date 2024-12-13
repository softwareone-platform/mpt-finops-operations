import sys
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app import settings

running_tests = "pytest" in sys.modules

db_conn_url = settings.test_postgres_async_url if running_tests else settings.postgres_async_url


db_engine = create_async_engine(
    str(db_conn_url),
    echo=False if running_tests else settings.debug,
    future=True,
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async_session = sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db_session)]
