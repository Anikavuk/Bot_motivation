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
        Attributes:
            :param db: Зависимость для базы данных. По умолчанию используется Depends(DBDependency).
            :type db: DBDependency
        """
        self.db = db
        self.model = User

    async def create_user(self, user: CreateUser) -> User:
        """
        Создает нового пользователя в базе данных.

        :param user: Объект с данными для создания пользователя.
        :type user: CreateUser
        :raises HTTPException: Если пользователь уже существует.
        :return created_user: Объект User
        """
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

    async def get_user_by_uuid(self, uuid: str) -> User | None:
        """
        Метод поиска пользователя по UUID.

        :param uuid: Идентификатор пользователя (Telegram ID или UUID сесиии)
        :type uuid: Str
        :return User | None: Объект пользователя, если найден, иначе None.
        """
        async with self.db.db_session() as session:
            query = select(self.model).where(self.model.uuid == uuid)
            result = await session.execute(query)
            return result.scalar_one_or_none()
