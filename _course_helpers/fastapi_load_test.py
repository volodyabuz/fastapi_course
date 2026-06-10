import time
import asyncio
import threading
from fastapi import APIRouter


router = APIRouter(prefix="/load_test", tags=["Нагрузочное тестирование"])


@router.get(
    "/sync/{id}",
    summary="Тестирование в синхронном режиме",
    description="Используется <i>time.sleep(3)</i>"
)
def sync_func(id: int):
    print(f"count streams: {threading.active_count()}")
    print(f"sync starts {id}: {time.time()}:.2f")
    time.sleep(3)
    print(f"sync ends {id}: {time.time()}:.2f")

@router.get(
    "/async/{id}",
    summary="Тестирование в асинхронном режиме",
    description="Используется <i>asyncio.sleep(3)</i>"
)
async def async_func(id: int):
    print(f"count streams: {threading.active_count()}")
    print(f"async starts {id}: {time.time()}:.2f")
    await asyncio.sleep(3)
    print(f"async ends {id}: {time.time()}:.2f")
