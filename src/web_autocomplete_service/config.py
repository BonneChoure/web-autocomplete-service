from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "Web Autocomplete Service"
    debug: bool = False

    # Autocomplete service
    autocomplete_terms_limit: int = 4

@lru_cache
def get_settings() -> Settings:
    return Settings()