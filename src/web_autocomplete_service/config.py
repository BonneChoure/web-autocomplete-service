from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    """Contains all useful settings for the app"""
    model_config = SettingsConfigDict(env_prefix="AUTOCOMPLETE_", env_file=".env")
    # App
    app_name: str = "Web Autocomplete Service"
    log_level: str = "INFO"

    # Data - default path
    input_dictionary_path: Path = BASE_DIR / "data" / "dictionary.txt"

    # Autocomplete service
    autocomplete_terms_limit: int = 4

    # Router 
    max_query_length: int = 100

@lru_cache
def get_settings() -> Settings:
    """Return Singleton Settings instance"""
    return Settings()