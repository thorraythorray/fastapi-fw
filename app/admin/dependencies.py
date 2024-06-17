from app.admin.schemas import RegisterSchema
from app.utils.crypts import crypte_content


def encrypt_passwd(data: dict) -> RegisterSchema:
    hash_passwd = crypte_content.hash(data["passwd"])
    data["passwd"] = hash_passwd
    return RegisterSchema(**data)
