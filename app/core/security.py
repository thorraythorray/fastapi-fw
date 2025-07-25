from authx import AuthX, AuthXConfig
from passlib.context import CryptContext


auth_manager = AuthX(config=AuthXConfig(**AUTHX_CONFIG))

hash_algorithm = CryptContext(schemes=["bcrypt"], deprecated="auto")
