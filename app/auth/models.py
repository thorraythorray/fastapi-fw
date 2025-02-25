from tortoise import fields

from app.const import GenderEnum
from app.base import BaseTimestampModel
from app.utils.crypto import hash_algorithm


class Role(BaseTimestampModel):
    name = fields.CharField(max_length=32, unique=True)
    is_admin = fields.BooleanField(default=False)

    class Meta:
        table = "admin_role"


class User(BaseTimestampModel):
    name = fields.CharField(max_length=64)
    password =fields.CharField(max_length=128)
    email = fields.CharField(max_length=128)
    phone = fields.CharField(max_length=16, null=True)
    age = fields.IntField(null=True)
    sex = fields.IntEnumField(enum_type=GenderEnum, default=GenderEnum.unkown.value)
    avatar = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)
    role = fields.ForeignKeyField('auth.Role', related_name='users', on_delete=fields.SET_NULL, null=True)

    class Meta:
        table = "admin_user"

    def verify_password(self, password):
        return hash_algorithm.verify(password, self.password)
