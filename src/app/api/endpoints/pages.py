import uuid
from src.app.core.logger import get_logger
from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone

from src.app.auth.schemas import CreateUser
from src.app.auth.user_service import UserService
from src.app.services.prediction_service import PredictionService
from src.app.services.motivation_ai import HuggingFacePredictor

logger = get_logger(name=__name__)

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Метод загрузки стартовой страницы"""
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@router.get("/create_user", response_class=HTMLResponse)
def create_user(request: Request):
    """Метод загрузки страницы создания пользователя"""
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())

    return templates.TemplateResponse(
        request=request, name="create_user.html", context={}
    )


@router.post("/save_user", response_class=HTMLResponse)
async def save_user(
    request: Request,
    name: str = Form(...),
    service: UserService = Depends(UserService),
):
    """Метод загрузки страницы сохранения пользователя"""
    session_id = request.session.get("session_id")
    if not session_id:
        logger.warning("Попытка сохранить пользователя без сессии")
        return templates.TemplateResponse(
            request=request,
            name="errors.html",
            context={"error": "Сессия недействительна. Попробуйте обновить страницу."},
            status_code=400,
        )
    try:
        existing_user = await service.get_user_by_uuid(session_id)
        if existing_user:
            await service.update_user_name(user_id=existing_user.id, new_name=name)
            logger.info(
                f"Пользователь обновлён: uuid={session_id},добавлено новое имя={name}"
            )
        else:
            user_data = CreateUser(name=name, uuid=session_id)
            await service.create_user(user=user_data)
            logger.info(f"Пользователь создан: name={name}, uuid={session_id}")
        return templates.TemplateResponse(
            request=request,
            name="save_user.html",
            context={"name": name},
        )
    except HTTPException as e:
        logger.warning(
            f"Ошибка при создании пользователя: {e.detail} (uuid={session_id})"
        )
        return templates.TemplateResponse(
            request=request,
            name="errors.html",
            context={"error": e.detail},
            status_code=e.status_code,
        )


@router.post("/get_prediction", response_class=HTMLResponse)
async def get_prediction(
    request: Request,
    name: Optional[str] = Form(None),
    user_service: UserService = Depends(UserService),
    prediction_service: PredictionService = Depends(PredictionService),
):
    """Метод загрузки страницы с предсказанием"""
    session_id = request.session.get("session_id")
    if not session_id:
        logger.warning("Попытка получить предсказание без сессии")
        return templates.TemplateResponse(
            request=request,
            name="errors.html",
            context={"error": "Сессия недействительна. Вернитесь на главную страницу."},
            status_code=400,
        )
    try:
        user = await user_service.get_user_by_uuid(session_id)
        if not user:
            user = await user_service.create_user(
                CreateUser(name=name, uuid=session_id)
            )
            logger.info(f"Пользователь создан: name={name}, uuid={session_id}")

        today_date = datetime.now(timezone.utc).date()
        logger.info(f"Сегодняшняя дата {today_date}")

        prediction_datetime = await user_service.get_date_prediction(session_id)
        if prediction_datetime is None:
            logger.info("Дата предсказания отсутствует — генерируем новое предсказание")
            needs_new_prediction = True
        else:
            local_date = prediction_datetime.astimezone(timezone.utc).date()
            logger.info(f"Дата с базы данных {prediction_datetime}")
            logger.info(f"Преобразованная дата {local_date}")
            needs_new_prediction = local_date != today_date

        prediction = await prediction_service.get_prediction_for_user(user.id)

        if prediction and not needs_new_prediction:
            response_text = prediction.main_prediction
        else:
            predictor = HuggingFacePredictor()
            response_text = predictor.get_prediction()
            await prediction_service.save_prediction_in_db(response_text, user.id)
            logger.info(
                f"Предсказание для пользователя user.id={user.id}  name={user.name}, uuid={session_id} сохранено"
            )

        return templates.TemplateResponse(
            request=request,
            name="get_prediction.html",
            context={"prediction": response_text, "name": name},
        )
    except HTTPException as e:
        logger.warning(
            f"Ошибка при загрузке страницы с предсказанием: {e.detail} (uuid={session_id})"
        )
        return templates.TemplateResponse(
            request=request,
            name="errors.html",
            context={"error": e.detail},
            status_code=e.status_code,
        )
