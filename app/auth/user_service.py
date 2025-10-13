from fastapi import Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, OperationalError, DBAPIError

from app.auth.schemas import CreateUser
from app.core.db_dependency import DBDependency
from app.db.models import User
from typing import List


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
        :raises HTTPException: Если база данных недоступна.

        :return: Объект User, созданный в базе данных.
        :rtype: User
        """
        try:
            async with self.db.db_session() as session:
                query = (
                    insert(self.model).values(**user.model_dump()).returning(self.model)
                )
                result = await session.execute(query)
                created_user = result.scalar_one()
                await session.commit()
                return created_user
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists.")
        except (OperationalError, DBAPIError, ConnectionRefusedError):
            raise HTTPException(
                status_code=503,
                detail="Database is not available. Please try again later.",
            )

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

    async def get_all_users(self) -> List[User]:
        """
        Метод выгрузки всех пользователей с датами
        :return: Список пользователей.
        """
        async with self.db.db_session() as session:
            query = select(self.model)
            result = await session.execute(query)
            users = result.scalars().all()
            return users
