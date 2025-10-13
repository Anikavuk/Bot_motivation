import uuid
from app.core.logger import Logger
from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth.schemas import CreateUser
from app.auth.user_service import UserService
from app.services.prediction_service import PredictionService
from app.services.motivation_ai import HuggingFacePredictor

logger_factory = Logger(mode="dev")
logger = logger_factory.get_logger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Метод загрузки стартовой страницы"""
    session_uuid = uuid.uuid4()
    return templates.TemplateResponse(
        "index.html", {"request": request, "id": session_uuid}
    )


@router.post("/create_user", response_class=HTMLResponse)
def create_user(
    request: Request,
    session_uuid: str = Form(...),
):
    """Метод загрузки страницы создания пользователя"""
    return templates.TemplateResponse(
        "create_user.html", {"request": request, "id": session_uuid}
    )


@router.post("/save_user", response_class=HTMLResponse)
async def save_user(
    request: Request,
    name: str = Form(...),
    session_uuid: str = Form(...),
    service: UserService = Depends(UserService),
):
    """Метод загрузки страницы сохранения пользователя"""
    try:
        user_data = CreateUser(name=name, uuid=session_uuid)
        await service.create_user(user=user_data)
        logger.info(f"Пользователь создан: name={name}, uuid={session_uuid}")
        return templates.TemplateResponse(
            "save_user.html", {"request": request, "name": name, "id": session_uuid}
        )
    except HTTPException as e:
        logger.warning(
            f"Ошибка при создании пользователя: {e.detail} (uuid={session_uuid})"
        )
        return templates.TemplateResponse(
            "errors.html",
            {"request": request, "error": e.detail},
            status_code=e.status_code,
        )


@router.post("/get_prediction", response_class=HTMLResponse)
async def get_prediction(
    request: Request,
    name: Optional[str] = Form(None),
    session_uuid: str = Form(...),
    user_service: UserService = Depends(UserService),
    prediction_service: PredictionService = Depends(PredictionService),
    timezone: str = Form(...),
):
    """Метод загрузки страницы с предсказанием"""
    try:
        user = await user_service.get_user_by_uuid(session_uuid)
        if not user:
            user = await user_service.create_user(
                CreateUser(name=name, uuid=session_uuid)
            )
            logger.info(f"Пользователь создан: name={name}, uuid={session_uuid}")

        prediction = await prediction_service.get_prediction_for_user(user.id)

        if prediction:
            response_text = prediction.main_prediction
        else:
            predictor = HuggingFacePredictor()
            response_text = predictor.get_prediction()
            await prediction_service.save_prediction_in_db(
                response_text, user.id, timezone
            )
            logger.info(
                f"Предсказание для пользователя user.id={user.id}  name={user.name}, uuid={session_uuid} сохранено"
            )

        return templates.TemplateResponse(
            "get_prediction.html",
            {
                "request": request,
                "prediction": response_text,
                "name": name,
                "id": session_uuid,
            },
        )
    except HTTPException as e:
        logger.warning(
            f"Ошибка при загрузке страницы с предсказанием: {e.detail} (uuid={session_uuid})"
        )
        return templates.TemplateResponse(
            "errors.html",
            {"request": request, "error": e.detail},
            status_code=e.status_code,
        )
