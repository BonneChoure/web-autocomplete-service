from contextlib import asynccontextmanager
from fastapi import FastAPI

from web_autocomplete_service.config import get_settings
from web_autocomplete_service.routers import autocomplete

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load data and build trie here
    yield

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan
)

app.include_router(autocomplete.router)