from typing import List
from pydantic import RedisDsn, MySQLDsn, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILES = ('.env', '.env.usr',)
ENV_ENCODING = 'utf-8'


class RedisSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 6379
    passwd: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        env_prefix = "REDIS_",
    )

    @property
    def default_redis_dsn(self) -> RedisDsn:
        return f'redis://:{self.passwd}@{self.host}:{self.port}/0'


class MysqlSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 3306
    user: str
    passwd: SecretStr
    db: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        env_prefix = "MYSQL_",
        extra='allow',
    )

    @property
    def mysql_dsn(self) -> MySQLDsn:
        return 'mysql://{}:{}@{}:{}/{}'.format(
            self.host, self.port, self.user, self.passwd.get_secret_value(), self.db,
        )


class Settings(BaseSettings):
    debug: bool = True
    server_host: str
    allowed_cors_origins: str

    redis: RedisSettings = RedisSettings()
    msyql: MysqlSettings = MysqlSettings()

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
    )

    @field_validator("allowed_cors_origins", mode='after')
    def split_allowed_cors_origins(cls, v: str) -> List[str]:
        return v.split(',')


print(Settings().dict())
