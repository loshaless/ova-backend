from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import transaction_route, merchant_route, virtual_transaction_route
from app.api.routes import user_route, account_route, test_route, category_route
from app.api.routes.external import grounding_route, transcription_route
from google.cloud import aiplatform

from app.core.config import PROJECT_ID
from app.core.logging import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    project_id: str = PROJECT_ID
    aiplatform.init(project=project_id, location="us-central1")
    yield
    print("Shutting down fast api application...")

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
app.include_router(transcription_route.router, tags=["external"])
app.include_router(user_route.router, tags=["user"])
app.include_router(account_route.router, tags=["account"])
app.include_router(transaction_route.router, tags=["transaction"])
app.include_router(category_route.router, tags=["category"])
app.include_router(grounding_route.router, tags=["external"])
app.include_router(merchant_route.router, tags=["merchant"])
app.include_router(virtual_transaction_route.router, tags=["virtual_transaction"])
