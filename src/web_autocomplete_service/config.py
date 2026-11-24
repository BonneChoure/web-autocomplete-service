from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    app_name: str = "Web Autocomplete Service"
    debug: bool = False

    # 