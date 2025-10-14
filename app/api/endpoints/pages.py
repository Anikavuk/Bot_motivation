import uuid
from app.core.logger import Logger
from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone

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
    session_uuid = request.cookies.get("session_id")

    if not session_uuid:
        session_uuid = str(uuid.uuid4())
    response = templates.TemplateResponse(
        "index.html", {"request": request, "id": session_uuid}
    )
    response.set_cookie(
        key="session_id",
        value=session_uuid,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=31536000,
        path="/",
    )

    return response


@router.post("/create_user", response_class=HTMLResponse)
def create_user(
    request: Request,
    session_uuid: str = Form(None),
):
    """Метод загрузки страницы создания пользователя"""
    final_uuid = session_uuid or request.cookies.get("session_id") or str(uuid.uuid4())
    response = templates.TemplateResponse(
        "create_user.html", {"request": request, "id": final_uuid}
    )
    response.set_cookie(
        key="session_id",
        value=final_uuid,
        httponly=True,
        samesite="lax",
        max_age=31536000,
        path="/",
    )

    return response


@router.post("/save_user", response_class=HTMLResponse)
async def save_user(
    request: Request,
    name: str = Form(...),
    session_uuid: str = Form(...),
    service: UserService = Depends(UserService),
):
    """Метод загрузки страницы сохранения пользователя"""
    try:
        existing_user = await service.get_user_by_uuid(session_uuid)
        if existing_user:
            await service.update_user_name(user_id=existing_user.id, new_name=name)
            logger.info(
                f"Пользователь обновлён: uuid={session_uuid},добавлено новое имя={name}"
            )
        else:
            user_data = CreateUser(name=name, uuid=session_uuid)
            await service.create_user(user=user_data)
            logger.info(f"Пользователь создан: name={name}, uuid={session_uuid}")
        response = templates.TemplateResponse(
            "save_user.html", {"request": request, "name": name, "id": session_uuid}
        )
        response.set_cookie(
            key="session_id",
            value=session_uuid,
            httponly=True,
            samesite="lax",
            max_age=31536000,
            path="/",
        )

        return response
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
):
    """Метод загрузки страницы с предсказанием"""
    try:
        user = await user_service.get_user_by_uuid(session_uuid)
        if not user:
            user = await user_service.create_user(
                CreateUser(name=name, uuid=session_uuid)
            )
            logger.info(f"Пользователь создан: name={name}, uuid={session_uuid}")

        today_date = datetime.now(timezone.utc).date()
        logger.info(f"Сегодняшняя дата {today_date}")
        prediction_datetime = await user_service.get_date_prediction(session_uuid)
        local_date = prediction_datetime.astimezone(timezone.utc).date()
        logger.info(f"Дата с базы данных {prediction_datetime}")
        logger.info(f"Преобразованная дата {local_date}")
        prediction = await prediction_service.get_prediction_for_user(user.id)

        if prediction and local_date == today_date:
            response_text = prediction.main_prediction
        else:
            predictor = HuggingFacePredictor()
            response_text = predictor.get_prediction()
            await prediction_service.save_prediction_in_db(response_text, user.id)
            logger.info(
                f"Предсказание для пользователя user.id={user.id}  name={user.name}, uuid={session_uuid} сохранено"
            )

        response = templates.TemplateResponse(
            "get_prediction.html",
            {
                "request": request,
                "prediction": response_text,
                "name": name,
                "id": session_uuid,
            },
        )
        response.set_cookie(
            key="session_id",
            value=session_uuid,
            httponly=True,
            samesite="lax",
            max_age=31536000,
            path="/",
        )
        return response
    except HTTPException as e:
        logger.warning(
            f"Ошибка при загрузке страницы с предсказанием: {e.detail} (uuid={session_uuid})"
        )
        return templates.TemplateResponse(
            "errors.html",
            {"request": request, "error": e.detail},
            status_code=e.status_code,
        )
