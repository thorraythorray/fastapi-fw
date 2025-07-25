from authx import AuthX, AuthXConfig
from passlib.context import CryptContext
from app.core.config import AUTHX_CONFIG


auth_manager = AuthX(config=AuthXConfig(**AUTHX_CONFIG))

hash_algorithm = CryptContext(schemes=["bcrypt"], deprecated="auto")
