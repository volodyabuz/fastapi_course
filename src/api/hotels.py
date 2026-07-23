from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение данных об отеле",
    description="Можно указать <b>id</b> или <b>title</b> для фильтрации"
)
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля")
):

    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            # query = query.filter_by(title=title) # добавление ОПЦИОНАЛЬНОГО параметра
            query = query.where(HotelsOrm.title.like(f"%{title}%"))
        if location:
            query = query.where(HotelsOrm.location.like(f"%{location}%"))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all() # scalars - вытащить объект из кортежа
        # first_hotel = result.first() # первое значение
        # result.one_or_none() # вернуть одно значение или ничего. А если значений больше - ошибка
    return hotels

@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Удалится отель с указанным <i>hotel_id</i>"
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router.post(
    "",
    summary="Добавление отеля",
    description="Добавляем данные об отеле: <b>title</b> и <b>name</b> обязательны!"
)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {"title": "Отель Rich 5 звезд у моря", "location": "Сочи, ул. Моря, 1"}},
    "2": {"summary": "Дубай", "value": {"title": "Отель Deluxe у фонтана", "location": "Дубай, ул. Шейха, 2"}}
}
)):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # Ниже строку убрать в ПРОДЕ
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True})) # param: compile_kwargs=показать данные в консоль
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})) # param: engine - явное указание СУБД
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}

@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Обновляем данные об отеле: <b>title</b> и <b>name</b> обязательны!"
)
def full_update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotels[hotel_id - 1]["title"] = hotel_data.title
    hotels[hotel_id - 1]["name"] = hotel_data.name
    return {"status": "OK", "id": hotel_id}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Обновляем данные об отеле: можно title, можно name"
)
def partial_update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    if hotel_data.title:
        hotels[hotel_id - 1]["title"] = hotel_data.title
    if hotel_data.name:
        hotels[hotel_id - 1]["name"] = hotel_data.name
    return {"status": "OK", "id": hotel_id}
