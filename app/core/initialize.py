from datetime import timedelta

from fastapi_login import LoginManager


SECRET = "super-secret-key"

login_manager = LoginManager(
    SECRET,
    token_url="/auth/token",
    default_expiry=timedelta(hours=2)
)


@login_manager.user_loader
def load_user(username: str):
    # user_dict = fake_users_db.get(username)
    # if user_dict:
    #     return UserInDB(**user_dict)
    return None
