import os
from typing import List

from pydantic import RedisDsn, MySQLDsn, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "5f-Kh8) GK~j!$^% Q&*p@#q"

ENV_FILES = (os.path.join(ROOT, '.env'), os.path.join(ROOT, '.env.usr'),)
ENV_ENCODING = 'utf-8'


class GeneralSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int
    passwd: SecretStr


class RedisSettings(GeneralSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        env_prefix = "REDIS_",
    )

    @property
    def default_dsn(self) -> RedisDsn:
        return f'redis://:{self.passwd}@{self.host}:{self.port}/0'


class MysqlSettings(GeneralSettings):
    user: str
    db: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        env_prefix = "MYSQL_",
    )

    @property
    def default_dsn(self) -> MySQLDsn:
        return 'mysql://{}:{}@{}:{}/{}'.format(
            self.user, self.passwd.get_secret_value(), self.host, self.port, self.db,
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


settings = Settings()


TORTOISE_ORM = {
    "connections": {"default": settings.mysql.default_dsn},
    "apps": {
        "aerich": {
            "models": ["aerich.models"],
            "default_connection": "default",  # 指定 Aerich 模型使用的默认连接
        },
        "admin": {
            "models": ["app.admin.models"],
            "default_connection": "default",
        },
    },
}
