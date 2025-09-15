import uuid

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


class UuidMixin:
    """
    Класс-миксин для добавления уникального идентификатора к объектам.

    :ivar uuid: Уникальный идентификатор объекта.
    :type uuid: UUID
    """

    uuid: Mapped[uuid] = mapped_column(PG_UUID(as_uuid=True), default=uuid.uuid4)
