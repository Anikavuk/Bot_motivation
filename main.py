import uvicorn
from fastapi import FastAPI
from app.api.endpoints import pages

app = FastAPI()
app.include_router(pages.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
