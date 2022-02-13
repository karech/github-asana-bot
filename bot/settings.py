from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False

    GITHUB_WEBHOOKS_TOKEN: Optional[str] = ''
    GITHUB_TOKEN: str

    ASANA_TOKEN: str

    DEV_BRANCH: str = 'dev'
    PROD_BRANCH: str = 'prod'

    SENTRY_DSN: str = ''

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
