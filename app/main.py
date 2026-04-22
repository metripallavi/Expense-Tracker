from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import APP_TITLE, APP_VERSION
from app.database import Base, engine
from app.models import expense, idempotency  # noqa
from app.routers.api_expenses import router as api_expenses_router
from app.routers.web import router as web_router
from app.utils.logging_config import configure_logging

configure_logging()

app = FastAPI(title=APP_TITLE, version=APP_VERSION)

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_expenses_router)
app.include_router(web_router)
