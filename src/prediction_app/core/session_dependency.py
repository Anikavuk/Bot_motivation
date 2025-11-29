import uuid

from fastapi import HTTPException, Request
from starlette.status import HTTP_400_BAD_REQUEST


class SessionDependency:
    """
    Класс для управления зависимостями, связанными с пользовательской сессией.
    """

    @staticmethod
    def checking_session_id(request: Request) -> str:
        """
        Гарантирует наличие session_id в сессии.
        Если отсутствует — создаёт новый UUID.

        Returns:
            str: существующий или новый session_id.
        """
        if "session_id" not in request.session:
            request.session["session_id"] = str(uuid.uuid4())
        return request.session["session_id"]

    @staticmethod
    def get_session_id_or_error(request: Request) -> str:
        """
        Извлекает session_id из сессии запроса.

        Raises:
            HTTPException: если session_id отсутствует.

        Returns:
            str: валидный session_id.
        """
        session_id = request.session.get("session_id")
        if not session_id:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Сессия недействительна. Попробуйте обновить страницу."
            )
        return session_id
