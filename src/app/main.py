from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_project_id
from app.api.routes import transcription_route, transaction, merchant
from app.api.routes import user, account_route, test_route, category_route, grounding
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
app.include_router(account_route.router, tags=["account"])
app.include_router(transaction.router, tags=["transaction"])
app.include_router(category_route.router, tags=["category"])
app.include_router(grounding.router, tags=["grounding"])
app.include_router(merchant.router, tags=["merchant"])
