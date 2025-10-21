import asyncio
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.app.api.endpoints.pages import router
from src.app.botlogic.commands import set_commands
from src.app.botlogic.handlers import handlers_router
from src.app.botlogic.handlers.handler_telegram import bot, dispatcher

load_dotenv()


@asynccontextmanager
async def dev_lifespan(app: FastAPI):
    await set_commands(bot)

    async def _start_polling():
        await dispatcher.start_polling(bot, handle_signals=False)

    polling_task = asyncio.create_task(_start_polling())

    yield

    polling_task.cancel()
    await bot.session.close()


web_app = FastAPI(lifespan=dev_lifespan)
web_app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "your-very-secret-key-change-in-prod"),
    max_age=31536000,
    same_site="lax",
    https_only=False,
)

web_app.include_router(router)


def run_app():
    dispatcher.include_router(handlers_router)
    uvicorn.run(
        web_app,
        host="127.0.0.1",
        port=8000,
        loop="asyncio",
        log_config=None,
        log_level="debug",
    )
