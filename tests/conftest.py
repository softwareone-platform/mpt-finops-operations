import uuid
from collections.abc import AsyncGenerator
from dataclasses import dataclass

import fastapi_pagination
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pytest_asyncio import is_async_test
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import db_engine
from app.main import app
from app.models import Entitlement, EntitlementCreate
from app.repositories import EntitlementRepository


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="session", autouse=True)
def fastapi_app() -> FastAPI:
    fastapi_pagination.add_pagination(app)
    return app


@pytest.fixture(autouse=True)
async def db_session() -> AsyncGenerator[AsyncSession]:
    session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

    async with session() as s:
        async with db_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        yield s

    async with db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await db_engine.dispose()


@pytest.fixture
async def api_client(fastapi_app: FastAPI) -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://v1/") as client:
        yield client


@dataclass
class RepositoryContainer:
    entitlements: EntitlementRepository


@pytest.fixture
def repos(db_session: AsyncSession) -> RepositoryContainer:
    return RepositoryContainer(
        entitlements=EntitlementRepository(db_session),
    )


@pytest.fixture
async def entitlement_aws(repos: RepositoryContainer) -> Entitlement:
    return await repos.entitlements.create(
        EntitlementCreate(
            sponsor_name="AWS",
            sponsor_external_id=f"EXTERNAL_ID_{uuid.uuid4().hex[:8]}",
            sponsor_container_id=f"CONTAINER_ID_{uuid.uuid4().hex[:8]}",
        )
    )


@pytest.fixture
async def entitlement_gcp(repos: RepositoryContainer) -> Entitlement:
    return await repos.entitlements.create(
        EntitlementCreate(
            sponsor_name="GCP",
            sponsor_external_id=f"EXTERNAL_ID_{uuid.uuid4().hex[:8]}",
            sponsor_container_id=f"CONTAINER_ID_{uuid.uuid4().hex[:8]}",
        )
    )
