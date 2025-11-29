import re

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """
    Базовый класс для моделей ORM, использующих SQLAlchemy.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa
        """
        Определяет имя таблицы в базе данных на основе имени класса. Если имя содержит после начала строки заглавную
        букву, то перед ней будет поставлен "_", если таких заглавных букв более чем одна, то "_" будет только перед
        первым вхождением

        Пример: SubscriptionsType = subscriptions_type

        :param cls: Класс, для которого генерируется имя таблицы.
        :type cls: type
        :returns: Имя таблицы в нижнем регистре с символами подчеркивания вместо заглавных букв.
        :rtype: str
        """
        name = re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "_", cls.__name__)
        return name.lower()
