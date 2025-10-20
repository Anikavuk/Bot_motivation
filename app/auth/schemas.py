from typing import Optional
from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    """
    Класс для создания пользователя.
    Attributes:
        name: Str имя пользователя, может быть пустым
        uuid: Str идентификатор пользователя, хранит строковое значение Telegram ID или UUID сесиии
    """

    name: Optional[str] = Field(
        default=None, max_length=50, description="Имя пользователя, может отсутствовать"
    )
    uuid: str = Field(..., description="ID telegram or UUID")
