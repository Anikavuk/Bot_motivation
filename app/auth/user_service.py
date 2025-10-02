from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from app.auth.schemas import CreateUser

from app.core.db_dependency import DBDependency
from app.db.models import User


class UserService:
    """
    Класс для создания пользователя в базе данных
    """

    def __init__(self, db: DBDependency = Depends(DBDependency)) -> None:
        """
        Инициализирует экземпляр класса.

        :param db: Зависимость для базы данных. По умолчанию используется Depends(DBDependency).
        :type db: DBDependency
        """
        self.db = db
        self.model = User

    async def create_user(self, user: CreateUser) -> None:
        """
        Создает нового пользователя в базе данных.

        :param user: Объект с данными для создания пользователя.
        :type user: CreateUser
        :raises HTTPException: Если пользователь уже существует.
        """
        if not user.session_or_telegram_id or user.session_or_telegram_id.strip() == "":
            raise HTTPException(
                status_code=400, detail="session_or_telegram_id is required"
            )
        async with self.db.db_session() as session:
            query = insert(self.model).values(**user.model_dump()).returning(self.model)

            try:
                result = await session.execute(query)
                created_user = result.scalar_one()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="User already exists.")

            await session.commit()
            return created_user

    async def get_user_by_session_or_telegram_id(self, session_or_telegram_id: str):
        async with self.db.db_session() as session:
            query = select(self.model).where(
                self.model.session_or_telegram_id == session_or_telegram_id
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
