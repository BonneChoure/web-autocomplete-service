from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    app_name: str = "Web Autocomplete Service"
    debug: bool = False

    # Autocomplete service
    autocomplete_terms_limit: int = 4