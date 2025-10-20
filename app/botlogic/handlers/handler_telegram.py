from aiogram import Bot
from aiogram import Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram import Router
from fastapi import HTTPException

from app.auth.schemas import CreateUser
from app.auth.user_service import UserService
from app.core.db_dependency import DBDependency
from app.core.logger import Logger
from app.core.settings import get_settings
from app.services.motivation_ai import HuggingFacePredictor
from app.services.prediction_service import PredictionService

logger_factory = Logger(mode="dev")
logger = logger_factory.get_logger(__name__)

bot: Bot = Bot(token=get_settings().bot_settings.bot_token.get_secret_value())
dispatcher: Dispatcher = Dispatcher()
main_router: Router = Router()
db_dependency: DBDependency = DBDependency()


@main_router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """Метод ответа на start приветствием"""
    await message.answer(
        "Привет, мой хороший! Я бот-мотиватор, "
        "буду тебя поддерживать в трудную минуту и давать прогноз на текущий день."
    )


@main_router.message(Command("about"))
async def about_handler(message: Message) -> None:
    """Метод ответа на about"""
    await message.answer(
        "🤖 Бот-мотиватор\n\n"
        "Я помогаю тебе начинать каждый день с позитива:\n"
        "• Даю персональный прогноз на день\n"
        "• Подбадриваю в трудные моменты\n"
        "• Напоминаю, что ты — молодец!\n\n"
        "🛠️ Версия: 1.0\n"
        "👨‍💻 Разработано: командой поросят\n"
    )


@main_router.message(Command("get_prediction"))
async def bot_get_prediction(message: Message) -> None:
    """Метод ответа на get_prediction"""
    telegram_user_id = str(message.from_user.id)
    name = message.from_user.full_name
    logger.info(
        f"Пользователь с телеграмма: telegram_user_id={telegram_user_id}  name={name}"
    )
    user_service = UserService(db=db_dependency)
    prediction_service = PredictionService(db=db_dependency)

    user = await user_service.get_user_by_uuid(telegram_user_id)
    if not user:
        user = await user_service.create_user(
            CreateUser(name=name, uuid=telegram_user_id)
        )
        logger.info(f"Пользователь создан: name={name}, uuid={telegram_user_id}")

    prediction = await prediction_service.get_prediction_for_user(user.id)

    if prediction:
        response_text = prediction.main_prediction
    else:
        predictor = HuggingFacePredictor()
        response_text = predictor.get_prediction()
        await prediction_service.save_prediction_in_db(response_text, user.id)
        logger.info(
            f"Предсказание для пользователя user.id={user.id}  name={user.name}, uuid={telegram_user_id} сохранено"
        )
    await message.answer(response_text)


@main_router.message(Command("register_user"))
async def register_user(message: Message) -> None:
    """Метод сохранения пользователя при регистрации"""
    try:
        telegram_user_id = str(message.from_user.id)
        name = message.from_user.full_name
        user_data = CreateUser(name=name, uuid=telegram_user_id)

        user_service = UserService(db=db_dependency)
        await user_service.create_user(user=user_data)

        logger.info(f"Пользователь создан: name={name}, uuid={telegram_user_id}")
        await message.answer(f"Приятно познакомиться, {name}")
    except HTTPException:
        await message.answer(
            "Пользователь в моей базе данных с таким именем уже есть! Ты под колпаком!"
        )
