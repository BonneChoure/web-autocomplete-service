from contextlib import asynccontextmanager
from fastapi import FastAPI

from web_autocomplete_service.config import get_settings
from web_autocomplete_service.routers import autocomplete
from web_autocomplete_service.core.dictionary import load_trie
from web_autocomplete_service.core.trie import Trie

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.trie = load_trie(Trie(), settings.input_dictionary_path)
    yield

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan
)

app.include_router(autocomplete.router)