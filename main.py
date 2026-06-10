import uvicorn
from fastapi import FastAPI

from hotels import router as router_hotels
from _course_helpers.fastapi_load_test import router as router_load_test


app = FastAPI()
app.include_router(router_hotels)
app.include_router(router_load_test)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
