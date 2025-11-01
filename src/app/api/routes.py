from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.app.core.logger import get_logger
from src.app.core.session_dependency import SessionDependency
from src.app.schemas.schemas import CreateUser
from src.app.services.motivation_service import HuggingFacePredictor
from src.app.services.prediction_service import PredictionService
from src.app.services.user_service import UserService

logger = get_logger(name=__name__)

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
def index(request: Request, session_id: str = Depends(SessionDependency.checking_session_id)):
    """Метод загрузки стартовой страницы"""
    logger.info("Пользователь зашел в приложение session_id=%s", session_id)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@router.post("/create_user", response_class=HTMLResponse)
def create_user(request: Request,
                session_id: str = Depends(SessionDependency.checking_session_id)):
    logger.info("Пользователь создает аккаунт session_id=%s", session_id)
    """Метод загрузки страницы создания пользователя"""
    return templates.TemplateResponse(
        request=request, name="create_user.html", context={}
    )


@router.post("/save_user", response_class=HTMLResponse)
async def save_user(
        request: Request,
        name: str = Form(...),
        user_service: UserService = Depends(UserService),
        session_id: str = Depends(SessionDependency.get_session_id_or_error),
):
    """Сохраняет или обновляет пользователя"""
    await user_service.get_or_create_user_by_session(session_id, name)
    return templates.TemplateResponse(
        request=request,
        name="save_user.html",
        context={"name": name},
    )

@router.post("/get_prediction", response_class=HTMLResponse)
async def get_prediction(
        request: Request,
        name: Optional[str] = Form(None),
        user_service: UserService = Depends(UserService),
        prediction_service: PredictionService = Depends(PredictionService),
        session_id: str = Depends(SessionDependency.get_session_id_or_error),
):
    """Метод загрузки страницы с предсказанием"""
    user = await user_service.get_or_create_user_by_session(session_id, name)

    prediction_text = await prediction_service.get_or_create_daily_prediction(
        user_id=user.id,
        user_name=user.name,
        session_id=session_id
    )

    return templates.TemplateResponse(
        request=request,
        name="get_prediction.html",
        context={"prediction": prediction_text, "name": user.name},
    )
