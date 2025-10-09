import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.endpoints.pages import router
from app.botlogic.commands import set_commands
from app.botlogic.handlers import handlers_router
from app.botlogic.handlers.handler_telegram import bot, dispatcher


@asynccontextmanager
async def dev_lifespan(app: FastAPI):
    await set_commands(bot)

    async def _start_polling():
        await dispatcher.start_polling(bot, handle_signals=False)

    polling_task = asyncio.create_task(_start_polling())

    yield

    polling_task.cancel()
    await bot.session.close()


async def register_bot_routers() -> None:
    """
    Регистрирует маршрутизаторы ботов у диспетчера приложений.
    """
    dispatcher.include_router(handlers_router)


def run_app():
    web_app = FastAPI(lifespan=dev_lifespan)
    web_app.include_router(router)
    asyncio.run(register_bot_routers())
    uvicorn.run(
        web_app,
        host="127.0.0.1",
        port=8000,
        loop="asyncio",
        log_config=None,
        log_level="debug",
    )
