import uuid


class Identification:
    """
    Класс для управления идентификатором пользователя на основе сессии и Telegram ID.

    Используется для генерации уникального значения cookie в формате:
        "<session_uuid>:<telegram_user_id>"

    Если сессия отсутствует или недействительна — создаётся новый UUID.
    Telegram ID может обновляться при его наличии в запросе.
    """

    def __init__(self, user_session: str | None = None):
        self.user_session = user_session

    def generate_cookie_value(self, telegram_user_id: str | None = None) -> str:
        """
        Генерирует значение cookie в формате 'uuid4:telegram_id'.

        Args:
            telegram_user_id (str | None): Необязательный Telegram ID пользователя.

        Returns:
            str: Строка вида "a1b2c3d4-...:123456789" или "a1b2c3d4-...:" если ID отсутствует.
        """
        session_uuid = None
        tg_id = None
        if self.user_session:
            parts = self.user_session.split(":", 1)
            session_uuid = parts[0] if len(parts) > 0 else None
            tg_id = parts[1] if len(parts) > 1 else None

        if not session_uuid:
            session_uuid = str(uuid.uuid4())

        if telegram_user_id is not None and telegram_user_id != tg_id:
            tg_id = telegram_user_id
        cookie_value = f"{session_uuid}:{tg_id if tg_id else ''}"
        return cookie_value
