from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from api import router as api_router
from core import create_superuser, Base

@asynccontextmanager
async def lifespan(main_app: FastAPI):

    await create_superuser()
    yield

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)
