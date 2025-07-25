import os
from datetime import timedelta
from typing import List

from pydantic import RedisDsn, MySQLDsn, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from memoization import cached, CachingAlgorithmFlag
from tortoise import fields, models

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "5f-Kh8) GK~j!$^% Q&*p@#q"

ENV_FILES = (os.path.join(ROOT, 'config/.env'), os.path.join(ROOT, 'config/.env.usr'),)
ENV_ENCODING = 'utf-8'


class GeneralSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int
    password: SecretStr


class RedisSettings(GeneralSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        env_prefix="REDIS_",
    )

    @property
    def default_dsn(self) -> RedisDsn:
        return f'redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/0'


class MysqlSettings(GeneralSettings):
    user: str
    db: str
    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        env_prefix="MYSQL_",
    )

    @property
    def default_dsn(self) -> MySQLDsn:
        return 'mysql://{}:{}@{}:{}/{}'.format(
            self.user, self.password.get_secret_value(), self.host, self.port, self.db,
        )


class Settings(BaseSettings):
    debug: bool = True
    server_host: str
    allowed_cors_origins: str
    redis: RedisSettings = RedisSettings()
    mysql: MysqlSettings = MysqlSettings()
    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        extra='allow',
    )

    @field_validator("allowed_cors_origins", mode='after')
    def split_allowed_cors_origins(cls, v: str) -> List[str]:
        return v.split(',')


@cached(max_size=1, algorithm=CachingAlgorithmFlag.LRU, thread_safe=True)
def _cached_settings():
    """
    the sesstings is cached, and refreshed when configuration files changed
    """
    return Settings()


settings = _cached_settings()


class BaseTimestampORM(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


TORTOISE_ORM = {
    "connections": {"default": settings.mysql.default_dsn},
    "apps": {
        "aerich": {
            "models": ["aerich.models"],
            "default_connection": "default",
        },
        "auth": {
            "models": [
                "app.api.auth.models"
            ],
            "default_connection": "default",
        },
    },
}

LOGIN_URL = '/api/admin/login'

AUTHX_CONFIG = {
    "JWT_ACCESS_TOKEN_EXPIRES": timedelta(hours=24),
    "JWT_SECRET_KEY": SECRET_KEY,
}

SKIP_RESPONSE_FORMAT_URLS = [
    # 可在此添加需要跳过统一响应格式的 URL
]
