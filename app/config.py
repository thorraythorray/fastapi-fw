from datetime import timedelta
import os

from pydantic import RedisDsn, MySQLDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "5f-Kh8) GK~j!$^% Q&*p@#q"

ENV_FILES = (
    os.path.join(ROOT, '.env'),
    os.path.join(ROOT, '.env.local'),

)

ENV_ENCODING = 'utf-8'

LOGIN_URL = '/api/admin/login'

class GeneralSettings(BaseSettings):
    host: str
    port: int
    password: SecretStr


class RedisSettings(GeneralSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        env_prefix="REDIS_",
        extra='ignore'
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
        extra='ignore'
    )

    @property
    def default_dsn(self) -> MySQLDsn:
        return 'mysql://{}:{}@{}:{}/{}'.format(
            self.user, self.password.get_secret_value(), self.host, self.port, self.db,
        )


class Settings(BaseSettings):
    debug: bool = True
    server_host: str

    redis: RedisSettings = RedisSettings()
    mysql: MysqlSettings = MysqlSettings()

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        extra='allow'
    )


settings = Settings()
# print(settings.model_dump())

TORTOISE_ORM = {
    "connections": {"default": settings.mysql.default_dsn},
    "apps": {
        "aerich": {
            "models": ["aerich.models"],
            "default_connection": "default",  # 指定 Aerich 模型使用的默认连接
        },
        "auth": {
            "models": [
                "app.auth.models"
            ],
            "default_connection": "default",
        },
        "auditor_logs": {
            "models": [
                "app.auditor_logs.models"
            ],
            "default_connection": "default",
        }
    },
}


AUTHX_CONFIG = {
    "JWT_ACCESS_TOKEN_EXPIRES": timedelta(hours=24),
    "JWT_SECRET_KEY": SECRET_KEY,
}


SKIP_RESPONSE_FORMAT_URLS = [

]
