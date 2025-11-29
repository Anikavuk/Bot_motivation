from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import BotCommand, BotCommandScopeDefault, Message

from prediction_app.botlogic.bot_keyboard import StartKeyboard
from prediction_app.botlogic.callbacks import ToneCallbackHandler
from prediction_app.core.logger import get_logger
from prediction_app.core.settings import get_settings


class BotManager:
    """
    Управляет жизненным циклом Telegram-бота на основе aiogram 3+.

    Отвечает за:
    - инициализацию бота, диспетчера и роутеров,
    - регистрацию команд и callback-обработчиков,
    - установку команд в меню бота.
    """

    def __init__(self):
        self.settings = get_settings()
        self.bot = Bot(token=self.settings.bot_settings.bot_token.get_secret_value())
        self.dispatcher = Dispatcher(bot=self.bot)
        self.tone_handler = ToneCallbackHandler()
        self.router = Router()
        self.register_commands()
        self.dispatcher.include_router(self.router)
        self.dispatcher.include_router(self.tone_handler.router)
        self.logger = get_logger(name=__name__)

    async def set_bot_commands(self) -> None:
        """Устанавливает команды в меню Telegram-бота"""
        commands = [
            BotCommand(command="start", description="Начало работы"),
        ]
        await self.bot.set_my_commands(commands, BotCommandScopeDefault())

    def register_commands(self) -> None:
        """
        Регистрирует обработчики текстовых команд в основном роутере.

        Поддерживаемые команды:
        - `/start` — отправляет приветственное сообщение с выбором тона предсказания.
        """

        @self.router.message(CommandStart)
        async def start_handler(message: Message) -> None:
            """
            Обрабатывает команду /start.

            Отправляет пользователю приветственное сообщение и клавиатуру
            с выбором стиля предсказания: "ласковое" или "суровое".
            Не требует ввода текста от пользователя — команда генерируется Telegram
            автоматически при старте диалога.

            Args:
                message (Message): Входящее сообщение с командой /start.
            """
            try:
                keyboard = StartKeyboard().build(start_message_id=message.message_id, user_id=message.from_user.id)
                welcome_text = (
                    "Привет, мой хороший! Я бот-мотиватор, "
                    "буду тебя поддерживать в трудную минуту и давать прогноз на текущий день. "
                    "Нажимай кнопку: какое предсказание ты сегодня хочешь - ласковое или суровое?"
                )
                self.logger.info(
                    f"Вызывается класс BotManager, где keyboard ={keyboard},message.message_id={message.message_id}"
                )
                await message.answer(
                    text=welcome_text,
                    reply_markup=keyboard,
                    reply_to_message_id=message.message_id,
                )
            except Exception as e:
                self.logger.error(f"Error in start_handler: {e}")
