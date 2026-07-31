from sqlalchemy import insert, select, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()  # scalars - вытащить объект из кортежа

    async def get_one_or_none(self, **filters_by):
        query = select(self.model).filter_by(**filters_by)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)

        return result.scalar_one()

    async def edit(self, data: BaseModel, **filters_by) -> None:
        edit_stmt = update(self.model).values(**data.model_dump()).filter_by(**filters_by)
        await self.session.execute(edit_stmt)

    async def delete(self, **filters_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filters_by)
        await self.session.execute(delete_stmt)
