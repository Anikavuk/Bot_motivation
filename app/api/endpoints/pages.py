
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.services.motivation_ai import HuggingFacePredictor
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Метод загрузки стартовой страницы"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/get_prediction", response_class=HTMLResponse)
async def get_prediction(request: Request):
    """Метод загрузки страницы с предсказанием"""
    predictor = HuggingFacePredictor()
    response_text = predictor.get_prediction()
    return templates.TemplateResponse(
        "get_prediction.html",
        {"request": request, "prediction": response_text}
    )

@router.post("/questions", response_class=HTMLResponse)
def questions(request: Request):
    """Метод загрузки анкеты пользователя"""
    return templates.TemplateResponse("questions.html", {"request": request})
