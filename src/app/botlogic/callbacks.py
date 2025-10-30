from aiogram import Router
from aiogram.types import CallbackQuery

from src.app.core.logger import get_logger
from src.app.services.motivation_ai import HuggingFacePredictor, StrictHuggingFacePredictor

logger = get_logger(name=__name__)
class ToneCallbackHandler:
    """
    Обработчик callback-запросов, связанных с выбором тона общения бота.

    Регистрирует обработчики для кнопок:
    - 'tone_sweet' — ласковый тон (использует HuggingFacePredictor),
    - 'tone_strict' — суровый тон (использует StrictHuggingFacePredictor).

    После выбора пользователю сразу отправляется соответствующее предсказание.
    """

    def __init__(self) -> None:
        self.router = Router()
        self._register_callbacks()

    def _register_callbacks(self) -> None:
        """
        Регистрирует обработчики callback-запросов в роутере.

        Подписывается на callback-данные, начинающиеся с:
        - 'sweet:' — вызывает handle_tone_sweet,
        - 'strict:' — вызывает handle_tone_strict.
        """
        self.router.callback_query(lambda c: c.data.startswith("sweet:"))(self.handle_tone_sweet)
        self.router.callback_query(lambda c: c.data.startswith("strict:"))(self.handle_tone_strict)

    async def handle_tone_sweet(self, callback: CallbackQuery) -> None:
        """
        Обрабатывает выбор ласкового тона.
        """
        await self._handle_tone(callback, HuggingFacePredictor)

    async def handle_tone_strict(self, callback: CallbackQuery) -> None:
        """
        Обрабатывает выбор сурового тона.
        """
        await self._handle_tone(callback, StrictHuggingFacePredictor)

    async def _handle_tone(self, callback: CallbackQuery, predictor_class) -> None:
        """
        Универсальный обработчик выбора тона общения.

        Выполняет следующие шаги:
        1. Парсит callback.data вида 'prefix:start_message_id:user_id'.
        2. Проверяет, что кнопку нажал тот же пользователь, который вызвал /start.
        3. Отправляет пользователю предсказание от указанного предиктора.
        4. Удаляет сообщение с кнопками выбора тона.

        Args:
            callback (CallbackQuery): Входящий callback-запрос.
            predictor_class (Type[HuggingFacePredictor]): Класс предсказателя, зависит от выбора тона предсказания,
                реализующий метод get_prediction() -> str.
        """
        _, start_message_id, user_id_str = callback.data.split(":")
        expected_user_id = int(user_id_str)
        if callback.from_user.id != expected_user_id:
            await callback.answer(
                "❌ Эта кнопка не для тебя! Вызови /start сам.",
                show_alert=True
            )
            return

        logger.info(
            f"Предсказание выбрали в чате={callback.message.chat.id}, "
            f"type={callback.message.chat.type}, predictor={predictor_class.__name__}"
        )
        await callback.answer()

        predictor = predictor_class()
        response_text = predictor.get_prediction()
        logger.info(f"Вызов {predictor_class.__name__} с предсказанием response_text={response_text}")

        await callback.message.answer(response_text, reply_to_message_id=start_message_id)

        try:
            await callback.message.delete()
        except Exception as e:
            logger.info(f"Не удалось удалить сообщение: {e}")