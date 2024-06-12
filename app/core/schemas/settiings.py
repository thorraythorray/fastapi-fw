import os
from typing import Any, Dict
from pydantic import Field
from pydantic_settings import BaseSettings, EnvSettingsSource


class Settings(BaseSettings):

    class Config:
        env_prefix = "MY_"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# print(settings)

# class Settings(BaseSettings):
#     DEBUG: bool = Field(False, env="DEBUG")

#     SERVER_HOST: str = Field(..., env="SERVER_HOST")

#     REDIS_HOST: str = Field(..., env="REDIS_HOST")
#     REDIS_PORT: str = Field(..., env="REDIS_PORT")
#     REDIS_PASSWD: str = Field(..., env="REDIS_PASSWD")

#     MYSQL_HOST: str = Field(..., env="MYSQL_HOST")
#     MYSQL_PORT: str = Field(..., env="MYSQL_PORT")
#     MYSQL_USER: str = Field(..., env="MYSQL_USER")
#     MYSQL_PASSWD: str = Field(..., env="MYSQL_PASSWD")
#     MYSQL_DB: str = Field(..., env="MYSQL_DB")

#     ALLOWED_CORS_ORIGINS: str = Field(..., env="ALLOWED_CORS_ORIGINS")

#     class Config:
#         env_file = ".env"

# print(Settings().MYSQL_USER)