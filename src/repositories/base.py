from sqlalchemy import insert, select


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

    async def add(self, **model_data):
        add_stmt = insert(self.model).values(**model_data).returning(self.model)
        result = await self.session.execute(add_stmt)
        return result.scalar_one()
