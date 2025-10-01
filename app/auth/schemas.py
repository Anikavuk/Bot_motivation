import datetime

from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    """
    Класс для создания пользователя.
    """

    name: str = Field(min_length=3, max_length=10, description="Имя пользователя")
    session_or_telegram_id: str = Field(description="ID telegram or UUID")


class UpdateUser(BaseModel):
    """
    Класс для обновления информации о пользователе - дня рождения и знака зодиака.
    """

    birthday: datetime.date = Field(description="Дата рождения пользователя")
    zodiac_sign: str = Field(description="Знак зодиака пользователя")
