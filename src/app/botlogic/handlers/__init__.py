from aiogram import Router

from src.app.botlogic.handlers.events import service_events_router
from src.app.botlogic.handlers.handler_telegram import main_router

routes = [
    main_router,
    service_events_router,
]

handlers_router = Router()
for _ in routes:
    handlers_router.include_router(_)
