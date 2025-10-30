import uvicorn
import asyncio
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.app.api.endpoints.pages import router
from src.app.botlogic.bot_manager import BotManager

load_dotenv()

@asynccontextmanager
async def dev_lifespan(app: FastAPI):
    bot_manager = BotManager()
    # bot_manager.dispatcher.include_router(bot_manager.router)

    await bot_manager.set_bot_commands()
    await bot_manager.bot.delete_webhook(drop_pending_updates=True)
    try:
        await bot_manager.bot.send_message(
            bot_manager.settings.bot_settings.admin_id,
            "Бот запущен"
        )
    except Exception as e:
        bot_manager.logger.error(f"Не удалось отправить startup-сообщение: {e}")

    # Запускаем polling
    polling_task = asyncio.create_task(
        bot_manager.dispatcher.start_polling(bot_manager.bot, handle_signals=False)
    )

    yield

    polling_task.cancel()
    try:
        await bot_manager.bot.send_message(
            bot_manager.settings.bot_settings.admin_id,
            "Бот остановлен"
        )
    except Exception as e:
        bot_manager.logger.error(f"Не удалось отправить shutdown-сообщение: {e}")
    await bot_manager.bot.session.close()
#
# @asynccontextmanager
# async def dev_lifespan(app: FastAPI):
#     dispatcher.include_router(handlers_router)
#     await set_commands(bot)
#
#     async def _start_polling():
#         await dispatcher.start_polling(bot, handle_signals=False)
#
#     polling_task = asyncio.create_task(_start_polling())
#
#     yield
#
#     polling_task.cancel()
#     await bot.session.close()


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
    uvicorn.run(
        web_app,
        host="127.0.0.1",
        port=8000,
        loop="asyncio",
        log_config=None,
        log_level="debug",
    )
