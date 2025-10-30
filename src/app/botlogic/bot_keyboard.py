from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.app.core.logger import get_logger

logger = get_logger(name=__name__)
class StartKeyboard:
    """
    Класс для создания стартовой inline-клавиатуры с выбором
    тона предсказания в Telegram-боте.

    Статический метод build() формирует клавиатуру из двух кнопок:
    - "Ласковое" с callback_data="tone_sweet"
    - "Суровое" с callback_data="tone_strict"

    Возвращает объект InlineKeyboardMarkup для использования в reply_markup.
    """

    @staticmethod
    def build(start_message_id: int, user_id: int) -> InlineKeyboardMarkup:
        callback_sweet = f"sweet:{start_message_id}:{user_id}"
        callback_strict = f"strict:{start_message_id}:{user_id}"
        button1 = InlineKeyboardButton(text="Ласковое", callback_data=callback_sweet)
        button2 = InlineKeyboardButton(text="Суровое", callback_data=callback_strict)
        logger.info(
            f"Вызывается класс StartKeyboard, где callback_sweet ={callback_sweet},callback_strict={callback_strict}"
        )
        return InlineKeyboardMarkup(inline_keyboard=[[button1, button2]])