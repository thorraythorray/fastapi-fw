from authx import AuthX, AuthXConfig

SECRET_KEY = "5f-Kh8) GK~j!$^% Q&*p@#q"

config = AuthXConfig(
     JWT_ALGORITHM = "HS256",
     JWT_SECRET_KEY = SECRET_KEY,
     JWT_TOKEN_LOCATION = ["headers"],
)

auth_manager = AuthX(config=config)
