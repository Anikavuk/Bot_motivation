import datetime
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
        default=None, max_length=10, description="Имя пользователя, может отсутствовать"
    )
    uuid: str = Field(..., description="ID telegram or UUID")


class UpdateUser(CreateUser, BaseModel):
    """
    Класс для обновления информации о пользователе - дня рождения и знака зодиака.
    Attributes:
        birthday: Data Дата рождения пользователя в формате YYYY-MM-DD
        zodiac_sign: Str знак зодиака
    """

    birthday: datetime.date = Field(..., description="Дата рождения пользователя")
    zodiac_sign: str = Field(..., description="Знак зодиака пользователя")
