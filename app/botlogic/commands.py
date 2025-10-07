from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начало работы"),
        BotCommand(command="get_prediction", description="Получить предсказание"),
        BotCommand(command="about", description="Информация о боте"),
        BotCommand(command="register_user", description="Зарегистрироваться"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
