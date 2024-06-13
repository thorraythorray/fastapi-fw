from pydantic import RedisDsn, MySQLDsn
from pydantic_settings import SettingsConfigDict

from settings.internal.common import ENV_ENCODING, ENV_FILES, GeneralSettings


class RedisSettings(GeneralSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding=ENV_ENCODING,
        env_prefix = "REDIS_",
    )

    @property
    def default_redis_dsn(self) -> RedisDsn:
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
    def mysql_dsn(self) -> MySQLDsn:
        return 'mysql://{}:{}@{}:{}/{}'.format(
            self.host, self.port, self.user, self.passwd.get_secret_value(), self.db,
        )
