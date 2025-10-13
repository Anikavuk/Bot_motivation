from datetime import timezone as dt_timezone, datetime
from zoneinfo import ZoneInfo
from fastapi import Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import OperationalError

from app.core.db_dependency import DBDependency
from app.db.models import User
from app.db.models.prediction import Prediction
from app.core.logger import Logger


logger_factory = Logger(mode="dev")
logger = logger_factory.get_logger(__name__)


class PredictionService:
    """
    Класс для сохранения и поиска предсказания в базе данных
    """

    def __init__(self, db: DBDependency = Depends(DBDependency)) -> None:
        """
        Инициализирует экземпляр класса.
        Attributes:
        :param db: Зависимость для базы данных. По умолчанию используется Depends(DBDependency).
        :type db: DBDependency
        """
        self.db = db
        self.user_model = User
        self.prediction_model = Prediction

    async def save_prediction_in_db(
        self, main_prediction: str, user_id: int, timezone: str
    ) -> None:
        """
        Создает новое предсказание в базе данных.

        :param main_prediction: Предсказание, которое сохраняется в базе данных.
        :type main_prediction: Str
        :param user_id: ID Пользователя, объект модели User.
        :type user_id: Int
        :param timezone: Таймзона пользователя
        :type timezone: Str
        :return None
        """
        user_tz = str(ZoneInfo(timezone))
        logger.info(f"Пользователь user_id={user_id} находится в тайм зоне {user_tz}")

        async with self.db.db_session() as session:
            try:
                query = insert(self.prediction_model).values(
                    main_prediction=main_prediction, user_id=user_id
                )
                update_query = (
                    update(self.user_model)
                    .where(self.user_model.id == user_id)
                    .values(
                        date_prediction=datetime.now(dt_timezone.utc),
                        user_timezone=user_tz,
                    )
                )

                await session.execute(query)
                await session.execute(update_query)
                await session.commit()
            except OperationalError:
                await session.rollback()
                raise HTTPException(
                    status_code=503, detail="Database is not available."
                )

    async def get_prediction_for_user(self, id: int) -> Prediction | None:
        """
        Выгружает предсказание по ID пользователю.

        :param id: ID Пользователя, объект модели User.
        :type id: Int
        :return :return Prediction | None: Объект Prediction, если предсказание
        найдено, иначе None.
        """
        async with self.db.db_session() as session:
            query = (
                select(self.prediction_model)
                .where(self.prediction_model.user_id == id)
                .limit(1)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def deleted_prediction(self, user_id) -> None:
        """Метод удаления предсказания по user_id"""
        async with self.db.db_session() as session:
            query = delete(self.prediction_model).where(
                self.prediction_model.user_id == user_id
            )
            await session.execute(query)
            await session.commit()
