from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.config.settings import settings
from app.config.database import engine, Base

from app.models import *

from app.middleware.auth_middleware import AuthenticationMiddleware
from app.routes.user_routes import router as user_router
from app.routes.product_routes import router as product_router
from app.routes.inventory_routes import router as inventory_router
from app.routes.order_routes import router as order_router
from app.routes.customer_routes import router as customer_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Web API cho quản lý bán hàng điện thoại",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthenticationMiddleware)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(order_router)
app.include_router(customer_router)


@app.get("/")
async def root(request: Request):
    return {
        "message": "API quản lý bán hàng điện thoại",
        "host": request.headers.get("host"),
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database URL: {settings.database_url}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False,
    )
