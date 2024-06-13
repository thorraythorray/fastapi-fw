from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from settings.internal.common import ENV_ENCODING, ENV_FILES
from settings.internal.db import MysqlSettings, RedisSettings


class Settings(BaseSettings):
    debug: bool = True
    server_host: str
    allowed_cors_origins: str

    redis: RedisSettings = RedisSettings()
    msyql: MysqlSettings = MysqlSettings()

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        extra='allow',
    )

    @field_validator("allowed_cors_origins", mode='after')
    def split_allowed_cors_origins(cls, v: str) -> List[str]:
        return v.split(',')


settings = Settings()
