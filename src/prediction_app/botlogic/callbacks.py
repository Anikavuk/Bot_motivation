from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.types import CallbackQuery

from prediction_app.botlogic.callback_data import StrictPrediction, SweetPrediction
from prediction_app.core.logger import get_logger
from prediction_app.services.motivation_service import (
    HuggingFacePredictor,
    StrictHuggingFacePredictor,
)

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
        self.router.callback_query(SweetPrediction.filter())(self.handle_tone_sweet)
        self.router.callback_query(StrictPrediction.filter())(self.handle_tone_strict)

    async def handle_tone_sweet(self, callback: CallbackQuery, callback_data: SweetPrediction) -> None:
        """
        Обрабатывает выбор ласкового тона.
        """
        await self._handle_tone(
            callback=callback,
            predictor_class=HuggingFacePredictor,
            callback_data=callback_data,
        )

    async def handle_tone_strict(self, callback: CallbackQuery, callback_data: StrictPrediction) -> None:
        """
        Обрабатывает выбор сурового тона.
        """
        await self._handle_tone(
            callback=callback,
            predictor_class=StrictHuggingFacePredictor,
            callback_data=callback_data,
        )

    @staticmethod
    async def _handle_tone(
        callback: CallbackQuery,
        predictor_class,
        callback_data: SweetPrediction | StrictPrediction,
    ) -> None:
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
        expected_user_id = callback_data.user_id
        if callback.from_user.id != expected_user_id:
            await callback.answer("❌ Эта кнопка не для тебя! Вызови /start сам.", show_alert=True)
            return

        await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action=ChatAction.TYPING)

        logger.info(
            f"Предсказание выбрали в чате={callback.message.chat.id}, "
            f"type={callback.message.chat.type}, predictor={predictor_class.__name__}"
        )

        predictor = predictor_class()
        response_text = predictor.get_prediction()
        logger.info(f"Вызов {predictor_class.__name__} с предсказанием response_text={response_text}")

        await callback.message.edit_text(response_text, reply_markup=None)
