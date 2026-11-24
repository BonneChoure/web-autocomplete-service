from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    # App
    app_name: str = "Web Autocomplete Service"
    debug: bool = False

    # Data
    input_dictionary_path: Path = BASE_DIR / "data" / "dictionary.txt"

    # Autocomplete service
    autocomplete_terms_limit: int = 4

@lru_cache
def get_settings() -> Settings:
    return Settings()