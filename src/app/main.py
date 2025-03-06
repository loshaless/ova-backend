from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_project_id
from app.route import test_route
from app.route import transcription_route
from app.route import user
from google.cloud import aiplatform

from app.core.logging import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    project_id: str = get_project_id()
    aiplatform.init(project=project_id, location="us-central1")
    yield

app = FastAPI(
    lifespan=lifespan,
    title="ova-backend",
    description="OVA BACKEND",
    root_path='/ova/api',
    docs_url='/docs',
    redoc_url='/redoc'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_route.router, tags=["test"])
app.include_router(transcription_route.router, tags=["transcript"])
app.include_router(user.router, tags=["user"])
