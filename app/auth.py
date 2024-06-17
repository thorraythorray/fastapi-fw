from authx import AuthX, AuthXConfig

from app.admin.models import User
from app.errors import AuthError, AuthForbbiden
from app.settings import SECRET_KEY


config = AuthXConfig(
     JWT_ALGORITHM = "HS256",
     JWT_SECRET_KEY = SECRET_KEY,
     JWT_TOKEN_LOCATION = ["headers"],
)

security_auth = AuthX(config=config)


async def verify_user(username: str, password: str):
    user = await User.filter(name=username).first()
    if not user:
        raise AuthError('用户不存在')

    if not user.verify_password(password):
        raise AuthForbbiden('密码错误')
