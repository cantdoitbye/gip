from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.middleware.error_handler import setup_exception_handlers
from app.routers import health, auth, users, dashboard, notifications, upload, settings as settings_router, traffic, forecasts, simulations, sites


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="AI Infrastructure Planning System",
    description="Backend API for AI-Powered Infrastructure Planning",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")
app.include_router(settings_router.router, prefix="/api/v1")
app.include_router(traffic.router, prefix="/api/v1")
app.include_router(forecasts.router, prefix="/api/v1")
app.include_router(simulations.router, prefix="/api/v1")
app.include_router(sites.router, prefix="/api/v1")

uploads_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
if os.path.exists(uploads_dir):
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
