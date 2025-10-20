from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import get_settings


class DBDependency:
    """
    Класс для управления зависимостями базы данных, используя SQLAlchemy.
    """

    def __init__(self) -> None:
        """
        Инициализирует экземпляр класса, отвечающего за взаимодействие с асинхронной базой данных.
        """
        settings = get_settings()
        self._engine = create_async_engine(
            url=settings.db_settings.db_url, echo=settings.db_settings.db_echo
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine, expire_on_commit=False, autocommit=False
        )

    @property
    def db_session(self) -> async_sessionmaker[AsyncSession]:
        """
        Декоратор для создания асинхронной сессии базы данных.

        :returns: Возвращает фабрику асинхронных сессий.
        :rtype: AsyncSession
        """
        return self._session_factory
