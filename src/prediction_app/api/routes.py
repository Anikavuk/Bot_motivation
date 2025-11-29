from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse

from prediction_app.core.logger import get_logger
from prediction_app.core.session_dependency import SessionDependency
from prediction_app.core.settings import get_templates
from prediction_app.services.prediction_service import PredictionService
from prediction_app.services.user_service import UserService

logger = get_logger(name=__name__)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    session_id: Annotated[str, Depends(SessionDependency.checking_session_id)],
):
    """Метод загрузки стартовой страницы"""
    logger.info("Пользователь зашел в приложение session_id=%s", session_id)

    return get_templates().TemplateResponse(request=request, name="index.html", context={})


@router.get("/create_user", response_class=HTMLResponse)
def create_user(
    request: Request,
    session_id: Annotated[str, Depends(SessionDependency.checking_session_id)],
):
    logger.info("Пользователь создает аккаунт session_id=%s", session_id)
    """Метод загрузки страницы создания пользователя"""
    return get_templates().TemplateResponse(request=request, name="create_user.html", context={})


@router.post("/save_user", response_class=HTMLResponse)
async def save_user(
    request: Request,
    user_service: Annotated[UserService, Depends(UserService)],
    session_id: Annotated[str, Depends(SessionDependency.checking_session_id)],
    name: str = Form(...),
):
    """Сохраняет или обновляет пользователя"""
    await user_service.get_or_create_user_by_session(session_id=session_id, name=name)
    return get_templates().TemplateResponse(request=request, name="save_user.html", context={"name": name})


@router.post("/get_prediction", response_class=HTMLResponse)
async def get_prediction(
    request: Request,
    user_service: Annotated[UserService, Depends(UserService)],
    session_id: Annotated[str, Depends(SessionDependency.checking_session_id)],
    prediction_service: Annotated[PredictionService, Depends(PredictionService)],
    name: str | None = Form(None),
):
    """Метод загрузки страницы с предсказанием"""
    user = await user_service.get_or_create_user_by_session(session_id=session_id, name=name)

    prediction_text = await prediction_service.get_or_create_daily_prediction(
        user_id=user.id, user_name=user.name, session_id=session_id
    )

    return get_templates().TemplateResponse(
        request=request,
        name="get_prediction.html",
        context={"prediction": prediction_text, "name": user.name},
    )
