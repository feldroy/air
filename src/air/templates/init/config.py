from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Environment variable specification"""

    DEBUG: bool = True
    DATABASE_URL: str = ''

settings = Settings()