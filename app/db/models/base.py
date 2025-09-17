from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """
    Базовый класс для моделей ORM, использующих SQLAlchemy.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Определяет название таблицы в базе данных на основе имени класса.

        :return: Название таблицы в формате snake_case.
        :rtype: Str
        """
        return cls.__name__.lower()
