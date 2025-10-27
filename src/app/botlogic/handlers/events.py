from src.app.botlogic.commands import set_commands
from src.app.botlogic.handlers.handler_telegram import bot
from src.app.core.settings import get_settings
from aiogram import Router


service_events_router = Router()


@service_events_router.startup()
async def start_bot() -> None:
    await set_commands(bot)
    await bot.send_message(get_settings().bot_settings.admin_id, "Бот запущен")


@service_events_router.shutdown()
async def stop_bot() -> None:
    await bot.send_message(get_settings().bot_settings.admin_id, "Бот остановлен")
