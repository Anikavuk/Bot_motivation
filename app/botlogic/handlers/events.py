from app.botlogic.commands import set_commands
from app.botlogic.handlers.start_stop import start_bot_msg, stop_bot_msg
from app.botlogic.settings import bot, Secrets


async def start_bot():
    await set_commands(bot)
    await bot.send_message(Secrets.admin_id, start_bot_msg())


async def stop_bot():
    await bot.send_message(Secrets.admin_id, stop_bot_msg())
