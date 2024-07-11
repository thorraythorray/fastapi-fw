from enum import IntEnum

from tortoise import fields

from app.core.base.model import TimestampModel
from app.core.utils.crypto import crypt_context


class Role(TimestampModel):
    name = fields.CharField(max_length=32, unique=True)

    class Meta:
        table = "admin_role"


class GenderEnum(IntEnum):
    UNKOWN = 0
    MALE = 1
    FEMALE = 2


class User(TimestampModel):
    name = fields.CharField(max_length=64)
    password =fields.CharField(max_length=128)
    email = fields.CharField(max_length=128)
    phone = fields.CharField(max_length=16, null=True)
    age = fields.IntField(null=True)
    sex = fields.IntEnumField(enum_type=GenderEnum, default=0)
    avatar = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)
    role = fields.ForeignKeyField('core.Role', related_name='users', on_delete=fields.SET_NULL, null=True)

    class Meta:
        table = "admin_user"

    def verify_password(self, password):
        return crypt_context.verify(password, self.password)
