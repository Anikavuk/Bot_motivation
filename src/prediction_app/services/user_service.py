from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, OperationalError

from prediction_app.core.db_dependency import DBDependency
from prediction_app.db.models import User
from prediction_app.schemas.schemas import CreateUser


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

    async def get_or_create_user_by_session(self, session_id: str, name: str | None = None) -> User:
        """
        Возвращает существующего пользователя по session_id или создаёт нового.

        Если пользователь существует и передано новое имя — обновляет имя.
        Если пользователь новый и имя не указано — использует значение по умолчанию.

        :param session_id: UUID сессии из запроса.
        :param name: Имя пользователя (опционально).
        :return: Объект User.
        :raises HTTPException: При ошибках базы данных.
        """
        # Получаем существующего пользователя
        user = await self.get_user_by_uuid(uuid=session_id)

        if user:
            # Если имя передано и отличается — обновляем
            if name is not None and user.name != name:
                await self.update_user_name(user_id=user.id, new_name=name)
                user.name = name
            return user
        else:
            user_data = CreateUser(name=name, uuid=session_id)
            return await self._create_user(user=user_data)

    async def _create_user(self, user: CreateUser) -> User:
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
                query = insert(self.model).values(**user.model_dump()).returning(self.model)
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

    async def update_user_name(self, user_id: int, new_name: str) -> None:
        """Метод добавления имени пользователя
        :param user_id: ID пользователя
        :type uuid: int
        :param new_name: новое имя пользователя
        :type new_name: str
        :return None
        """
        async with self.db.db_session() as session:
            query = update(self.model).where(self.model.id == user_id).values(name=new_name)
            await session.execute(query)
            await session.commit()

    async def get_date_prediction(self, uuid: str) -> datetime | None:
        """Метод выгружает дату предсказания по uuid пользователя
        :param uuid: Идентификатор пользователя (Telegram ID или UUID сесиии)
        :type uuid: Str
        :return date_prediction | None: Дата предсказания, если есть в базе данных, иначе None.
        """
        async with self.db.db_session() as session:
            query = select(self.model.date_prediction).where(self.model.uuid == uuid).limit(1)
            result = await session.execute(query)
            return result.scalar_one_or_none()
