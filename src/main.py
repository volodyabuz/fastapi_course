from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
# from _course_helpers.fastapi_load_test import router as router_load_test
from src.config import settings

print(f"{settings.DB_NAME=}")

app = FastAPI()

app.include_router(router_hotels)
# app.include_router(router_load_test)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
