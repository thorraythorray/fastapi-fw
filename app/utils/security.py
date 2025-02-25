from datetime import timedelta

from authx import AuthX, AuthXConfig

from app.settings import SECRET_KEY


authx_config = AuthXConfig(
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24),
    JWT_SECRET_KEY=SECRET_KEY,
)

auth_manager = AuthX(config=authx_config)
