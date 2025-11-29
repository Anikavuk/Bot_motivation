import asyncio
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from prediction_app.api.routes import router
from prediction_app.botlogic.bot_manager import BotManager
from prediction_app.core.settings import get_settings

load_dotenv()


@asynccontextmanager
async def dev_lifespan(app: FastAPI):
    bot_manager = BotManager()

    await bot_manager.set_bot_commands()
    await bot_manager.bot.delete_webhook(drop_pending_updates=True)
    try:
        await bot_manager.bot.send_message(bot_manager.settings.bot_settings.admin_id, "Бот запущен")
    except Exception as e:
        bot_manager.logger.error(f"Не удалось отправить startup-сообщение: {e}")

    # Запускаем polling
    polling_task = asyncio.create_task(bot_manager.dispatcher.start_polling(bot_manager.bot, handle_signals=False))

    yield

    polling_task.cancel()
    try:
        await bot_manager.bot.send_message(bot_manager.settings.bot_settings.admin_id, "Бот остановлен")
    except Exception as e:
        bot_manager.logger.error(f"Не удалось отправить shutdown-сообщение: {e}")
    await bot_manager.bot.session.close()


web_app = FastAPI(lifespan=dev_lifespan)
web_app.add_middleware(
    SessionMiddleware,
    secret_key=get_settings().session_secret.get_secret_value(),
    max_age=31536000,
    same_site="lax",
    https_only=False,
)

web_app.include_router(router)


def run_app():
    uvicorn.run(web_app, host="0.0.0.0", port=8000, loop="asyncio", log_config=None)
