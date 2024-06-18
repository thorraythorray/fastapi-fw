from app.core.schemas.admin import RegisterSchema
from app.core.utils.passlib import crypt_content


def encrypt_passwd(data: dict) -> RegisterSchema:
    hash_passwd = crypt_content.hash(data["passwd"])
    data["passwd"] = hash_passwd
    return RegisterSchema(**data)
