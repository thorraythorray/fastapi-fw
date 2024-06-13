from pydantic import SecretStr
from pydantic_settings import BaseSettings

ENV_FILES = ('.env', '.env.usr',)
ENV_ENCODING = 'utf-8'

class GeneralSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int
    passwd: SecretStr
