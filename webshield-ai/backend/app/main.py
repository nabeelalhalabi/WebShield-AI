from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router
from app.config.constants import APP_DESCRIPTION
from app.config.logging_config import configure_logging
from app.config.settings import get_settings

settings = get_settings()
configure_logging(settings.debug)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=APP_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"name": settings.app_name, "version": settings.app_version}
