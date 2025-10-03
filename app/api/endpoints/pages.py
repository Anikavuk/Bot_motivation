import uuid

from fastapi import APIRouter, Depends, Request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth.schemas import CreateUser
from app.auth.user_service import UserService
from app.services.prediction_service import PredictionService
from app.services.motivation_ai import HuggingFacePredictor

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Метод загрузки стартовой страницы"""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/create_user", response_class=HTMLResponse)
def create_user(request: Request):
    """Метод загрузки страницы создания пользователя"""
    session_uuid = uuid.uuid4()
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
    user_data = CreateUser(name=name, uuid=session_uuid)
    await service.create_user(user=user_data)
    return templates.TemplateResponse(
        "save_user.html", {"request": request, "name": name, "id": session_uuid}
    )


@router.post("/get_prediction", response_class=HTMLResponse)
async def get_prediction(
    request: Request,
    name: str = Form(...),
    session_uuid: str = Form(...),
    user_service: UserService = Depends(UserService),
    prediction_service: PredictionService = Depends(PredictionService),
):
    """Метод загрузки страницы с предсказанием"""
    user = await user_service.get_user_by_uuid(session_uuid)
    if not user:
        user = await user_service.create_user(CreateUser(name=name, uuid=session_uuid))

    prediction = await prediction_service.get_prediction_for_user(user.id)

    if prediction:
        response_text = prediction.main_prediction
    else:
        predictor = HuggingFacePredictor()
        response_text = predictor.get_prediction()
        await prediction_service.save_prediction_in_db(response_text, user.id)

    return templates.TemplateResponse(
        "get_prediction.html",
        {
            "request": request,
            "prediction": response_text,
            "name": name,
            "id": session_uuid,
        },
    )


@router.post("/questions", response_class=HTMLResponse)
def questions(request: Request):
    """Метод загрузки анкеты пользователя"""
    return templates.TemplateResponse("questions.html", {"request": request})
