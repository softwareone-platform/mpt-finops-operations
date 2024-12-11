from typing import ClassVar
from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination.limit_offset import LimitOffsetPage, LimitOffsetParams
from sqlalchemy import delete, select
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Entitlement, EntitlementCreate, EntitlementUpdate, UUIDModel


class BaseRepository[ModelT: UUIDModel, ModelCreateT: SQLModel, ModelUpdateT: SQLModel]:
    # TODO: Extract these from the type hints if possible
    #       self.__orig_class__.__args__[0]

    model_cls: ClassVar[type[ModelT]]
    model_create_cls: ClassVar[type[ModelCreateT]]
    model_update_cls: ClassVar[type[ModelUpdateT]]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ModelCreateT) -> ModelT:
        obj = self.model_cls(**data.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

        return obj

    async def get(self, id: str | UUID) -> ModelT:
        statement = select(self.model_cls).where(self.model_cls.id == id)
        results = await self.session.execute(statement=statement)
        obj: ModelT | None = results.scalar_one_or_none()

        if obj is None:
            raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="The object hasn't been found!")

        return obj

    async def fetch_all(self) -> list[ModelT]:
        results = await self.session.execute(statement=select(self.model_cls))
        return results.scalars().all()

    async def fetch_page(self, pagination_params: LimitOffsetParams | None = None) -> LimitOffsetPage[ModelT]:
        return await paginate(self.session, self.model_cls, pagination_params)

    async def update(self, id: str | UUID, data: ModelUpdateT) -> ModelT:
        obj = await self.get(id=id)

        for k, v in data.dict(exclude_unset=True).items():
            setattr(obj, k, v)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

        return obj

    async def delete(self, id: str | UUID) -> bool:
        statement = delete(self.model_cls).where(self.model_cls.id == id)

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True


class EntitlementRepository(BaseRepository[Entitlement, EntitlementCreate, EntitlementUpdate]):
    model_cls = Entitlement
    model_create_cls = EntitlementCreate
    model_update_cls = EntitlementUpdate
