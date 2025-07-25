from enum import IntEnum

from tortoise import fields

from app.core.base import BaseTimestampORM
from app.core.security import hash_algorithm


class GenderEnum(IntEnum):
    UNKOWN = 0
    MALE = 1
    FEMALE = 2


GENDER_TEXT_CONVERT = {
    GenderEnum.UNKOWN: '未知',
    GenderEnum.MALE: '男',
    GenderEnum.FEMALE: '女',
}


class Permission(BaseTimestampORM):
    name = fields.CharField(max_length=64)
    code = fields.CharField(max_length=64, unique=True)
    description = fields.CharField(max_length=256, null=True)
    parent = fields.ForeignKeyField(
        'auth.Permission',
        related_name='children',
        on_delete=fields.CASCADE,
        null=True
    )

    class Meta:
        table = "admin_permission"

    def dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
        }

    async def nexts(self):
        nodes = []
        await self.fetch_related('children')
        for i in self.children:
            item = i.dump()
            item["children"] = await i.nexts()
            nodes.append(item)
        return nodes

    async def trees(self, include_child=True):
        data = self.dump()
        if include_child:
            data["children"] = await self.nexts()
        return data


class Role(BaseTimestampORM):
    name = fields.CharField(max_length=32, unique=True)
    is_admin = fields.BooleanField(default=False)
    permissions = fields.ManyToManyField(
        'auth.Permission',
        related_name='roles',
        null=True,
        on_delete=fields.SET_NULL
    )

    class Meta:
        table = "admin_role"


class User(BaseTimestampORM):
    name = fields.CharField(max_length=64)
    password = fields.CharField(max_length=128)
    email = fields.CharField(max_length=128)
    phone = fields.CharField(max_length=16, null=True)
    age = fields.IntField(null=True)
    sex = fields.IntEnumField(enum_type=GenderEnum, default=GenderEnum.UNKOWN.value)
    avatar = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)
    role = fields.ForeignKeyField('auth.Role', related_name='users', on_delete=fields.SET_NULL, null=True)

    class Meta:
        table = "admin_user"

    def verify_password(self, password):
        return hash_algorithm.verify(password, self.password)
