from fastapi import FastAPI

from app.api.endpoints import pages

app = FastAPI()
app.include_router(pages.router)
