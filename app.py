import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from api import router as api_router


http_bearer = None
# http_bearer = HTTPBearer(auto_error=False)

app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)
