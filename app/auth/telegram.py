import asyncio

from aiogram import Dispatcher
from aiogram.types import Message

from app.botlogic.handlers.events import start_bot, stop_bot
from app.botlogic.settings import bot

from app.core.logger import Logger

logger_factory = Logger(mode="dev")
logger = logger_factory.get_logger(__name__)


async def echo(message: Message):
    text = "Твои планы уже так далеко, что даже время позавидует — держись, суперзвёздочка!"
    await message.answer(text)


async def start():
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    # dp.message.register(simple.start_command, Command(commands="start"))
    dp.message.register(echo)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
