from app.admin.schemas import UserRegisterSchema, UserSchema

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(user: UserSchema) -> dict:
    data = user.model_dump()
    hash_passwd = pwd_context.hash(data["passwd"])
    data["passwd"] = hash_passwd
    return data
