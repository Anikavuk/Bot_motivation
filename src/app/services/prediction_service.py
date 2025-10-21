from datetime import timezone as dt_timezone, datetime
from fastapi import Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.exc import OperationalError

from src.app.core.db_dependency import DBDependency
from src.app.db.models import User
from src.app.db.models import Prediction
from src.app.core.logger import get_logger


logger = get_logger(name=__name__)


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

    async def save_prediction_in_db(self, main_prediction: str, user_id: int) -> None:
        """
        Создает новое предсказание в базе данных.

        :param main_prediction: Предсказание, которое сохраняется в базе данных.
        :type main_prediction: Str
        :param user_id: ID Пользователя, объект модели User.
        :type user_id: Int
        :return None
        """
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
                    )
                )

                await session.execute(query)
                await session.execute(update_query)
                await session.commit()
                logger.info(f"Пользователь user_id={user_id} сохранен")
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
                .order_by(self.prediction_model.id.desc())
                .limit(1)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
