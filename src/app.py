from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from api import router as api_router
from src.core import create_superuser

@asynccontextmanager
async def lifespan(main_app: FastAPI):
    await create_superuser()
    yield

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("src.app:app", host="localhost", port=8080, reload=True)
