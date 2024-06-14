from datetime import timedelta

from fastapi_login import LoginManager

from app.admin.models import User
from app.settings import SECRET_KEY

login_manager = LoginManager(
    SECRET_KEY,
    token_url="/auth/token",
    default_expiry=timedelta(hours=2)
)


@login_manager.user_loader
async def load_user(username: str):
    return await User.get(username=username)
