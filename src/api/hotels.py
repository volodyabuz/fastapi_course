from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get(
    "",
    summary="Получение данных об отеле",
    description="Можно указать <b>id</b> или <b>title</b> для фильтрации"
)
def get_hotels(
        pagination: PaginationDep,
        id: int | None= Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels[(pagination.page-1) * pagination.per_page
    :pagination.per_page + (pagination.page-1) * pagination.per_page]:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_

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
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {"title": "Отель Сочи 5 звезд у моря", "name": "Отель у моря"}},
    "2": {"summary": "Дубай", "value": {"title": "Отель Дубай у фонтана", "name": "Dubai у фонтана"}}
}
)):
    global hotels
    hotels.append(
        {"id": hotels[-1]["id"] + 1, "title": hotel_data.title, "name": hotel_data.name}
    )
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
