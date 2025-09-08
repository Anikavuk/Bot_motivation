import uuid

# from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class Uuid_Mixin:
    """
    Класс-миксин для добавления уникального идентификатора к объектам.

    :ivar uuid: Уникальный идентификатор объекта.
    :type uuid: UUID
    """

    uuid: Mapped[uuid] = mapped_column(PG_UUID(as_uuid=True), default=uuid.uuid4)
