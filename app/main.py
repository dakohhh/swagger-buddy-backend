from fastapi import FastAPI
from sqlmodel import SQLModel  # noqa: F401
from settings.config import settings
from contextlib import asynccontextmanager
from app.user.router import router as user_router_v1
from app.project.router import router as project_router_v1
from app.database.config import create_db_and_tables  # noqa: F401
from app.common.handlers import configure_error_middleware
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        # Only should be used in development, most preferred to use alembic to track migrations
        # await create_db_and_tables()
        yield
    finally:
        pass



def register_routers(app: FastAPI):
    """Register all application routers/controllers"""
    app.include_router(user_router_v1)
    app.include_router(project_router_v1)
    # app.include_router(auth_router_v1)
    # Add more routers here as the application grows


def create_app() -> FastAPI:
    """
    Bootstrap the application similar to NestJS module system
    """
    # Create FastAPI instance with configuration
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url=settings.API_DOCS.API_DOCS_URL,
        redoc_url=settings.API_DOCS.API_REDOC_URL,
        openapi_url=settings.API_DOCS.OPENAPI_URL,
        swagger_ui_parameters={"persistAuthorization": True},
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS_PROCESSED,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        max_age=3600,
    )

    
    # Register routers/controllers
    register_routers(app)

    configure_error_middleware(app)
    
    return app