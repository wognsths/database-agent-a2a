import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class DBSettings(BaseSettings):
    TEST_MODE: bool = True
    
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "postgres"

    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 20
    ECHO_SQL: bool = False
    
    BLOCKED_QUERY: str = "INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

    @property
    def url(self) -> str:
        if self.TEST_MODE:
            return "sqlite:///./test.db"
        
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
@lru_cache(maxsize=1)
def get_dbsettings() -> DBSettings:
    return DBSettings()