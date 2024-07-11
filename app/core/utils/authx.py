from datetime import timedelta

from authx import AuthX, AuthXConfig

SECRET_KEY = "5f-Kh8) GK~j!$^% Q&*p@#q"


config = AuthXConfig(
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=15),
    JWT_SECRET_KEY=SECRET_KEY,
)

auth_manager = AuthX(config=config)
