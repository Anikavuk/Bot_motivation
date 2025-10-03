from fastapi import Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.exc import OperationalError

from app.core.db_dependency import DBDependency
from app.db.models import User
from app.db.models.prediction import Prediction


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
        :type main_prediction: HuggingFacePredictor
        :param user_id: ID Пользователя, объект модели User.
        :type user_id: Int
        :return None
        """

        async with self.db.db_session() as session:
            query = insert(self.prediction_model).values(
                main_prediction=main_prediction, user_id=user_id
            )

            try:
                await session.execute(query)
            except OperationalError:
                await session.rollback()
                raise HTTPException(
                    status_code=503, detail="Database is not available."
                )

                await session.commit()

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
