from app.botlogic.commands import set_commands
from app.botlogic.handlers.handler_telegram import bot
from app.core.settings import settings
from aiogram import Router


service_events_router = Router()


@service_events_router.startup()
async def start_bot() -> None:
    await set_commands(bot)
    await bot.send_message(settings.bot_settings.admin_id, "Бот запущен")


@service_events_router.shutdown()
async def stop_bot() -> None:
    await bot.send_message(settings.bot_settings.admin_id, "Бот остановлен")
