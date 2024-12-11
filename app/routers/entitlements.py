from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi_pagination.limit_offset import LimitOffsetPage

from app import repositories
from app.db import DBSession
from app.models import EntitlementCreate, EntitlementRead, EntitlementUpdate


async def get_entitlement_repo(session: DBSession) -> repositories.EntitlementRepository:
    return repositories.EntitlementRepository(session=session)


EntitlementRepo = Annotated[repositories.EntitlementRepository, Depends(get_entitlement_repo)]


router = APIRouter()


@router.get("/", response_model=LimitOffsetPage[EntitlementRead])
async def get_entitlements(entitlements: EntitlementRepo):
    return await entitlements.fetch_page()


@router.get("/{id}", response_model=EntitlementRead)
async def get_entitlement_by_id(id: str, entitlements: EntitlementRepo):
    return await entitlements.get(id=id)


@router.post("/", response_model=EntitlementRead, status_code=status.HTTP_201_CREATED)
async def create_entitlement(data: EntitlementCreate, entitlements: EntitlementRepo):
    return await entitlements.create(data=data)


@router.patch("/{id}", response_model=EntitlementRead)
async def update_entitlement(id: str, data: EntitlementUpdate, entitlements: EntitlementRepo):
    return await entitlements.update(id=id, data=data)
