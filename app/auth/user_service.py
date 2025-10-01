from fastapi import Depends, HTTPException
from sqlalchemy import insert
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

        async with self.db.db_session() as session:
            query = (
                insert(self.model)
                .values(**user.model_dump())
                .returning(self.model.session_or_telegram_id, self.model.name)
            )

            try:
                result = await session.execute(query)

            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="User already exists.")

            await session.commit()
        row = result.fetchone()  # Теперь работает
        session_id, name = row
        return session_id, name
